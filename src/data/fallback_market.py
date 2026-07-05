"""Fallback market data when Binance is unreachable (common on cloud hosts)."""

from __future__ import annotations

from typing import Any

import pandas as pd
import requests

_BYBIT_INTERVALS = {
    "1m": "1",
    "3m": "3",
    "5m": "5",
    "15m": "15",
    "30m": "30",
    "1h": "60",
    "4h": "240",
    "1d": "D",
}

_OKX_BARS = {
    "1m": "1m",
    "3m": "3m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1H",
    "4h": "4H",
    "1d": "1D",
}


def _klines_dataframe(rows: list[list[Any]]) -> pd.DataFrame:
    df = pd.DataFrame(
        rows,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "quote_volume",
        ],
    )
    numeric_cols = ["open", "high", "low", "close", "volume", "quote_volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["close_time"] = df["open_time"]
    df["trades"] = 0
    df["taker_buy_base"] = 0.0
    df["taker_buy_quote"] = 0.0
    df["ignore"] = 0
    return df


def _fetch_bybit_klines(*, interval: str, limit: int, timeout: float) -> pd.DataFrame | None:
    bybit_interval = _BYBIT_INTERVALS.get(interval)
    if not bybit_interval:
        return None

    response = requests.get(
        "https://api.bybit.com/v5/market/kline",
        params={
            "category": "spot",
            "symbol": "BTCUSDT",
            "interval": bybit_interval,
            "limit": min(limit, 1000),
        },
        timeout=timeout,
    )
    response.raise_for_status()
    raw = (response.json().get("result") or {}).get("list") or []
    if not raw:
        return None

    rows = [
        [
            int(row[0]),
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6] if len(row) > 6 else row[5],
        ]
        for row in reversed(raw)
    ]
    return _klines_dataframe(rows)


def _fetch_okx_klines(*, interval: str, limit: int, timeout: float) -> pd.DataFrame | None:
    bar = _OKX_BARS.get(interval)
    if not bar:
        return None

    response = requests.get(
        "https://www.okx.com/api/v5/market/candles",
        params={"instId": "BTC-USDT", "bar": bar, "limit": min(limit, 300)},
        timeout=timeout,
    )
    response.raise_for_status()
    raw = response.json().get("data") or []
    if not raw:
        return None

    rows = [
        [
            int(row[0]),
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6] if len(row) > 6 else row[5],
        ]
        for row in reversed(raw)
    ]
    return _klines_dataframe(rows)


def fetch_fallback_klines(
    *,
    interval: str = "1m",
    limit: int = 500,
    timeout: float = 15.0,
) -> tuple[pd.DataFrame | None, str | None]:
    """Try Bybit then OKX for OHLCV when Binance is blocked."""
    for name, fetcher in (("Bybit", _fetch_bybit_klines), ("OKX", _fetch_okx_klines)):
        try:
            df = fetcher(interval=interval, limit=limit, timeout=timeout)
            if df is not None and not df.empty:
                return df, name
        except Exception:
            continue
    return None, None


def pick_fallback_price(exchange_snapshots: dict[str, dict[str, Any]]) -> tuple[float | None, str | None]:
    """Use the first live alt-exchange price when Binance price is missing."""
    for name, snap in exchange_snapshots.items():
        price = snap.get("price")
        if price is not None and float(price) > 0:
            return float(price), name
    return None, None
