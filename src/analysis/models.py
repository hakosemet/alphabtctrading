"""Analysis result data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import pandas as pd

Recommendation = Literal["long", "short", "wait"]


@dataclass
class ComponentScore:
    name: str
    score: float
    weight: float
    detail: str


@dataclass
class MarketStatusPanel:
    trend: str
    volatility: str
    liquidity: str


@dataclass
class TradeQuality:
    grade: str
    score: int
    stars: int


@dataclass
class DashboardInsights:
    market_status: MarketStatusPanel
    trade_quality: TradeQuality
    fear_greed: dict[str, Any] = field(default_factory=dict)
    news_sentiment: dict[str, Any] = field(default_factory=dict)
    onchain_data: dict[str, Any] = field(default_factory=dict)
    whale_data: dict[str, Any] = field(default_factory=dict)
    source_status: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisResult:
    symbol: str
    price: float
    score: float
    recommendation: Recommendation
    confidence: str
    stop_loss: float
    take_profit: float
    risk_reward: float
    explanation: str
    components: list[ComponentScore] = field(default_factory=list)
    indicators: dict = field(default_factory=dict)
    heatmap_source: str = "volume_profile"
    data_sources: list[str] = field(default_factory=list)
    heatmap: pd.DataFrame | None = None
    hub: dict | None = None
    supported_sources: list[str] = field(default_factory=list)
    data_quality: str = "full"
    insights: DashboardInsights | None = None
    take_profits: dict[str, float] = field(default_factory=dict)
    risk_profile: dict[str, float] = field(default_factory=dict)
    reasons_enter: list[str] = field(default_factory=list)
    reasons_avoid: list[str] = field(default_factory=list)
    fear_greed: dict[str, Any] = field(default_factory=dict)
    news_sentiment: dict[str, Any] = field(default_factory=dict)
    onchain_data: dict[str, Any] = field(default_factory=dict)
    whale_data: dict[str, Any] = field(default_factory=dict)
    source_status: dict[str, Any] = field(default_factory=dict)
    enhanced_explanation: str = ""
    trade_setup: dict[str, Any] = field(default_factory=dict)
    trade_setups: list[dict[str, Any]] = field(default_factory=list)
    platform_checks: dict[str, Any] = field(default_factory=dict)
