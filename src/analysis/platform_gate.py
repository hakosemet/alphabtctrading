"""Minimal one-check-per-platform gate before trade setups are approved."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

Recommendation = Literal["long", "short", "wait"]

ALT_EXCHANGES = ("BingX", "Bybit", "OKX", "Bitget", "MEXC", "Coinbase", "Kraken")


@dataclass
class PlatformCheck:
    platform: str
    passed: bool
    detail: str


@dataclass
class PlatformGateResult:
    checks: list[PlatformCheck]
    passed: bool
    passed_count: int
    total: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "checks": [asdict(c) for c in self.checks],
            "passed": self.passed,
            "passed_count": self.passed_count,
            "total": self.total,
        }


def _status(info: dict | None) -> str:
    if not info:
        return "offline"
    return str(info.get("status", "offline"))


def _exchange_check(
    name: str,
    info: dict | None,
    *,
    snapshot: dict | None,
    reference_price: float,
) -> PlatformCheck:
    status = _status(info)
    if status not in ("online", "degraded"):
        return PlatformCheck(name, False, "Offline")

    snap = snapshot or {}
    price = snap.get("price")
    if price and reference_price > 0:
        spread_bps = abs(float(price) - reference_price) / reference_price * 10_000
        if spread_bps > 35:
            return PlatformCheck(name, False, f"Price diverges {spread_bps:.0f} bps")
        detail = f"Live ${float(price):,.0f}"
        funding = snap.get("funding_rate")
        if funding is not None:
            detail += f" · funding {float(funding) * 100:.3f}%"
        return PlatformCheck(name, True, detail)

    if status == "degraded":
        return PlatformCheck(name, True, "Degraded — usable")
    return PlatformCheck(name, True, "Connected")


def _cross_exchange_check(cross: dict | None, recommendation: Recommendation) -> PlatformCheck:
    cross = cross or {}
    online = int(cross.get("online_count") or 0)
    if online < 2:
        return PlatformCheck("Exchange Consensus", False, f"Only {online} alt feed(s)")

    if not cross.get("price_consensus_ok"):
        spread = cross.get("price_dispersion_bps")
        label = f"{spread:.0f} bps spread" if spread is not None else "Prices diverged"
        return PlatformCheck("Exchange Consensus", False, label)

    direction = cross.get("consensus_direction", "mixed")
    if recommendation == "wait":
        return PlatformCheck("Exchange Consensus", True, cross.get("summary", "Aligned"))
    if direction == "mixed":
        return PlatformCheck("Exchange Consensus", True, "Multi-exchange prices aligned")
    if direction == recommendation:
        return PlatformCheck("Exchange Consensus", True, f"{online} exchanges agree · {direction.upper()}")
    return PlatformCheck("Exchange Consensus", False, f"Funding/flow favors {direction.upper()}")


def _fear_greed_check(recommendation: Recommendation, data: dict | None) -> PlatformCheck:
    value = (data or {}).get("value")
    if value is None:
        return PlatformCheck("Fear & Greed", False, "No index data")
    if recommendation == "long" and value >= 88:
        return PlatformCheck("Fear & Greed", False, f"Extreme greed ({value})")
    if recommendation == "short" and value <= 12:
        return PlatformCheck("Fear & Greed", False, f"Extreme fear ({value})")
    return PlatformCheck("Fear & Greed", True, f"Index {value} — OK")


def _news_check(recommendation: Recommendation, data: dict | None) -> PlatformCheck:
    summary = (data or {}).get("summary") or {}
    score = summary.get("score")
    if score is None:
        status = (data or {}).get("status", "offline")
        if status in ("online", "degraded"):
            return PlatformCheck("News & Sentiment", True, "Feed online")
        return PlatformCheck("News & Sentiment", False, "No sentiment score")
    if recommendation == "long" and score < 30:
        return PlatformCheck("News & Sentiment", False, f"Bearish news ({score}/100)")
    if recommendation == "short" and score > 70:
        return PlatformCheck("News & Sentiment", False, f"Bullish news ({score}/100)")
    return PlatformCheck("News & Sentiment", True, f"Sentiment {score}/100 — OK")


def _onchain_check(data: dict | None, info: dict | None) -> PlatformCheck:
    status = _status(info)
    if status == "online":
        return PlatformCheck("On-Chain", True, "Data available")
    if status == "placeholder":
        return PlatformCheck("On-Chain", True, "Placeholder — not blocking")
    if data:
        return PlatformCheck("On-Chain", True, "Partial data")
    return PlatformCheck("On-Chain", False, "Unavailable")


def _whale_check(data: dict | None, info: dict | None) -> PlatformCheck:
    status = _status(info if info else data)
    if status in ("online", "degraded", "placeholder"):
        label = "Active" if status == "online" else status
        return PlatformCheck("Whale Alerts", True, label)
    return PlatformCheck("Whale Alerts", False, "Offline")


def run_platform_gate(
    *,
    recommendation: Recommendation,
    price: float,
    hub: dict | None,
    fear_greed: dict | None,
    news_sentiment: dict | None,
    onchain_data: dict | None,
    whale_data: dict | None,
    coinglass_enabled: bool,
) -> PlatformGateResult:
    """Run exactly one check per Bitcoin data platform."""
    hub = hub or {}
    sources = hub.get("source_status") or {}
    exchange_snapshots = hub.get("exchange_snapshots") or {}
    cross = hub.get("cross_exchange") or {}

    checks: list[PlatformCheck] = []

    binance = sources.get("Binance") or {}
    if _status(binance) == "online" and price > 0:
        checks.append(PlatformCheck("Binance", True, "Live BTC price"))
    else:
        checks.append(PlatformCheck("Binance", False, "Primary feed down"))

    coinglass = sources.get("Coinglass") or {}
    if not coinglass_enabled:
        checks.append(PlatformCheck("Coinglass", True, "Skipped — no API key"))
    elif _status(coinglass) in ("online", "degraded"):
        checks.append(PlatformCheck("Coinglass", True, "Derivatives data OK"))
    else:
        checks.append(PlatformCheck("Coinglass", False, "Derivatives offline"))

    for name in ALT_EXCHANGES:
        checks.append(
            _exchange_check(
                name,
                sources.get(name),
                snapshot=exchange_snapshots.get(name),
                reference_price=price,
            )
        )

    checks.append(_cross_exchange_check(cross, recommendation))
    checks.append(_fear_greed_check(recommendation, fear_greed))
    checks.append(_news_check(recommendation, news_sentiment))
    checks.append(_onchain_check(onchain_data, sources.get("On-Chain")))
    checks.append(_whale_check(whale_data, sources.get("Whale data")))

    if recommendation == "wait":
        passed = False
    elif hub.get("critical_missing"):
        passed = False
    else:
        critical = {"Binance", "Exchange Consensus", "Fear & Greed", "News & Sentiment"}
        passed = all(c.passed for c in checks if c.platform in critical)

    passed_count = sum(1 for c in checks if c.passed)
    return PlatformGateResult(
        checks=checks,
        passed=passed,
        passed_count=passed_count,
        total=len(checks),
    )
