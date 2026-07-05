"""UI entry points — thin facade over dashboard and shared widgets."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from src.ui.dashboard import render_dashboard
from src.ui.time_utils import normalize_last_updated
from src.ui.tradingview import render_tradingview_chart
from src.ui.primitives import empty_state, error_state, premium_nav, welcome_empty_state

__all__ = [
    "render_header_bar",
    "render_analyze_button",
    "render_empty_state",
    "render_error_state",
    "render_dashboard",
    "render_tradingview_chart",
]


def render_header_bar(last_updated: datetime | None = None) -> None:
    """Render the premium navigation header."""
    safe_updated = normalize_last_updated(last_updated)
    st.markdown(premium_nav(last_updated=safe_updated), unsafe_allow_html=True)


def render_analyze_button() -> bool:
    return st.button("Analyze Market", type="primary", use_container_width=True)


def render_empty_state() -> None:
    html = welcome_empty_state()
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)


def render_error_state(message: str) -> None:
    st.markdown(error_state(message), unsafe_allow_html=True)
