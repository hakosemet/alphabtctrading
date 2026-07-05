"""Fetch OHLCV and derivatives data from Binance public APIs."""

from __future__ import annotations

from typing import Any

import pandas as pd
import requests

SPOT_BASE = "https://api.binance.com"
FUTURES_BASE = "https://fapi.binance.com"


class BinanceClient:
    def __init__(self, symbol: str = "BTCUSDT", timeout: int = 15) -> None:
        self.symbol = symbol
        self.timeout = timeout

    def _get(self, base: str, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{base}{path}"
        response = requests.get(url, params=params or {}, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_klines(
        self,
        interval: str = "1h",
        limit: int = 500,
    ) -> pd.DataFrame:
        raw = self._get(
            SPOT_BASE,
            "/api/v3/klines",
            {"symbol": self.symbol, "interval": interval, "limit": limit},
        )
        df = pd.DataFrame(
            raw,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_volume",
                "trades",
                "taker_buy_base",
                "taker_buy_quote",
                "ignore",
            ],
        )
        numeric_cols = ["open", "high", "low", "close", "volume", "quote_volume", "taker_buy_base"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)
        return df

    def get_funding_rate(self) -> float | None:
        try:
            data = self._get(
                FUTURES_BASE,
                "/fapi/v1/premiumIndex",
                {"symbol": self.symbol},
            )
            return float(data.get("lastFundingRate", 0))
        except requests.RequestException:
            return None

    def get_open_interest(self) -> float | None:
        try:
            data = self._get(
                FUTURES_BASE,
                "/fapi/v1/openInterest",
                {"symbol": self.symbol},
            )
            return float(data.get("openInterest", 0))
        except requests.RequestException:
            return None

    def get_long_short_ratio(self, period: str = "1h", limit: int = 30) -> pd.DataFrame | None:
        try:
            raw = self._get(
                FUTURES_BASE,
                "/futures/data/globalLongShortAccountRatio",
                {"symbol": self.symbol, "period": period, "limit": limit},
            )
            df = pd.DataFrame(raw)
            if df.empty:
                return None
            df["longShortRatio"] = pd.to_numeric(df["longShortRatio"], errors="coerce")
            df["longAccount"] = pd.to_numeric(df["longAccount"], errors="coerce")
            df["shortAccount"] = pd.to_numeric(df["shortAccount"], errors="coerce")
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
            return df
        except requests.RequestException:
            return None

    def get_ticker_price(self) -> float:
        data = self._get(SPOT_BASE, "/api/v3/ticker/price", {"symbol": self.symbol})
        return float(data["price"])

    def get_order_book(self, limit: int = 20) -> dict | None:
        try:
            data = self._get(
                SPOT_BASE,
                "/api/v3/depth",
                {"symbol": self.symbol, "limit": limit},
            )
            return {
                "bids": data.get("bids", []),
                "asks": data.get("asks", []),
                "lastUpdateId": data.get("lastUpdateId"),
            }
        except requests.RequestException:
            return None
