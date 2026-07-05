"""Risk management: levels, position sizing, take-profit targets."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.analysis.models import AnalysisResult, Recommendation
from src.ui.theme import confidence_percent


@dataclass
class TakeProfitLevels:
    tp1: float
    tp2: float
    tp3: float
    tp4: float


@dataclass
class RiskProfile:
    level: str
    probability: float
    invalidation: float
    position_size_btc: float
    position_size_usd: float
    risk_per_trade_usd: float


def _atr(df: pd.DataFrame, price: float) -> float:
    atr_proxy = (df["high"] - df["low"]).tail(14).mean()
    if pd.isna(atr_proxy) or atr_proxy <= 0:
        atr_proxy = price * 0.015
    return float(atr_proxy)


def compute_take_profits(
    price: float,
    recommendation: Recommendation,
    df: pd.DataFrame,
) -> TakeProfitLevels:
    atr = _atr(df, price)
    if recommendation == "short":
        return TakeProfitLevels(
            tp1=price - atr * 0.75,
            tp2=price - atr * 1.5,
            tp3=price - atr * 2.5,
            tp4=price - atr * 4.0,
        )
    if recommendation == "long":
        return TakeProfitLevels(
            tp1=price + atr * 0.75,
            tp2=price + atr * 1.5,
            tp3=price + atr * 2.5,
            tp4=price + atr * 4.0,
        )
    return TakeProfitLevels(
        tp1=price + atr * 0.5,
        tp2=price + atr * 1.0,
        tp3=price + atr * 1.5,
        tp4=price + atr * 2.0,
    )


def compute_invalidation(price: float, recommendation: Recommendation, stop_loss: float) -> float:
    if recommendation == "long":
        return min(stop_loss, price * 0.985)
    if recommendation == "short":
        return max(stop_loss, price * 1.015)
    return stop_loss


def compute_risk_profile(
    result: AnalysisResult,
    df: pd.DataFrame,
    *,
    account_size: float = 10_000.0,
    risk_pct: float = 1.0,
) -> RiskProfile:
    risk_per_unit = abs(result.price - result.stop_loss)
    risk_budget = account_size * (risk_pct / 100.0)
    position_btc = risk_budget / risk_per_unit if risk_per_unit > 0 else 0.0
    position_usd = position_btc * result.price

    conf_pct = confidence_percent(result.confidence)
    atr = _atr(df, result.price)
    volatility_pct = (atr / result.price) * 100 if result.price else 0.0

    probability = min(0.85, max(0.25, (conf_pct / 100.0) * 0.55 + (abs(result.score - 50) / 50.0) * 0.35))

    if conf_pct >= 70 and volatility_pct < 2.5:
        level = "LOW"
    elif conf_pct >= 50 and volatility_pct < 4.0:
        level = "MEDIUM"
    else:
        level = "HIGH"

    if result.recommendation == "wait":
        level = "HIGH"
        probability = min(probability, 0.35)

    invalidation = compute_invalidation(result.price, result.recommendation, result.stop_loss)

    return RiskProfile(
        level=level,
        probability=round(probability, 2),
        invalidation=invalidation,
        position_size_btc=round(position_btc, 6),
        position_size_usd=round(position_usd, 2),
        risk_per_trade_usd=round(risk_budget, 2),
    )
