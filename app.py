"""Streamlit UI for Bitcoin market analysis."""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analysis.scorer import MarketAnalyzer
from src.ui.auth import render_login_gate
from src.ui.components import (
    render_dashboard,
    render_error_state,
    render_header_bar,
)
from src.ui.sidebar import AUTO_REFRESH_SECONDS, render_sidebar
from src.ui.styles import inject_global_styles
from src.ui.time_utils import normalize_last_updated

load_dotenv(ROOT / ".env", override=True)

st.set_page_config(
    page_title="AlphaBTC",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def _get_last_updated() -> datetime | None:
    return normalize_last_updated(st.session_state.get("last_updated"))


def _run_analysis(symbol: str, interval: str, api_key: str) -> None:
    analyzer = MarketAnalyzer(
        symbol=symbol,
        interval=interval,
        coinglass_api_key=api_key or None,
    )
    st.session_state["last_result"] = analyzer.analyze()
    st.session_state["last_updated"] = datetime.now(timezone.utc)


def _auto_refresh(symbol: str, interval: str, api_key: str) -> None:
    seconds = AUTO_REFRESH_SECONDS

    try:
        from streamlit_autorefresh import st_autorefresh

        tick = st_autorefresh(interval=seconds * 1000, key="btc_dashboard_autorefresh")
        if tick > 0 and "last_result" in st.session_state:
            try:
                _run_analysis(symbol, interval, api_key)
            except Exception:
                pass
        return
    except ImportError:
        pass

    try:
        @st.fragment(run_every=timedelta(seconds=seconds))
        def _refresh_worker() -> None:
            try:
                _run_analysis(symbol, interval, api_key)
            except Exception:
                return

        _refresh_worker()
    except TypeError:
        last = normalize_last_updated(st.session_state.get("last_updated"))
        if last is not None:
            elapsed = (datetime.now(timezone.utc) - last).total_seconds()
            if elapsed >= seconds:
                try:
                    _run_analysis(symbol, interval, api_key)
                except Exception:
                    pass
                st.rerun()
            remaining = max(5, int(seconds - elapsed))
            st.markdown(
                f'<meta http-equiv="refresh" content="{remaining}">',
                unsafe_allow_html=True,
            )


def main() -> None:
    inject_global_styles(dark_mode=True, project_root=ROOT, hide_sidebar=True)

    if not render_login_gate(project_root=ROOT):
        return

    sidebar = render_sidebar()
    render_header_bar(_get_last_updated())

    st.markdown('<div class="dashboard-shell">', unsafe_allow_html=True)
    st.markdown(
        '<p class="safety-banner">PRIVATE PROJECT</p>',
        unsafe_allow_html=True,
    )

    if "last_result" not in st.session_state:
        with st.spinner("Fetching market data and running AI analysis..."):
            try:
                _run_analysis(sidebar.symbol, sidebar.interval, sidebar.api_key)
            except Exception as exc:
                render_error_state(str(exc))
                st.markdown("</div>", unsafe_allow_html=True)
                return
        st.rerun()

    st.session_state["chart_interval"] = "1m"
    render_dashboard(
        st.session_state["last_result"],
        dark=True,
        risk_settings=sidebar.risk_settings,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    _auto_refresh(sidebar.symbol, sidebar.interval, sidebar.api_key)


if __name__ == "__main__":
    main()
