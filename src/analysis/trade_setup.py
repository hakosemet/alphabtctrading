"""Trade setup — safe directional levels after trader & market review."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

import pandas as pd

from src.analysis.models import AnalysisResult, Recommendation
from src.analysis.platform_gate import PlatformGateResult, run_platform_gate
from src.ui.theme import confidence_percent

MIN_RR = 1.5

TRADE_CONFIG: dict[str, Any] = {
    "stop_atr": 1.0,
    "stop_cap_atr": 2.0,
    "r_multiples": (1.5, 2.5, 4.0, 6.0),
    "atr_tp_steps": (0.8, 1.4, 2.2, 3.5),
    "risk_pct": 0.75,
    "risk_pct_conservative": 0.5,
    "min_conf": 62,
}

TradeDirection = Literal["long", "short", "none"]


@dataclass
class TradeSetupPlan:
    entry: float
    stop_loss: float
    take_profit: float
    tp1: float
    tp2: float
    tp3: float
    tp4: float
    risk_reward: float
    atr: float
    atr_pct: float
    swing_support: float
    swing_resistance: float
    risk_per_unit: float
    reward_per_unit: float
    setup_allowed: bool
    setup_grade: str
    setup_message: str
    data_notes: list[str]
    direction: TradeDirection = "none"
    signal: str = "wait"
    variant_name: str = "Standard"
    risk_pct: float = 0.75


def _true_atr(df: pd.DataFrame, period: int = 14) -> float:
    if df is None or df.empty or len(df) < 2:
        return 0.0

    high = df["high"]
    low = df["low"]
    close = df["close"]
    prev_close = close.shift(1)
    tr = pd.concat(
        [(high - low), (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    atr = tr.tail(period).mean()
    if pd.isna(atr) or atr <= 0:
        return float((high - low).tail(period).mean() or 0)
    return float(atr)


def _swing_levels(df: pd.DataFrame, lookback: int = 60) -> tuple[float, float]:
    window = df.tail(lookback)
    return float(window["low"].min()), float(window["high"].max())


def _heatmap_levels(
    heatmap: pd.DataFrame | None,
    price: float,
) -> tuple[float | None, float | None]:
    if heatmap is None or heatmap.empty:
        return None, None

    below = heatmap[heatmap["price_level"] < price]
    above = heatmap[heatmap["price_level"] > price]
    support = None
    resistance = None
    if not below.empty:
        support = float(below.loc[below["intensity"].idxmax(), "price_level"])
    if not above.empty:
        resistance = float(above.loc[above["intensity"].idxmax(), "price_level"])
    return support, resistance


def _order_book_levels(order_book: dict | None, price: float) -> tuple[float | None, float | None]:
    if not order_book:
        return None, None
    bids = order_book.get("bids") or []
    asks = order_book.get("asks") or []
    bid_prices = [float(b[0]) for b in bids[:10] if len(b) >= 2]
    ask_prices = [float(a[0]) for a in asks[:10] if len(a) >= 2]
    support = max(bid_prices) if bid_prices else None
    resistance = min(ask_prices) if ask_prices else None
    if support and support >= price:
        support = None
    if resistance and resistance <= price:
        resistance = None
    return support, resistance


def _pick_support(*levels: float | None, price: float, fallback_atr: float) -> float:
    valid = [lvl for lvl in levels if lvl is not None and lvl < price]
    if valid:
        return max(valid)
    return price - fallback_atr * 0.75


def _pick_resistance(*levels: float | None, price: float, fallback_atr: float) -> float:
    valid = [lvl for lvl in levels if lvl is not None and lvl > price]
    if valid:
        return min(valid)
    return price + fallback_atr * 0.75


def _trader_consensus_direction(result: AnalysisResult) -> tuple[Recommendation, list[str], int, int]:
    """Weight score, components, checklist, fear/greed and news like a trader desk."""
    notes: list[str] = []
    if result.recommendation in ("long", "short"):
        notes.append(f"Market signal: {result.recommendation.upper()}")
        return result.recommendation, notes, 1, 0

    long_votes = 0
    short_votes = 0

    if result.score >= 52:
        long_votes += 2
    elif result.score <= 48:
        short_votes += 2
    else:
        long_votes += 1 if result.score >= 50 else 0
        short_votes += 1 if result.score < 50 else 0

    for component in result.components:
        if component.score >= 58:
            long_votes += 1
        elif component.score <= 42:
            short_votes += 1

    enters = [r for r in (result.reasons_enter or []) if "No strong" not in r]
    avoids = [r for r in (result.reasons_avoid or []) if "No major" not in r]

    for reason in enters:
        lower = reason.lower()
        if any(k in lower for k in ("bullish", "long", "support", "healthy")):
            long_votes += 1
        if any(k in lower for k in ("bearish", "short", "resistance")):
            short_votes += 1

    for reason in avoids:
        lower = reason.lower()
        if any(k in lower for k in ("overbought", "resistance", "high funding")):
            short_votes += 1
        if any(k in lower for k in ("oversold", "weak volume")):
            long_votes += 1

    fear = (result.fear_greed or {}).get("value")
    if fear is not None:
        if fear >= 55:
            long_votes += 1
        elif fear <= 45:
            short_votes += 1

    news_score = ((result.news_sentiment or {}).get("summary") or {}).get("score")
    if news_score is not None:
        if news_score >= 55:
            long_votes += 1
        elif news_score <= 45:
            short_votes += 1

    cross = (result.hub or {}).get("cross_exchange") or {}
    if cross.get("price_consensus_ok"):
        notes.append(cross.get("summary", "Multi-exchange price consensus OK"))
        direction_hint = cross.get("consensus_direction")
        if direction_hint == "long":
            long_votes += 2
        elif direction_hint == "short":
            short_votes += 2
        boost = int(cross.get("trade_quality_boost") or 0)
        if boost >= 10:
            if direction_hint == "long":
                long_votes += 1
            elif direction_hint == "short":
                short_votes += 1
    elif int(cross.get("online_count") or 0) >= 2:
        notes.append("Exchange prices diverged — lower conviction")

    direction: Recommendation = "long" if long_votes >= short_votes else "short"
    notes.append(f"Trader consensus: {direction.upper()} ({long_votes} bull · {short_votes} bear)")
    notes.append(f"Checklist: {len(enters)} enter · {len(avoids)} avoid")
    return direction, notes, long_votes, short_votes


def _market_review_passes(
    result: AnalysisResult,
    *,
    long_votes: int,
    short_votes: int,
) -> tuple[bool, list[str]]:
    notes: list[str] = []
    conf = confidence_percent(result.confidence)
    enter = [r for r in (result.reasons_enter or []) if "No strong" not in r]
    avoid = [r for r in (result.reasons_avoid or []) if "No major" not in r]

    if result.recommendation in ("long", "short") and conf >= TRADE_CONFIG["min_conf"]:
        if len(enter) > len(avoid):
            notes.append("Strong signal — confirmations lead warnings")
            return True, notes

    if result.recommendation == "wait":
        margin = abs(long_votes - short_votes)
        if margin >= 2 and len(enter) >= len(avoid):
            notes.append("WAIT market — safe lean after trader weighting")
            return True, notes
        if margin >= 1 and conf >= 50:
            notes.append("WAIT market — cautious lean, reduced size")
            return True, notes
        notes.append("Mixed desk view — conservative plan only")
        return False, notes

    if conf < TRADE_CONFIG["min_conf"]:
        notes.append(f"Low confidence ({conf}%) — conservative sizing")
        return False, notes

    if len(avoid) >= len(enter):
        notes.append("Warnings match confirmations")
        return False, notes

    return True, notes


def _build_targets(
    price: float,
    stop: float,
    direction: Recommendation,
    atr: float,
    structure_level: float,
) -> tuple[float, float, float, float]:
    r_multiples = TRADE_CONFIG["r_multiples"]
    atr_steps = TRADE_CONFIG["atr_tp_steps"]
    risk = abs(price - stop)
    if risk <= 0:
        risk = max(atr * 0.5, price * 0.002)
    min_step = max(atr * 0.3, price * 0.0006)

    if direction == "long":
        tps = [price + max(risk * r_multiples[i], atr * atr_steps[i]) for i in range(4)]
        for i in range(1, 4):
            tps[i] = max(tps[i], tps[i - 1] + min_step)
        if structure_level > price:
            tps[3] = max(tps[3], structure_level)
        for i in range(4):
            tps[i] = max(tps[i], price + min_step * (i + 1))
    else:
        tps = [price - max(risk * r_multiples[i], atr * atr_steps[i]) for i in range(4)]
        for i in range(1, 4):
            tps[i] = min(tps[i], tps[i - 1] - min_step)
        if structure_level < price:
            tps[3] = min(tps[3], structure_level)
        for i in range(4):
            tps[i] = min(tps[i], price - min_step * (i + 1))

    return tps[0], tps[1], tps[2], tps[3]


def _build_directional_setup(
    result: AnalysisResult,
    df: pd.DataFrame,
    *,
    direction: Recommendation,
    heatmap: pd.DataFrame | None,
    order_book: dict | None,
    review_notes: list[str],
    review_ok: bool,
    conservative: bool,
) -> TradeSetupPlan:
    price = float(result.price)
    atr = _true_atr(df)
    if atr <= 0:
        atr = price * 0.0015

    swing_low, swing_high = _swing_levels(df)
    hm_support, hm_resistance = _heatmap_levels(heatmap, price)
    ob_support, ob_resistance = _order_book_levels(order_book, price)

    stop_atr = float(TRADE_CONFIG["stop_atr"]) * (1.15 if conservative else 1.0)
    stop_cap = float(TRADE_CONFIG["stop_cap_atr"]) * (1.15 if conservative else 1.0)
    risk_pct = float(
        TRADE_CONFIG["risk_pct_conservative"] if conservative else TRADE_CONFIG["risk_pct"]
    )

    if direction == "long":
        support = _pick_support(swing_low, hm_support, ob_support, price=price, fallback_atr=atr)
        stop = min(support, price - atr * stop_atr)
        stop = max(stop, price - atr * stop_cap)
        min_step = max(atr * 0.3, price * 0.0006)
        stop = min(stop, price - min_step)
        resistance = _pick_resistance(swing_high, hm_resistance, ob_resistance, price=price, fallback_atr=atr)
        tp1, tp2, tp3, tp4 = _build_targets(price, stop, "long", atr, resistance)
        take_profit = tp3
    else:
        resistance = _pick_resistance(swing_high, hm_resistance, ob_resistance, price=price, fallback_atr=atr)
        stop = max(resistance, price + atr * stop_atr)
        stop = min(stop, price + atr * stop_cap)
        min_step = max(atr * 0.3, price * 0.0006)
        stop = max(stop, price + min_step)
        support = _pick_support(swing_low, hm_support, ob_support, price=price, fallback_atr=atr)
        tp1, tp2, tp3, tp4 = _build_targets(price, stop, "short", atr, support)
        take_profit = tp3

    risk = abs(price - stop)
    reward = abs(take_profit - price)
    rr = reward / risk if risk > 0 else 0.0

    conf = confidence_percent(result.confidence)
    if review_ok and rr >= 2.5 and conf >= 70:
        grade, allowed = "A", True
    elif review_ok and rr >= MIN_RR:
        grade, allowed = "B", True
    elif rr >= MIN_RR:
        grade, allowed = "C", conservative
    else:
        grade, allowed = "CAUTION", False

    notes = [
        f"Trade direction: {direction.upper()}",
        f"Signal: {result.recommendation.upper()}",
        f"ATR(14): ${atr:,.2f} ({atr / price * 100:.2f}%)",
        f"Swing ${swing_low:,.2f} – ${swing_high:,.2f}",
        *review_notes,
    ]

    return TradeSetupPlan(
        entry=round(price, 2),
        stop_loss=round(stop, 2),
        take_profit=round(take_profit, 2),
        tp1=round(tp1, 2),
        tp2=round(tp2, 2),
        tp3=round(tp3, 2),
        tp4=round(tp4, 2),
        risk_reward=round(rr, 2),
        atr=round(atr, 2),
        atr_pct=round(atr / price * 100, 3),
        swing_support=round(swing_low, 2),
        swing_resistance=round(swing_high, 2),
        risk_per_unit=round(risk, 2),
        reward_per_unit=round(reward, 2),
        setup_allowed=allowed,
        setup_grade=grade,
        setup_message="",
        data_notes=notes,
        direction=direction,
        signal=result.recommendation,
        risk_pct=risk_pct,
    )


def build_trade_setup(
    result: AnalysisResult,
    df: pd.DataFrame,
    *,
    heatmap: pd.DataFrame | None = None,
    order_book: dict | None = None,
    coinglass_enabled: bool = False,
) -> tuple[TradeSetupPlan, PlatformGateResult]:
    gate = run_platform_gate(
        recommendation=result.recommendation,
        price=float(result.price),
        hub=result.hub,
        fear_greed=result.fear_greed,
        news_sentiment=result.news_sentiment,
        onchain_data=result.onchain_data,
        whale_data=result.whale_data,
        coinglass_enabled=coinglass_enabled,
    )

    direction, consensus_notes, long_votes, short_votes = _trader_consensus_direction(result)
    review_ok, review_notes = _market_review_passes(
        result, long_votes=long_votes, short_votes=short_votes,
    )
    conservative = result.recommendation == "wait" or not review_ok

    plan = _build_directional_setup(
        result,
        df,
        direction=direction,
        heatmap=heatmap,
        order_book=order_book,
        review_notes=consensus_notes + review_notes,
        review_ok=review_ok,
        conservative=conservative,
    )
    return plan, gate


def apply_trade_setup_to_result(
    result: AnalysisResult,
    plan: TradeSetupPlan,
    *,
    gate: PlatformGateResult | None = None,
) -> None:
    if plan.direction in ("long", "short"):
        result.stop_loss = plan.stop_loss
        result.take_profit = plan.take_profit
        result.risk_reward = plan.risk_reward
        result.take_profits = {
            "tp1": plan.tp1,
            "tp2": plan.tp2,
            "tp3": plan.tp3,
            "tp4": plan.tp4,
        }
    result.trade_setup = asdict(plan)
    result.trade_setups = []
    if gate is not None:
        result.platform_checks = gate.to_dict()
