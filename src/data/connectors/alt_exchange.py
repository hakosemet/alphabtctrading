"""Shared alt-exchange connector built on public REST APIs."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.data.connectors.base import BaseConnector
from src.data.exchange_api import EXCHANGE_FETCHERS
from src.data.hub_models import SourceInfo


class AltExchangeConnector(BaseConnector):
    enabled = True

    def __init__(self, exchange_key: str, *, timeout: int = 15) -> None:
        super().__init__(timeout=timeout)
        if exchange_key not in EXCHANGE_FETCHERS:
            raise ValueError(f"Unknown exchange: {exchange_key}")
        self.name = exchange_key
        self._fetch = EXCHANGE_FETCHERS[exchange_key]

    def probe(self) -> SourceInfo:
        bundle = self._fetch(timeout=self.timeout)
        if bundle.get("price") is None:
            errors = "; ".join(bundle.get("errors") or []) or "No price"
            return self._info(status="offline", error=errors)
        fields = [field for field in ("price", "funding_rate", "open_interest") if bundle.get(field) is not None]
        status = "degraded" if bundle.get("errors") else "online"
        return self._info(status=status, fields=fields, error="; ".join(bundle.get("errors") or []) or None)

    def fetch_market_bundle(self, interval: str = "1h", limit: int = 500) -> dict[str, Any]:
        del interval, limit
        return self._fetch(timeout=self.timeout)
