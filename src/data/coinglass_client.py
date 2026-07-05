"""Optional Coinglass API client for derivatives and liquidation heatmap data."""

from __future__ import annotations

import os
from typing import Any

import pandas as pd
import requests

BASE_URL = "https://open-api-v4.coinglass.com"


class CoinglassClient:
    def __init__(self, api_key: str | None = None, timeout: int = 15) -> None:
        self.api_key = api_key or os.getenv("COINGLASS_API_KEY", "").strip()
        self.timeout = timeout
        self.enabled = bool(self.api_key)

    def _headers(self) -> dict[str, str]:
        return {"CG-API-KEY": self.api_key, "accept": "application/json"}

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        if not self.enabled:
            return None
        url = f"{BASE_URL}{path}"
        response = requests.get(
            url,
            headers=self._headers(),
            params=params or {},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if str(payload.get("code")) != "0":
            raise ValueError(payload.get("msg", "Coinglass API error"))
        return payload.get("data")

    def get_funding_rates(self) -> list[dict[str, Any]] | None:
        try:
            data = self._get("/api/futures/funding-rate/exchange-list")
            if not data:
                return None
            for item in data:
                if item.get("symbol") == "BTC":
                    return item.get("stablecoin_margin_list") or []
            return None
        except (requests.RequestException, ValueError):
            return None

    def get_open_interest_history(
        self,
        exchange: str = "Binance",
        interval: str = "1h",
        limit: int = 50,
    ) -> pd.DataFrame | None:
        try:
            data = self._get(
                "/api/futures/open-interest/history",
                {
                    "exchange": exchange,
                    "symbol": "BTCUSDT",
                    "interval": interval,
                    "limit": limit,
                },
            )
            if not data:
                return None
            df = pd.DataFrame(data)
            for col in ("open", "high", "low", "close"):
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            if "time" in df.columns:
                df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
            return df
        except (requests.RequestException, ValueError):
            return None

    def get_liquidation_heatmap(self, range_param: str = "3d") -> dict[str, Any] | None:
        """Fetch liquidation heatmap model2 data when API key is available."""
        try:
            return self._get(
                "/api/futures/liquidation/heatmap/model2",
                {"symbol": "BTC", "range": range_param},
            )
        except (requests.RequestException, ValueError):
            return None

    def get_long_short_ratio_history(
        self,
        interval: str = "1h",
        limit: int = 50,
    ) -> pd.DataFrame | None:
        try:
            data = self._get(
                "/api/futures/global-long-short-account-ratio/history",
                {"symbol": "BTC", "interval": interval, "limit": limit},
            )
            if not data:
                return None
            df = pd.DataFrame(data)
            for col in ("longRate", "shortRate", "longShortRatio"):
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            if "time" in df.columns:
                df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
            return df
        except (requests.RequestException, ValueError):
            return None
