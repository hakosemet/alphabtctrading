"""Composite scoring engine for Bitcoin market analysis."""

from __future__ import annotations

import pandas as pd

from src.analysis.models import AnalysisResult, ComponentScore, Recommendation
from src.data.data_hub import BitcoinDataHub
from src.data.hub_models import HubSnapshot
from src.indicators.technical import (
    build_volume_heatmap,
    compute_emas,
    compute_macd,
    compute_rsi,
    compute_volume_metrics,
    parse_coinglass_heatmap,
    summarize_volume,
)


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def _score_ema_trend(df: pd.DataFrame) -> ComponentScore:
    latest = df.iloc[-1]
    price = latest["close"]
    ema9 = latest.get("ema_9")
    ema21 = latest.get("ema_21")
    ema50 = latest.get("ema_50")
    ema200 = latest.get("ema_200")

    score = 50.0
    details: list[str] = []

    if pd.notna(ema9) and pd.notna(ema21):
        if ema9 > ema21:
            score += 12
            details.append("EMA9 above EMA21 (short-term bullish)")
        else:
            score -= 12
            details.append("EMA9 below EMA21 (short-term bearish)")

    if pd.notna(ema50) and pd.notna(ema200):
        if ema50 > ema200:
            score += 18
            details.append("EMA50 above EMA200 (primary uptrend)")
        else:
            score -= 18
            details.append("EMA50 below EMA200 (primary downtrend)")

    if pd.notna(ema21):
        if price > ema21:
            score += 8
            details.append("Price trading above EMA21")
        else:
            score -= 8
            details.append("Price trading below EMA21")

    return ComponentScore(
        name="EMA Trend",
        score=_clamp(score),
        weight=0.25,
        detail="; ".join(details),
    )


def _score_macd(df: pd.DataFrame) -> ComponentScore:
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    macd = latest.get("macd")
    signal = latest.get("macd_signal")
    hist = latest.get("macd_hist")
    prev_hist = prev.get("macd_hist")

    score = 50.0
    details: list[str] = []

    if pd.notna(macd) and pd.notna(signal):
        if macd > signal:
            score += 15
            details.append("MACD line above signal line")
        else:
            score -= 15
            details.append("MACD line below signal line")

    if pd.notna(hist):
        if hist > 0:
            score += 10
            details.append("Positive MACD histogram")
        else:
            score -= 10
            details.append("Negative MACD histogram")

    if pd.notna(hist) and pd.notna(prev_hist):
        if hist > prev_hist:
            score += 8
            details.append("MACD momentum improving")
        else:
            score -= 8
            details.append("MACD momentum weakening")

    return ComponentScore(
        name="MACD",
        score=_clamp(score),
        weight=0.20,
        detail="; ".join(details),
    )


def _score_rsi(df: pd.DataFrame) -> ComponentScore:
    rsi = df.iloc[-1].get("rsi")
    score = 50.0
    details: list[str] = []

    if pd.isna(rsi):
        return ComponentScore(name="RSI", score=50.0, weight=0.15, detail="RSI unavailable")

    if rsi >= 70:
        score = 25
        details.append(f"RSI overbought at {rsi:.1f}")
    elif rsi <= 30:
        score = 75
        details.append(f"RSI oversold at {rsi:.1f}")
    elif rsi >= 55:
        score = 65
        details.append(f"RSI bullish zone at {rsi:.1f}")
    elif rsi <= 45:
        score = 35
        details.append(f"RSI bearish zone at {rsi:.1f}")
    else:
        score = 50
        details.append(f"RSI neutral at {rsi:.1f}")

    return ComponentScore(
        name="RSI",
        score=_clamp(score),
        weight=0.15,
        detail="; ".join(details),
    )


def _score_volume(df: pd.DataFrame) -> ComponentScore:
    latest = df.iloc[-1]
    vol_ratio = latest.get("volume_ratio")
    taker_buy = latest.get("taker_buy_ratio")
    score = 50.0
    details: list[str] = []

    if pd.notna(vol_ratio):
        if vol_ratio >= 1.5:
            score += 10
            details.append(f"Volume surge ({vol_ratio:.2f}x average)")
        elif vol_ratio <= 0.7:
            score -= 8
            details.append(f"Low volume ({vol_ratio:.2f}x average)")
        else:
            details.append(f"Normal volume ({vol_ratio:.2f}x average)")

    vol_btc = latest.get("volume")
    if pd.notna(vol_btc) and vol_btc > 0:
        details.append(f"Current candle: {float(vol_btc):,.2f} BTC")

    if pd.notna(taker_buy):
        if taker_buy >= 0.55:
            score += 12
            details.append(f"Strong taker buy pressure ({taker_buy:.1%})")
        elif taker_buy <= 0.45:
            score -= 12
            details.append(f"Taker sell dominance ({taker_buy:.1%})")
        else:
            details.append(f"Balanced taker flow ({taker_buy:.1%})")

    return ComponentScore(
        name="Volume",
        score=_clamp(score),
        weight=0.15,
        detail="; ".join(details) or "Volume data neutral",
    )


def _score_heatmap(
    heatmap: pd.DataFrame | None,
    price: float,
    source: str,
) -> ComponentScore:
    if heatmap is None or heatmap.empty:
        return ComponentScore(
            name="Heatmap",
            score=50.0,
            weight=0.10,
            detail="No heatmap data available",
        )

    below = heatmap[heatmap["price_level"] < price]
    above = heatmap[heatmap["price_level"] > price]

    support_strength = below["intensity"].sum() if not below.empty else 0
    resistance_strength = above["intensity"].sum() if not above.empty else 0
    total = support_strength + resistance_strength

    score = 50.0
    if total > 0:
        support_pct = support_strength / total
        score = support_pct * 100

    nearest_support = below.iloc[-1]["price_level"] if not below.empty else None
    nearest_resistance = above.iloc[0]["price_level"] if not above.empty else None

    details = [f"Source: {source}"]
    if nearest_support is not None:
        details.append(f"Nearest support ~${nearest_support:,.0f}")
    if nearest_resistance is not None:
        details.append(f"Nearest resistance ~${nearest_resistance:,.0f}")
    if total > 0:
        details.append(f"Support vs resistance intensity: {support_strength / total:.0%} / {resistance_strength / total:.0%}")

    return ComponentScore(
        name="Heatmap",
        score=_clamp(score),
        weight=0.10,
        detail="; ".join(details),
    )


def _score_derivatives(
    funding_rate: float | None,
    long_short_ratio: float | None,
    oi_change_pct: float | None,
) -> ComponentScore:
    score = 50.0
    details: list[str] = []

    if funding_rate is not None:
        if funding_rate > 0.0005:
            score -= 10
            details.append(f"Elevated positive funding ({funding_rate:.4%}) — crowded longs")
        elif funding_rate < -0.0002:
            score += 10
            details.append(f"Negative funding ({funding_rate:.4%}) — shorts paying longs")
        else:
            details.append(f"Funding rate neutral ({funding_rate:.4%})")

    if long_short_ratio is not None:
        if long_short_ratio > 1.2:
            score -= 8
            details.append(f"Long-heavy positioning (L/S {long_short_ratio:.2f})")
        elif long_short_ratio < 0.85:
            score += 8
            details.append(f"Short-heavy positioning (L/S {long_short_ratio:.2f})")
        else:
            details.append(f"Balanced long/short ratio ({long_short_ratio:.2f})")

    if oi_change_pct is not None:
        if oi_change_pct > 3:
            details.append(f"Open interest rising (+{oi_change_pct:.1f}%) — new capital entering")
        elif oi_change_pct < -3:
            details.append(f"Open interest falling ({oi_change_pct:.1f}%) — positions unwinding")

    return ComponentScore(
        name="Derivatives Sentiment",
        score=_clamp(score),
        weight=0.15,
        detail="; ".join(details) or "Derivatives data neutral",
    )


def _recommendation_from_score(score: float) -> Recommendation:
    if score >= 62:
        return "long"
    if score <= 38:
        return "short"
    return "wait"


def _confidence_label(score: float, components: list[ComponentScore], hub: HubSnapshot | None = None) -> str:
    spread = max(c.score for c in components) - min(c.score for c in components)
    distance_from_neutral = abs(score - 50)

    if distance_from_neutral >= 25 and spread <= 35:
        base = "High"
    elif distance_from_neutral >= 15:
        base = "Medium"
    else:
        base = "Low"

    if hub is None:
        return base

    missing = len(hub.missing_fields)
    if hub.critical_missing or missing >= 4:
        return "Low"
    if missing >= 2 and base == "High":
        return "Medium"
    if missing >= 1 and base == "High":
        return "Medium"
    return base


def _calc_sl_tp(
    price: float,
    recommendation: Recommendation,
    df: pd.DataFrame,
    heatmap: pd.DataFrame | None,
) -> tuple[float, float, float]:
    atr_proxy = (df["high"] - df["low"]).tail(14).mean()
    if pd.isna(atr_proxy) or atr_proxy <= 0:
        atr_proxy = price * 0.015

    support = price - atr_proxy * 1.5
    resistance = price + atr_proxy * 1.5

    if heatmap is not None and not heatmap.empty:
        below = heatmap[heatmap["price_level"] < price]
        above = heatmap[heatmap["price_level"] > price]
        if not below.empty:
            support = below.loc[below["intensity"].idxmax(), "price_level"]
        if not above.empty:
            resistance = above.loc[above["intensity"].idxmax(), "price_level"]

    if recommendation == "long":
        stop_loss = min(support, price - atr_proxy)
        take_profit = max(resistance, price + atr_proxy * 2)
    elif recommendation == "short":
        stop_loss = max(resistance, price + atr_proxy)
        take_profit = min(support, price - atr_proxy * 2)
    else:
        stop_loss = price - atr_proxy
        take_profit = price + atr_proxy

    risk = abs(price - stop_loss)
    reward = abs(take_profit - price)
    rr = reward / risk if risk > 0 else 0.0
    return stop_loss, take_profit, rr


def _build_explanation(
    result_score: float,
    recommendation: Recommendation,
    confidence: str,
    components: list[ComponentScore],
    price: float,
    stop_loss: float,
    take_profit: float,
    data_sources: list[str],
    heatmap_source: str,
    hub: HubSnapshot | None = None,
) -> str:
    rec_text = {
        "long": "enter a long position",
        "short": "enter a short position",
        "wait": "stay on the sidelines and wait for clearer confirmation",
    }[recommendation]

    lines = [
        f"Bitcoin is trading at ${price:,.2f}. The composite score is {result_score:.1f}/100, "
        f"suggesting you should {rec_text}. Confidence is {confidence.lower()}.",
        "",
        "Signal breakdown:",
    ]

    for component in components:
        bias = "bullish" if component.score >= 55 else "bearish" if component.score <= 45 else "neutral"
        lines.append(
            f"• {component.name} ({component.score:.0f}/100, {bias}): {component.detail}"
        )

    lines.extend(
        [
            "",
            f"Risk management: stop loss at ${stop_loss:,.2f}, take profit at ${take_profit:,.2f}.",
            f"Heatmap derived from {heatmap_source}.",
            f"Data sources used in signal: {', '.join(data_sources)}.",
        ]
    )

    if hub is not None:
        lines.extend(
            [
                "",
                "Data Hub summary:",
                f"• Quality: {hub.data_quality} ({hub.confidence_impact})",
                f"• Available: {', '.join(hub.available_fields) or 'none'}",
            ]
        )
        if hub.missing_fields:
            lines.append(f"• Missing: {', '.join(hub.missing_fields)}")
        if hub.force_wait:
            lines.append("• Critical market data missing — WAIT enforced by Data Hub.")
        online = [name for name, info in hub.source_status.items() if info.status == "online"]
        if online:
            lines.append(f"• Online sources: {', '.join(online)}")

    lines.extend(
        [
            "",
            "Note: This is a technical analysis tool, not financial advice. "
            "Always validate signals with your own research and position sizing rules.",
        ]
    )
    return "\n".join(lines)


class MarketAnalyzer:
    def __init__(
        self,
        symbol: str = "BTCUSDT",
        interval: str = "1h",
        coinglass_api_key: str | None = None,
    ) -> None:
        self.symbol = symbol
        self.interval = interval
        self.data_hub = BitcoinDataHub(symbol=symbol, coinglass_api_key=coinglass_api_key)

    def analyze(self) -> AnalysisResult:
        hub = self.data_hub.fetch(interval=self.interval, limit=500)

        if hub.force_wait or hub.price is None or hub.candles is None or hub.candles.empty:
            return self._missing_data_result(hub)

        df = compute_emas(hub.candles)
        df = compute_macd(df)
        df = compute_rsi(df)
        df = compute_volume_metrics(df)

        price = float(hub.price)
        funding = hub.funding_rate
        long_short = hub.long_short_ratio
        oi_change_pct = hub.open_interest_change_pct

        data_sources = list(hub.sources) or ["Binance"]
        heatmap_source = "volume profile (Binance)"
        heatmap = build_volume_heatmap(df)

        if self.data_hub.coinglass.enabled:
            try:
                cg_heatmap = self.data_hub.coinglass.get_liquidation_heatmap()
                parsed = parse_coinglass_heatmap(cg_heatmap, price)
                if parsed is not None and not parsed.empty:
                    heatmap = parsed
                    heatmap_source = "Coinglass liquidation heatmap"
            except Exception:
                pass

        components = [
            _score_ema_trend(df),
            _score_macd(df),
            _score_rsi(df),
            _score_volume(df),
            _score_heatmap(heatmap, price, heatmap_source),
            _score_derivatives(funding, long_short, oi_change_pct),
        ]

        total_weight = sum(c.weight for c in components)
        score = sum(c.score * c.weight for c in components) / total_weight
        score = _clamp(score)

        recommendation = _recommendation_from_score(score)
        if hub.force_wait:
            recommendation = "wait"

        confidence = _confidence_label(score, components, hub)
        stop_loss, take_profit, rr = _calc_sl_tp(price, recommendation, df, heatmap)

        latest = df.iloc[-1]
        vol_summary = summarize_volume(df, interval=self.interval)
        indicators = {
            "ema_9": float(latest.get("ema_9", 0) or 0),
            "ema_21": float(latest.get("ema_21", 0) or 0),
            "ema_50": float(latest.get("ema_50", 0) or 0),
            "ema_200": float(latest.get("ema_200", 0) or 0),
            "macd": float(latest.get("macd", 0) or 0),
            "macd_signal": float(latest.get("macd_signal", 0) or 0),
            "macd_hist": float(latest.get("macd_hist", 0) or 0),
            "rsi": float(latest.get("rsi", 0) or 0),
            "volume_ratio": float(latest.get("volume_ratio", 0) or 0),
            "taker_buy_ratio": float(latest.get("taker_buy_ratio", 0) or 0),
            "volume_btc": vol_summary.get("volume_btc", 0.0),
            "volume_sma_btc": vol_summary.get("volume_sma_btc", 0.0),
            "volume_24h_btc": vol_summary.get("volume_24h_btc", 0.0),
            "quote_volume_usdt": vol_summary.get("quote_volume_usdt", 0.0),
            "volume_24h_usdt": vol_summary.get("volume_24h_usdt", 0.0),
            "volume_history": [float(v) for v in df.tail(48)["volume"].tolist()],
            "funding_rate": funding,
            "long_short_ratio": long_short,
            "oi_change_pct": oi_change_pct,
        }

        explanation = _build_explanation(
            score,
            recommendation,
            confidence,
            components,
            price,
            stop_loss,
            take_profit,
            data_sources,
            heatmap_source,
            hub,
        )

        result = AnalysisResult(
            symbol=self.symbol,
            price=price,
            score=score,
            recommendation=recommendation,
            confidence=confidence,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_reward=rr,
            explanation=explanation,
            components=components,
            indicators=indicators,
            heatmap_source=heatmap_source,
            data_sources=data_sources,
            heatmap=heatmap,
            hub=hub.to_dict(),
            supported_sources=data_sources,
            data_quality=hub.data_quality,
        )

        try:
            from src.analysis.ai_decision_engine import enrich_analysis

            return enrich_analysis(
                result,
                candles=df,
                heatmap=heatmap,
                coinglass_enabled=self.data_hub.coinglass.enabled,
            )
        except Exception:
            return result

    def _missing_data_result(self, hub: HubSnapshot) -> AnalysisResult:
        price = float(hub.price or 0)
        missing_text = ", ".join(hub.missing_fields) or "critical market feeds"
        explanation = (
            f"Unable to produce a directional signal because required data is missing ({missing_text}).\n\n"
            f"Data Hub quality: {hub.data_quality}. Confidence impact: {hub.confidence_impact}.\n"
            f"Connected sources: {', '.join(hub.sources) or 'none'}.\n\n"
            "Recommendation: WAIT until price and candle data are available.\n\n"
            "Note: This is a technical analysis tool, not financial advice."
        )
        return AnalysisResult(
            symbol=self.symbol,
            price=price,
            score=50.0,
            recommendation="wait",
            confidence="Low",
            stop_loss=price * 0.985 if price else 0.0,
            take_profit=price * 1.015 if price else 0.0,
            risk_reward=0.0,
            explanation=explanation,
            components=[
                ComponentScore(
                    name="Data Hub",
                    score=50.0,
                    weight=1.0,
                    detail=f"Missing required fields: {missing_text}",
                )
            ],
            indicators={},
            heatmap_source="unavailable",
            data_sources=list(hub.sources),
            heatmap=None,
            hub=hub.to_dict(),
            supported_sources=list(hub.sources),
            data_quality=hub.data_quality,
        )
