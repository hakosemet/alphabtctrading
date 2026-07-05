"""Technical indicator calculations."""

from __future__ import annotations

import numpy as np
import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def compute_emas(df: pd.DataFrame, periods: tuple[int, ...] = (9, 21, 50, 200)) -> pd.DataFrame:
    out = df.copy()
    for period in periods:
        out[f"ema_{period}"] = ema(out["close"], period)
    return out


def compute_macd(
    df: pd.DataFrame,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    out = df.copy()
    ema_fast = ema(out["close"], fast)
    ema_slow = ema(out["close"], slow)
    out["macd"] = ema_fast - ema_slow
    out["macd_signal"] = ema(out["macd"], signal)
    out["macd_hist"] = out["macd"] - out["macd_signal"]
    return out


def compute_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    out = df.copy()
    delta = out["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    out["rsi"] = 100 - (100 / (1 + rs))
    return out


INTERVAL_MINUTES: dict[str, int] = {
    "1m": 1,
    "3m": 3,
    "5m": 5,
    "15m": 15,
    "30m": 30,
    "1h": 60,
    "4h": 240,
    "1d": 1440,
}


def compute_volume_metrics(df: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    out = df.copy()
    out["volume_sma"] = out["volume"].rolling(lookback).mean()
    out["volume_ratio"] = out["volume"] / out["volume_sma"]
    out["taker_buy_ratio"] = out["taker_buy_base"] / out["volume"].replace(0, np.nan)
    return out


def summarize_volume(df: pd.DataFrame, *, interval: str = "1h") -> dict[str, float]:
    """Absolute BTC / USDT volume stats for the indicators panel."""
    if df is None or df.empty:
        return {}

    latest = df.iloc[-1]
    minutes = INTERVAL_MINUTES.get(interval, 60)
    bars_24h = max(1, int((24 * 60) / minutes))
    window = df.tail(bars_24h)

    quote_col = "quote_volume" if "quote_volume" in df.columns else None
    volume_24h_usdt = float(window[quote_col].sum()) if quote_col else 0.0
    quote_volume = float(latest[quote_col]) if quote_col and pd.notna(latest.get(quote_col)) else 0.0

    return {
        "volume_btc": float(latest.get("volume") or 0),
        "volume_sma_btc": float(latest.get("volume_sma") or 0),
        "volume_24h_btc": float(window["volume"].sum()),
        "quote_volume_usdt": quote_volume,
        "volume_24h_usdt": volume_24h_usdt,
    }


def build_volume_heatmap(
    df: pd.DataFrame,
    bins: int = 30,
    lookback: int = 120,
) -> pd.DataFrame:
    """Price-volume profile used as a heatmap proxy when Coinglass is unavailable."""
    window = df.tail(lookback)
    price_min = window["low"].min()
    price_max = window["high"].max()
    if price_min >= price_max:
        price_max = price_min * 1.001

    edges = np.linspace(price_min, price_max, bins + 1)
    midpoints = (edges[:-1] + edges[1:]) / 2
    volumes = np.zeros(bins)

    for _, row in window.iterrows():
        low_idx = np.searchsorted(edges, row["low"], side="right") - 1
        high_idx = np.searchsorted(edges, row["high"], side="left")
        low_idx = max(0, min(bins - 1, low_idx))
        high_idx = max(0, min(bins - 1, high_idx))
        span = max(1, high_idx - low_idx + 1)
        share = row["volume"] / span
        for idx in range(low_idx, high_idx + 1):
            volumes[idx] += share

    heatmap = pd.DataFrame({"price_level": midpoints, "volume": volumes})
    heatmap["intensity"] = heatmap["volume"] / heatmap["volume"].max() if heatmap["volume"].max() else 0
    return heatmap.sort_values("price_level")


def parse_coinglass_heatmap(raw: dict | list | None, current_price: float) -> pd.DataFrame | None:
    """Normalize Coinglass heatmap payloads into price/intensity rows."""
    if not raw:
        return None

    rows: list[dict[str, float]] = []

    if isinstance(raw, dict):
        price_list = raw.get("prices") or raw.get("y") or raw.get("priceList")
        liq_list = raw.get("liquidationLeverage") or raw.get("data") or raw.get("values")
        if isinstance(price_list, list) and isinstance(liq_list, list):
            for price, intensity in zip(price_list, liq_list, strict=False):
                try:
                    rows.append({"price_level": float(price), "intensity": float(intensity)})
                except (TypeError, ValueError):
                    continue
        elif "list" in raw and isinstance(raw["list"], list):
            for item in raw["list"]:
                if not isinstance(item, dict):
                    continue
                price = item.get("price") or item.get("priceLevel")
                intensity = item.get("amount") or item.get("value") or item.get("liquidation")
                if price is not None and intensity is not None:
                    rows.append({"price_level": float(price), "intensity": float(intensity)})

    if isinstance(raw, list):
        for item in raw:
            if not isinstance(item, dict):
                continue
            price = item.get("price") or item.get("priceLevel")
            intensity = item.get("amount") or item.get("value") or item.get("liquidation")
            if price is not None and intensity is not None:
                rows.append({"price_level": float(price), "intensity": float(intensity)})

    if not rows:
        return None

    df = pd.DataFrame(rows)
    max_intensity = df["intensity"].max()
    if max_intensity:
        df["intensity"] = df["intensity"] / max_intensity
    df["distance_pct"] = ((df["price_level"] - current_price) / current_price) * 100
    return df.sort_values("price_level")
