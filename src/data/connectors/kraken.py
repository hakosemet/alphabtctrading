"""Kraken market-data connector."""

from __future__ import annotations

from src.data.connectors.alt_exchange import AltExchangeConnector


class KrakenConnector(AltExchangeConnector):
    def __init__(self, timeout: int = 15) -> None:
        super().__init__("Kraken", timeout=timeout)
