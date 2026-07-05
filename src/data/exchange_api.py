"""Public REST fetchers for multi-exchange BTC market data."""

from __future__ import annotations

from typing import Any, Callable

import requests

Bundle = dict[str, Any]


def _empty_bundle() -> Bundle:
    return {
        "price": None,
        "funding_rate": None,
        "open_interest": None,
        "candles": None,
        "volume": None,
        "errors": [],
    }


def _get_json(url: str, *, params: dict | None = None, timeout: int = 15) -> Any:
    response = requests.get(url, params=params or {}, timeout=timeout)
    response.raise_for_status()
    return response.json()


def _run(label: str, fn: Callable[[], Any], bundle: Bundle) -> Any:
    try:
        return fn()
    except Exception as exc:
        bundle["errors"].append(f"{label}: {exc}")
        return None


def fetch_bybit(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://api.bybit.com/v5/market/tickers",
            params={"category": "linear", "symbol": "BTCUSDT"},
            timeout=timeout,
        )
        row = (data.get("result") or {}).get("list") or [{}]
        item = row[0]
        bundle["funding_rate"] = float(item.get("fundingRate") or 0)
        return float(item["lastPrice"])

    def _oi() -> float:
        data = _get_json(
            "https://api.bybit.com/v5/market/open-interest",
            params={"category": "linear", "symbol": "BTCUSDT", "intervalTime": "1h", "limit": 1},
            timeout=timeout,
        )
        row = (data.get("result") or {}).get("list") or [{}]
        return float(row[0].get("openInterest") or 0)

    bundle["price"] = _run("price", _price, bundle)
    bundle["open_interest"] = _run("open_interest", _oi, bundle)
    return bundle


def fetch_okx(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://www.okx.com/api/v5/market/ticker",
            params={"instId": "BTC-USDT"},
            timeout=timeout,
        )
        row = (data.get("data") or [{}])[0]
        return float(row["last"])

    def _funding() -> float:
        data = _get_json(
            "https://www.okx.com/api/v5/public/funding-rate",
            params={"instId": "BTC-USDT-SWAP"},
            timeout=timeout,
        )
        row = (data.get("data") or [{}])[0]
        return float(row.get("fundingRate") or 0)

    def _oi() -> float:
        data = _get_json(
            "https://www.okx.com/api/v5/public/open-interest",
            params={"instId": "BTC-USDT-SWAP"},
            timeout=timeout,
        )
        row = (data.get("data") or [{}])[0]
        return float(row.get("oi") or 0)

    bundle["price"] = _run("price", _price, bundle)
    bundle["funding_rate"] = _run("funding_rate", _funding, bundle)
    bundle["open_interest"] = _run("open_interest", _oi, bundle)
    return bundle


def fetch_bingx(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://open-api.bingx.com/openApi/swap/v2/quote/ticker",
            params={"symbol": "BTC-USDT"},
            timeout=timeout,
        )
        payload = data.get("data") or {}
        if bundle.get("funding_rate") is None and payload.get("lastFundingRate") is not None:
            bundle["funding_rate"] = float(payload["lastFundingRate"])
        return float(payload["lastPrice"])

    def _funding() -> float:
        data = _get_json(
            "https://open-api.bingx.com/openApi/swap/v2/quote/premiumIndex",
            params={"symbol": "BTC-USDT"},
            timeout=timeout,
        )
        payload = data.get("data") or {}
        return float(payload.get("lastFundingRate") or 0)

    bundle["price"] = _run("price", _price, bundle)
    if bundle["funding_rate"] is None:
        bundle["funding_rate"] = _run("funding_rate", _funding, bundle)
    return bundle


def fetch_bitget(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://api.bitget.com/api/v2/mix/market/ticker",
            params={"symbol": "BTCUSDT", "productType": "USDT-FUTURES"},
            timeout=timeout,
        )
        row = (data.get("data") or [{}])[0]
        if row.get("fundingRate") is not None:
            bundle["funding_rate"] = float(row["fundingRate"])
        return float(row["lastPr"])

    def _oi() -> float:
        data = _get_json(
            "https://api.bitget.com/api/v2/mix/market/open-interest",
            params={"symbol": "BTCUSDT", "productType": "USDT-FUTURES"},
            timeout=timeout,
        )
        row = (data.get("data") or [{}])[0]
        return float(row.get("openInterest") or row.get("size") or 0)

    bundle["price"] = _run("price", _price, bundle)
    bundle["open_interest"] = _run("open_interest", _oi, bundle)
    return bundle


def fetch_mexc(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://contract.mexc.com/api/v1/contract/ticker",
            params={"symbol": "BTC_USDT"},
            timeout=timeout,
        )
        payload = data.get("data") or {}
        if payload.get("fundingRate") is not None:
            bundle["funding_rate"] = float(payload["fundingRate"])
        return float(payload["lastPrice"])

    bundle["price"] = _run("price", _price, bundle)
    return bundle


def fetch_coinbase(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
            timeout=timeout,
        )
        return float(data["price"])

    bundle["price"] = _run("price", _price, bundle)
    return bundle


def fetch_kraken(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://api.kraken.com/0/public/Ticker",
            params={"pair": "XBTUSD"},
            timeout=timeout,
        )
        pair = (data.get("result") or {}).get("XXBTZUSD") or {}
        last = pair.get("c") or [None]
        return float(last[0])

    bundle["price"] = _run("price", _price, bundle)
    return bundle


EXCHANGE_FETCHERS: dict[str, Callable[..., Bundle]] = {
    "Bybit": fetch_bybit,
    "OKX": fetch_okx,
    "BingX": fetch_bingx,
    "Bitget": fetch_bitget,
    "MEXC": fetch_mexc,
    "Coinbase": fetch_coinbase,
    "Kraken": fetch_kraken,
}
