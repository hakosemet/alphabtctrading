"""UI helper utilities — presentation text and safe formatting."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.ui.time_utils import format_last_updated, normalize_last_updated

if TYPE_CHECKING:
    from src.analysis.models import AnalysisResult

from src.ui.theme import confidence_percent

__all__ = [
    "normalize_last_updated",
    "format_last_updated",
    "component_bias",
    "recommendation_insight",
    "signal_plain_language_summary",
    "indicator_rows",
]


def component_bias(score: float) -> str:
    if score >= 55:
        return "bullish"
    if score <= 45:
        return "bearish"
    return "neutral"


def recommendation_insight(result: AnalysisResult) -> str:
    """One-line assistant-style summary for the recommendation panel."""
    drivers = sorted(result.components, key=lambda c: abs(c.score - 50), reverse=True)[:2]
    driver_text = ", ".join(f"{c.name} ({component_bias(c.score)})" for c in drivers)

    templates = {
        "long": (
            f"Bullish momentum detected across key indicators. "
            f"Primary drivers: {driver_text}. Consider long exposure with defined risk."
        ),
        "short": (
            f"Bearish pressure is building in the market structure. "
            f"Primary drivers: {driver_text}. Short bias favored with tight risk control."
        ),
        "wait": (
            f"Signals are mixed and conviction is low. "
            f"Primary drivers: {driver_text}. Wait for clearer alignment before entering."
        ),
    }
    return templates[result.recommendation]


def signal_plain_language_summary(
    recommendation: str,
    confidence: str,
    score: float,
) -> list[tuple[str, str]]:
    """Plain-language explanation of direction, confidence, and suggested action."""
    pct = confidence_percent(confidence)
    direction_label = recommendation.upper()

    direction_text = {
        "long": (
            f"The overall score is {score:.0f}/100. "
            "Technically, the market leans bullish — a buy-side bias (LONG)."
        ),
        "short": (
            f"The overall score is {score:.0f}/100. "
            "Technically, the market leans bearish — a sell-side bias (SHORT)."
        ),
        "wait": (
            f"The overall score is {score:.0f}/100. "
            "Signals are mixed — there is no clear direction yet (WAIT)."
        ),
    }[recommendation]

    confidence_text = {
        "High": (
            f"Confidence is high ({pct}%). "
            "Most indicators point the same way — the signal is relatively strong."
        ),
        "Medium": (
            f"Confidence is medium ({pct}%). "
            "Some indicators agree, but not all — proceed with caution."
        ),
        "Low": (
            f"Confidence is low ({pct}%). "
            "Indicators disagree or some data is missing — the signal is weak."
        ),
    }.get(
        confidence,
        f"Confidence is {confidence.lower()} ({pct}%).",
    )

    if recommendation == "wait":
        action_text = "Stay on the sidelines until indicators align more clearly."
    elif pct >= 70:
        action_text = (
            f"Direction and confidence agree. "
            f"You may consider a {direction_label} setup with defined risk and a stop loss."
        )
    else:
        action_text = (
            f"The badge shows {direction_label}, but confidence is too low for an aggressive entry. "
            "Wait for stronger alignment before opening a position."
        )

    return [
        ("Direction", direction_text),
        ("Confidence", confidence_text),
        ("What to do", action_text),
    ]


def indicator_rows(result: AnalysisResult) -> list[tuple[str, str, str | None]]:
    """Return (label, value, tone) tuples for indicator metric cards."""
    ind = result.indicators
    rows: list[tuple[str, str, str | None]] = [
        ("RSI (14)", f"{ind.get('rsi', 0):.1f}", _rsi_tone(ind.get("rsi"))),
        ("MACD Histogram", f"{ind.get('macd_hist', 0):.2f}", _macd_tone(ind.get("macd_hist"))),
        ("EMA 9", f"${ind.get('ema_9', 0):,.2f}", None),
        ("EMA 21", f"${ind.get('ema_21', 0):,.2f}", None),
        ("EMA 50", f"${ind.get('ema_50', 0):,.2f}", None),
        ("EMA 200", f"${ind.get('ema_200', 0):,.2f}", None),
        ("Volume Ratio", f"{ind.get('volume_ratio', 0):.2f}x", None),
        ("Taker Buy %", f"{ind.get('taker_buy_ratio', 0):.1%}", None),
    ]
    if ind.get("funding_rate") is not None:
        rows.append(("Funding Rate", f"{ind['funding_rate']:.4%}", _funding_tone(ind["funding_rate"])))
    if ind.get("long_short_ratio") is not None:
        rows.append(("Long / Short Ratio", f"{ind['long_short_ratio']:.2f}", None))
    if ind.get("oi_change_pct") is not None:
        rows.append(("OI Change", f"{ind['oi_change_pct']:+.1f}%", None))
    return rows


def _rsi_tone(rsi: float | None) -> str | None:
    if rsi is None:
        return None
    if rsi >= 70:
        return "short"
    if rsi <= 30:
        return "long"
    return "wait"


def _macd_tone(hist: float | None) -> str | None:
    if hist is None:
        return None
    return "long" if hist > 0 else "short" if hist < 0 else "wait"


def _funding_tone(rate: float) -> str | None:
    if rate > 0.0005:
        return "short"
    if rate < -0.0002:
        return "long"
    return "wait"
