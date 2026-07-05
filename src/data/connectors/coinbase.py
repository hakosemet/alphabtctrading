"""Coinbase market-data connector."""

from __future__ import annotations

from src.data.connectors.alt_exchange import AltExchangeConnector


class CoinbaseConnector(AltExchangeConnector):
    def __init__(self, timeout: int = 15) -> None:
        super().__init__("Coinbase", timeout=timeout)
