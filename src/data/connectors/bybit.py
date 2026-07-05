"""Bybit market-data connector."""

from __future__ import annotations

from src.data.connectors.alt_exchange import AltExchangeConnector


class BybitConnector(AltExchangeConnector):
    def __init__(self, timeout: int = 15) -> None:
        super().__init__("Bybit", timeout=timeout)
