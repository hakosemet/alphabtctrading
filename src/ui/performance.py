"""Streamlit caching layer — keeps analyzers alive and skips duplicate market fetches."""

from __future__ import annotations

import streamlit as st

from src.analysis.models import AnalysisResult
from src.analysis.scorer import MarketAnalyzer
from src.ui.sidebar import AUTO_REFRESH_SECONDS

# Refresh slightly before the UI auto-refresh so users see new data on schedule.
_ANALYSIS_CACHE_TTL = max(30, AUTO_REFRESH_SECONDS - 5)


@st.cache_resource(show_spinner=False)
def get_market_analyzer(symbol: str, interval: str, api_key: str) -> MarketAnalyzer:
    """Reuse one analyzer (and its in-memory hub TTL cache) across reruns."""
    return MarketAnalyzer(
        symbol=symbol,
        interval=interval,
        coinglass_api_key=api_key or None,
    )


@st.cache_data(ttl=_ANALYSIS_CACHE_TTL, show_spinner=False)
def run_cached_market_analysis(symbol: str, interval: str, api_key: str) -> AnalysisResult:
    """Cache full analysis output to prevent repeated API work on Streamlit reruns."""
    analyzer = get_market_analyzer(symbol, interval, api_key)
    return analyzer.analyze()


def clear_analysis_cache() -> None:
    """Clear cached analysis after auth changes or manual refresh hooks."""
    run_cached_market_analysis.clear()
    get_market_analyzer.clear()
