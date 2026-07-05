"""BingX market-data connector."""

from __future__ import annotations

from src.data.connectors.alt_exchange import AltExchangeConnector


class BingXConnector(AltExchangeConnector):
    def __init__(self, timeout: int = 15) -> None:
        super().__init__("BingX", timeout=timeout)
