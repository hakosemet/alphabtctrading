"""Simple keyword-based headline sentiment analysis."""

from __future__ import annotations

from typing import Any

POSITIVE_WORDS = frozenset(
    {
        "bullish",
        "etf",
        "inflow",
        "rally",
        "breakout",
        "adoption",
        "institutional",
        "surge",
        "record",
        "approval",
        "accumulation",
    }
)

NEGATIVE_WORDS = frozenset(
    {
        "bearish",
        "hack",
        "lawsuit",
        "outflow",
        "crash",
        "liquidation",
        "ban",
        "selloff",
        "fraud",
        "exploit",
        "collapse",
        "dump",
    }
)


def analyze_headline_sentiment(text: str) -> str:
    """Return positive, negative, or neutral for a headline."""
    tokens = {word.strip(".,!?\"'()[]") for word in text.lower().split()}
    pos = len(tokens & POSITIVE_WORDS)
    neg = len(tokens & NEGATIVE_WORDS)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


def summarize_sentiment(headlines: list[dict[str, Any]]) -> dict[str, Any]:
    if not headlines:
        return {
            "label": "neutral",
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "score": 50,
        }

    counts = {"positive": 0, "negative": 0, "neutral": 0}
    for item in headlines:
        label = str(item.get("sentiment", "neutral"))
        counts[label] = counts.get(label, 0) + 1

    total = max(len(headlines), 1)
    score = 50 + int(((counts["positive"] - counts["negative"]) / total) * 50)
    score = max(0, min(100, score))

    if counts["positive"] > counts["negative"]:
        label = "bullish"
    elif counts["negative"] > counts["positive"]:
        label = "bearish"
    else:
        label = "neutral"

    return {
        "label": label,
        "positive": counts["positive"],
        "negative": counts["negative"],
        "neutral": counts["neutral"],
        "score": score,
    }
