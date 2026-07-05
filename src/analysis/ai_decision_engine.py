"""AI decision engine — enriches MarketAnalyzer output with dashboard insights."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

import pandas as pd

from src.analysis.models import AnalysisResult, DashboardInsights, MarketStatusPanel, TradeQuality
from src.analysis.risk_manager import (
    TakeProfitLevels,
    compute_risk_profile,
    compute_take_profits,
)
from src.data.fear_greed import FearGreedClient
from src.data.news_client import NewsClient
from src.data.onchain_client import OnChainClient
from src.data.whale_client import WhaleClient
from src.ui.theme import BRAND, confidence_percent


def enrich_analysis(
    result: AnalysisResult,
    *,
    candles: pd.DataFrame,
    heatmap: pd.DataFrame | None = None,
    account_size: float = 10_000.0,
    risk_pct: float = 1.0,
    coinglass_enabled: bool = False,
) -> AnalysisResult:
    """Attach dashboard insights without changing core recommendation logic."""
    try:
        fear_data, fear_info = FearGreedClient().fetch()
        news_data, news_info = NewsClient().fetch()
        onchain_data, onchain_info = OnChainClient().fetch()
        whale_data, whale_info = WhaleClient().fetch()
    except Exception as exc:
        result.enhanced_explanation = result.explanation
        result.insights = None
        return result

    market_status = _market_status(result, candles)
    trade_quality = _trade_quality(result)
    take_profits = compute_take_profits(result.price, result.recommendation, candles)
    risk_profile = compute_risk_profile(
        result,
        candles,
        account_size=account_size,
        risk_pct=risk_pct,
    )
    reasons_enter, reasons_avoid = _entry_reasons(result, candles, heatmap)

    source_status = _build_source_status(
        result,
        fear_info=fear_info,
        news_info=news_info,
        onchain_info=onchain_info,
        whale_info=whale_info,
        coinglass_enabled=coinglass_enabled,
    )

    enhanced = _build_enhanced_explanation(
        result=result,
        market_status=market_status,
        trade_quality=trade_quality,
        take_profits=take_profits,
        risk_profile=risk_profile,
        reasons_enter=reasons_enter,
        reasons_avoid=reasons_avoid,
        fear_data=fear_data,
        news_data=news_data,
    )

    result.take_profits = asdict(take_profits)
    result.risk_profile = asdict(risk_profile)
    result.reasons_enter = reasons_enter
    result.reasons_avoid = reasons_avoid
    result.fear_greed = fear_data
    result.news_sentiment = news_data
    result.onchain_data = onchain_data
    result.whale_data = whale_data
    result.source_status = source_status
    result.enhanced_explanation = enhanced
    result.insights = DashboardInsights(
        market_status=market_status,
        trade_quality=trade_quality,
        fear_greed=fear_data,
        news_sentiment=news_data,
        onchain_data=onchain_data,
        whale_data=whale_data,
        source_status=source_status,
    )

    try:
        from src.analysis.trade_setup import apply_trade_setup_to_result, build_trade_setup

        order_book = (result.hub or {}).get("order_book")
        plan, gate = build_trade_setup(
            result,
            candles,
            heatmap=heatmap,
            order_book=order_book,
            coinglass_enabled=coinglass_enabled,
        )
        apply_trade_setup_to_result(result, plan, gate=gate)
    except Exception:
        pass

    return result


def _market_status(result: AnalysisResult, df: pd.DataFrame) -> MarketStatusPanel:
    atr = (df["high"] - df["low"]).tail(14).mean()
    vol_pct = (atr / result.price) * 100 if result.price else 0.0
    volume_ratio = float(result.indicators.get("volume_ratio") or 1.0)

    if result.score >= 58:
        trend = "Bullish"
    elif result.score <= 42:
        trend = "Bearish"
    else:
        trend = "Sideways"

    volatility = "High volatility" if vol_pct >= 2.5 else "Normal volatility"
    liquidity = "Low liquidity" if volume_ratio < 0.8 else "Normal liquidity"

    return MarketStatusPanel(
        trend=trend,
        volatility=volatility,
        liquidity=liquidity,
    )


def _trade_quality(result: AnalysisResult) -> TradeQuality:
    conf_pct = confidence_percent(result.confidence)
    composite = (result.score * 0.45) + (conf_pct * 0.55)

    if result.recommendation == "wait" or conf_pct < 40:
        grade = "No Trade"
        stars = 0
    elif composite >= 82:
        grade = "A+"
        stars = 5
    elif composite >= 72:
        grade = "A"
        stars = 4
    elif composite >= 60:
        grade = "B"
        stars = 3
    else:
        grade = "C"
        stars = 2

    return TradeQuality(
        grade=grade,
        score=int(round(composite)),
        stars=stars,
    )


def _entry_reasons(
    result: AnalysisResult,
    df: pd.DataFrame,
    heatmap: pd.DataFrame | None,
) -> tuple[list[str], list[str]]:
    ind = result.indicators
    latest = df.iloc[-1]
    enter: list[str] = []
    avoid: list[str] = []

    ema9 = latest.get("ema_9")
    ema21 = latest.get("ema_21")
    ema50 = latest.get("ema_50")
    ema200 = latest.get("ema_200")
    if pd.notna(ema9) and pd.notna(ema21) and pd.notna(ema50) and pd.notna(ema200):
        if ema9 > ema21 > ema50 > ema200:
            enter.append("EMA alignment — bullish stack")
        elif ema9 < ema21 < ema50 < ema200:
            enter.append("EMA alignment — bearish stack")
        else:
            avoid.append("Mixed EMA alignment")

    rsi = ind.get("rsi")
    if rsi is not None:
        if 45 <= rsi <= 65:
            enter.append(f"RSI condition healthy ({rsi:.1f})")
        elif rsi >= 75:
            avoid.append(f"RSI overbought ({rsi:.1f})")
        elif rsi <= 25:
            avoid.append(f"RSI oversold ({rsi:.1f}) — reversal risk")

    macd_hist = ind.get("macd_hist")
    if macd_hist is not None:
        if macd_hist > 0:
            enter.append("MACD direction — bullish momentum")
        elif macd_hist < 0:
            enter.append("MACD direction — bearish momentum")

    volume_ratio = ind.get("volume_ratio") or 0
    if volume_ratio >= 1.1:
        enter.append(f"Volume confirmation ({volume_ratio:.2f}x average)")
    elif volume_ratio < 0.8:
        avoid.append(f"Weak volume ({volume_ratio:.2f}x average)")

    funding = ind.get("funding_rate")
    if funding is not None:
        if abs(funding) <= 0.0003:
            enter.append("Funding neutral")
        elif abs(funding) >= 0.0008:
            avoid.append(f"High funding ({funding:.4%})")

    cross = (result.hub or {}).get("cross_exchange") or {}
    online = int(cross.get("online_count") or 0)
    if online >= 3 and cross.get("price_consensus_ok"):
        enter.append(f"{online} exchanges aligned on BTC price")
    elif online >= 2 and not cross.get("price_consensus_ok"):
        avoid.append("Exchange price spread too wide")
    bias = cross.get("funding_bias")
    if bias == "long_crowded":
        avoid.append("Funding crowded long across exchanges")
    elif bias == "short_crowded":
        avoid.append("Funding crowded short across exchanges")
    elif bias == "neutral" and online >= 2:
        enter.append("Cross-exchange funding balanced")

    ls_ratio = ind.get("long_short_ratio")
    if ls_ratio is not None:
        enter.append(f"Long/Short ratio at {ls_ratio:.2f}")

    if heatmap is not None and not heatmap.empty:
        below = heatmap[heatmap["price_level"] < result.price]
        above = heatmap[heatmap["price_level"] > result.price]
        if not below.empty:
            enter.append("Heatmap support nearby")
        if not above.empty:
            support_res = "Heatmap resistance nearby"
            if result.recommendation == "long":
                avoid.append(support_res)
            else:
                enter.append(support_res)

    spread = max(c.score for c in result.components) - min(c.score for c in result.components) if result.components else 0
    if spread <= 25:
        enter.append("Trend strength — indicators aligned")
    else:
        avoid.append("Mixed indicators — low alignment")

    conf_pct = confidence_percent(result.confidence)
    if conf_pct < 70:
        avoid.append(f"Low confidence ({conf_pct}%)")

    atr = (df["high"] - df["low"]).tail(14).mean()
    if result.price and (atr / result.price) * 100 >= 3.0:
        avoid.append("Too much volatility for aggressive entries")

    if not enter:
        enter.append("No strong entry confirmations detected")
    if not avoid:
        avoid.append("No major warning flags detected")

    return enter, avoid


def _build_source_status(
    result: AnalysisResult,
    *,
    fear_info,
    news_info,
    onchain_info,
    whale_info,
    coinglass_enabled: bool,
) -> dict[str, Any]:
    hub_sources = (result.hub or {}).get("source_status") or {}
    binance_status = "online" if "Binance" in (result.data_sources or []) else hub_sources.get("Binance", {}).get("status", "offline")

    return {
        "Binance": binance_status,
        "Coinglass": "online" if coinglass_enabled else hub_sources.get("Coinglass", {}).get("status", "offline"),
        "Fear & Greed": fear_info.status,
        "News RSS": news_info.status,
        "On-chain": onchain_info.status,
        "Whale data": whale_info.status,
    }


def _build_enhanced_explanation(
    *,
    result: AnalysisResult,
    market_status: MarketStatusPanel,
    trade_quality: TradeQuality,
    take_profits: TakeProfitLevels,
    risk_profile,
    reasons_enter: list[str],
    reasons_avoid: list[str],
    fear_data: dict,
    news_data: dict,
) -> str:
    conf_pct = confidence_percent(result.confidence)
    lines = [
        f"=== {BRAND['product']} — Analysis Report ===",
        "",
        f"Recommendation: {result.recommendation.upper()}",
        f"Why: Composite score {result.score:.1f}/100 with {result.confidence} confidence ({conf_pct}%).",
        "",
        "What confirms the setup:",
    ]
    lines.extend([f"  ✓ {item}" for item in reasons_enter[:8]])
    lines.extend(["", "What can cancel the setup:"])
    lines.extend([f"  ✗ {item}" for item in reasons_avoid[:8]])
    lines.extend(
        [
            "",
            f"Suggested stop loss: ${result.stop_loss:,.2f}",
            f"Invalidation level: ${risk_profile.invalidation:,.2f}",
            f"TP targets: TP1 ${take_profits.tp1:,.2f} | TP2 ${take_profits.tp2:,.2f} | "
            f"TP3 ${take_profits.tp3:,.2f} | TP4 ${take_profits.tp4:,.2f}",
            "",
            f"Risk level: {risk_profile.level} | Estimated probability: {risk_profile.probability:.0%}",
            f"Position size (1% risk): {risk_profile.position_size_btc:.6f} BTC "
            f"(${risk_profile.position_size_usd:,.2f})",
            "",
            f"Market status: {market_status.trend} | {market_status.volatility} | {market_status.liquidity}",
            f"Trade quality: {trade_quality.grade} ({trade_quality.score}/100)",
            "",
        ]
    )

    if fear_data.get("value") is not None:
        lines.append(
            f"Fear & Greed Index: {fear_data['value']} ({fear_data.get('classification', 'N/A')})"
        )
    news_summary = news_data.get("summary") or {}
    if news_summary:
        lines.append(
            f"News sentiment: {news_summary.get('label', 'neutral')} "
            f"(score {news_summary.get('score', 50)}/100)"
        )

    lines.extend(
        [
            "",
            "Disclaimer: Educational tool only. Not financial advice. "
            "Past performance does not guarantee future results.",
        ]
    )
    return "\n".join(lines)
