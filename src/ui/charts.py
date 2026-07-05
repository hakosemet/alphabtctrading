"""Theme-aware Plotly charts."""

from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.graph_objects as go
import streamlit as st

from src.ui.theme import PLOTLY_CONFIG, chart_layout, gauge_steps, get_palette, score_color

if TYPE_CHECKING:
    from src.analysis.models import AnalysisResult

_GAUGE_HEIGHT = 360
_HEATMAP_HEIGHT = 400


def render_score_gauge(score: float, *, dark: bool = False) -> None:
    palette = get_palette(dark)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={
                "suffix": "/100",
                "font": {"size": 48, "color": palette["text"], "family": "Inter, system-ui, sans-serif"},
            },
            title={"text": "Composite Score", "font": {"size": 15, "color": palette["text_secondary"]}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickmode": "array",
                    "tickvals": [19, 50, 81],
                    "ticktext": ["Weak", "Neutral", "Strong"],
                    "tickcolor": palette["text_muted"],
                    "tickfont": {"size": 12, "color": palette["text_secondary"]},
                },
                "bar": {"color": score_color(score, dark), "thickness": 0.72},
                "bgcolor": palette["surface_alt"],
                "borderwidth": 0,
                "steps": gauge_steps(dark),
            },
        )
    )
    layout = chart_layout(palette)
    layout["margin"] = {"l": 24, "r": 24, "t": 56, "b": 36}
    fig.update_layout(height=_GAUGE_HEIGHT, **layout)
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


def render_heatmap_chart(result: AnalysisResult, *, dark: bool = False) -> None:
    palette = get_palette(dark)
    heatmap = result.heatmap
    if heatmap is None or heatmap.empty:
        return

    intensity_col = "intensity" if "intensity" in heatmap.columns else "volume"
    fig = go.Figure(
        go.Bar(
            x=heatmap[intensity_col],
            y=heatmap["price_level"],
            orientation="h",
            marker=dict(
                color=heatmap[intensity_col],
                colorscale=[
                    [0, palette["surface_alt"]],
                    [0.5, palette["heatmap_mid"]],
                    [1, palette["short"]],
                ],
                showscale=True,
                colorbar=dict(title="Intensity", thickness=10, len=0.55, outlinewidth=0),
            ),
            hovertemplate="Price: $%{y:,.0f}<br>Intensity: %{x:.2f}<extra></extra>",
        )
    )
    fig.add_hline(
        y=result.price,
        line_dash="dash",
        line_color=palette["accent"],
        line_width=1.5,
        annotation_text=f"${result.price:,.0f}",
        annotation_font=dict(color=palette["accent"], size=10),
    )
    fig.update_layout(
        height=_HEATMAP_HEIGHT,
        title=dict(text=result.heatmap_source, font=dict(size=12, color=palette["text_muted"])),
        xaxis_title="Intensity",
        yaxis_title="Price (USD)",
        **chart_layout(palette),
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


def render_volume_chart(volumes: list[float], *, dark: bool = False) -> None:
    """Bar chart of recent BTC candle volume."""
    if not volumes:
        return

    palette = get_palette(dark)
    fig = go.Figure(
        go.Bar(
            x=list(range(1, len(volumes) + 1)),
            y=volumes,
            marker=dict(color=palette["accent"], opacity=0.85),
            hovertemplate="Bar %{x}<br>Volume: %{y:,.2f} BTC<extra></extra>",
        )
    )
    fig.update_layout(
        height=280,
        title=dict(text="BTC Volume (last candles)", font=dict(size=12, color=palette["text_muted"])),
        xaxis_title="Candle",
        yaxis_title="Volume (BTC)",
        **chart_layout(palette),
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
