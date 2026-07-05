"""Tabbed dashboard layout."""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

from src.ui.charts import render_score_gauge
from src.ui.helpers import indicator_rows, signal_plain_language_summary
from src.ui.primitives import (
    bitcoin_chart_brand,
    bitcoin_chart_logo,
    brand_footer,
    component_card,
    empty_state,
    market_signal_hero,
    metric_card,
    metric_card_wrap,
    prose_block,
    risk_enhanced_panel,
    risk_warning_banner,
    section_heading,
)
from src.ui.theme import RECOMMENDATION_STYLE, confidence_percent
from src.ui.tradingview import render_tradingview_chart

if TYPE_CHECKING:
    from src.analysis.models import AnalysisResult


def _render_metric_row(cards: list[str], columns: int = 4) -> None:
    cols = st.columns(columns, gap="medium")
    for col, card in zip(cols, cards, strict=False):
        with col:
            st.markdown(metric_card_wrap(card), unsafe_allow_html=True)


def render_ai_dashboard_tab(result: AnalysisResult, *, dark: bool) -> None:
    interval = st.session_state.get("chart_interval", "1m")

    st.markdown('<div class="ai-dashboard-top">', unsafe_allow_html=True)
    st.markdown(
        market_signal_hero(result.recommendation, result.confidence),
        unsafe_allow_html=True,
    )
    st.markdown(section_heading("Live Chart", tight=True, large=True), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(bitcoin_chart_logo(placement="above"), unsafe_allow_html=True)
    st.markdown(
        '<p class="chart-tagline">LETS MAKE MONEY $</p>',
        unsafe_allow_html=True,
    )
    render_tradingview_chart(interval=interval, dark=dark)
    st.markdown(bitcoin_chart_logo(placement="below"), unsafe_allow_html=True)
    st.markdown(bitcoin_chart_brand(), unsafe_allow_html=True)


def render_overview_tab(result: AnalysisResult, *, dark: bool) -> None:
    style = RECOMMENDATION_STYLE[result.recommendation]

    st.markdown('<div class="overview-tab">', unsafe_allow_html=True)

    _render_metric_row([
        metric_card("Price", f"${result.price:,.2f}"),
        metric_card("Direction", style["label"], tone=style["tone"]),
        metric_card("Signal strength", f"{result.confidence} · {confidence_percent(result.confidence)}%"),
        metric_card("Risk / Reward", f"{result.risk_reward:.2f}", tone="long" if result.risk_reward >= 1.5 else "wait"),
    ])

    st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.15, 1], gap="large")
    with left:
        render_score_gauge(result.score, dark=dark)
    with right:
        badge_html = (
            f'<div class="overview-signal-only">'
            f'<div class="signal-badge signal-badge--{style["tone"]}">{style["label"]}</div>'
            f"</div>"
        )
        if hasattr(st, "html"):
            st.html(badge_html)
        else:
            st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_trade_setup_tab(result: AnalysisResult, *, dark: bool) -> None:
    setup = result.trade_setup or {}
    direction = setup.get("direction") or result.recommendation
    if direction not in ("long", "short"):
        direction = "long" if result.score >= 50 else "short"
    style = RECOMMENDATION_STYLE[direction]

    st.markdown(section_heading("Trade Setup"), unsafe_allow_html=True)

    tp_tone = "long" if direction == "long" else "short"
    sl_tone = "short" if direction == "long" else "long"
    _render_metric_row([
        metric_card("Direction", style["label"], tone=style["tone"]),
        metric_card("Entry", f"${setup.get('entry', result.price):,.2f}"),
        metric_card("Stop Loss", f"${setup.get('stop_loss', 0):,.2f}", tone=sl_tone),
        metric_card("TP1", f"${setup.get('tp1', 0):,.2f}", tone=tp_tone),
    ], columns=4)
    _render_metric_row([
        metric_card("TP2", f"${setup.get('tp2', 0):,.2f}", tone=tp_tone),
        metric_card("TP3", f"${setup.get('tp3', 0):,.2f}", tone=tp_tone),
        metric_card("TP4", f"${setup.get('tp4', 0):,.2f}", tone=tp_tone),
        metric_card("R/R", f"{setup.get('risk_reward', 0):.2f}", tone="long" if setup.get("risk_reward", 0) >= 1.5 else "wait"),
    ], columns=4)
    st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)

    st.markdown(section_heading("Live Chart", large=True), unsafe_allow_html=True)
    interval = st.session_state.get("chart_interval", "1m")
    render_tradingview_chart(
        interval=interval,
        dark=dark,
        height=480,
        chart_id="btc-trade-setup-chart",
    )


def render_risk_tab(result: AnalysisResult, *, risk_settings: dict[str, float]) -> None:
    st.markdown(section_heading("Risk Overview"), unsafe_allow_html=True)
    st.markdown(risk_enhanced_panel(result.risk_profile), unsafe_allow_html=True)

    max_risk_pct = float(risk_settings.get("max_risk_pct", 1.0))
    account_size = float(risk_settings.get("account_size", 10000.0))
    risk_per_unit = abs(result.price - result.stop_loss)
    max_risk_usd = account_size * (max_risk_pct / 100)
    position_size = max_risk_usd / risk_per_unit if risk_per_unit > 0 else 0.0
    position_value = position_size * result.price
    pct = confidence_percent(result.confidence)

    st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)
    _render_metric_row([
        metric_card("Sidebar Risk / Trade", f"{max_risk_pct:.2f}%"),
        metric_card("Risk Budget", f"${max_risk_usd:,.2f}"),
        metric_card("Est. Position Size", f"{position_size:.4f} BTC"),
        metric_card("Position Value", f"${position_value:,.2f}"),
    ])

    summary = signal_plain_language_summary(result.recommendation, result.confidence, result.score)
    lines = [
        f"Stop distance: ${risk_per_unit:,.2f} per BTC",
        f"Direction: {result.recommendation.upper()} (score {result.score:.0f}/100)",
        f"Signal strength: {result.confidence} ({pct}%)",
        "",
        summary[2][1],
        "",
        "Position sizing uses sidebar settings. AI engine uses 1% risk baseline for suggestions.",
    ]
    st.markdown(prose_block("\n".join(lines)), unsafe_allow_html=True)
    st.markdown(
        risk_warning_banner(result.recommendation, result.confidence, result.score),
        unsafe_allow_html=True,
    )


def render_indicators_tab(result: AnalysisResult) -> None:
    st.markdown(section_heading("Technical Indicators"), unsafe_allow_html=True)
    rows = indicator_rows(result)
    for i in range(0, len(rows), 4):
        chunk = rows[i : i + 4]
        _render_metric_row(
            [metric_card(label, value, tone=tone) for label, value, tone in chunk],
            columns=min(4, len(chunk)),
        )
        st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)

    st.markdown(section_heading("Signal Components"), unsafe_allow_html=True)
    cols = st.columns(3, gap="medium")
    for idx, component in enumerate(result.components):
        with cols[idx % 3]:
            st.markdown(component_card(component.name, component.score, component.detail), unsafe_allow_html=True)


def render_dashboard(
    result: AnalysisResult,
    *,
    dark: bool,
    risk_settings: dict[str, float] | None = None,
) -> None:
    settings = risk_settings or {}
    tabs = st.tabs([
        "AI Dashboard",
        "Overview",
        "Trade Setup",
        "Risk",
        "Indicators",
    ])

    with tabs[0]:
        render_ai_dashboard_tab(result, dark=dark)
    with tabs[1]:
        render_overview_tab(result, dark=dark)
    with tabs[2]:
        render_trade_setup_tab(result, dark=dark)
    with tabs[3]:
        render_risk_tab(result, risk_settings=settings)
    with tabs[4]:
        render_indicators_tab(result)

    st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)
    st.markdown(
        brand_footer(sources=", ".join(result.data_sources)),
        unsafe_allow_html=True,
    )
