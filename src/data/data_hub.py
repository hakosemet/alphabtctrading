"""Unified Bitcoin Data Hub — aggregates multi-source market intelligence."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from src.analysis.cross_exchange import build_cross_exchange_summary
from src.data.cache import TTLCache
from src.data.coinglass_client import CoinglassClient
from src.data.connectors import (
    BinanceConnector,
    BingXConnector,
    BitgetConnector,
    BybitConnector,
    CoinbaseConnector,
    KrakenConnector,
    MEXCConnector,
    OKXConnector,
)
from src.data.hub_models import HubSnapshot, SourceInfo
from src.data.news_sentiment import NewsSentimentProvider
from src.data.onchain import OnChainProvider
from src.indicators.technical import parse_coinglass_heatmap

TRACKED_FIELDS = [
    "price",
    "candles",
    "volume",
    "order_book",
    "funding_rate",
    "open_interest",
    "long_short_ratio",
    "liquidations",
]

CRITICAL_FIELDS = ["price", "candles"]


class BitcoinDataHub:
    """Collects Bitcoin data from trusted sources with graceful degradation."""

    def __init__(
        self,
        *,
        symbol: str = "BTCUSDT",
        coinglass_api_key: str | None = None,
        timeout: int = 15,
        cache_ttl: int = 60,
    ) -> None:
        self.symbol = symbol
        self.timeout = timeout
        self.cache = TTLCache(default_ttl=cache_ttl)
        self.binance = BinanceConnector(symbol=symbol, timeout=timeout)
        self.coinglass = CoinglassClient(api_key=coinglass_api_key, timeout=timeout)
        self.onchain = OnChainProvider()
        self.news_sentiment = NewsSentimentProvider()
        self.alt_connectors = [
            BingXConnector(timeout=timeout),
            BybitConnector(timeout=timeout),
            OKXConnector(timeout=timeout),
            BitgetConnector(timeout=timeout),
            MEXCConnector(timeout=timeout),
            CoinbaseConnector(timeout=timeout),
            KrakenConnector(timeout=timeout),
        ]

    def fetch(self, *, interval: str = "1h", limit: int = 500, use_cache: bool = True) -> HubSnapshot:
        cache_key = f"{self.symbol}:{interval}:{limit}"
        if use_cache:
            cached = self.cache.get(cache_key)
            if isinstance(cached, HubSnapshot):
                return cached

        snapshot = HubSnapshot(last_updated=datetime.now(timezone.utc))
        self._fetch_binance(snapshot, interval=interval, limit=limit)
        self._fetch_coinglass(snapshot, interval=interval)
        self._fetch_alt_exchanges(snapshot)
        self._fetch_onchain(snapshot)
        self._fetch_news_sentiment(snapshot)
        self._finalize_snapshot(snapshot)

        if use_cache:
            self.cache.set(cache_key, snapshot, ttl=self.cache._default_ttl)
        return snapshot

    def _fetch_binance(self, snapshot: HubSnapshot, *, interval: str, limit: int) -> None:
        probe = self.binance.probe()
        snapshot.source_status[self.binance.name] = probe

        try:
            bundle = self.binance.fetch_market_bundle(interval=interval, limit=limit)
        except Exception as exc:
            snapshot.source_status[self.binance.name] = SourceInfo(
                name=self.binance.name,
                status="offline",
                error=str(exc),
            )
            return

        snapshot.price = bundle.get("price")
        snapshot.candles = bundle.get("candles")
        snapshot.volume = bundle.get("volume")
        snapshot.order_book = bundle.get("order_book")
        snapshot.funding_rate = bundle.get("funding_rate")
        snapshot.open_interest = bundle.get("open_interest")
        snapshot.long_short_ratio = bundle.get("long_short_ratio")

        errors = bundle.get("errors") or []
        status: str = "online"
        if errors and snapshot.price is not None:
            status = "degraded"
        elif snapshot.price is None:
            status = "offline"

        snapshot.source_status[self.binance.name] = SourceInfo(
            name=self.binance.name,
            status=status,  # type: ignore[arg-type]
            last_updated=datetime.now(timezone.utc) if snapshot.price is not None else None,
            error="; ".join(errors) if errors else None,
            fields=[field for field in TRACKED_FIELDS if getattr(snapshot, field, None) is not None],
        )
        if snapshot.price is not None and self.binance.name not in snapshot.sources:
            snapshot.sources.append(self.binance.name)

    def _fetch_coinglass(self, snapshot: HubSnapshot, *, interval: str) -> None:
        if not self.coinglass.enabled:
            snapshot.source_status["Coinglass"] = SourceInfo(
                name="Coinglass",
                status="offline",
                error="API key not configured",
                fields=[],
            )
            return

        errors: list[str] = []
        fields: list[str] = []
        liquidation_payload: dict[str, Any] = {"heatmap": None, "source": "Coinglass"}

        try:
            oi_hist = self.coinglass.get_open_interest_history(interval=interval)
            if oi_hist is not None and len(oi_hist) >= 2 and "close" in oi_hist.columns:
                latest_oi = oi_hist.iloc[-1]["close"]
                prev_oi = oi_hist.iloc[-2]["close"]
                snapshot.open_interest = float(latest_oi)
                fields.append("open_interest")
                if prev_oi:
                    snapshot.open_interest_change_pct = ((latest_oi - prev_oi) / prev_oi) * 100
                    fields.append("open_interest_change_pct")
        except Exception as exc:
            errors.append(f"open_interest: {exc}")

        try:
            cg_funding = self.coinglass.get_funding_rates()
            if cg_funding:
                preferred = {"Binance", "Bybit", "OKX", "BingX", "Bitget", "MEXC"}
                rates: list[float] = []
                for entry in cg_funding:
                    exchange = str(entry.get("exchange") or "")
                    rate = entry.get("funding_rate")
                    if exchange in preferred and rate is not None:
                        rates.append(float(rate))
                if rates:
                    snapshot.funding_rate = sum(rates) / len(rates)
                    fields.append("funding_rate")
                else:
                    for entry in cg_funding:
                        if entry.get("exchange") == "Binance":
                            snapshot.funding_rate = float(entry.get("funding_rate", snapshot.funding_rate or 0))
                            fields.append("funding_rate")
                            break
        except Exception as exc:
            errors.append(f"funding_rate: {exc}")

        try:
            cg_ls = self.coinglass.get_long_short_ratio_history(interval=interval, limit=2)
            if cg_ls is not None and not cg_ls.empty and "longShortRatio" in cg_ls.columns:
                snapshot.long_short_ratio = float(cg_ls.iloc[-1]["longShortRatio"])
                fields.append("long_short_ratio")
        except Exception as exc:
            errors.append(f"long_short_ratio: {exc}")

        try:
            raw_heatmap = self.coinglass.get_liquidation_heatmap()
            parsed = parse_coinglass_heatmap(raw_heatmap, snapshot.price or 0.0)
            liquidation_payload["heatmap_rows"] = 0 if parsed is None else len(parsed)
            liquidation_payload["heatmap"] = "available" if parsed is not None else None
            snapshot.liquidations = liquidation_payload
            if parsed is not None:
                fields.append("liquidations")
        except Exception as exc:
            errors.append(f"liquidations: {exc}")
            snapshot.liquidations = liquidation_payload

        status = "online" if fields else "degraded"
        if errors and not fields:
            status = "offline"

        snapshot.source_status["Coinglass"] = SourceInfo(
            name="Coinglass",
            status=status,  # type: ignore[arg-type]
            last_updated=datetime.now(timezone.utc) if fields else None,
            error="; ".join(errors) if errors else None,
            fields=fields,
        )
        if fields and "Coinglass" not in snapshot.sources:
            snapshot.sources.append("Coinglass")

    def _fetch_alt_exchanges(self, snapshot: HubSnapshot) -> None:
        # Performance: query alternative exchanges in parallel instead of sequentially.
        def _load_connector(connector):
            try:
                bundle = connector.fetch_market_bundle()
                return connector, bundle, None
            except Exception as exc:
                return connector, None, exc

        max_workers = min(8, max(1, len(self.alt_connectors)))
        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="hub-alt") as pool:
            futures = [pool.submit(_load_connector, connector) for connector in self.alt_connectors]
            for future in as_completed(futures):
                connector, bundle, error = future.result()
                if error is not None or bundle is None:
                    snapshot.source_status[connector.name] = SourceInfo(
                        name=connector.name,
                        status="offline",
                        error=str(error),
                    )
                    continue

                snapshot.exchange_snapshots[connector.name] = {
                    "price": bundle.get("price"),
                    "funding_rate": bundle.get("funding_rate"),
                    "open_interest": bundle.get("open_interest"),
                    "errors": bundle.get("errors") or [],
                }

                errors = bundle.get("errors") or []
                fields = [
                    field
                    for field in ("price", "funding_rate", "open_interest")
                    if bundle.get(field) is not None
                ]
                if bundle.get("price") is None:
                    status = "offline"
                elif errors:
                    status = "degraded"
                else:
                    status = "online"

                snapshot.source_status[connector.name] = SourceInfo(
                    name=connector.name,
                    status=status,  # type: ignore[arg-type]
                    last_updated=datetime.now(timezone.utc) if bundle.get("price") is not None else None,
                    error="; ".join(errors) if errors else None,
                    fields=fields,
                )
                if bundle.get("price") is not None and connector.name not in snapshot.sources:
                    snapshot.sources.append(connector.name)

        snapshot.cross_exchange = build_cross_exchange_summary(
            snapshot.exchange_snapshots,
            reference_price=float(snapshot.price or 0),
        )

    def _fetch_onchain(self, snapshot: HubSnapshot) -> None:
        try:
            payload, info = self.onchain.fetch()
            snapshot.onchain = payload
            snapshot.source_status[info.name] = info
        except Exception as exc:
            snapshot.onchain = {}
            snapshot.source_status["On-Chain"] = SourceInfo(
                name="On-Chain",
                status="offline",
                error=str(exc),
            )

    def _fetch_news_sentiment(self, snapshot: HubSnapshot) -> None:
        try:
            news, sentiment, info = self.news_sentiment.fetch()
            snapshot.news = news
            snapshot.sentiment = sentiment
            snapshot.source_status[info.name] = info
        except Exception as exc:
            snapshot.news = {}
            snapshot.sentiment = {}
            snapshot.source_status["News & Sentiment"] = SourceInfo(
                name="News & Sentiment",
                status="offline",
                error=str(exc),
            )

    def _finalize_snapshot(self, snapshot: HubSnapshot) -> None:
        available: list[str] = []
        missing: list[str] = []

        for field in TRACKED_FIELDS:
            value = getattr(snapshot, field, None)
            if field == "candles":
                ok = isinstance(value, pd.DataFrame) and not value.empty
            elif field == "liquidations":
                ok = isinstance(value, dict) and value.get("heatmap") == "available"
            else:
                ok = value is not None
            if ok:
                available.append(field)
            else:
                missing.append(field)

        snapshot.available_fields = available
        snapshot.missing_fields = missing
        snapshot.critical_missing = any(field in missing for field in CRITICAL_FIELDS)
        snapshot.force_wait = snapshot.critical_missing

        if snapshot.critical_missing:
            snapshot.data_quality = "critical"
            snapshot.confidence_impact = "critical — WAIT recommended"
        elif len(missing) >= 4:
            snapshot.data_quality = "partial"
            snapshot.confidence_impact = "high — confidence reduced"
        elif missing:
            snapshot.data_quality = "partial"
            snapshot.confidence_impact = "moderate — some inputs missing"
        else:
            snapshot.data_quality = "full"
            snapshot.confidence_impact = "none"

        snapshot.last_updated = datetime.now(timezone.utc)
