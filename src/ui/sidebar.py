"""Sidebar settings — no visible sidebar UI (analysis runs automatically after login)."""

from __future__ import annotations

import os
from dataclasses import dataclass

__all__ = ["SidebarSettings", "AUTO_REFRESH_SECONDS", "render_sidebar"]

AUTO_REFRESH_SECONDS = 60
AUTO_TIMEFRAME = "1m"
DEFAULT_ACCOUNT_SIZE = 10_000.0
DEFAULT_MAX_RISK_PCT = 1.0


@dataclass
class SidebarSettings:
    symbol: str
    interval: str
    api_key: str
    dark_mode: bool
    analyze_clicked: bool
    auto_refresh: bool
    refresh_seconds: int
    risk_settings: dict[str, float]


def render_sidebar() -> SidebarSettings:
    """Return dashboard configuration (sidebar hidden in UI)."""
    return SidebarSettings(
        symbol="BTCUSDT",
        interval=AUTO_TIMEFRAME,
        api_key=os.getenv("COINGLASS_API_KEY", ""),
        dark_mode=True,
        analyze_clicked=False,
        auto_refresh=True,
        refresh_seconds=AUTO_REFRESH_SECONDS,
        risk_settings={
            "max_risk_pct": DEFAULT_MAX_RISK_PCT,
            "account_size": DEFAULT_ACCOUNT_SIZE,
        },
    )
