"""Data structures for the unified Bitcoin Data Hub."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

import pandas as pd

SourceStatus = Literal["online", "offline", "degraded", "placeholder"]


@dataclass
class SourceInfo:
    name: str
    status: SourceStatus
    last_updated: datetime | None = None
    error: str | None = None
    fields: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "error": self.error,
            "fields": self.fields,
        }


@dataclass
class HubSnapshot:
    price: float | None = None
    candles: pd.DataFrame | None = None
    volume: float | None = None
    order_book: dict[str, Any] | None = None
    funding_rate: float | None = None
    open_interest: float | None = None
    open_interest_change_pct: float | None = None
    long_short_ratio: float | None = None
    liquidations: dict[str, Any] | None = None
    onchain: dict[str, Any] = field(default_factory=dict)
    news: dict[str, Any] = field(default_factory=dict)
    sentiment: dict[str, Any] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)
    source_status: dict[str, SourceInfo] = field(default_factory=dict)
    last_updated: datetime | None = None
    missing_fields: list[str] = field(default_factory=list)
    available_fields: list[str] = field(default_factory=list)
    data_quality: str = "partial"
    confidence_impact: str = "none"
    critical_missing: bool = False
    force_wait: bool = False
    exchange_snapshots: dict[str, dict[str, Any]] = field(default_factory=dict)
    cross_exchange: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "price": self.price,
            "candles": None if self.candles is None else f"{len(self.candles)} rows",
            "volume": self.volume,
            "order_book": self.order_book,
            "funding_rate": self.funding_rate,
            "open_interest": self.open_interest,
            "open_interest_change_pct": self.open_interest_change_pct,
            "long_short_ratio": self.long_short_ratio,
            "liquidations": self.liquidations,
            "onchain": self.onchain,
            "news": self.news,
            "sentiment": self.sentiment,
            "sources": self.sources,
            "source_status": {k: v.to_dict() for k, v in self.source_status.items()},
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "missing_fields": self.missing_fields,
            "available_fields": self.available_fields,
            "data_quality": self.data_quality,
            "confidence_impact": self.confidence_impact,
            "critical_missing": self.critical_missing,
            "force_wait": self.force_wait,
            "exchange_snapshots": self.exchange_snapshots,
            "cross_exchange": self.cross_exchange,
        }
