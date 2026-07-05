"""Cross-exchange price and funding consensus for trade quality."""

from __future__ import annotations

from statistics import median
from typing import Any


def build_cross_exchange_summary(
    exchange_snapshots: dict[str, dict[str, Any]],
    *,
    reference_price: float,
) -> dict[str, Any]:
    """Aggregate live exchange feeds into a trade-quality consensus."""
    online: list[str] = []
    prices: list[float] = []
    fundings: list[float] = []

    for name, snap in exchange_snapshots.items():
        price = snap.get("price")
        if price is None or float(price) <= 0:
            continue
        online.append(name)
        prices.append(float(price))
        funding = snap.get("funding_rate")
        if funding is not None:
            fundings.append(float(funding))

    if not prices:
        return {
            "online_exchanges": [],
            "online_count": 0,
            "price_consensus_ok": False,
            "price_dispersion_bps": None,
            "median_price": reference_price,
            "avg_funding_rate": None,
            "funding_bias": "unknown",
            "consensus_direction": "mixed",
            "trade_quality_boost": 0,
            "summary": "No alt-exchange prices online",
        }

    med = float(median(prices))
    ref = reference_price if reference_price > 0 else med
    dispersion_bps = max(abs(p - med) / med * 10_000 for p in prices) if med > 0 else 0.0
    price_consensus_ok = dispersion_bps <= 25.0 and len(online) >= 2

    avg_funding = sum(fundings) / len(fundings) if fundings else None
    funding_bias = "neutral"
    if avg_funding is not None:
        if avg_funding >= 0.00008:
            funding_bias = "long_crowded"
        elif avg_funding <= -0.00008:
            funding_bias = "short_crowded"

    positive = sum(1 for f in fundings if f > 0)
    negative = sum(1 for f in fundings if f < 0)
    if fundings and positive >= len(fundings) * 0.65:
        consensus_direction = "short"
    elif fundings and negative >= len(fundings) * 0.65:
        consensus_direction = "long"
    elif ref > 0 and med >= ref * 1.0002:
        consensus_direction = "long"
    elif ref > 0 and med <= ref * 0.9998:
        consensus_direction = "short"
    else:
        consensus_direction = "mixed"

    boost = 0
    if price_consensus_ok:
        boost += 8
    if len(online) >= 4:
        boost += 6
    if len(fundings) >= 3:
        boost += 4

    summary = (
        f"{len(online)} exchanges live | spread {dispersion_bps:.1f} bps | "
        f"funding {funding_bias.replace('_', ' ')}"
    )

    return {
        "online_exchanges": online,
        "online_count": len(online),
        "price_consensus_ok": price_consensus_ok,
        "price_dispersion_bps": round(dispersion_bps, 2),
        "median_price": round(med, 2),
        "avg_funding_rate": round(avg_funding, 6) if avg_funding is not None else None,
        "funding_bias": funding_bias,
        "consensus_direction": consensus_direction,
        "trade_quality_boost": boost,
        "summary": summary,
    }
