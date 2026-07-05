"""Primary Binance market-data connector."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.data.binance_client import BinanceClient
from src.data.connectors.base import BaseConnector
from src.data.hub_models import SourceInfo


class BinanceConnector(BaseConnector):
    name = "Binance"
    enabled = True

    def __init__(self, symbol: str = "BTCUSDT", timeout: int = 15) -> None:
        super().__init__(timeout=timeout)
        self.symbol = symbol
        self.client = BinanceClient(symbol=symbol, timeout=timeout)

    def probe(self) -> SourceInfo:
        price, error = self.safe_call("price", self.client.get_ticker_price)
        if price is None:
            return self._info(status="offline", error=error)
        return self._info(
            status="online",
            fields=["price", "candles", "volume", "order_book", "funding_rate", "open_interest", "long_short_ratio"],
        )

    def fetch_market_bundle(self, interval: str, limit: int = 500) -> dict[str, Any]:
        bundle: dict[str, Any] = {
            "price": None,
            "candles": None,
            "volume": None,
            "order_book": None,
            "funding_rate": None,
            "open_interest": None,
            "long_short_ratio": None,
            "errors": [],
        }

        price, err = self.safe_call("price", self.client.get_ticker_price)
        bundle["price"] = price
        if err:
            bundle["errors"].append(err)

        candles, err = self.safe_call("candles", lambda: self.client.get_klines(interval=interval, limit=limit))
        bundle["candles"] = candles
        if err:
            bundle["errors"].append(err)
        elif isinstance(candles, pd.DataFrame) and not candles.empty:
            bundle["volume"] = float(candles.iloc[-1]["volume"])

        order_book, err = self.safe_call("order_book", lambda: self.client.get_order_book(limit=20))
        bundle["order_book"] = order_book
        if err:
            bundle["errors"].append(err)

        funding, err = self.safe_call("funding_rate", self.client.get_funding_rate)
        bundle["funding_rate"] = funding
        if err:
            bundle["errors"].append(err)

        oi, err = self.safe_call("open_interest", self.client.get_open_interest)
        bundle["open_interest"] = oi
        if err:
            bundle["errors"].append(err)

        ls_df, err = self.safe_call(
            "long_short_ratio",
            lambda: self.client.get_long_short_ratio(period=interval),
        )
        if isinstance(ls_df, pd.DataFrame) and not ls_df.empty:
            bundle["long_short_ratio"] = float(ls_df.iloc[-1]["longShortRatio"])
        elif err:
            bundle["errors"].append(err)

        return bundle
