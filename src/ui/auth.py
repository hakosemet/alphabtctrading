"""Password gate for dashboard access."""

from __future__ import annotations

import os
import secrets
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.ui.primitives import bitcoin_chart_logo, login_purchase_panel
from src.analytics.tiktok_pixel import track_view_content

ROOT = Path(__file__).resolve().parents[2]
_SESSION_KEY = "authenticated"


def is_authenticated() -> bool:
    return bool(st.session_state.get(_SESSION_KEY))


def _expected_password() -> str:
    load_dotenv(ROOT / ".env", override=True)
    return os.getenv("DASHBOARD_PASSWORD", "").strip()


def _render_html_block(html: str) -> None:
    """Render trusted HTML via markdown (st.html shows a white box with raw tags)."""
    st.markdown(html, unsafe_allow_html=True)


def _render_login_logo() -> None:
    """Large centered Bitcoin logo on the login screen."""
    _render_html_block(bitcoin_chart_logo(placement="login"))


def render_login_gate(*, project_root: Path) -> bool:
    """Show the entry password screen. Returns True when access is granted."""
    del project_root  # reserved for future branding assets

    if is_authenticated():
        return True

    expected = _expected_password()
    if not expected:
        st.error("Dashboard password is not configured. Set DASHBOARD_PASSWORD in your .env file.")
        return False

    _col_left, col_center, _col_right = st.columns([0.35, 3.3, 0.35])
    with col_center:
        _render_login_logo()

        # TikTok event — ViewContent: login / purchase panel visible
        track_view_content(content_category="login")

        with st.form("dashboard_login", clear_on_submit=False):
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Enter Dashboard", type="primary", use_container_width=True)

        if submitted:
            if secrets.compare_digest(password, expected):
                st.session_state[_SESSION_KEY] = True
                from src.ui.performance import clear_analysis_cache

                clear_analysis_cache()
                st.rerun()
            st.error("Incorrect password. Please try again.")

        _render_html_block(login_purchase_panel())

    return False
