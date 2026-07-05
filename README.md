# Bitcoin Market Analyzer

Python app that analyzes the Bitcoin market using Binance spot/futures data and optional Coinglass derivatives data. Computes EMA, MACD, RSI, volume, and a price heatmap, then outputs a 0–100 score with a **long**, **short**, or **wait** recommendation.

## Features

- Live OHLCV from Binance
- Technical indicators: EMA (9/21/50/200), MACD, RSI, volume analysis
- Heatmap: Coinglass liquidation heatmap (with API key) or Binance volume profile fallback
- Derivatives context: funding rate, long/short ratio, open interest change
- Composite score (0–100), confidence, stop loss, take profit, and written explanation
- Simple Streamlit UI with an **Analyze** button

## Quick start
