"""Design tokens and theme palettes."""

from __future__ import annotations

APP_VERSION = "1.0"

BRAND = {
    "author_he": "אופיר קדוש",
    "author_en": "Ofir Kadosh",
    "since_year": "2026",
    "product": "AlphaBTC",
    "website": "https://alphabtctrading.com",
    "website_label": "alphabtctrading.com",
    "contact_email": "AlphabtcTool@outlook.com",
}


def brand_caption() -> str:
    """Author line shown under the app title."""
    return "AlphaBTC Private Project ( Don't bring anyone )"


# Bitcoin brand colors
BITCOIN_ORANGE = "#F7931A"
BITCOIN_ORANGE_DARK = "#E8820C"
BITCOIN_ORANGE_LIGHT = "#FFB84D"
BITCOIN_GOLD = "#F2A900"
BITCOIN_CREAM = "#FFF4E6"
BITCOIN_CREAM_SURFACE = "#FFFAF3"

LIGHT_PALETTE = {
    "bg": "#FFF4E6",
    "surface": "#FFFAF3",
    "surface_alt": "#FFEED9",
    "border": "#F5D5A8",
    "text": "#1A1108",
    "text_secondary": "#6B4423",
    "text_muted": "#9A7349",
    "accent": BITCOIN_ORANGE,
    "accent_hover": BITCOIN_ORANGE_DARK,
    "accent_soft": "#FFE8CC",
    "long": "#059669",
    "long_bg": "#ecfdf5",
    "long_border": "#a7f3d0",
    "short": "#dc2626",
    "short_bg": "#fef2f2",
    "short_border": "#fecaca",
    "wait": BITCOIN_GOLD,
    "wait_bg": "#FFF8E7",
    "wait_border": "#F5D58A",
    "error_bg": "#fef2f2",
    "error_border": "#fecaca",
    "error_text": "#991b1b",
    "heatmap_mid": BITCOIN_GOLD,
    "chart_grid": "#F5D5A8",
}

DARK_PALETTE = {
    "bg": "#080604",
    "surface": "#16100a",
    "surface_alt": "#22160e",
    "border": "#3d2a18",
    "text": "#FFF9F2",
    "text_secondary": "#E0B88A",
    "text_muted": "#A67C52",
    "accent": BITCOIN_ORANGE,
    "accent_hover": BITCOIN_ORANGE_LIGHT,
    "accent_soft": "rgba(247, 147, 26, 0.16)",
    "long": "#34d399",
    "long_bg": "rgba(6, 78, 59, 0.42)",
    "long_border": "#065f46",
    "short": "#f87171",
    "short_bg": "rgba(69, 10, 10, 0.42)",
    "short_border": "#7f1d1d",
    "wait": BITCOIN_GOLD,
    "wait_bg": "rgba(61, 46, 10, 0.5)",
    "wait_border": "#78550F",
    "error_bg": "#450a0a",
    "error_border": "#7f1d1d",
    "error_text": "#fecaca",
    "heatmap_mid": BITCOIN_ORANGE,
    "chart_grid": "#3d2818",
}

SPACING = {
    "xs": "0.5rem",
    "sm": "0.875rem",
    "md": "1.25rem",
    "lg": "1.75rem",
    "xl": "2.5rem",
}
RADIUS = {"sm": "12px", "md": "16px", "lg": "20px", "full": "999px"}
SHADOW = {
    "sm": "0 2px 10px rgba(0, 0, 0, 0.22), 0 1px 3px rgba(0, 0, 0, 0.14)",
    "md": "0 14px 36px rgba(0, 0, 0, 0.32), 0 0 0 1px rgba(247, 147, 26, 0.08)",
    "lg": "0 24px 56px rgba(0, 0, 0, 0.42), 0 0 0 1px rgba(247, 147, 26, 0.12)",
}
FONT = {
    "sans": "'Inter', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
    "display": "'Inter', 'Segoe UI', system-ui, sans-serif",
}

RECOMMENDATION_STYLE: dict[str, dict[str, str]] = {
    "long": {"label": "LONG", "symbol": "▲", "tone": "long"},
    "short": {"label": "SHORT", "symbol": "▼", "tone": "short"},
    "wait": {"label": "WAIT", "symbol": "◆", "tone": "wait"},
}

PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}


def get_palette(dark: bool = False) -> dict[str, str]:
    return DARK_PALETTE if dark else LIGHT_PALETTE


def score_tone(score: float) -> str:
    if score >= 62:
        return "long"
    if score <= 38:
        return "short"
    return "wait"


def score_color(score: float, dark: bool = False) -> str:
    palette = get_palette(dark)
    return palette[score_tone(score)]


def gauge_steps(dark: bool = False) -> list[dict]:
    palette = get_palette(dark)
    return [
        {"range": [0, 38], "color": palette["short_bg"]},
        {"range": [38, 62], "color": palette["wait_bg"]},
        {"range": [62, 100], "color": palette["long_bg"]},
    ]


def confidence_percent(confidence: str) -> int:
    return {"High": 85, "Medium": 62, "Low": 38}.get(confidence, 50)


def chart_layout(palette: dict[str, str]) -> dict:
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter, system-ui, sans-serif",
            "color": palette["text_secondary"],
            "size": 12,
        },
        "margin": {"l": 12, "r": 12, "t": 44, "b": 12},
        "xaxis": {"gridcolor": palette["chart_grid"], "zerolinecolor": palette["chart_grid"]},
        "yaxis": {"gridcolor": palette["chart_grid"], "zerolinecolor": palette["chart_grid"]},
    }
