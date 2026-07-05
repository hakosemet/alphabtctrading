# Ofir Kadosh Bitcoin AI Dashboard — Full Project (Single File Backup)

Generated: 2026-07-05 15:26:24 UTC
Root: `C:\Users\NORIS\btc-market-analyzer`
Files: 61

Restore: run `python restore_from_backup.py` or copy each section back to the matching path.

## Table of Contents

- [.env.example](#file--env-example)
- [.gitignore](#file--gitignore)
- [_streamlit_test.txt](#file-_streamlit_test-txt)
- [app.py](#file-app-py)
- [assets\README.txt](#file-assets-README-txt)
- [generate_export.py](#file-generate_export-py)
- [README.md](#file-README-md)
- [requirements.txt](#file-requirements-txt)
- [SNAPSHOT_README.txt](#file-SNAPSHOT_README-txt)
- [src\__init__.py](#file-src-__init__-py)
- [src\analysis\__init__.py](#file-src-analysis-__init__-py)
- [src\analysis\ai_decision_engine.py](#file-src-analysis-ai_decision_engine-py)
- [src\analysis\cross_exchange.py](#file-src-analysis-cross_exchange-py)
- [src\analysis\models.py](#file-src-analysis-models-py)
- [src\analysis\platform_gate.py](#file-src-analysis-platform_gate-py)
- [src\analysis\risk_manager.py](#file-src-analysis-risk_manager-py)
- [src\analysis\scorer.py](#file-src-analysis-scorer-py)
- [src\analysis\sentiment.py](#file-src-analysis-sentiment-py)
- [src\analysis\trade_setup.py](#file-src-analysis-trade_setup-py)
- [src\data\__init__.py](#file-src-data-__init__-py)
- [src\data\binance_client.py](#file-src-data-binance_client-py)
- [src\data\cache.py](#file-src-data-cache-py)
- [src\data\coinglass_client.py](#file-src-data-coinglass_client-py)
- [src\data\connectors\__init__.py](#file-src-data-connectors-__init__-py)
- [src\data\connectors\alt_exchange.py](#file-src-data-connectors-alt_exchange-py)
- [src\data\connectors\base.py](#file-src-data-connectors-base-py)
- [src\data\connectors\binance_connector.py](#file-src-data-connectors-binance_connector-py)
- [src\data\connectors\bingx.py](#file-src-data-connectors-bingx-py)
- [src\data\connectors\bitget.py](#file-src-data-connectors-bitget-py)
- [src\data\connectors\bybit.py](#file-src-data-connectors-bybit-py)
- [src\data\connectors\coinbase.py](#file-src-data-connectors-coinbase-py)
- [src\data\connectors\kraken.py](#file-src-data-connectors-kraken-py)
- [src\data\connectors\mexc.py](#file-src-data-connectors-mexc-py)
- [src\data\connectors\okx.py](#file-src-data-connectors-okx-py)
- [src\data\data_hub.py](#file-src-data-data_hub-py)
- [src\data\exchange_api.py](#file-src-data-exchange_api-py)
- [src\data\fallback_market.py](#file-src-data-fallback_market-py)
- [src\data\fear_greed.py](#file-src-data-fear_greed-py)
- [src\data\feed_cache.py](#file-src-data-feed_cache-py)
- [src\data\hub_models.py](#file-src-data-hub_models-py)
- [src\data\news_client.py](#file-src-data-news_client-py)
- [src\data\news_sentiment.py](#file-src-data-news_sentiment-py)
- [src\data\onchain.py](#file-src-data-onchain-py)
- [src\data\onchain_client.py](#file-src-data-onchain_client-py)
- [src\data\whale_client.py](#file-src-data-whale_client-py)
- [src\indicators\__init__.py](#file-src-indicators-__init__-py)
- [src\indicators\technical.py](#file-src-indicators-technical-py)
- [src\ui\__init__.py](#file-src-ui-__init__-py)
- [src\ui\auth.py](#file-src-ui-auth-py)
- [src\ui\background.py](#file-src-ui-background-py)
- [src\ui\charts.py](#file-src-ui-charts-py)
- [src\ui\components.py](#file-src-ui-components-py)
- [src\ui\dashboard.py](#file-src-ui-dashboard-py)
- [src\ui\helpers.py](#file-src-ui-helpers-py)
- [src\ui\performance.py](#file-src-ui-performance-py)
- [src\ui\primitives.py](#file-src-ui-primitives-py)
- [src\ui\sidebar.py](#file-src-ui-sidebar-py)
- [src\ui\styles.py](#file-src-ui-styles-py)
- [src\ui\theme.py](#file-src-ui-theme-py)
- [src\ui\time_utils.py](#file-src-ui-time_utils-py)
- [src\ui\tradingview.py](#file-src-ui-tradingview-py)

---

<a id="file--env-example"></a>
## File: `.env.example`


```text
# Optional: Coinglass API key for liquidation heatmap and enriched derivatives data
COINGLASS_API_KEY=

# Required: password to open the dashboard (all users must enter it)
DASHBOARD_PASSWORD=16081993

# Optional on-chain / whale providers (placeholders until live endpoints are wired)
GLASSNODE_API_KEY=
CRYPTOQUANT_API_KEY=
ARKHAM_API_KEY=
WHALE_ALERT_API_KEY=
```

---

<a id="file--gitignore"></a>
## File: `.gitignore`


```text
.venv/
__pycache__/
*.pyc
.env
.streamlit/
```

---

<a id="file-_streamlit_test-txt"></a>
## File: `_streamlit_test.txt`


```text
﻿python : 2026-07-04 19:50:42.420 Uvicorn server started on 0.0.0.0:8502
At C:\Users\NORIS\AppData\Local\Temp\ps-script-69595d4f-e40f-4ae5-a692-db38b7b8ab80.ps1:115 char:52
+ ... -analyzer"; python -m streamlit run app.py --server.headless true --s ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (2026-07-04 19:5...on 0.0.0.0:8502:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8502
  Network URL: http://10.0.0.1:8502
  External URL: http://79.177.129.235:8502
```

---

<a id="file-app-py"></a>
## File: `app.py`


```python
"""Streamlit UI for Bitcoin market analysis."""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ui.performance import run_cached_market_analysis
from src.ui.auth import render_login_gate
from src.ui.components import (
    render_dashboard,
    render_error_state,
    render_header_bar,
)
from src.ui.sidebar import AUTO_REFRESH_SECONDS, render_sidebar
from src.ui.styles import inject_global_styles
from src.ui.time_utils import normalize_last_updated

load_dotenv(ROOT / ".env", override=True)

st.set_page_config(
    page_title="AlphaBTC",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def _get_last_updated() -> datetime | None:
    return normalize_last_updated(st.session_state.get("last_updated"))


def _run_analysis(symbol: str, interval: str, api_key: str) -> None:
    # Performance: Streamlit cache skips duplicate Binance / enrichment calls on reruns.
    st.session_state["last_result"] = run_cached_market_analysis(symbol, interval, api_key or "")
    st.session_state["last_updated"] = datetime.now(timezone.utc)


def _auto_refresh(symbol: str, interval: str, api_key: str) -> None:
    seconds = AUTO_REFRESH_SECONDS

    try:
        from streamlit_autorefresh import st_autorefresh

        tick = st_autorefresh(interval=seconds * 1000, key="btc_dashboard_autorefresh")
        if tick > 0 and "last_result" in st.session_state:
            try:
                _run_analysis(symbol, interval, api_key)
            except Exception:
                pass
        return
    except ImportError:
        pass

    try:
        @st.fragment(run_every=timedelta(seconds=seconds))
        def _refresh_worker() -> None:
            try:
                _run_analysis(symbol, interval, api_key)
            except Exception:
                return

        _refresh_worker()
    except TypeError:
        last = normalize_last_updated(st.session_state.get("last_updated"))
        if last is not None:
            elapsed = (datetime.now(timezone.utc) - last).total_seconds()
            if elapsed >= seconds:
                try:
                    _run_analysis(symbol, interval, api_key)
                except Exception:
                    pass
                st.rerun()
            remaining = max(5, int(seconds - elapsed))
            st.markdown(
                f'<meta http-equiv="refresh" content="{remaining}">',
                unsafe_allow_html=True,
            )


def main() -> None:
    inject_global_styles(dark_mode=True, project_root=ROOT, hide_sidebar=True)

    if not render_login_gate(project_root=ROOT):
        return

    sidebar = render_sidebar()
    render_header_bar(_get_last_updated())

    st.markdown('<div class="dashboard-shell">', unsafe_allow_html=True)
    st.markdown(
        '<p class="safety-banner">PRIVATE PROJECT</p>',
        unsafe_allow_html=True,
    )

    if "last_result" not in st.session_state:
        with st.spinner("Fetching market data and running AI analysis..."):
            try:
                _run_analysis(sidebar.symbol, sidebar.interval, sidebar.api_key)
            except Exception as exc:
                render_error_state(str(exc))
                st.markdown("</div>", unsafe_allow_html=True)
                return

    st.session_state["chart_interval"] = "1m"
    render_dashboard(
        st.session_state["last_result"],
        dark=True,
        risk_settings=sidebar.risk_settings,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    _auto_refresh(sidebar.symbol, sidebar.interval, sidebar.api_key)


if __name__ == "__main__":
    main()
```

---

<a id="file-assets-README-txt"></a>
## File: `assets\README.txt`


```text
# Custom background image
#
# Place your image here as:
#   assets/background.jpg
#
# Supported fallbacks: .jpeg, .png, .webp
#
# The app applies it automatically on every startup with:
#   - full-page cover, centered, no repeat, fixed while scrolling
#   - ~45% dark overlay for readability
#   - glass-style semi-transparent cards
#
# If background.jpg is missing, the default theme is used (no crash).
```

---

<a id="file-generate_export-py"></a>
## File: `generate_export.py`


```python
"""Export the entire project into a single backup file."""

from __future__ import annotations

import base64
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "OFIR_KADOSH_BTC_DASHBOARD_FULL_PROJECT.md"

SKIP_DIRS = {".venv", "__pycache__", ".git", "backups", ".streamlit"}
SKIP_FILES = {
    OUTPUT.name,
    "PROJECT_EXPORT.md",
    ".env",
}
TEXT_SUFFIXES = {".py", ".md", ".txt", ".example", ".gitignore", ".env.example"}
BINARY_ASSETS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

LANG = {
    ".py": "python",
    ".md": "markdown",
    ".txt": "text",
    ".example": "text",
    ".gitignore": "text",
}


def _collect_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.name in SKIP_FILES:
            continue
        if rel.suffix.lower() in TEXT_SUFFIXES or rel.name == ".gitignore":
            files.append(path)
            continue
        if rel.suffix.lower() in BINARY_ASSETS:
            files.append(path)
    return files


def _anchor(rel: Path) -> str:
    return str(rel).replace("/", "-").replace("\\", "-").replace(".", "-")


def main() -> None:
    files = _collect_files()
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: list[str] = [
        "# Ofir Kadosh Bitcoin AI Dashboard — Full Project (Single File Backup)",
        "",
        f"Generated: {generated}",
        f"Root: `{ROOT}`",
        f"Files: {len(files)}",
        "",
        "Restore: run `python restore_from_backup.py` or copy each section back to the matching path.",
        "",
        "## Table of Contents",
        "",
    ]

    for path in files:
        rel = path.relative_to(ROOT)
        lines.append(f"- [{rel}](#file-{_anchor(rel)})")

    lines.extend(["", "---", ""])

    for path in files:
        rel = path.relative_to(ROOT)
        suffix = path.suffix.lower()
        lines.extend([f'<a id="file-{_anchor(rel)}"></a>', f"## File: `{rel}`", ""])

        if suffix in BINARY_ASSETS:
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            lines.extend([
                "",
                f"Binary file ({path.stat().st_size:,} bytes). Restore with base64 decode.",
                "",
                "```base64",
                encoded,
                "```",
                "",
                "---",
                "",
            ])
            continue

        lang = LANG.get(suffix, LANG.get(path.name, "text"))
        content = path.read_text(encoding="utf-8", errors="replace").rstrip()
        lines.extend([
            "",
            f"```{lang}",
            content,
            "```",
            "",
            "---",
            "",
        ])

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved full project to: {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size:,} bytes")
    print(f"Files: {len(files)}")


if __name__ == "__main__":
    main()
```

---

<a id="file-README-md"></a>
## File: `README.md`


```markdown
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
```

---

<a id="file-requirements-txt"></a>
## File: `requirements.txt`


```text
streamlit
plotly
pandas
numpy
requests
python-dotenv
feedparser
ta
streamlit-autorefresh
```

---

<a id="file-SNAPSHOT_README-txt"></a>
## File: `SNAPSHOT_README.txt`


```text
Ofir Kadosh Bitcoin AI Dashboard — Saved snapshot
================================================

This folder documents the saved project state.

Current settings (fixed):
- Dark mode: always on
- Auto refresh: every 60 seconds
- Timeframe: 1m
- Tabs: AI Dashboard, Overview, Trade Setup, Risk, Indicators

To run:
  pip install -r requirements.txt
  python -m streamlit run app.py

To regenerate full code export:
  python generate_export.py

Backup zip (if created): backups/btc-market-analyzer-snapshot.zip
```

---

<a id="file-src-__init__-py"></a>
## File: `src\__init__.py`


```python

```

---

<a id="file-src-analysis-__init__-py"></a>
## File: `src\analysis\__init__.py`


```python

```

---

<a id="file-src-analysis-ai_decision_engine-py"></a>
## File: `src\analysis\ai_decision_engine.py`


```python
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
from src.data.feed_cache import fetch_enrichment_feeds_parallel
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
    # Performance: parallel + TTL-cached enrichment feeds (Fear/Greed, news, on-chain, whales).
    feeds = fetch_enrichment_feeds_parallel()
    fear_data = feeds["fear_data"]
    fear_info = feeds["fear_info"]
    news_data = feeds["news_data"]
    news_info = feeds["news_info"]
    onchain_data = feeds["onchain_data"]
    onchain_info = feeds["onchain_info"]
    whale_data = feeds["whale_data"]
    whale_info = feeds["whale_info"]

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

    def _status(info) -> str:
        if info is None:
            return "offline"
        return getattr(info, "status", "offline")

    return {
        "Binance": binance_status,
        "Coinglass": "online" if coinglass_enabled else hub_sources.get("Coinglass", {}).get("status", "offline"),
        "Fear & Greed": _status(fear_info),
        "News RSS": _status(news_info),
        "On-chain": _status(onchain_info),
        "Whale data": _status(whale_info),
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
```

---

<a id="file-src-analysis-cross_exchange-py"></a>
## File: `src\analysis\cross_exchange.py`


```python
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
```

---

<a id="file-src-analysis-models-py"></a>
## File: `src\analysis\models.py`


```python
"""Analysis result data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import pandas as pd

Recommendation = Literal["long", "short", "wait"]


@dataclass
class ComponentScore:
    name: str
    score: float
    weight: float
    detail: str


@dataclass
class MarketStatusPanel:
    trend: str
    volatility: str
    liquidity: str


@dataclass
class TradeQuality:
    grade: str
    score: int
    stars: int


@dataclass
class DashboardInsights:
    market_status: MarketStatusPanel
    trade_quality: TradeQuality
    fear_greed: dict[str, Any] = field(default_factory=dict)
    news_sentiment: dict[str, Any] = field(default_factory=dict)
    onchain_data: dict[str, Any] = field(default_factory=dict)
    whale_data: dict[str, Any] = field(default_factory=dict)
    source_status: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisResult:
    symbol: str
    price: float
    score: float
    recommendation: Recommendation
    confidence: str
    stop_loss: float
    take_profit: float
    risk_reward: float
    explanation: str
    components: list[ComponentScore] = field(default_factory=list)
    indicators: dict = field(default_factory=dict)
    heatmap_source: str = "volume_profile"
    data_sources: list[str] = field(default_factory=list)
    heatmap: pd.DataFrame | None = None
    hub: dict | None = None
    supported_sources: list[str] = field(default_factory=list)
    data_quality: str = "full"
    insights: DashboardInsights | None = None
    take_profits: dict[str, float] = field(default_factory=dict)
    risk_profile: dict[str, float] = field(default_factory=dict)
    reasons_enter: list[str] = field(default_factory=list)
    reasons_avoid: list[str] = field(default_factory=list)
    fear_greed: dict[str, Any] = field(default_factory=dict)
    news_sentiment: dict[str, Any] = field(default_factory=dict)
    onchain_data: dict[str, Any] = field(default_factory=dict)
    whale_data: dict[str, Any] = field(default_factory=dict)
    source_status: dict[str, Any] = field(default_factory=dict)
    enhanced_explanation: str = ""
    trade_setup: dict[str, Any] = field(default_factory=dict)
    trade_setups: list[dict[str, Any]] = field(default_factory=list)
    platform_checks: dict[str, Any] = field(default_factory=dict)
```

---

<a id="file-src-analysis-platform_gate-py"></a>
## File: `src\analysis\platform_gate.py`


```python
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
```

---

<a id="file-src-analysis-risk_manager-py"></a>
## File: `src\analysis\risk_manager.py`


```python
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
```

---

<a id="file-src-analysis-scorer-py"></a>
## File: `src\analysis\scorer.py`


```python
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
```

---

<a id="file-src-analysis-sentiment-py"></a>
## File: `src\analysis\sentiment.py`


```python
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
```

---

<a id="file-src-analysis-trade_setup-py"></a>
## File: `src\analysis\trade_setup.py`


```python
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
```

---

<a id="file-src-data-__init__-py"></a>
## File: `src\data\__init__.py`


```python
"""Data layer — unified Bitcoin Data Hub and source connectors."""

from src.data.data_hub import BitcoinDataHub
from src.data.hub_models import HubSnapshot, SourceInfo

__all__ = ["BitcoinDataHub", "HubSnapshot", "SourceInfo"]
```

---

<a id="file-src-data-binance_client-py"></a>
## File: `src\data\binance_client.py`


```python
"""Fetch OHLCV and derivatives data from Binance public APIs."""

from __future__ import annotations

from typing import Any

import pandas as pd
import requests

SPOT_BASE = "https://api.binance.com"
FUTURES_BASE = "https://fapi.binance.com"


class BinanceClient:
    def __init__(self, symbol: str = "BTCUSDT", timeout: int = 15) -> None:
        self.symbol = symbol
        self.timeout = timeout

    def _get(self, base: str, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{base}{path}"
        response = requests.get(url, params=params or {}, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_klines(
        self,
        interval: str = "1h",
        limit: int = 500,
    ) -> pd.DataFrame:
        raw = self._get(
            SPOT_BASE,
            "/api/v3/klines",
            {"symbol": self.symbol, "interval": interval, "limit": limit},
        )
        df = pd.DataFrame(
            raw,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_volume",
                "trades",
                "taker_buy_base",
                "taker_buy_quote",
                "ignore",
            ],
        )
        numeric_cols = ["open", "high", "low", "close", "volume", "quote_volume", "taker_buy_base"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)
        return df

    def get_funding_rate(self) -> float | None:
        try:
            data = self._get(
                FUTURES_BASE,
                "/fapi/v1/premiumIndex",
                {"symbol": self.symbol},
            )
            return float(data.get("lastFundingRate", 0))
        except requests.RequestException:
            return None

    def get_open_interest(self) -> float | None:
        try:
            data = self._get(
                FUTURES_BASE,
                "/fapi/v1/openInterest",
                {"symbol": self.symbol},
            )
            return float(data.get("openInterest", 0))
        except requests.RequestException:
            return None

    def get_long_short_ratio(self, period: str = "1h", limit: int = 30) -> pd.DataFrame | None:
        try:
            raw = self._get(
                FUTURES_BASE,
                "/futures/data/globalLongShortAccountRatio",
                {"symbol": self.symbol, "period": period, "limit": limit},
            )
            df = pd.DataFrame(raw)
            if df.empty:
                return None
            df["longShortRatio"] = pd.to_numeric(df["longShortRatio"], errors="coerce")
            df["longAccount"] = pd.to_numeric(df["longAccount"], errors="coerce")
            df["shortAccount"] = pd.to_numeric(df["shortAccount"], errors="coerce")
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
            return df
        except requests.RequestException:
            return None

    def get_ticker_price(self) -> float:
        data = self._get(SPOT_BASE, "/api/v3/ticker/price", {"symbol": self.symbol})
        return float(data["price"])

    def get_order_book(self, limit: int = 20) -> dict | None:
        try:
            data = self._get(
                SPOT_BASE,
                "/api/v3/depth",
                {"symbol": self.symbol, "limit": limit},
            )
            return {
                "bids": data.get("bids", []),
                "asks": data.get("asks", []),
                "lastUpdateId": data.get("lastUpdateId"),
            }
        except requests.RequestException:
            return None
```

---

<a id="file-src-data-cache-py"></a>
## File: `src\data\cache.py`


```python
"""Simple in-memory TTL cache for API responses."""

from __future__ import annotations

import time
from typing import Any, TypeVar

T = TypeVar("T")


class TTLCache:
    def __init__(self, default_ttl: int = 60) -> None:
        self._default_ttl = default_ttl
        self._store: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if time.time() >= expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, *, ttl: int | None = None) -> None:
        seconds = self._default_ttl if ttl is None else ttl
        self._store[key] = (time.time() + seconds, value)

    def clear(self) -> None:
        self._store.clear()
```

---

<a id="file-src-data-coinglass_client-py"></a>
## File: `src\data\coinglass_client.py`


```python
"""Optional Coinglass API client for derivatives and liquidation heatmap data."""

from __future__ import annotations

import os
from typing import Any

import pandas as pd
import requests

BASE_URL = "https://open-api-v4.coinglass.com"


class CoinglassClient:
    def __init__(self, api_key: str | None = None, timeout: int = 15) -> None:
        self.api_key = api_key or os.getenv("COINGLASS_API_KEY", "").strip()
        self.timeout = timeout
        self.enabled = bool(self.api_key)

    def _headers(self) -> dict[str, str]:
        return {"CG-API-KEY": self.api_key, "accept": "application/json"}

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        if not self.enabled:
            return None
        url = f"{BASE_URL}{path}"
        response = requests.get(
            url,
            headers=self._headers(),
            params=params or {},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if str(payload.get("code")) != "0":
            raise ValueError(payload.get("msg", "Coinglass API error"))
        return payload.get("data")

    def get_funding_rates(self) -> list[dict[str, Any]] | None:
        try:
            data = self._get("/api/futures/funding-rate/exchange-list")
            if not data:
                return None
            for item in data:
                if item.get("symbol") == "BTC":
                    return item.get("stablecoin_margin_list") or []
            return None
        except (requests.RequestException, ValueError):
            return None

    def get_open_interest_history(
        self,
        exchange: str = "Binance",
        interval: str = "1h",
        limit: int = 50,
    ) -> pd.DataFrame | None:
        try:
            data = self._get(
                "/api/futures/open-interest/history",
                {
                    "exchange": exchange,
                    "symbol": "BTCUSDT",
                    "interval": interval,
                    "limit": limit,
                },
            )
            if not data:
                return None
            df = pd.DataFrame(data)
            for col in ("open", "high", "low", "close"):
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            if "time" in df.columns:
                df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
            return df
        except (requests.RequestException, ValueError):
            return None

    def get_liquidation_heatmap(self, range_param: str = "3d") -> dict[str, Any] | None:
        """Fetch liquidation heatmap model2 data when API key is available."""
        try:
            return self._get(
                "/api/futures/liquidation/heatmap/model2",
                {"symbol": "BTC", "range": range_param},
            )
        except (requests.RequestException, ValueError):
            return None

    def get_long_short_ratio_history(
        self,
        interval: str = "1h",
        limit: int = 50,
    ) -> pd.DataFrame | None:
        try:
            data = self._get(
                "/api/futures/global-long-short-account-ratio/history",
                {"symbol": "BTC", "interval": interval, "limit": limit},
            )
            if not data:
                return None
            df = pd.DataFrame(data)
            for col in ("longRate", "shortRate", "longShortRatio"):
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            if "time" in df.columns:
                df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
            return df
        except (requests.RequestException, ValueError):
            return None
```

---

<a id="file-src-data-connectors-__init__-py"></a>
## File: `src\data\connectors\__init__.py`


```python
"""Exchange and data source connectors."""

from src.data.connectors.base import BaseConnector
from src.data.connectors.binance_connector import BinanceConnector
from src.data.connectors.bingx import BingXConnector
from src.data.connectors.bitget import BitgetConnector
from src.data.connectors.bybit import BybitConnector
from src.data.connectors.coinbase import CoinbaseConnector
from src.data.connectors.kraken import KrakenConnector
from src.data.connectors.mexc import MEXCConnector
from src.data.connectors.okx import OKXConnector

__all__ = [
    "BaseConnector",
    "BinanceConnector",
    "BingXConnector",
    "BitgetConnector",
    "BybitConnector",
    "OKXConnector",
    "CoinbaseConnector",
    "KrakenConnector",
    "MEXCConnector",
]
```

---

<a id="file-src-data-connectors-alt_exchange-py"></a>
## File: `src\data\connectors\alt_exchange.py`


```python
"""Shared alt-exchange connector built on public REST APIs."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.data.connectors.base import BaseConnector
from src.data.exchange_api import EXCHANGE_FETCHERS
from src.data.hub_models import SourceInfo


class AltExchangeConnector(BaseConnector):
    enabled = True

    def __init__(self, exchange_key: str, *, timeout: int = 15) -> None:
        super().__init__(timeout=timeout)
        if exchange_key not in EXCHANGE_FETCHERS:
            raise ValueError(f"Unknown exchange: {exchange_key}")
        self.name = exchange_key
        self._fetch = EXCHANGE_FETCHERS[exchange_key]

    def probe(self) -> SourceInfo:
        bundle = self._fetch(timeout=self.timeout)
        if bundle.get("price") is None:
            errors = "; ".join(bundle.get("errors") or []) or "No price"
            return self._info(status="offline", error=errors)
        fields = [field for field in ("price", "funding_rate", "open_interest") if bundle.get(field) is not None]
        status = "degraded" if bundle.get("errors") else "online"
        return self._info(status=status, fields=fields, error="; ".join(bundle.get("errors") or []) or None)

    def fetch_market_bundle(self, interval: str = "1h", limit: int = 500) -> dict[str, Any]:
        del interval, limit
        return self._fetch(timeout=self.timeout)
```

---

<a id="file-src-data-connectors-base-py"></a>
## File: `src\data\connectors\base.py`


```python
"""Base connector with timeout-safe API calls."""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Callable, TypeVar

from src.data.hub_models import SourceInfo, SourceStatus

T = TypeVar("T")


class BaseConnector(ABC):
    name: str = "base"
    enabled: bool = False

    def __init__(self, timeout: int = 15) -> None:
        self.timeout = timeout

    @abstractmethod
    def probe(self) -> SourceInfo:
        """Return connector availability without heavy fetching."""

    def safe_call(self, label: str, fn: Callable[[], T], default: T | None = None) -> tuple[T | None, str | None]:
        try:
            return fn(), None
        except Exception as exc:
            return default, f"{label}: {exc}"

    def _info(
        self,
        *,
        status: SourceStatus,
        fields: list[str] | None = None,
        error: str | None = None,
    ) -> SourceInfo:
        return SourceInfo(
            name=self.name,
            status=status,
            last_updated=datetime.now(timezone.utc) if status == "online" else None,
            error=error,
            fields=fields or [],
        )
```

---

<a id="file-src-data-connectors-binance_connector-py"></a>
## File: `src\data\connectors\binance_connector.py`


```python
"""Primary Binance market-data connector."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.data.binance_client import BinanceClient
from src.data.connectors.base import BaseConnector
from src.data.hub_models import SourceInfo


class BinanceConnector(BaseConnector):
    name = "Binance"
    enabled = True

    def __init__(self, symbol: str = "BTCUSDT", timeout: int = 15) -> None:
        super().__init__(timeout=timeout)
        self.symbol = symbol
        self.client = BinanceClient(symbol=symbol, timeout=timeout)

    def probe(self) -> SourceInfo:
        price, error = self.safe_call("price", self.client.get_ticker_price)
        if price is None:
            return self._info(status="offline", error=error)
        return self._info(
            status="online",
            fields=["price", "candles", "volume", "order_book", "funding_rate", "open_interest", "long_short_ratio"],
        )

    def fetch_market_bundle(self, interval: str, limit: int = 500) -> dict[str, Any]:
        bundle: dict[str, Any] = {
            "price": None,
            "candles": None,
            "volume": None,
            "order_book": None,
            "funding_rate": None,
            "open_interest": None,
            "long_short_ratio": None,
            "errors": [],
        }

        price, err = self.safe_call("price", self.client.get_ticker_price)
        bundle["price"] = price
        if err:
            bundle["errors"].append(err)

        candles, err = self.safe_call("candles", lambda: self.client.get_klines(interval=interval, limit=limit))
        bundle["candles"] = candles
        if err:
            bundle["errors"].append(err)
        elif isinstance(candles, pd.DataFrame) and not candles.empty:
            bundle["volume"] = float(candles.iloc[-1]["volume"])

        order_book, err = self.safe_call("order_book", lambda: self.client.get_order_book(limit=20))
        bundle["order_book"] = order_book
        if err:
            bundle["errors"].append(err)

        funding, err = self.safe_call("funding_rate", self.client.get_funding_rate)
        bundle["funding_rate"] = funding
        if err:
            bundle["errors"].append(err)

        oi, err = self.safe_call("open_interest", self.client.get_open_interest)
        bundle["open_interest"] = oi
        if err:
            bundle["errors"].append(err)

        ls_df, err = self.safe_call(
            "long_short_ratio",
            lambda: self.client.get_long_short_ratio(period=interval),
        )
        if isinstance(ls_df, pd.DataFrame) and not ls_df.empty:
            bundle["long_short_ratio"] = float(ls_df.iloc[-1]["longShortRatio"])
        elif err:
            bundle["errors"].append(err)

        return bundle
```

---

<a id="file-src-data-connectors-bingx-py"></a>
## File: `src\data\connectors\bingx.py`


```python
"""BingX market-data connector."""

from __future__ import annotations

from src.data.connectors.alt_exchange import AltExchangeConnector


class BingXConnector(AltExchangeConnector):
    def __init__(self, timeout: int = 15) -> None:
        super().__init__("BingX", timeout=timeout)
```

---

<a id="file-src-data-connectors-bitget-py"></a>
## File: `src\data\connectors\bitget.py`


```python
"""Bitget market-data connector."""

from __future__ import annotations

from src.data.connectors.alt_exchange import AltExchangeConnector


class BitgetConnector(AltExchangeConnector):
    def __init__(self, timeout: int = 15) -> None:
        super().__init__("Bitget", timeout=timeout)
```

---

<a id="file-src-data-connectors-bybit-py"></a>
## File: `src\data\connectors\bybit.py`


```python
"""Bybit market-data connector."""

from __future__ import annotations

from src.data.connectors.alt_exchange import AltExchangeConnector


class BybitConnector(AltExchangeConnector):
    def __init__(self, timeout: int = 15) -> None:
        super().__init__("Bybit", timeout=timeout)
```

---

<a id="file-src-data-connectors-coinbase-py"></a>
## File: `src\data\connectors\coinbase.py`


```python
"""Coinbase market-data connector."""

from __future__ import annotations

from src.data.connectors.alt_exchange import AltExchangeConnector


class CoinbaseConnector(AltExchangeConnector):
    def __init__(self, timeout: int = 15) -> None:
        super().__init__("Coinbase", timeout=timeout)
```

---

<a id="file-src-data-connectors-kraken-py"></a>
## File: `src\data\connectors\kraken.py`


```python
"""Kraken market-data connector."""

from __future__ import annotations

from src.data.connectors.alt_exchange import AltExchangeConnector


class KrakenConnector(AltExchangeConnector):
    def __init__(self, timeout: int = 15) -> None:
        super().__init__("Kraken", timeout=timeout)
```

---

<a id="file-src-data-connectors-mexc-py"></a>
## File: `src\data\connectors\mexc.py`


```python
"""MEXC market-data connector."""

from __future__ import annotations

from src.data.connectors.alt_exchange import AltExchangeConnector


class MEXCConnector(AltExchangeConnector):
    def __init__(self, timeout: int = 15) -> None:
        super().__init__("MEXC", timeout=timeout)
```

---

<a id="file-src-data-connectors-okx-py"></a>
## File: `src\data\connectors\okx.py`


```python
"""OKX market-data connector."""

from __future__ import annotations

from src.data.connectors.alt_exchange import AltExchangeConnector


class OKXConnector(AltExchangeConnector):
    def __init__(self, timeout: int = 15) -> None:
        super().__init__("OKX", timeout=timeout)
```

---

<a id="file-src-data-data_hub-py"></a>
## File: `src\data\data_hub.py`


```python
"""Unified Bitcoin Data Hub — aggregates multi-source market intelligence."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any

import pandas as pd

from src.analysis.cross_exchange import build_cross_exchange_summary
from src.data.cache import TTLCache
from src.data.coinglass_client import CoinglassClient
from src.data.connectors import (
    BinanceConnector,
    BingXConnector,
    BitgetConnector,
    BybitConnector,
    CoinbaseConnector,
    KrakenConnector,
    MEXCConnector,
    OKXConnector,
)
from src.data.hub_models import HubSnapshot, SourceInfo
from src.data.news_sentiment import NewsSentimentProvider
from src.data.onchain import OnChainProvider
from src.data.fallback_market import fetch_fallback_klines, pick_fallback_price
from src.indicators.technical import parse_coinglass_heatmap

TRACKED_FIELDS = [
    "price",
    "candles",
    "volume",
    "order_book",
    "funding_rate",
    "open_interest",
    "long_short_ratio",
    "liquidations",
]

CRITICAL_FIELDS = ["price", "candles"]


class BitcoinDataHub:
    """Collects Bitcoin data from trusted sources with graceful degradation."""

    def __init__(
        self,
        *,
        symbol: str = "BTCUSDT",
        coinglass_api_key: str | None = None,
        timeout: int = 15,
        cache_ttl: int = 60,
    ) -> None:
        self.symbol = symbol
        self.timeout = timeout
        self.cache = TTLCache(default_ttl=cache_ttl)
        self.binance = BinanceConnector(symbol=symbol, timeout=timeout)
        self.coinglass = CoinglassClient(api_key=coinglass_api_key, timeout=timeout)
        self.onchain = OnChainProvider()
        self.news_sentiment = NewsSentimentProvider()
        self.alt_connectors = [
            BingXConnector(timeout=timeout),
            BybitConnector(timeout=timeout),
            OKXConnector(timeout=timeout),
            BitgetConnector(timeout=timeout),
            MEXCConnector(timeout=timeout),
            CoinbaseConnector(timeout=timeout),
            KrakenConnector(timeout=timeout),
        ]

    def fetch(self, *, interval: str = "1h", limit: int = 500, use_cache: bool = True) -> HubSnapshot:
        cache_key = f"{self.symbol}:{interval}:{limit}"
        if use_cache:
            cached = self.cache.get(cache_key)
            if isinstance(cached, HubSnapshot):
                return cached

        snapshot = HubSnapshot(last_updated=datetime.now(timezone.utc))
        self._fetch_binance(snapshot, interval=interval, limit=limit)
        self._fetch_coinglass(snapshot, interval=interval)
        self._fetch_alt_exchanges(snapshot)
        self._apply_market_fallback(snapshot, interval=interval, limit=limit)
        self._fetch_onchain(snapshot)
        self._fetch_news_sentiment(snapshot)
        self._finalize_snapshot(snapshot)

        if use_cache:
            self.cache.set(cache_key, snapshot, ttl=self.cache._default_ttl)
        return snapshot

    def _fetch_binance(self, snapshot: HubSnapshot, *, interval: str, limit: int) -> None:
        probe = self.binance.probe()
        snapshot.source_status[self.binance.name] = probe

        try:
            bundle = self.binance.fetch_market_bundle(interval=interval, limit=limit)
        except Exception as exc:
            snapshot.source_status[self.binance.name] = SourceInfo(
                name=self.binance.name,
                status="offline",
                error=str(exc),
            )
            return

        snapshot.price = bundle.get("price")
        snapshot.candles = bundle.get("candles")
        snapshot.volume = bundle.get("volume")
        snapshot.order_book = bundle.get("order_book")
        snapshot.funding_rate = bundle.get("funding_rate")
        snapshot.open_interest = bundle.get("open_interest")
        snapshot.long_short_ratio = bundle.get("long_short_ratio")

        errors = bundle.get("errors") or []
        status: str = "online"
        if errors and snapshot.price is not None:
            status = "degraded"
        elif snapshot.price is None:
            status = "offline"

        snapshot.source_status[self.binance.name] = SourceInfo(
            name=self.binance.name,
            status=status,  # type: ignore[arg-type]
            last_updated=datetime.now(timezone.utc) if snapshot.price is not None else None,
            error="; ".join(errors) if errors else None,
            fields=[field for field in TRACKED_FIELDS if getattr(snapshot, field, None) is not None],
        )
        if snapshot.price is not None and self.binance.name not in snapshot.sources:
            snapshot.sources.append(self.binance.name)

    def _fetch_coinglass(self, snapshot: HubSnapshot, *, interval: str) -> None:
        if not self.coinglass.enabled:
            snapshot.source_status["Coinglass"] = SourceInfo(
                name="Coinglass",
                status="offline",
                error="API key not configured",
                fields=[],
            )
            return

        errors: list[str] = []
        fields: list[str] = []
        liquidation_payload: dict[str, Any] = {"heatmap": None, "source": "Coinglass"}

        try:
            oi_hist = self.coinglass.get_open_interest_history(interval=interval)
            if oi_hist is not None and len(oi_hist) >= 2 and "close" in oi_hist.columns:
                latest_oi = oi_hist.iloc[-1]["close"]
                prev_oi = oi_hist.iloc[-2]["close"]
                snapshot.open_interest = float(latest_oi)
                fields.append("open_interest")
                if prev_oi:
                    snapshot.open_interest_change_pct = ((latest_oi - prev_oi) / prev_oi) * 100
                    fields.append("open_interest_change_pct")
        except Exception as exc:
            errors.append(f"open_interest: {exc}")

        try:
            cg_funding = self.coinglass.get_funding_rates()
            if cg_funding:
                preferred = {"Binance", "Bybit", "OKX", "BingX", "Bitget", "MEXC"}
                rates: list[float] = []
                for entry in cg_funding:
                    exchange = str(entry.get("exchange") or "")
                    rate = entry.get("funding_rate")
                    if exchange in preferred and rate is not None:
                        rates.append(float(rate))
                if rates:
                    snapshot.funding_rate = sum(rates) / len(rates)
                    fields.append("funding_rate")
                else:
                    for entry in cg_funding:
                        if entry.get("exchange") == "Binance":
                            snapshot.funding_rate = float(entry.get("funding_rate", snapshot.funding_rate or 0))
                            fields.append("funding_rate")
                            break
        except Exception as exc:
            errors.append(f"funding_rate: {exc}")

        try:
            cg_ls = self.coinglass.get_long_short_ratio_history(interval=interval, limit=2)
            if cg_ls is not None and not cg_ls.empty and "longShortRatio" in cg_ls.columns:
                snapshot.long_short_ratio = float(cg_ls.iloc[-1]["longShortRatio"])
                fields.append("long_short_ratio")
        except Exception as exc:
            errors.append(f"long_short_ratio: {exc}")

        try:
            raw_heatmap = self.coinglass.get_liquidation_heatmap()
            parsed = parse_coinglass_heatmap(raw_heatmap, snapshot.price or 0.0)
            liquidation_payload["heatmap_rows"] = 0 if parsed is None else len(parsed)
            liquidation_payload["heatmap"] = "available" if parsed is not None else None
            snapshot.liquidations = liquidation_payload
            if parsed is not None:
                fields.append("liquidations")
        except Exception as exc:
            errors.append(f"liquidations: {exc}")
            snapshot.liquidations = liquidation_payload

        status = "online" if fields else "degraded"
        if errors and not fields:
            status = "offline"

        snapshot.source_status["Coinglass"] = SourceInfo(
            name="Coinglass",
            status=status,  # type: ignore[arg-type]
            last_updated=datetime.now(timezone.utc) if fields else None,
            error="; ".join(errors) if errors else None,
            fields=fields,
        )
        if fields and "Coinglass" not in snapshot.sources:
            snapshot.sources.append("Coinglass")

    def _fetch_alt_exchanges(self, snapshot: HubSnapshot) -> None:
        # Performance: query alternative exchanges in parallel instead of sequentially.
        def _load_connector(connector):
            try:
                bundle = connector.fetch_market_bundle()
                return connector, bundle, None
            except Exception as exc:
                return connector, None, exc

        max_workers = min(8, max(1, len(self.alt_connectors)))
        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="hub-alt") as pool:
            futures = [pool.submit(_load_connector, connector) for connector in self.alt_connectors]
            for future in as_completed(futures):
                connector, bundle, error = future.result()
                if error is not None or bundle is None:
                    snapshot.source_status[connector.name] = SourceInfo(
                        name=connector.name,
                        status="offline",
                        error=str(error),
                    )
                    continue

                snapshot.exchange_snapshots[connector.name] = {
                    "price": bundle.get("price"),
                    "funding_rate": bundle.get("funding_rate"),
                    "open_interest": bundle.get("open_interest"),
                    "errors": bundle.get("errors") or [],
                }

                errors = bundle.get("errors") or []
                fields = [
                    field
                    for field in ("price", "funding_rate", "open_interest")
                    if bundle.get(field) is not None
                ]
                if bundle.get("price") is None:
                    status = "offline"
                elif errors:
                    status = "degraded"
                else:
                    status = "online"

                snapshot.source_status[connector.name] = SourceInfo(
                    name=connector.name,
                    status=status,  # type: ignore[arg-type]
                    last_updated=datetime.now(timezone.utc) if bundle.get("price") is not None else None,
                    error="; ".join(errors) if errors else None,
                    fields=fields,
                )
                if bundle.get("price") is not None and connector.name not in snapshot.sources:
                    snapshot.sources.append(connector.name)

        snapshot.cross_exchange = build_cross_exchange_summary(
            snapshot.exchange_snapshots,
            reference_price=float(snapshot.price or 0),
        )

    def _apply_market_fallback(self, snapshot: HubSnapshot, *, interval: str, limit: int) -> None:
        """Backfill price/candles from alt exchanges when Binance is blocked on cloud hosts."""
        needs_price = snapshot.price is None or float(snapshot.price or 0) <= 0
        candles = snapshot.candles
        needs_candles = candles is None or (isinstance(candles, pd.DataFrame) and candles.empty)
        if not needs_price and not needs_candles:
            return

        if needs_price:
            price, source = pick_fallback_price(snapshot.exchange_snapshots)
            if price is not None:
                snapshot.price = price
                if source and source not in snapshot.sources:
                    snapshot.sources.append(source)

        if needs_candles:
            df, source = fetch_fallback_klines(interval=interval, limit=limit, timeout=float(self.timeout))
            if df is not None and not df.empty:
                snapshot.candles = df
                snapshot.volume = float(df.iloc[-1]["volume"])
                if snapshot.price is None or float(snapshot.price or 0) <= 0:
                    snapshot.price = float(df.iloc[-1]["close"])
                if source:
                    if source not in snapshot.sources:
                        snapshot.sources.append(source)
                    snapshot.source_status[source] = SourceInfo(
                        name=source,
                        status="online",
                        last_updated=datetime.now(timezone.utc),
                        error="Candle fallback — Binance unreachable from this host",
                        fields=["price", "candles", "volume"],
                    )

        if needs_price and snapshot.price is not None and float(snapshot.price) > 0:
            binance_info = snapshot.source_status.get(self.binance.name)
            if binance_info and binance_info.status == "offline":
                snapshot.source_status[self.binance.name] = SourceInfo(
                    name=self.binance.name,
                    status="offline",
                    last_updated=binance_info.last_updated,
                    error=(binance_info.error or "Unreachable") + " — using alt-exchange fallback",
                    fields=binance_info.fields,
                )

    def _fetch_onchain(self, snapshot: HubSnapshot) -> None:
        try:
            payload, info = self.onchain.fetch()
            snapshot.onchain = payload
            snapshot.source_status[info.name] = info
        except Exception as exc:
            snapshot.onchain = {}
            snapshot.source_status["On-Chain"] = SourceInfo(
                name="On-Chain",
                status="offline",
                error=str(exc),
            )

    def _fetch_news_sentiment(self, snapshot: HubSnapshot) -> None:
        try:
            news, sentiment, info = self.news_sentiment.fetch()
            snapshot.news = news
            snapshot.sentiment = sentiment
            snapshot.source_status[info.name] = info
        except Exception as exc:
            snapshot.news = {}
            snapshot.sentiment = {}
            snapshot.source_status["News & Sentiment"] = SourceInfo(
                name="News & Sentiment",
                status="offline",
                error=str(exc),
            )

    def _finalize_snapshot(self, snapshot: HubSnapshot) -> None:
        available: list[str] = []
        missing: list[str] = []

        for field in TRACKED_FIELDS:
            value = getattr(snapshot, field, None)
            if field == "candles":
                ok = isinstance(value, pd.DataFrame) and not value.empty
            elif field == "liquidations":
                ok = isinstance(value, dict) and value.get("heatmap") == "available"
            else:
                ok = value is not None
            if ok:
                available.append(field)
            else:
                missing.append(field)

        snapshot.available_fields = available
        snapshot.missing_fields = missing
        snapshot.critical_missing = any(field in missing for field in CRITICAL_FIELDS)
        snapshot.force_wait = snapshot.critical_missing

        if snapshot.critical_missing:
            snapshot.data_quality = "critical"
            snapshot.confidence_impact = "critical — WAIT recommended"
        elif len(missing) >= 4:
            snapshot.data_quality = "partial"
            snapshot.confidence_impact = "high — confidence reduced"
        elif missing:
            snapshot.data_quality = "partial"
            snapshot.confidence_impact = "moderate — some inputs missing"
        else:
            snapshot.data_quality = "full"
            snapshot.confidence_impact = "none"

        snapshot.last_updated = datetime.now(timezone.utc)
```

---

<a id="file-src-data-exchange_api-py"></a>
## File: `src\data\exchange_api.py`


```python
"""Public REST fetchers for multi-exchange BTC market data."""

from __future__ import annotations

from typing import Any, Callable

import requests

Bundle = dict[str, Any]


def _empty_bundle() -> Bundle:
    return {
        "price": None,
        "funding_rate": None,
        "open_interest": None,
        "candles": None,
        "volume": None,
        "errors": [],
    }


def _get_json(url: str, *, params: dict | None = None, timeout: int = 15) -> Any:
    response = requests.get(url, params=params or {}, timeout=timeout)
    response.raise_for_status()
    return response.json()


def _run(label: str, fn: Callable[[], Any], bundle: Bundle) -> Any:
    try:
        return fn()
    except Exception as exc:
        bundle["errors"].append(f"{label}: {exc}")
        return None


def fetch_bybit(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://api.bybit.com/v5/market/tickers",
            params={"category": "linear", "symbol": "BTCUSDT"},
            timeout=timeout,
        )
        row = (data.get("result") or {}).get("list") or [{}]
        item = row[0]
        bundle["funding_rate"] = float(item.get("fundingRate") or 0)
        return float(item["lastPrice"])

    def _oi() -> float:
        data = _get_json(
            "https://api.bybit.com/v5/market/open-interest",
            params={"category": "linear", "symbol": "BTCUSDT", "intervalTime": "1h", "limit": 1},
            timeout=timeout,
        )
        row = (data.get("result") or {}).get("list") or [{}]
        return float(row[0].get("openInterest") or 0)

    bundle["price"] = _run("price", _price, bundle)
    bundle["open_interest"] = _run("open_interest", _oi, bundle)
    return bundle


def fetch_okx(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://www.okx.com/api/v5/market/ticker",
            params={"instId": "BTC-USDT"},
            timeout=timeout,
        )
        row = (data.get("data") or [{}])[0]
        return float(row["last"])

    def _funding() -> float:
        data = _get_json(
            "https://www.okx.com/api/v5/public/funding-rate",
            params={"instId": "BTC-USDT-SWAP"},
            timeout=timeout,
        )
        row = (data.get("data") or [{}])[0]
        return float(row.get("fundingRate") or 0)

    def _oi() -> float:
        data = _get_json(
            "https://www.okx.com/api/v5/public/open-interest",
            params={"instId": "BTC-USDT-SWAP"},
            timeout=timeout,
        )
        row = (data.get("data") or [{}])[0]
        return float(row.get("oi") or 0)

    bundle["price"] = _run("price", _price, bundle)
    bundle["funding_rate"] = _run("funding_rate", _funding, bundle)
    bundle["open_interest"] = _run("open_interest", _oi, bundle)
    return bundle


def fetch_bingx(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://open-api.bingx.com/openApi/swap/v2/quote/ticker",
            params={"symbol": "BTC-USDT"},
            timeout=timeout,
        )
        payload = data.get("data") or {}
        if bundle.get("funding_rate") is None and payload.get("lastFundingRate") is not None:
            bundle["funding_rate"] = float(payload["lastFundingRate"])
        return float(payload["lastPrice"])

    def _funding() -> float:
        data = _get_json(
            "https://open-api.bingx.com/openApi/swap/v2/quote/premiumIndex",
            params={"symbol": "BTC-USDT"},
            timeout=timeout,
        )
        payload = data.get("data") or {}
        return float(payload.get("lastFundingRate") or 0)

    bundle["price"] = _run("price", _price, bundle)
    if bundle["funding_rate"] is None:
        bundle["funding_rate"] = _run("funding_rate", _funding, bundle)
    return bundle


def fetch_bitget(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://api.bitget.com/api/v2/mix/market/ticker",
            params={"symbol": "BTCUSDT", "productType": "USDT-FUTURES"},
            timeout=timeout,
        )
        row = (data.get("data") or [{}])[0]
        if row.get("fundingRate") is not None:
            bundle["funding_rate"] = float(row["fundingRate"])
        return float(row["lastPr"])

    def _oi() -> float:
        data = _get_json(
            "https://api.bitget.com/api/v2/mix/market/open-interest",
            params={"symbol": "BTCUSDT", "productType": "USDT-FUTURES"},
            timeout=timeout,
        )
        row = (data.get("data") or [{}])[0]
        return float(row.get("openInterest") or row.get("size") or 0)

    bundle["price"] = _run("price", _price, bundle)
    bundle["open_interest"] = _run("open_interest", _oi, bundle)
    return bundle


def fetch_mexc(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://contract.mexc.com/api/v1/contract/ticker",
            params={"symbol": "BTC_USDT"},
            timeout=timeout,
        )
        payload = data.get("data") or {}
        if payload.get("fundingRate") is not None:
            bundle["funding_rate"] = float(payload["fundingRate"])
        return float(payload["lastPrice"])

    bundle["price"] = _run("price", _price, bundle)
    return bundle


def fetch_coinbase(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
            timeout=timeout,
        )
        return float(data["price"])

    bundle["price"] = _run("price", _price, bundle)
    return bundle


def fetch_kraken(*, timeout: int = 15) -> Bundle:
    bundle = _empty_bundle()

    def _price() -> float:
        data = _get_json(
            "https://api.kraken.com/0/public/Ticker",
            params={"pair": "XBTUSD"},
            timeout=timeout,
        )
        pair = (data.get("result") or {}).get("XXBTZUSD") or {}
        last = pair.get("c") or [None]
        return float(last[0])

    bundle["price"] = _run("price", _price, bundle)
    return bundle


EXCHANGE_FETCHERS: dict[str, Callable[..., Bundle]] = {
    "Bybit": fetch_bybit,
    "OKX": fetch_okx,
    "BingX": fetch_bingx,
    "Bitget": fetch_bitget,
    "MEXC": fetch_mexc,
    "Coinbase": fetch_coinbase,
    "Kraken": fetch_kraken,
}
```

---

<a id="file-src-data-fallback_market-py"></a>
## File: `src\data\fallback_market.py`


```python
"""Fallback market data when Binance is unreachable (common on cloud hosts)."""

from __future__ import annotations

from typing import Any

import pandas as pd
import requests

_BYBIT_INTERVALS = {
    "1m": "1",
    "3m": "3",
    "5m": "5",
    "15m": "15",
    "30m": "30",
    "1h": "60",
    "4h": "240",
    "1d": "D",
}

_OKX_BARS = {
    "1m": "1m",
    "3m": "3m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1H",
    "4h": "4H",
    "1d": "1D",
}


def _klines_dataframe(rows: list[list[Any]]) -> pd.DataFrame:
    df = pd.DataFrame(
        rows,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "quote_volume",
        ],
    )
    numeric_cols = ["open", "high", "low", "close", "volume", "quote_volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df["close_time"] = df["open_time"]
    df["trades"] = 0
    df["taker_buy_base"] = 0.0
    df["taker_buy_quote"] = 0.0
    df["ignore"] = 0
    return df


def _fetch_bybit_klines(*, interval: str, limit: int, timeout: float) -> pd.DataFrame | None:
    bybit_interval = _BYBIT_INTERVALS.get(interval)
    if not bybit_interval:
        return None

    response = requests.get(
        "https://api.bybit.com/v5/market/kline",
        params={
            "category": "spot",
            "symbol": "BTCUSDT",
            "interval": bybit_interval,
            "limit": min(limit, 1000),
        },
        timeout=timeout,
    )
    response.raise_for_status()
    raw = (response.json().get("result") or {}).get("list") or []
    if not raw:
        return None

    rows = [
        [
            int(row[0]),
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6] if len(row) > 6 else row[5],
        ]
        for row in reversed(raw)
    ]
    return _klines_dataframe(rows)


def _fetch_okx_klines(*, interval: str, limit: int, timeout: float) -> pd.DataFrame | None:
    bar = _OKX_BARS.get(interval)
    if not bar:
        return None

    response = requests.get(
        "https://www.okx.com/api/v5/market/candles",
        params={"instId": "BTC-USDT", "bar": bar, "limit": min(limit, 300)},
        timeout=timeout,
    )
    response.raise_for_status()
    raw = response.json().get("data") or []
    if not raw:
        return None

    rows = [
        [
            int(row[0]),
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6] if len(row) > 6 else row[5],
        ]
        for row in reversed(raw)
    ]
    return _klines_dataframe(rows)


def fetch_fallback_klines(
    *,
    interval: str = "1m",
    limit: int = 500,
    timeout: float = 15.0,
) -> tuple[pd.DataFrame | None, str | None]:
    """Try Bybit then OKX for OHLCV when Binance is blocked."""
    for name, fetcher in (("Bybit", _fetch_bybit_klines), ("OKX", _fetch_okx_klines)):
        try:
            df = fetcher(interval=interval, limit=limit, timeout=timeout)
            if df is not None and not df.empty:
                return df, name
        except Exception:
            continue
    return None, None


def pick_fallback_price(exchange_snapshots: dict[str, dict[str, Any]]) -> tuple[float | None, str | None]:
    """Use the first live alt-exchange price when Binance price is missing."""
    for name, snap in exchange_snapshots.items():
        price = snap.get("price")
        if price is not None and float(price) > 0:
            return float(price), name
    return None, None
```

---

<a id="file-src-data-fear_greed-py"></a>
## File: `src\data\fear_greed.py`


```python
"""Fear & Greed Index client (Alternative.me)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import requests

from src.data.hub_models import SourceInfo

FNG_URL = "https://api.alternative.me/fng/"


class FearGreedClient:
    name = "Fear & Greed"

    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout

    def fetch(self, limit: int = 1) -> tuple[dict[str, Any], SourceInfo]:
        try:
            response = requests.get(
                FNG_URL,
                params={"limit": limit, "format": "json"},
                timeout=self.timeout,
            )
            response.raise_for_status()
            payload = response.json()
            entries = payload.get("data") or []
            if not entries:
                raise ValueError("Empty Fear & Greed response")

            latest = entries[0]
            value = int(latest.get("value", 0))
            classification = str(latest.get("value_classification", "Unknown"))
            timestamp = latest.get("timestamp")

            data = {
                "status": "online",
                "value": value,
                "classification": classification,
                "timestamp": timestamp,
                "provider": "Alternative.me",
            }
            info = SourceInfo(
                name=self.name,
                status="online",
                last_updated=datetime.now(timezone.utc),
                fields=["fear_greed_index"],
            )
            return data, info
        except Exception as exc:
            data = {
                "status": "offline",
                "value": None,
                "classification": None,
                "provider": "Alternative.me",
                "error": str(exc),
            }
            info = SourceInfo(
                name=self.name,
                status="offline",
                last_updated=datetime.now(timezone.utc),
                error=str(exc),
                fields=["fear_greed_index"],
            )
            return data, info
```

---

<a id="file-src-data-feed_cache-py"></a>
## File: `src\data\feed_cache.py`


```python
"""TTL cache + parallel fetch for slow enrichment feeds (Fear/Greed, news, on-chain, whales)."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, TypeVar

from src.data.cache import TTLCache
from src.data.fear_greed import FearGreedClient
from src.data.hub_models import SourceInfo
from src.data.news_client import NewsClient
from src.data.onchain_client import OnChainClient
from src.data.whale_client import WhaleClient

T = TypeVar("T")

# Shared process cache — avoids duplicate HTTP calls between Streamlit reruns.
_ENRICHMENT_CACHE = TTLCache(default_ttl=120)

# Slower-moving feeds can stay cached longer than the 60s market refresh.
_FEED_TTLS: dict[str, int] = {
    "fear_greed": 300,
    "news": 180,
    "onchain": 600,
    "whale": 600,
}


def _cached_feed(name: str, fetcher: Callable[[], T]) -> T:
    """Return a cached feed payload or fetch and store it with a feed-specific TTL."""
    cached = _ENRICHMENT_CACHE.get(name)
    if cached is not None:
        return cached
    value = fetcher()
    _ENRICHMENT_CACHE.set(name, value, ttl=_FEED_TTLS.get(name, 120))
    return value


def _fetch_fear_greed() -> tuple[dict[str, Any], SourceInfo]:
    return FearGreedClient().fetch()


def _fetch_news() -> tuple[dict[str, Any], SourceInfo]:
    return NewsClient().fetch()


def _fetch_onchain() -> tuple[dict[str, Any], SourceInfo]:
    return OnChainClient().fetch()


def _fetch_whale() -> tuple[dict[str, Any], SourceInfo]:
    return WhaleClient().fetch()


def _safe_feed(
    name: str,
    fetcher: Callable[[], tuple[dict[str, Any], SourceInfo]],
) -> tuple[dict[str, Any], SourceInfo | None, Exception | None]:
    try:
        data, info = _cached_feed(name, fetcher)
        return data, info, None
    except Exception as exc:
        return {}, None, exc


def fetch_enrichment_feeds_parallel() -> dict[str, Any]:
    """Load all enrichment feeds concurrently; one failure does not block the others."""
    jobs = {
        "fear_greed": _fetch_fear_greed,
        "news": _fetch_news,
        "onchain": _fetch_onchain,
        "whale": _fetch_whale,
    }
    results: dict[str, Any] = {
        "fear_data": {},
        "fear_info": None,
        "news_data": {},
        "news_info": None,
        "onchain_data": {},
        "onchain_info": None,
        "whale_data": {},
        "whale_info": None,
        "errors": [],
    }

    with ThreadPoolExecutor(max_workers=4, thread_name_prefix="enrich") as pool:
        future_map = {
            pool.submit(_safe_feed, name, fetcher): name for name, fetcher in jobs.items()
        }
        for future in as_completed(future_map):
            name = future_map[future]
            data, info, error = future.result()
            if name == "fear_greed":
                results["fear_data"] = data
                results["fear_info"] = info
            elif name == "news":
                results["news_data"] = data
                results["news_info"] = info
            elif name == "onchain":
                results["onchain_data"] = data
                results["onchain_info"] = info
            elif name == "whale":
                results["whale_data"] = data
                results["whale_info"] = info
            if error is not None:
                results["errors"].append(f"{name}: {error}")

    return results
```

---

<a id="file-src-data-hub_models-py"></a>
## File: `src\data\hub_models.py`


```python
"""Data structures for the unified Bitcoin Data Hub."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

import pandas as pd

SourceStatus = Literal["online", "offline", "degraded", "placeholder"]


@dataclass
class SourceInfo:
    name: str
    status: SourceStatus
    last_updated: datetime | None = None
    error: str | None = None
    fields: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "error": self.error,
            "fields": self.fields,
        }


@dataclass
class HubSnapshot:
    price: float | None = None
    candles: pd.DataFrame | None = None
    volume: float | None = None
    order_book: dict[str, Any] | None = None
    funding_rate: float | None = None
    open_interest: float | None = None
    open_interest_change_pct: float | None = None
    long_short_ratio: float | None = None
    liquidations: dict[str, Any] | None = None
    onchain: dict[str, Any] = field(default_factory=dict)
    news: dict[str, Any] = field(default_factory=dict)
    sentiment: dict[str, Any] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)
    source_status: dict[str, SourceInfo] = field(default_factory=dict)
    last_updated: datetime | None = None
    missing_fields: list[str] = field(default_factory=list)
    available_fields: list[str] = field(default_factory=list)
    data_quality: str = "partial"
    confidence_impact: str = "none"
    critical_missing: bool = False
    force_wait: bool = False
    exchange_snapshots: dict[str, dict[str, Any]] = field(default_factory=dict)
    cross_exchange: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "price": self.price,
            "candles": None if self.candles is None else f"{len(self.candles)} rows",
            "volume": self.volume,
            "order_book": self.order_book,
            "funding_rate": self.funding_rate,
            "open_interest": self.open_interest,
            "open_interest_change_pct": self.open_interest_change_pct,
            "long_short_ratio": self.long_short_ratio,
            "liquidations": self.liquidations,
            "onchain": self.onchain,
            "news": self.news,
            "sentiment": self.sentiment,
            "sources": self.sources,
            "source_status": {k: v.to_dict() for k, v in self.source_status.items()},
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "missing_fields": self.missing_fields,
            "available_fields": self.available_fields,
            "data_quality": self.data_quality,
            "confidence_impact": self.confidence_impact,
            "critical_missing": self.critical_missing,
            "force_wait": self.force_wait,
            "exchange_snapshots": self.exchange_snapshots,
            "cross_exchange": self.cross_exchange,
        }
```

---

<a id="file-src-data-news_client-py"></a>
## File: `src\data\news_client.py`


```python
"""Crypto news RSS client with simple headline sentiment."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

try:
    import feedparser
except ImportError:
    feedparser = None

from src.analysis.sentiment import analyze_headline_sentiment, summarize_sentiment
from src.data.hub_models import SourceInfo

RSS_FEEDS: dict[str, str] = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "Cointelegraph": "https://cointelegraph.com/rss",
    "Bitcoin Magazine": "https://bitcoinmagazine.com/.rss/full/",
}


class NewsClient:
    name = "News RSS"

    def __init__(self, timeout: float = 12.0, max_items: int = 15) -> None:
        self.timeout = timeout
        self.max_items = max_items

    def fetch(self) -> tuple[dict[str, Any], SourceInfo]:
        headlines: list[dict[str, Any]] = []
        errors: list[str] = []

        if feedparser is None:
            data = {
                "status": "offline",
                "headlines": [],
                "summary": summarize_sentiment([]),
                "error": "feedparser not installed",
            }
            info = SourceInfo(
                name=self.name,
                status="offline",
                last_updated=datetime.now(timezone.utc),
                error="feedparser not installed",
                fields=["headlines", "sentiment"],
            )
            return data, info

        for source, url in RSS_FEEDS.items():
            try:
                parsed = feedparser.parse(url, request_headers={"User-Agent": "btc-market-analyzer/1.0"})
                for entry in (parsed.entries or [])[: self.max_items // len(RSS_FEEDS) + 3]:
                    title = str(getattr(entry, "title", "") or "").strip()
                    if not title:
                        continue
                    sentiment = analyze_headline_sentiment(title)
                    headlines.append(
                        {
                            "source": source,
                            "title": title,
                            "link": getattr(entry, "link", ""),
                            "sentiment": sentiment,
                        }
                    )
            except Exception as exc:
                errors.append(f"{source}: {exc}")

        headlines = headlines[: self.max_items]
        summary = summarize_sentiment(headlines)

        if headlines:
            status = "online"
            source_status = "online"
            error = "; ".join(errors) if errors else None
        else:
            status = "offline"
            source_status = "offline"
            error = "; ".join(errors) if errors else "No headlines fetched"

        data = {
            "status": status,
            "headlines": headlines,
            "summary": summary,
            "feeds": list(RSS_FEEDS.keys()),
            "error": error,
        }
        info = SourceInfo(
            name=self.name,
            status=source_status,
            last_updated=datetime.now(timezone.utc),
            error=error if source_status != "online" else None,
            fields=["headlines", "sentiment"],
        )
        return data, info
```

---

<a id="file-src-data-news_sentiment-py"></a>
## File: `src\data\news_sentiment.py`


```python
"""News and sentiment placeholders for future API integrations."""

from __future__ import annotations

from datetime import datetime, timezone

from src.data.hub_models import SourceInfo


class NewsSentimentProvider:
    name = "News & Sentiment"

    def fetch(self) -> tuple[dict, dict, SourceInfo]:
        news = {
            "headlines": {"status": "placeholder", "items": [], "provider": "future crypto news API"},
            "macro_events": {"status": "placeholder", "items": [], "provider": "future macro calendar API"},
        }
        sentiment = {
            "fear_greed_index": {"status": "placeholder", "value": None, "provider": "future Fear & Greed API"},
            "social_sentiment": {"status": "placeholder", "value": None, "provider": "future social sentiment API"},
        }
        info = SourceInfo(
            name=self.name,
            status="placeholder",
            last_updated=datetime.now(timezone.utc),
            error="News and sentiment APIs not yet connected",
            fields=["headlines", "macro_events", "fear_greed_index", "social_sentiment"],
        )
        return news, sentiment, info
```

---

<a id="file-src-data-onchain-py"></a>
## File: `src\data\onchain.py`


```python
"""On-chain data placeholders for future API integrations."""

from __future__ import annotations

from datetime import datetime, timezone

from src.data.hub_models import SourceInfo


class OnChainProvider:
    name = "On-Chain"

    def fetch(self) -> tuple[dict, SourceInfo]:
        payload = {
            "exchange_inflows": {"status": "placeholder", "value": None, "provider": "future API"},
            "exchange_outflows": {"status": "placeholder", "value": None, "provider": "future API"},
            "whale_transactions": {"status": "placeholder", "value": None, "provider": "future API"},
            "active_addresses": {"status": "placeholder", "value": None, "provider": "future API"},
            "miner_flows": {"status": "placeholder", "value": None, "provider": "future API"},
            "stablecoin_flows": {"status": "placeholder", "value": None, "provider": "future API"},
        }
        info = SourceInfo(
            name=self.name,
            status="placeholder",
            last_updated=datetime.now(timezone.utc),
            error="On-chain APIs not yet connected",
            fields=list(payload.keys()),
        )
        return payload, info
```

---

<a id="file-src-data-onchain_client-py"></a>
## File: `src\data\onchain_client.py`


```python
"""On-chain data client with optional API key providers."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

from src.data.hub_models import SourceInfo

SUPPORTED_PROVIDERS = ("Glassnode", "CryptoQuant", "Arkham")


class OnChainClient:
    name = "On-Chain"

    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout
        self.glassnode_key = os.getenv("GLASSNODE_API_KEY", "").strip()
        self.cryptoquant_key = os.getenv("CRYPTOQUANT_API_KEY", "").strip()
        self.arkham_key = os.getenv("ARKHAM_API_KEY", "").strip()

    def fetch(self) -> tuple[dict[str, Any], SourceInfo]:
        payload: dict[str, Any] = {
            "exchange_inflows": self._field("Glassnode", self.glassnode_key),
            "exchange_outflows": self._field("Glassnode", self.glassnode_key),
            "active_addresses": self._field("Glassnode", self.glassnode_key),
            "miner_flows": self._field("CryptoQuant", self.cryptoquant_key),
            "stablecoin_flows": self._field("CryptoQuant", self.cryptoquant_key),
            "entity_labels": self._field("Arkham", self.arkham_key),
        }

        has_key = any([self.glassnode_key, self.cryptoquant_key, self.arkham_key])
        if has_key:
            payload = self._try_fetch_live(payload)

        if has_key and any(v.get("status") == "online" for v in payload.values()):
            status = "online"
            error = None
        elif has_key:
            status = "offline"
            error = "API keys present but live on-chain fetch failed or unsupported"
        else:
            status = "placeholder"
            error = "Unavailable — add API key (GLASSNODE_API_KEY, CRYPTOQUANT_API_KEY, ARKHAM_API_KEY)"

        info = SourceInfo(
            name=self.name,
            status=status,
            last_updated=datetime.now(timezone.utc),
            error=error,
            fields=list(payload.keys()),
        )
        return payload, info

    @staticmethod
    def _field(provider: str, api_key: str) -> dict[str, Any]:
        if not api_key:
            return {
                "status": "unavailable",
                "value": None,
                "provider": provider,
                "message": "Unavailable — add API key",
            }
        return {
            "status": "pending",
            "value": None,
            "provider": provider,
            "message": f"{provider} key detected — live endpoint not wired yet",
        }

    def _try_fetch_live(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self.glassnode_key:
            try:
                response = requests.get(
                    "https://api.glassnode.com/v1/metrics/addresses/active_count",
                    params={"a": "BTC", "api_key": self.glassnode_key, "i": "24h"},
                    timeout=self.timeout,
                )
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        payload["active_addresses"] = {
                            "status": "online",
                            "value": data[-1].get("v"),
                            "provider": "Glassnode",
                        }
            except Exception:
                pass
        return payload
```

---

<a id="file-src-data-whale_client-py"></a>
## File: `src\data\whale_client.py`


```python
"""Whale activity client with optional API key providers."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from src.data.hub_models import SourceInfo

SUPPORTED_PROVIDERS = ("Whale Alert", "Glassnode", "CryptoQuant", "Arkham")


class WhaleClient:
    name = "Whale Data"

    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout
        self.whale_alert_key = os.getenv("WHALE_ALERT_API_KEY", "").strip()
        self.glassnode_key = os.getenv("GLASSNODE_API_KEY", "").strip()
        self.cryptoquant_key = os.getenv("CRYPTOQUANT_API_KEY", "").strip()
        self.arkham_key = os.getenv("ARKHAM_API_KEY", "").strip()

    def fetch(self) -> tuple[dict[str, Any], SourceInfo]:
        payload = {
            "large_transfers": self._provider_block("Whale Alert", self.whale_alert_key),
            "exchange_whale_inflow": self._provider_block("CryptoQuant", self.cryptoquant_key),
            "exchange_whale_outflow": self._provider_block("CryptoQuant", self.cryptoquant_key),
            "labeled_wallets": self._provider_block("Arkham", self.arkham_key),
            "whale_accumulation": self._provider_block("Glassnode", self.glassnode_key),
        }

        has_key = any([self.whale_alert_key, self.glassnode_key, self.cryptoquant_key, self.arkham_key])
        if has_key:
            status = "placeholder"
            error = "API keys detected — whale endpoints prepared but not fully wired"
        else:
            status = "placeholder"
            error = "Unavailable — add API key (WHALE_ALERT_API_KEY, GLASSNODE_API_KEY, etc.)"

        info = SourceInfo(
            name=self.name,
            status=status,
            last_updated=datetime.now(timezone.utc),
            error=error,
            fields=list(payload.keys()),
        )
        return payload, info

    @staticmethod
    def _provider_block(provider: str, api_key: str) -> dict[str, Any]:
        if not api_key:
            return {
                "status": "unavailable",
                "value": None,
                "provider": provider,
                "message": "Unavailable — add API key",
            }
        return {
            "status": "pending",
            "value": None,
            "provider": provider,
            "message": f"{provider} key detected — awaiting live integration",
        }
```

---

<a id="file-src-indicators-__init__-py"></a>
## File: `src\indicators\__init__.py`


```python

```

---

<a id="file-src-indicators-technical-py"></a>
## File: `src\indicators\technical.py`


```python
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
```

---

<a id="file-src-ui-__init__-py"></a>
## File: `src\ui\__init__.py`


```python
"""UI layer public exports."""

from src.ui.components import (
    render_analyze_button,
    render_dashboard,
    render_empty_state,
    render_error_state,
    render_header_bar,
)
from src.ui.sidebar import SidebarSettings, render_sidebar
from src.ui.styles import inject_global_styles

__all__ = [
    "SidebarSettings",
    "inject_global_styles",
    "render_sidebar",
    "render_header_bar",
    "render_analyze_button",
    "render_empty_state",
    "render_error_state",
    "render_dashboard",
]
```

---

<a id="file-src-ui-auth-py"></a>
## File: `src\ui\auth.py`


```python
"""Password gate for dashboard access."""

from __future__ import annotations

import os
import secrets
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from src.ui.primitives import bitcoin_chart_logo, login_purchase_panel

ROOT = Path(__file__).resolve().parents[2]
_SESSION_KEY = "authenticated"


def is_authenticated() -> bool:
    return bool(st.session_state.get(_SESSION_KEY))


def _expected_password() -> str:
    load_dotenv(ROOT / ".env", override=True)
    return os.getenv("DASHBOARD_PASSWORD", "").strip()


def _render_html_block(html: str) -> None:
    """Render trusted HTML via markdown (st.html shows a white box with raw tags)."""
    st.markdown(html, unsafe_allow_html=True)


def _render_login_logo() -> None:
    """Large centered Bitcoin logo on the login screen."""
    _render_html_block(bitcoin_chart_logo(placement="login"))


def render_login_gate(*, project_root: Path) -> bool:
    """Show the entry password screen. Returns True when access is granted."""
    del project_root  # reserved for future branding assets

    if is_authenticated():
        return True

    expected = _expected_password()
    if not expected:
        st.error("Dashboard password is not configured. Set DASHBOARD_PASSWORD in your .env file.")
        return False

    _col_left, col_center, _col_right = st.columns([0.35, 3.3, 0.35])
    with col_center:
        _render_login_logo()

        with st.form("dashboard_login", clear_on_submit=False):
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Enter Dashboard", type="primary", use_container_width=True)

        if submitted:
            if secrets.compare_digest(password, expected):
                st.session_state[_SESSION_KEY] = True
                from src.ui.performance import clear_analysis_cache

                clear_analysis_cache()
                st.rerun()
            st.error("Incorrect password. Please try again.")

        _render_html_block(login_purchase_panel())

    return False
```

---

<a id="file-src-ui-background-py"></a>
## File: `src\ui\background.py`


```python
"""Local background image loading for custom page styling."""

from __future__ import annotations

import base64
from pathlib import Path

PRIMARY_BACKGROUND = "background.jpg"

BACKGROUND_FILENAMES = (
    "background.jpg",
    "background.jpeg",
    "background.png",
    "background.webp",
)

MIME_BY_SUFFIX = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}

# Warm Bitcoin-tinted overlay for readable text over the photo
OVERLAY_RGBA = "rgba(26, 17, 8, 0.52)"


def ensure_assets_dir(project_root: Path) -> Path:
    """Create the assets folder if it does not exist."""
    assets_dir = project_root / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    return assets_dir


def find_background_image(project_root: Path) -> Path | None:
    """Return assets/background.jpg if present, otherwise any supported image."""
    assets_dir = ensure_assets_dir(project_root)

    primary = assets_dir / PRIMARY_BACKGROUND
    if primary.is_file() and primary.stat().st_size > 0:
        return primary

    for name in BACKGROUND_FILENAMES:
        if name == PRIMARY_BACKGROUND:
            continue
        candidate = assets_dir / name
        if candidate.is_file() and candidate.stat().st_size > 0:
            return candidate
    return None


def _to_data_uri(image_path: Path) -> str | None:
    try:
        mime = MIME_BY_SUFFIX.get(image_path.suffix.lower(), "image/jpeg")
        encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{encoded}"
    except OSError:
        return None


def build_background_css(project_root: Path | None) -> tuple[str, bool]:
    """
    Build CSS for a fixed full-page background with dark overlay and glass cards.
    Returns (css_fragment, has_background). Safe when the image file is missing.
    """
    if project_root is None:
        return "", False

    image_path = find_background_image(project_root)
    if image_path is None:
        return "", False

    data_uri = _to_data_uri(image_path)
    if data_uri is None:
        return "", False

    css = f"""
        :root {{
            --glass-bg: rgba(42, 26, 14, 0.58);
            --glass-bg-hover: rgba(42, 26, 14, 0.72);
            --glass-border: rgba(247, 147, 26, 0.22);
            --glass-border-hover: rgba(247, 147, 26, 0.45);
            --glass-blur: 18px;
            --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.28);
            --glass-shadow-hover: 0 14px 40px rgba(247, 147, 26, 0.12);
            --surface: var(--glass-bg);
            --surface-alt: rgba(247, 147, 26, 0.08);
            --border: var(--glass-border);
            --bg: transparent;
        }}

        .stApp {{
            background-color: #1A1108;
            background-image:
                radial-gradient(ellipse 70% 45% at 50% -10%, rgba(247, 147, 26, 0.15), transparent),
                linear-gradient({OVERLAY_RGBA}, {OVERLAY_RGBA}),
                url("{data_uri}");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            font-family: var(--font);
            color: #f8fafc;
            overflow-x: clip;
        }}

        .block-container,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {{
            background: transparent !important;
        }}

        .card,
        .rec-panel,
        .state-panel,
        .card--prose,
        .safety-banner,
        .hub-source,
        .hub-summary,
        .hub-fields,
        .risk-alert,
        [data-testid="stExpander"],
        .brand-footer {{
            background: var(--glass-bg) !important;
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            border: 1px solid var(--glass-border) !important;
            box-shadow: var(--glass-shadow);
            transition: transform 0.22s ease, box-shadow 0.22s ease,
                        border-color 0.22s ease, background 0.22s ease;
        }}

        .card:hover,
        .rec-panel:hover,
        .state-panel--empty:hover,
        .hub-source:hover {{
            transform: translateY(-2px);
            box-shadow: var(--glass-shadow-hover);
            border-color: var(--glass-border-hover) !important;
            background: var(--glass-bg-hover) !important;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background: rgba(42, 26, 14, 0.78) !important;
            backdrop-filter: blur(var(--glass-blur));
            -webkit-backdrop-filter: blur(var(--glass-blur));
            border-right: 1px solid rgba(247, 147, 26, 0.18) !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            background: rgba(42, 26, 14, 0.42) !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: var(--radius-sm);
            padding: 0.25rem 0.375rem;
        }}

        @media (max-width: 768px) {{
            .stApp {{
                background-attachment: scroll;
            }}
        }}
    """
    return css, True


def build_bitcoin_fallback_css(*, dark_mode: bool = True) -> str:
    """Bitcoin-themed page background when no custom image is loaded."""
    if dark_mode:
        return """
        .stApp {
            background-color: #080604 !important;
            background-image:
                radial-gradient(ellipse 90% 55% at 50% -20%, rgba(247, 147, 26, 0.26), transparent),
                radial-gradient(ellipse 50% 45% at 100% 85%, rgba(242, 169, 0, 0.12), transparent),
                radial-gradient(ellipse 45% 35% at 0% 55%, rgba(247, 147, 26, 0.1), transparent),
                linear-gradient(180deg, #120c08 0%, #080604 42%, #0a0705 100%) !important;
            background-attachment: fixed;
        }
        """
    return """
        .stApp {
            background-color: #FFF4E6 !important;
            background-image:
                radial-gradient(ellipse 80% 50% at 50% 0%, rgba(247, 147, 26, 0.14), transparent),
                linear-gradient(180deg, #FFF8F0 0%, #FFEED9 55%, #FFDDB3 100%) !important;
            background-attachment: fixed;
        }
        """


def build_streamlit_surface_css() -> str:
    """Remove Streamlit default white backgrounds."""
    return """
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stHeader"],
        section.main,
        .block-container {
            background: transparent !important;
        }
        [data-testid="stSidebar"] {
            background: var(--surface) !important;
            border-right: 1px solid var(--border) !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            background: var(--surface) !important;
        }
        iframe {
            border-radius: var(--radius-sm);
        }
    """
```

---

<a id="file-src-ui-charts-py"></a>
## File: `src\ui\charts.py`


```python
"""Theme-aware Plotly charts."""

from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.graph_objects as go
import streamlit as st

from src.ui.theme import PLOTLY_CONFIG, chart_layout, gauge_steps, get_palette, score_color

if TYPE_CHECKING:
    from src.analysis.models import AnalysisResult

_GAUGE_HEIGHT = 360
_HEATMAP_HEIGHT = 400
_VOLUME_HEIGHT = 280


@st.cache_data(show_spinner=False)
def _build_score_gauge_figure(score: float, dark: bool) -> go.Figure:
    """Performance: cache Plotly gauge figure — score only changes on refresh."""
    palette = get_palette(dark)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={
                "suffix": "/100",
                "font": {"size": 48, "color": palette["text"], "family": "Inter, system-ui, sans-serif"},
            },
            title={"text": "Composite Score", "font": {"size": 15, "color": palette["text_secondary"]}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickmode": "array",
                    "tickvals": [19, 50, 81],
                    "ticktext": ["Weak", "Neutral", "Strong"],
                    "tickcolor": palette["text_muted"],
                    "tickfont": {"size": 12, "color": palette["text_secondary"]},
                },
                "bar": {"color": score_color(score, dark), "thickness": 0.72},
                "bgcolor": palette["surface_alt"],
                "borderwidth": 0,
                "steps": gauge_steps(dark),
            },
        )
    )
    layout = chart_layout(palette)
    layout["margin"] = {"l": 24, "r": 24, "t": 56, "b": 36}
    fig.update_layout(height=_GAUGE_HEIGHT, **layout)
    return fig


@st.cache_data(show_spinner=False)
def _build_volume_chart_figure(volumes: tuple[float, ...], dark: bool) -> go.Figure:
    """Performance: cache volume bar chart for unchanged candle history."""
    palette = get_palette(dark)
    fig = go.Figure(
        go.Bar(
            x=list(range(1, len(volumes) + 1)),
            y=list(volumes),
            marker=dict(color=palette["accent"], opacity=0.85),
            hovertemplate="Bar %{x}<br>Volume: %{y:,.2f} BTC<extra></extra>",
        )
    )
    fig.update_layout(
        height=_VOLUME_HEIGHT,
        title=dict(text="BTC Volume (last candles)", font=dict(size=12, color=palette["text_muted"])),
        xaxis_title="Candle",
        yaxis_title="Volume (BTC)",
        **chart_layout(palette),
    )
    return fig


def render_score_gauge(score: float, *, dark: bool = False) -> None:
    fig = _build_score_gauge_figure(score, dark)
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


def render_heatmap_chart(result: AnalysisResult, *, dark: bool = False) -> None:
    palette = get_palette(dark)
    heatmap = result.heatmap
    if heatmap is None or heatmap.empty:
        return

    intensity_col = "intensity" if "intensity" in heatmap.columns else "volume"
    fig = go.Figure(
        go.Bar(
            x=heatmap[intensity_col],
            y=heatmap["price_level"],
            orientation="h",
            marker=dict(
                color=heatmap[intensity_col],
                colorscale=[
                    [0, palette["surface_alt"]],
                    [0.5, palette["heatmap_mid"]],
                    [1, palette["short"]],
                ],
                showscale=True,
                colorbar=dict(title="Intensity", thickness=10, len=0.55, outlinewidth=0),
            ),
            hovertemplate="Price: $%{y:,.0f}<br>Intensity: %{x:.2f}<extra></extra>",
        )
    )
    fig.add_hline(
        y=result.price,
        line_dash="dash",
        line_color=palette["accent"],
        line_width=1.5,
        annotation_text=f"${result.price:,.0f}",
        annotation_font=dict(color=palette["accent"], size=10),
    )
    fig.update_layout(
        height=_HEATMAP_HEIGHT,
        title=dict(text=result.heatmap_source, font=dict(size=12, color=palette["text_muted"])),
        xaxis_title="Intensity",
        yaxis_title="Price (USD)",
        **chart_layout(palette),
    )
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)


def render_volume_chart(volumes: list[float], *, dark: bool = False) -> None:
    """Bar chart of recent BTC candle volume."""
    if not volumes:
        return

    fig = _build_volume_chart_figure(tuple(volumes), dark)
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
```

---

<a id="file-src-ui-components-py"></a>
## File: `src\ui\components.py`


```python
"""UI entry points — thin facade over dashboard and shared widgets."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from src.ui.dashboard import render_dashboard
from src.ui.time_utils import normalize_last_updated
from src.ui.tradingview import render_tradingview_chart
from src.ui.primitives import empty_state, error_state, premium_nav, welcome_empty_state

__all__ = [
    "render_header_bar",
    "render_analyze_button",
    "render_empty_state",
    "render_error_state",
    "render_dashboard",
    "render_tradingview_chart",
]


def render_header_bar(last_updated: datetime | None = None) -> None:
    """Render the premium navigation header."""
    safe_updated = normalize_last_updated(last_updated)
    st.markdown(premium_nav(last_updated=safe_updated), unsafe_allow_html=True)


def render_analyze_button() -> bool:
    return st.button("Analyze Market", type="primary", use_container_width=True)


def render_empty_state() -> None:
    html = welcome_empty_state()
    if hasattr(st, "html"):
        st.html(html)
    else:
        st.markdown(html, unsafe_allow_html=True)


def render_error_state(message: str) -> None:
    st.markdown(error_state(message), unsafe_allow_html=True)
```

---

<a id="file-src-ui-dashboard-py"></a>
## File: `src\ui\dashboard.py`


```python
"""Tabbed dashboard layout."""

from __future__ import annotations

from typing import TYPE_CHECKING

import streamlit as st

from src.ui.charts import render_score_gauge, render_volume_chart
from src.ui.helpers import indicator_rows, signal_plain_language_summary
from src.ui.primitives import (
    bitcoin_chart_brand,
    bitcoin_chart_logo,
    brand_footer,
    checklist_panel,
    component_card,
    empty_state,
    market_signal_hero,
    metric_card,
    metric_card_wrap,
    prose_block,
    risk_enhanced_panel,
    risk_warning_banner,
    section_heading,
)
from src.ui.theme import RECOMMENDATION_STYLE, confidence_percent
from src.ui.tradingview import render_tradingview_chart

if TYPE_CHECKING:
    from src.analysis.models import AnalysisResult


def _render_metric_row(cards: list[str], columns: int = 4) -> None:
    cols = st.columns(columns, gap="medium")
    for col, card in zip(cols, cards, strict=False):
        with col:
            st.markdown(metric_card_wrap(card), unsafe_allow_html=True)


def _panel_open() -> None:
    st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)


def _panel_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def render_ai_dashboard_tab(result: AnalysisResult, *, dark: bool) -> None:
    interval = st.session_state.get("chart_interval", "1m")

    _panel_open()
    st.markdown(
        market_signal_hero(
            result.recommendation,
            result.confidence,
            price=result.price,
            score=result.score,
        ),
        unsafe_allow_html=True,
    )
    st.markdown(section_heading("Live Chart", tight=True, large=True), unsafe_allow_html=True)
    st.markdown(bitcoin_chart_logo(placement="above"), unsafe_allow_html=True)
    st.markdown(
        '<p class="chart-tagline">LETS MAKE MONEY $</p>',
        unsafe_allow_html=True,
    )
    render_tradingview_chart(interval=interval, dark=dark)
    st.markdown(bitcoin_chart_logo(placement="below"), unsafe_allow_html=True)
    st.markdown(bitcoin_chart_brand(), unsafe_allow_html=True)
    _panel_close()


def render_overview_tab(result: AnalysisResult, *, dark: bool) -> None:
    style = RECOMMENDATION_STYLE[result.recommendation]

    st.markdown('<div class="overview-tab">', unsafe_allow_html=True)
    _panel_open()

    _render_metric_row([
        metric_card("Price", f"${result.price:,.2f}"),
        metric_card("Direction", style["label"], tone=style["tone"]),
        metric_card("Signal strength", f"{result.confidence} · {confidence_percent(result.confidence)}%"),
        metric_card("Risk / Reward", f"{result.risk_reward:.2f}", tone="long" if result.risk_reward >= 1.5 else "wait"),
    ])

    st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.15, 1], gap="large")
    with left:
        render_score_gauge(result.score, dark=dark)
    with right:
        badge_html = (
            f'<div class="overview-signal-only">'
            f'<div class="signal-badge signal-badge--hero signal-badge--{style["tone"]}">'
            f'<span class="signal-badge__symbol">{style["symbol"]}</span>'
            f'<span class="signal-badge__label">{style["label"]}</span>'
            f"</div></div>"
        )
        if hasattr(st, "html"):
            st.html(badge_html)
        else:
            st.markdown(badge_html, unsafe_allow_html=True)

    _panel_close()
    st.markdown("</div>", unsafe_allow_html=True)


def render_trade_setup_tab(result: AnalysisResult, *, dark: bool) -> None:
    setup = result.trade_setup or {}
    entry = float(setup.get("entry") or result.price or 0)

    _panel_open()
    st.markdown(section_heading("Trade Setup"), unsafe_allow_html=True)

    if entry <= 0:
        st.markdown(
            empty_state(
                title="Market data unavailable",
                description=(
                    "Price and candle data could not be loaded from this server. "
                    "This often happens when Binance blocks cloud hosting IPs. "
                    "Check Overview → Connected Sources, then redeploy after updating environment variables."
                ),
            ),
            unsafe_allow_html=True,
        )
        _panel_close()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    direction = setup.get("direction") or result.recommendation
    if direction not in ("long", "short"):
        if result.recommendation in ("long", "short"):
            direction = result.recommendation
        else:
            direction = "wait"
    if direction == "wait":
        st.markdown(
            empty_state(
                title="No active trade setup",
                description="The market signal is WAIT — levels appear when a directional setup is available.",
            ),
            unsafe_allow_html=True,
        )
        _panel_close()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    style = RECOMMENDATION_STYLE[direction]

    tp_tone = "long" if direction == "long" else "short"
    sl_tone = "short" if direction == "long" else "long"
    _render_metric_row([
        metric_card("Direction", style["label"], tone=style["tone"]),
        metric_card("Entry", f"${entry:,.2f}"),
        metric_card("Stop Loss", f"${setup.get('stop_loss', 0):,.2f}", tone=sl_tone),
        metric_card("TP1", f"${setup.get('tp1', 0):,.2f}", tone=tp_tone),
    ], columns=4)
    _render_metric_row([
        metric_card("TP2", f"${setup.get('tp2', 0):,.2f}", tone=tp_tone),
        metric_card("TP3", f"${setup.get('tp3', 0):,.2f}", tone=tp_tone),
        metric_card("TP4", f"${setup.get('tp4', 0):,.2f}", tone=tp_tone),
        metric_card("R/R", f"{setup.get('risk_reward', 0):.2f}", tone="long" if setup.get("risk_reward", 0) >= 1.5 else "wait"),
    ], columns=4)
    st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)

    st.markdown(section_heading("Live Chart", large=True), unsafe_allow_html=True)
    interval = st.session_state.get("chart_interval", "1m")
    render_tradingview_chart(
        interval=interval,
        dark=dark,
        height=480,
        chart_id="btc-trade-setup-chart",
    )

    if result.reasons_enter or result.reasons_avoid:
        st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown(
                checklist_panel(
                    title="Reasons to enter",
                    items=result.reasons_enter or ["Run analysis for checklist"],
                    positive=True,
                ),
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                checklist_panel(
                    title="Reasons NOT to enter",
                    items=result.reasons_avoid or ["Run analysis for warnings"],
                    positive=False,
                ),
                unsafe_allow_html=True,
            )

    _panel_close()


def render_risk_tab(result: AnalysisResult, *, risk_settings: dict[str, float]) -> None:
    _panel_open()
    st.markdown(section_heading("Risk Overview"), unsafe_allow_html=True)
    st.markdown(risk_enhanced_panel(result.risk_profile), unsafe_allow_html=True)

    max_risk_pct = float(risk_settings.get("max_risk_pct", 1.0))
    account_size = float(risk_settings.get("account_size", 10000.0))
    risk_per_unit = abs(result.price - result.stop_loss)
    max_risk_usd = account_size * (max_risk_pct / 100)
    position_size = max_risk_usd / risk_per_unit if risk_per_unit > 0 else 0.0
    position_value = position_size * result.price
    pct = confidence_percent(result.confidence)

    st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)
    _render_metric_row([
        metric_card("Risk / Trade", f"{max_risk_pct:.2f}%"),
        metric_card("Risk Budget", f"${max_risk_usd:,.2f}"),
        metric_card("Est. Position Size", f"{position_size:.4f} BTC"),
        metric_card("Position Value", f"${position_value:,.2f}"),
    ])

    summary = signal_plain_language_summary(result.recommendation, result.confidence, result.score)
    lines = [
        f"Stop distance: ${risk_per_unit:,.2f} per BTC",
        f"Direction: {result.recommendation.upper()} (score {result.score:.0f}/100)",
        f"Signal strength: {result.confidence} ({pct}%)",
        "",
        summary[2][1],
        "",
        "Position sizing uses default 1% risk baseline for suggestions.",
    ]
    st.markdown(prose_block("\n".join(lines)), unsafe_allow_html=True)
    st.markdown(
        risk_warning_banner(result.recommendation, result.confidence, result.score),
        unsafe_allow_html=True,
    )
    _panel_close()


def render_indicators_tab(result: AnalysisResult, *, dark: bool = False) -> None:
    _panel_open()
    st.markdown(section_heading("Technical Indicators"), unsafe_allow_html=True)
    rows = indicator_rows(result)
    for i in range(0, len(rows), 4):
        chunk = rows[i : i + 4]
        _render_metric_row(
            [metric_card(label, value, tone=tone) for label, value, tone in chunk],
            columns=min(4, len(chunk)),
        )
        st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)

    volume_history = result.indicators.get("volume_history") or []
    if volume_history:
        st.markdown(section_heading("BTC Volume Chart"), unsafe_allow_html=True)
        render_volume_chart(volume_history, dark=dark)
        st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)

    st.markdown(section_heading("Signal Components"), unsafe_allow_html=True)
    cols = st.columns(3, gap="medium")
    for idx, component in enumerate(result.components):
        with cols[idx % 3]:
            st.markdown(component_card(component.name, component.score, component.detail), unsafe_allow_html=True)
    _panel_close()


def render_dashboard(
    result: AnalysisResult,
    *,
    dark: bool,
    risk_settings: dict[str, float] | None = None,
) -> None:
    settings = risk_settings or {}
    tabs = st.tabs([
        "AI Dashboard",
        "Overview",
        "Trade Setup",
        "Risk",
        "Indicators",
    ])

    with tabs[0]:
        render_ai_dashboard_tab(result, dark=dark)
    with tabs[1]:
        render_overview_tab(result, dark=dark)
    with tabs[2]:
        render_trade_setup_tab(result, dark=dark)
    with tabs[3]:
        render_risk_tab(result, risk_settings=settings)
    with tabs[4]:
        render_indicators_tab(result, dark=dark)

    st.markdown("<div class='section-gap section-gap--sm'></div>", unsafe_allow_html=True)
    st.markdown(
        brand_footer(sources=", ".join(result.data_sources)),
        unsafe_allow_html=True,
    )
```

---

<a id="file-src-ui-helpers-py"></a>
## File: `src\ui\helpers.py`


```python
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
    vol_ratio = ind.get("volume_ratio")
    rows: list[tuple[str, str, str | None]] = [
        ("RSI (14)", f"{ind.get('rsi', 0):.1f}", _rsi_tone(ind.get("rsi"))),
        ("MACD Histogram", f"{ind.get('macd_hist', 0):.2f}", _macd_tone(ind.get("macd_hist"))),
        ("EMA 9", f"${ind.get('ema_9', 0):,.2f}", None),
        ("EMA 21", f"${ind.get('ema_21', 0):,.2f}", None),
        ("EMA 50", f"${ind.get('ema_50', 0):,.2f}", None),
        ("EMA 200", f"${ind.get('ema_200', 0):,.2f}", None),
        ("BTC Volume", _format_btc_volume(ind.get("volume_btc", 0)), _volume_tone(vol_ratio)),
        ("24h BTC Volume", _format_btc_volume(ind.get("volume_24h_btc", 0)), None),
        ("Volume USDT", _format_usdt_volume(ind.get("quote_volume_usdt", 0)), None),
        ("24h Volume USDT", _format_usdt_volume(ind.get("volume_24h_usdt", 0)), None),
        ("Volume Ratio", f"{float(vol_ratio):.2f}x" if vol_ratio is not None else "—", _volume_tone(vol_ratio)),
        ("Avg Volume (20)", _format_btc_volume(ind.get("volume_sma_btc", 0)), None),
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


def _volume_tone(ratio: float | None) -> str | None:
    if ratio is None:
        return None
    if ratio >= 1.5:
        return "long"
    if ratio <= 0.7:
        return "short"
    return "wait"


def _format_btc_volume(volume: float | None) -> str:
    vol = float(volume or 0)
    if vol >= 1000:
        return f"{vol:,.0f} BTC"
    if vol >= 1:
        return f"{vol:,.2f} BTC"
    return f"{vol:.4f} BTC"


def _format_usdt_volume(volume: float | None) -> str:
    vol = float(volume or 0)
    if vol >= 1_000_000_000:
        return f"${vol / 1e9:.2f}B"
    if vol >= 1_000_000:
        return f"${vol / 1e6:.1f}M"
    if vol >= 1_000:
        return f"${vol / 1e3:.1f}K"
    return f"${vol:,.0f}"
```

---

<a id="file-src-ui-performance-py"></a>
## File: `src\ui\performance.py`


```python
"""Streamlit caching layer — keeps analyzers alive and skips duplicate market fetches."""

from __future__ import annotations

import streamlit as st

from src.analysis.models import AnalysisResult
from src.analysis.scorer import MarketAnalyzer
from src.ui.sidebar import AUTO_REFRESH_SECONDS

# Refresh slightly before the UI auto-refresh so users see new data on schedule.
_ANALYSIS_CACHE_TTL = max(30, AUTO_REFRESH_SECONDS - 5)


@st.cache_resource(show_spinner=False)
def get_market_analyzer(symbol: str, interval: str, api_key: str) -> MarketAnalyzer:
    """Reuse one analyzer (and its in-memory hub TTL cache) across reruns."""
    return MarketAnalyzer(
        symbol=symbol,
        interval=interval,
        coinglass_api_key=api_key or None,
    )


@st.cache_data(ttl=_ANALYSIS_CACHE_TTL, show_spinner=False)
def run_cached_market_analysis(symbol: str, interval: str, api_key: str) -> AnalysisResult:
    """Cache full analysis output to prevent repeated API work on Streamlit reruns."""
    analyzer = get_market_analyzer(symbol, interval, api_key)
    return analyzer.analyze()


def clear_analysis_cache() -> None:
    """Clear cached analysis after auth changes or manual refresh hooks."""
    run_cached_market_analysis.clear()
    get_market_analyzer.clear()
```

---

<a id="file-src-ui-primitives-py"></a>
## File: `src\ui\primitives.py`


```python
"""HTML primitives for the dashboard UI."""

from __future__ import annotations

import html
from datetime import datetime

from src.ui.time_utils import format_last_updated, normalize_last_updated
from src.ui.theme import APP_VERSION, BRAND, RECOMMENDATION_STYLE, brand_caption, confidence_percent, score_tone


def premium_nav(*, last_updated: datetime | None = None) -> str:
    """Sticky premium SaaS navigation header."""
    title = html.escape(BRAND["product"])
    tagline = html.escape(brand_caption())

    dt = normalize_last_updated(last_updated)
    updated_text = html.escape(format_last_updated(dt))
    if dt is not None:
        status_label = "Live"
        status_class = "status-dot--live"
    else:
        status_label = "Ready"
        status_class = "status-dot--idle"

    return f"""
    <header class="premium-nav-outer">
        <div class="premium-nav">
            <div class="premium-nav__inner">
                <div class="premium-nav__left">
                    <div class="premium-nav__logo" aria-label="Bitcoin">
                        <span class="premium-nav__logo-symbol">₿</span>
                        <span class="premium-nav__logo-text">BTC</span>
                    </div>
                    <div class="premium-nav__brand">
                        <h1 class="premium-nav__title">{title}</h1>
                        <p class="premium-nav__tagline">{tagline}</p>
                    </div>
                </div>
                <div class="premium-nav__right">
                    <div class="premium-nav__status">
                        <span class="status-dot {status_class}" aria-hidden="true"></span>
                        <span>{status_label}</span>
                    </div>
                    <div class="premium-nav__updated">
                        <span class="premium-nav__updated-label">Updated</span>
                        {updated_text}
                    </div>
                </div>
            </div>
            <div class="premium-nav__divider" aria-hidden="true"></div>
        </div>
    </header>
    """


def section_heading(text: str, *, tight: bool = False, large: bool = False) -> str:
    cls = "section-heading"
    if tight:
        cls += " section-heading--tight"
    if large:
        cls += " section-heading--large"
    return f'<h3 class="{cls}">{html.escape(text)}</h3>'


def bitcoin_chart_logo(*, placement: str = "below") -> str:
    """Centered Bitcoin logo shown near the live chart."""
    modifiers = {
        "above": " chart-bitcoin-logo--above",
        "below": " chart-bitcoin-logo--below",
        "login": " chart-bitcoin-logo--login",
    }
    modifier = modifiers.get(placement, " chart-bitcoin-logo--below")
    return f"""<div class="chart-bitcoin-logo{modifier}" aria-label="Bitcoin">
        <svg class="chart-bitcoin-logo__svg" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img">
            <circle cx="32" cy="32" r="32" fill="#F7931A"/>
            <path fill="#FFFFFF" d="M46.1,27.4c0.7-4.7-2.9-7.2-7.8-8.9l1.6-6.3l-3.8-0.9l-1.5,6.1c-1-0.3-2-0.5-3-0.8l1.5-6.1l-3.8-0.9l-1.6,6.3c-0.8-0.2-1.6-0.4-2.4-0.6v-0.1l-5.2-1.3l-1,4.1c0,0-2.9,0.7-2.8,0.8c-1.7,0.4-2,1.4-1.9,2.3c0.1,0.6,0.8,4,0.8,4s-0.6,1.7-1.2,2.7c-1,1.4-2.8,2.5-2.8,2.5s2.1,1,2,1c-1.4,3.7-2.7,7.3-2.7,7.3s2.9,0.7,2.9,0.7l-1.6,6.3l3.8,0.9l1.6-6.3c1,0.3,2.1,0.5,3.1,0.8l-1.6,6.2l3.8,0.9l1.6-6.3c6.5,1.2,11.4,0.7,13.5-5.2c1.7-4.7-0.1-7.5-3.5-9.4c2.5-0.6,4.4-2.3,5-5.7L46.1,27.4z M39.9,41.4c-1.2,4.8-9.3,2.2-12,1.6l2.1-8.5C32.4,35.3,41.2,36.6,39.9,41.4z M41.2,27.4c-1.1,4.5-8,2.3-10.3,1.7l1.9-7.6C35.2,22.1,42.4,23.2,41.2,27.4z"/>
        </svg>
    </div>"""


def bitcoin_chart_brand() -> str:
    """Large Bitcoin symbol and name shown below the chart logo."""
    email = html.escape("NORISKNOGLORY@Outlook.co.il")
    return f"""
    <div class="chart-bitcoin-brand" aria-label="Bitcoin">
        <div class="chart-bitcoin-brand__symbol">₿</div>
        <div class="chart-bitcoin-brand__name">Bitcoin</div>
        <a class="chart-bitcoin-brand__email" href="mailto:{email}">{email}</a>
    </div>
    """

def metric_card(label: str, value: str, *, tone: str | None = None) -> str:
    tone_cls = f" card--tone-{tone}" if tone else ""
    accent = f'<div class="card__accent card__accent--{tone}"></div>' if tone else '<div class="card__accent"></div>'
    return f"""
    <div class="card card--metric card--elevated{tone_cls}">
        {accent}
        <div class="card__label">{html.escape(label)}</div>
        <div class="card__value">{html.escape(value)}</div>
    </div>
    """


def metric_card_wrap(inner: str) -> str:
    return f'<div class="card-wrap">{inner}</div>'


def component_card(name: str, score: float, detail: str) -> str:
    tone = score_tone(score)
    return f"""
    <div class="card card--component card--elevated card--tone-{tone}">
        <div class="card__accent card__accent--{tone}"></div>
        <div class="card__label">{html.escape(name)}</div>
        <div class="card__value">{score:.0f}<span class="card__suffix">/100</span></div>
        <div class="progress-track">
            <div class="progress-fill progress-fill--{tone}" style="width:{score:.0f}%;"></div>
        </div>
        <p class="card__detail">{html.escape(detail)}</p>
    </div>
    """


def recommendation_panel(
    recommendation: str,
    insight: str,
    confidence: str,
    score: float,
    *,
    summary_rows: list[tuple[str, str]] | None = None,
    show_meaning: bool = True,
    show_insight: bool = True,
) -> str:
    style = RECOMMENDATION_STYLE[recommendation]
    pct = confidence_percent(confidence)

    meaning_html = ""
    if show_meaning:
        if summary_rows is None:
            from src.ui.helpers import signal_plain_language_summary

            summary_rows = signal_plain_language_summary(recommendation, confidence, score)

        summary_html = "".join(
            f"""
            <div class="signal-summary__row">
                <div class="signal-summary__label">{html.escape(label)}</div>
                <p class="signal-summary__text">{html.escape(text)}</p>
            </div>
            """
            for label, text in summary_rows
        )
        meaning_html = f"""
        <div class="signal-summary">
            <div class="signal-summary__heading">What this means</div>
            {summary_html}
        </div>
        """

    insight_html = ""
    if show_insight:
        insight_html = f'<p class="rec-panel__insight">{html.escape(insight)}</p>'

    return f"""
    <div class="rec-panel card--elevated rec-panel--{style['tone']}">
        <div class="signal-badge signal-badge--{style['tone']}">{style['label']}</div>
        {insight_html}
        {meaning_html}
        <div class="rec-panel__confidence">
            <div class="rec-panel__conf-row">
                <span class="card__label">Signal strength</span>
                <span class="rec-panel__conf-value">{html.escape(confidence)} · {pct}%</span>
            </div>
            <div class="progress-track progress-track--lg">
                <div class="progress-fill progress-fill--{style['tone']}" style="width:{pct}%;"></div>
            </div>
        </div>
    </div>
    """


def risk_warning_banner(
    recommendation: str,
    confidence: str,
    score: float,
) -> str:
    pct = confidence_percent(confidence)
    if pct >= 70 or recommendation == "wait":
        return ""

    direction = recommendation.upper()
    return f"""
    <div class="risk-alert risk-alert--banner" role="alert">
        <strong>Heads up</strong>
        <span>
            Direction is {direction} (score {score:.0f}/100), but signal strength is only {pct}%.
            Read the summary below before entering — waiting is often the safer choice.
        </span>
    </div>
    """


def market_signal_hero(
    recommendation: str,
    confidence: str,
    *,
    price: float | None = None,
    score: float | None = None,
) -> str:
    """Large LONG / SHORT / WAIT signal for the AI Dashboard."""
    style = RECOMMENDATION_STYLE.get(recommendation, RECOMMENDATION_STYLE["wait"])
    pct = confidence_percent(confidence)

    price_html = ""
    if price is not None:
        price_html = f'<div class="signal-hero__stat"><span class="signal-hero__stat-label">BTC Price</span><span class="signal-hero__stat-value">${price:,.2f}</span></div>'

    score_html = ""
    if score is not None:
        score_html = (
            f'<div class="signal-hero__stat signal-hero__stat--score">'
            f'<span class="signal-hero__stat-label">Score</span>'
            f'<span class="signal-hero__stat-value">{score:.0f}<span class="signal-hero__stat-suffix">/100</span></span>'
            f"</div>"
        )

    return f"""
    <div class="signal-hero signal-hero--panel" role="status" aria-label="Market signal {html.escape(style['label'])}">
        <div class="signal-hero__row">
            {price_html}
            <div class="signal-badge signal-badge--hero signal-badge--{style['tone']}">
                <span class="signal-badge__symbol" aria-hidden="true">{style['symbol']}</span>
                <span class="signal-badge__label">{style['label']}</span>
            </div>
            {score_html}
        </div>
        <p class="signal-hero__confidence">
            Signal strength: {html.escape(confidence)} · {pct}%
        </p>
    </div>
    """


def welcome_empty_state() -> str:
    """Landing hero — Bitcoin logo only before first analysis."""
    return f"""
    <div class="state-panel state-panel--empty state-panel--welcome state-panel--logo-only">
        {bitcoin_chart_logo(placement="above")}
    </div>
    """


def empty_state(*, title: str, description: str, compact: bool = False) -> str:
    cls = "state-panel state-panel--empty"
    if compact:
        cls += " state-panel--compact"
    return f"""
    <div class="{cls}">
        <div class="state-panel__icon">📊</div>
        <div class="state-panel__title">{html.escape(title)}</div>
        <p class="state-panel__desc">{html.escape(description)}</p>
    </div>
    """


def error_state(message: str) -> str:
    return f"""
    <div class="state-panel state-panel--error" role="alert">
        <div class="state-panel__title">Analysis failed</div>
        <p class="state-panel__desc">{html.escape(message)}</p>
    </div>
    """


def prose_block(text: str) -> str:
    return f'<div class="card card--prose card--elevated">{html.escape(text)}</div>'


def login_gate_logo_only() -> str:
    """Login header — Bitcoin logo only (no title/subtitle text)."""
    return f"""
    <div class="login-gate">
        <div class="login-gate__panel login-gate__panel--logo-only">
            {bitcoin_chart_logo(placement="above")}
        </div>
    </div>
    """


def login_gate_shell() -> str:
    """Deprecated — kept for compatibility; logo only."""
    return login_gate_logo_only()


def login_purchase_panel() -> str:
    """Purchase instructions shown on the login screen."""
    email = html.escape("AlphabtcTool@outlook.com")
    wallet = html.escape("1ME6L23cLzYu3iAEEjdwDVSE578P2mssDW")
    return f"""
    <div class="login-purchase card card--elevated">
        <div class="card__accent"></div>
        <h3 class="login-purchase__title">Purchase Alpha BTC Trading Tool</h3>
        <p class="login-purchase__price">Price: <strong>$99 USD</strong></p>
        <p class="login-purchase__line">Payment Method: <strong>Bitcoin (BTC) only.</strong></p>
        <div class="login-purchase__wallet-block">
            <span class="login-purchase__label">BTC Wallet:</span>
            <span class="login-purchase__wallet">{wallet}</span>
        </div>
        <p class="login-purchase__line">
            After payment, send a transaction screenshot to
            <a class="login-purchase__email" href="mailto:{email}">{email}</a>.
        </p>
        <p class="login-purchase__note">
            Your access credentials will be sent within 12 hours after payment verification.
        </p>
    </div>
    """


def brand_footer(*, sources: str) -> str:
    return f"""
    <footer class="brand-footer card card--elevated">
        <div class="card__accent"></div>
        <p class="brand-footer__disclaimer">Educational tool only. Not financial advice.</p>
        <p class="brand-footer__meta">
            Built by {html.escape(BRAND['author_en'])} · {html.escape(BRAND['website_label'])} · v{html.escape(APP_VERSION)}
        </p>
        <p class="brand-footer__meta brand-footer__meta--muted">
            {html.escape(BRAND['product'])} · Data: {html.escape(sources)}
        </p>
    </footer>
    """


def data_hub_panel(hub: dict) -> str:
    if not hub:
        return empty_state(
            title="Data Hub unavailable",
            description="Run analysis to populate the unified data layer.",
            compact=True,
        )

    source_rows = []
    for name, info in (hub.get("source_status") or {}).items():
        status = html.escape(str(info.get("status", "offline")))
        updated = info.get("last_updated") or "—"
        error = info.get("error")
        status_cls = f"hub-status hub-status--{status}"
        error_html = f'<div class="hub-source__error">{html.escape(error)}</div>' if error else ""
        source_rows.append(
            f"""
            <div class="hub-source card card--elevated">
                <div class="hub-source__head">
                    <span class="hub-source__name">{html.escape(name)}</span>
                    <span class="{status_cls}">{status.upper()}</span>
                </div>
                <div class="hub-source__meta">Last updated: {html.escape(str(updated))}</div>
                {error_html}
            </div>
            """
        )

    available = ", ".join(hub.get("available_fields") or []) or "None"
    missing = ", ".join(hub.get("missing_fields") or []) or "None"
    quality = html.escape(str(hub.get("data_quality", "unknown")))
    impact = html.escape(str(hub.get("confidence_impact", "none")))
    last_updated = html.escape(str(hub.get("last_updated") or "—"))

    return f"""
    <div class="hub-panel">
        <div class="hub-summary card card--elevated">
            <div class="hub-summary__grid">
                <div><span class="card__label">Data quality</span><div class="hub-summary__value">{quality}</div></div>
                <div><span class="card__label">Last updated</span><div class="hub-summary__value">{last_updated}</div></div>
                <div><span class="card__label">Confidence impact</span><div class="hub-summary__value">{impact}</div></div>
                <div><span class="card__label">Active sources</span><div class="hub-summary__value">{len(hub.get("sources") or [])}</div></div>
            </div>
        </div>
        <div class="section-gap section-gap--sm"></div>
        <h4 class="section-heading">Connected Sources</h4>
        <div class="hub-source-grid">{''.join(source_rows)}</div>
        <div class="section-gap section-gap--sm"></div>
        <div class="hub-fields card card--prose card--elevated">
            <strong>Available data:</strong> {html.escape(available)}
            <br><br>
            <strong>Missing data:</strong> {html.escape(missing)}
        </div>
    </div>
    """


def stars_display(count: int, max_stars: int = 5) -> str:
    filled = max(0, min(max_stars, count))
    return "★" * filled + "☆" * (max_stars - filled)


def market_status_panel(*, trend: str, volatility: str, liquidity: str) -> str:
    items = [
        ("Market trend", trend, _status_tone(trend)),
        ("Volatility", volatility, _status_tone(volatility)),
        ("Liquidity", liquidity, _status_tone(liquidity)),
    ]
    cards = "".join(
        f"""
        <div class="card card--metric card--elevated card--tone-{tone}">
            <div class="card__label">{html.escape(label)}</div>
            <div class="card__value card__value--sm">{html.escape(value)}</div>
        </div>
        """
        for label, value, tone in items
    )
    return f'<div class="status-grid">{cards}</div>'


def _status_tone(value: str) -> str:
    lower = value.lower()
    if "bull" in lower:
        return "long"
    if "bear" in lower:
        return "short"
    if "high" in lower or "low" in lower:
        return "wait"
    return "wait"


def trade_quality_panel(*, grade: str, score: int, stars: int) -> str:
    tone = "long" if grade in {"A+", "A"} else "wait" if grade == "B" else "short" if grade == "C" else "wait"
    if grade == "No Trade":
        tone = "short"
    return f"""
    <div class="card card--elevated trade-quality card--tone-{tone}">
        <div class="card__label">Trade Quality</div>
        <div class="trade-quality__grade">{html.escape(grade)}</div>
        <div class="trade-quality__score">{score}/100</div>
        <div class="trade-quality__stars" aria-label="{stars} of 5 stars">{stars_display(stars)}</div>
    </div>
    """


def checklist_panel(*, title: str, items: list[str], positive: bool = True) -> str:
    cls = "checklist checklist--positive" if positive else "checklist checklist--negative"
    icon = "✓" if positive else "!"
    rows = "".join(
        f'<li class="checklist__item"><span class="checklist__icon">{icon}</span>{html.escape(item)}</li>'
        for item in items
    )
    return f"""
    <div class="card card--elevated {cls}">
        <div class="card__label">{html.escape(title)}</div>
        <ul class="checklist__list">{rows}</ul>
    </div>
    """


def source_status_panel(source_status: dict) -> str:
    if not source_status:
        return empty_state(title="No source status", description="Run analysis first.", compact=True)

    rows = []
    for name, status in source_status.items():
        status_str = html.escape(str(status))
        cls = f"hub-status hub-status--{status_str}"
        rows.append(
            f"""
            <div class="source-pill card card--elevated">
                <span class="source-pill__name">{html.escape(name)}</span>
                <span class="{cls}">{status_str.upper()}</span>
            </div>
            """
        )
    return f'<div class="source-status-grid">{"".join(rows)}</div>'


def fear_greed_panel(data: dict) -> str:
    if not data or data.get("value") is None:
        msg = html.escape(str(data.get("error") or "Fear & Greed data unavailable"))
        return f'<div class="card card--elevated card--prose">{msg}</div>'

    value = int(data["value"])
    tone = "long" if value >= 55 else "short" if value <= 45 else "wait"
    return f"""
    <div class="card card--elevated card--tone-{tone}">
        <div class="card__label">Fear &amp; Greed Index</div>
        <div class="card__value">{value}</div>
        <div class="card__detail">{html.escape(str(data.get("classification", "")))}</div>
        <div class="card__detail">Provider: {html.escape(str(data.get("provider", "Alternative.me")))}</div>
    </div>
    """


def news_sentiment_panel(data: dict) -> str:
    summary = data.get("summary") or {}
    headlines = data.get("headlines") or []
    headline_rows = "".join(
        f"""
        <li class="news-item news-item--{html.escape(str(item.get('sentiment', 'neutral')))}">
            <span class="news-item__source">{html.escape(str(item.get('source', '')))}</span>
            {html.escape(str(item.get('title', '')))}
        </li>
        """
        for item in headlines[:8]
    )
    if not headline_rows:
        headline_rows = "<li class='news-item'>No headlines fetched.</li>"

    return f"""
    <div class="card card--elevated news-panel">
        <div class="card__label">News Sentiment</div>
        <div class="news-panel__summary">
            {html.escape(str(summary.get('label', 'neutral')).title())}
            · score {summary.get('score', 50)}/100
            · +{summary.get('positive', 0)} / −{summary.get('negative', 0)} headlines
        </div>
        <ul class="news-panel__list">{headline_rows}</ul>
    </div>
    """


def risk_enhanced_panel(risk_profile: dict) -> str:
    if not risk_profile:
        return empty_state(title="Risk data unavailable", description="Run analysis first.", compact=True)

    return f"""
    <div class="card card--elevated risk-panel">
        <div class="risk-panel__grid">
            <div><span class="card__label">Risk Level</span><div class="card__value card__value--sm">{html.escape(str(risk_profile.get('level', 'N/A')))}</div></div>
            <div><span class="card__label">Probability</span><div class="card__value card__value--sm">{float(risk_profile.get('probability', 0)):.0%}</div></div>
            <div><span class="card__label">Invalidation</span><div class="card__value card__value--sm">${float(risk_profile.get('invalidation', 0)):,.2f}</div></div>
            <div><span class="card__label">Position (1% risk)</span><div class="card__value card__value--sm">{float(risk_profile.get('position_size_btc', 0)):.6f} BTC</div></div>
        </div>
        <p class="card__detail">Risk budget: ${float(risk_profile.get('risk_per_trade_usd', 0)):,.2f} · Notional: ${float(risk_profile.get('position_size_usd', 0)):,.2f}</p>
    </div>
    """


def placeholder_data_panel(title: str, payload: dict) -> str:
    rows = []
    for key, info in (payload or {}).items():
        if not isinstance(info, dict):
            continue
        status = html.escape(str(info.get("status", "unavailable")))
        message = html.escape(str(info.get("message") or info.get("provider") or ""))
        rows.append(
            f"""
            <div class="placeholder-row">
                <strong>{html.escape(key.replace('_', ' ').title())}</strong>
                <span class="hub-status hub-status--{status}">{status.upper()}</span>
                <div class="card__detail">{message}</div>
            </div>
            """
        )
    body = "".join(rows) or "<p class='card__detail'>No data available.</p>"
    return f"""
    <div class="card card--elevated card--prose">
        <div class="card__label">{html.escape(title)}</div>
        {body}
    </div>
    """


def platform_gate_panel(checks: dict) -> str:
    if not checks:
        return empty_state(
            title="Platform checks pending",
            description="Run analysis to validate all Bitcoin data sources.",
            compact=True,
        )

    rows = []
    for item in checks.get("checks") or []:
        passed = item.get("passed")
        icon = "✓" if passed else "✗"
        tone = "long" if passed else "short"
        rows.append(
            f"""
            <div class="checklist__item checklist--{'positive' if passed else 'negative'}">
                <span class="checklist__icon">{icon}</span>
                <span><strong>{html.escape(str(item.get('platform', '')))}</strong> — {html.escape(str(item.get('detail', '')))}</span>
            </div>
            """
        )

    passed = checks.get("passed")
    summary = checks.get("passed_count", 0)
    total = checks.get("total", 0)
    gate_tone = "long" if passed else "short"
    gate_label = "APPROVED" if passed else "BLOCKED"

    return f"""
    <div class="card card--elevated card--tone-{gate_tone}">
        <div class="card__label">Platform Gate — {gate_label} ({summary}/{total})</div>
        <p class="card__detail">One minimal check per source — Binance, exchanges, Coinglass, Fear &amp; Greed, News, On-chain, Whales.</p>
        <ul class="checklist__list">{''.join(rows)}</ul>
    </div>
    """


def trade_variant_heading(name: str, *, grade: str, allowed: bool, risk_pct: float, message: str) -> str:
    tone = "long" if allowed else "wait"
    status = "ACTIVE" if allowed else "INACTIVE"
    return f"""
    <div class="card card--elevated card--tone-{tone}" style="margin-top: 1.25rem;">
        <div class="card__label">Trade — {html.escape(name)} · {html.escape(status)} · Grade {html.escape(grade)} · Risk {risk_pct:.2f}%</div>
        <p class="card__detail">{html.escape(message)}</p>
    </div>
    """
```

---

<a id="file-src-ui-sidebar-py"></a>
## File: `src\ui\sidebar.py`


```python
"""Sidebar settings — no visible sidebar UI (analysis runs automatically after login)."""

from __future__ import annotations

import os
from dataclasses import dataclass

__all__ = ["SidebarSettings", "AUTO_REFRESH_SECONDS", "render_sidebar"]

AUTO_REFRESH_SECONDS = 60
AUTO_TIMEFRAME = "1m"
DEFAULT_ACCOUNT_SIZE = 10_000.0
DEFAULT_MAX_RISK_PCT = 1.0


@dataclass
class SidebarSettings:
    symbol: str
    interval: str
    api_key: str
    dark_mode: bool
    analyze_clicked: bool
    auto_refresh: bool
    refresh_seconds: int
    risk_settings: dict[str, float]


def render_sidebar() -> SidebarSettings:
    """Return dashboard configuration (sidebar hidden in UI)."""
    return SidebarSettings(
        symbol="BTCUSDT",
        interval=AUTO_TIMEFRAME,
        api_key=os.getenv("COINGLASS_API_KEY", ""),
        dark_mode=True,
        analyze_clicked=False,
        auto_refresh=True,
        refresh_seconds=AUTO_REFRESH_SECONDS,
        risk_settings={
            "max_risk_pct": DEFAULT_MAX_RISK_PCT,
            "account_size": DEFAULT_ACCOUNT_SIZE,
        },
    )
```

---

<a id="file-src-ui-styles-py"></a>
## File: `src\ui\styles.py`


```python
"""Global CSS — light/dark themes via CSS variables."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from src.ui.background import build_background_css, build_bitcoin_fallback_css, build_streamlit_surface_css, ensure_assets_dir
from src.ui.theme import FONT, RADIUS, SHADOW, SPACING, get_palette

# Project root (btc-market-analyzer/) — used for assets/background.jpg
_DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[2]


def inject_global_styles(
    *,
    dark_mode: bool = True,
    project_root: Path | None = None,
    hide_sidebar: bool = False,
) -> None:
    root = project_root or _DEFAULT_PROJECT_ROOT
    ensure_assets_dir(root)

    p = get_palette(dark_mode)
    background_css, has_background = build_background_css(root)
    if not has_background:
        background_css = build_bitcoin_fallback_css(dark_mode=dark_mode)
    surface_css = build_streamlit_surface_css()

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {{
            --bg: {p['bg']};
            --surface: {p['surface']};
            --surface-alt: {p['surface_alt']};
            --border: {p['border']};
            --text: {p['text']};
            --text-secondary: {p['text_secondary']};
            --text-muted: {p['text_muted']};
            --accent: {p['accent']};
            --accent-hover: {p['accent_hover']};
            --accent-soft: {p['accent_soft']};
            --long: {p['long']};
            --short: {p['short']};
            --wait: {p['wait']};
            --long-bg: {p['long_bg']};
            --short-bg: {p['short_bg']};
            --wait-bg: {p['wait_bg']};
            --long-border: {p['long_border']};
            --short-border: {p['short_border']};
            --wait-border: {p['wait_border']};
            --error-bg: {p['error_bg']};
            --error-border: {p['error_border']};
            --error-text: {p['error_text']};
            --space-xs: {SPACING['xs']};
            --space-sm: {SPACING['sm']};
            --space-md: {SPACING['md']};
            --space-lg: {SPACING['lg']};
            --space-xl: {SPACING['xl']};
            --radius: {RADIUS['md']};
            --radius-sm: {RADIUS['sm']};
            --radius-lg: {RADIUS['lg']};
            --radius-full: {RADIUS['full']};
            --shadow: {SHADOW['sm']};
            --shadow-md: {SHADOW['md']};
            --shadow-lg: {SHADOW['lg']};
            --font: {FONT['sans']};
            --font-display: {FONT['display']};
            --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
        }}

        .stApp {{
            background: var(--bg);
            font-family: var(--font);
            color: var(--text);
            overflow-x: clip;
        }}

        {background_css}

        {surface_css}

        .block-container {{
            padding-top: clamp(0.5rem, 2vw, 1rem);
            padding-bottom: clamp(1.25rem, 4vw, 2.5rem);
            padding-left: clamp(0.75rem, 3vw, 1.5rem);
            padding-right: clamp(0.75rem, 3vw, 1.5rem);
            max-width: 1240px;
            margin-left: auto;
            margin-right: auto;
        }}

        .dashboard-shell {{
            width: 100%;
        }}

        .dashboard-panel {{
            background: linear-gradient(165deg, rgba(34, 22, 14, 0.82) 0%, rgba(18, 12, 8, 0.94) 100%);
            border: 1px solid rgba(247, 147, 26, 0.18);
            border-radius: var(--radius-lg);
            padding: clamp(1.125rem, 3vw, 1.75rem);
            margin-bottom: var(--space-md);
            box-shadow: var(--shadow-md);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }}

        .safety-banner {{
            text-align: center;
            font-family: var(--font-display);
            font-size: clamp(0.875rem, 2.2vw, 1.25rem);
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--accent);
            background: linear-gradient(135deg, rgba(247, 147, 26, 0.12) 0%, rgba(30, 20, 12, 0.75) 100%);
            border: 1px solid rgba(247, 147, 26, 0.28);
            border-radius: var(--radius);
            padding: clamp(0.625rem, 2vw, 0.875rem) clamp(1rem, 3vw, 1.5rem);
            margin: 0 0 var(--space-lg);
            box-shadow: var(--shadow);
        }}

        /* ── Premium sticky navigation ── */
        .premium-nav-outer {{
            margin-left: calc(50% - 50vw);
            margin-right: calc(50% - 50vw);
            width: 100vw;
            max-width: 100vw;
            box-sizing: border-box;
            position: sticky;
            top: 0;
            z-index: 999;
            margin-bottom: var(--space-lg);
        }}
        .premium-nav {{
            background: linear-gradient(165deg, rgba(45, 28, 16, 0.98) 0%, rgba(26, 17, 10, 0.99) 55%, rgba(12, 8, 5, 1) 100%);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35),
                        0 1px 0 rgba(247, 147, 26, 0.15) inset;
            border-bottom: 1px solid rgba(247, 147, 26, 0.22);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }}
        .premium-nav__inner {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: var(--space-lg);
            max-width: 1160px;
            margin: 0 auto;
            padding: clamp(1rem, 3vw, 1.375rem) clamp(1rem, 4vw, 1.5rem);
            box-sizing: border-box;
        }}
        .premium-nav__left {{
            display: flex;
            align-items: center;
            gap: 0.875rem;
            min-width: 0;
            flex: 1;
        }}
        .premium-nav__logo {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.4rem;
            width: auto;
            min-height: 2.75rem;
            padding: 0 0.875rem;
            flex-shrink: 0;
            border-radius: var(--radius-sm);
            background: rgba(247, 147, 26, 0.12);
            border: 1px solid rgba(247, 147, 26, 0.28);
            color: #f7931a;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .premium-nav__logo-symbol {{
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1;
        }}
        .premium-nav__logo-text {{
            font-size: 0.9375rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            line-height: 1;
            color: #FFF4E6;
        }}
        .premium-nav__logo:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(247, 147, 26, 0.2);
        }}
        .premium-nav__brand {{
            min-width: 0;
        }}
        .premium-nav__tagline {{
            font-family: var(--font);
            font-size: clamp(0.8125rem, 1.9vw, 0.9375rem);
            font-weight: 500;
            letter-spacing: 0.04em;
            line-height: 1.35;
            color: #D4A574;
            margin: 0.375rem 0 0;
            padding: 0;
            text-transform: none;
        }}
        .premium-nav__author {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.35rem 0.5rem;
            font-family: var(--font);
            font-size: clamp(0.75rem, 1.7vw, 0.8125rem);
            font-weight: 500;
            line-height: 1.45;
            color: #94a3b8;
            margin: 0.25rem 0 0;
            padding: 0;
            max-width: 100%;
        }}
        .premium-nav__author-name {{
            color: #cbd5e1;
            font-weight: 600;
        }}
        .premium-nav__subtitle {{
            display: none;
        }}
        .premium-nav__title {{
            font-family: var(--font-display);
            font-size: clamp(1.25rem, 3.2vw, 1.75rem);
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.15;
            color: #ffffff;
            margin: 0;
            padding: 0;
            white-space: normal;
            overflow: visible;
            text-overflow: unset;
        }}
        .premium-nav__meta {{
            display: none;
        }}
        .premium-nav__sep {{
            color: #475569;
            user-select: none;
        }}
        .premium-nav__link {{
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            color: #cbd5e1;
            text-decoration: none;
            transition: color 0.18s ease;
        }}
        .premium-nav__link:hover {{
            color: #ffffff;
            text-decoration: underline;
            text-underline-offset: 2px;
        }}
        .premium-nav__globe {{
            font-size: 0.8125em;
            line-height: 1;
        }}
        .premium-nav__version {{
            color: #64748b;
        }}
        .premium-nav__right {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 0.375rem;
            flex-shrink: 0;
        }}
        .premium-nav__status {{
            display: inline-flex;
            align-items: center;
            gap: 0.4375rem;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #e2e8f0;
        }}
        .status-dot {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            flex-shrink: 0;
        }}
        .status-dot--live {{
            background: #22c55e;
            box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.25);
            animation: pulse-dot 2s ease infinite;
        }}
        .status-dot--idle {{
            background: #64748b;
            box-shadow: 0 0 0 2px rgba(100, 116, 139, 0.25);
        }}
        @keyframes pulse-dot {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.55; }}
        }}
        .premium-nav__updated {{
            font-size: 0.6875rem;
            color: #64748b;
            text-align: right;
            line-height: 1.4;
            max-width: 14rem;
        }}
        .premium-nav__updated-label {{
            color: #94a3b8;
            font-weight: 500;
            margin-right: 0.25rem;
        }}
        .premium-nav__divider {{
            height: 2px;
            background: linear-gradient(
                90deg,
                transparent 0%,
                rgba(99, 102, 241, 0.5) 25%,
                rgba(247, 147, 26, 0.45) 50%,
                rgba(99, 102, 241, 0.5) 75%,
                transparent 100%
            );
        }}

        /* ── Layout spacing ── */
        .section-gap {{ height: var(--space-md); }}
        .section-gap--sm {{ height: var(--space-sm); }}
        .section-heading {{
            font-size: 0.9375rem;
            font-weight: 700;
            color: var(--text);
            margin: 0 0 var(--space-md);
            letter-spacing: 0.02em;
            display: flex;
            align-items: center;
            gap: 0.625rem;
        }}
        .section-heading::before {{
            content: "";
            width: 4px;
            height: 1.1em;
            border-radius: var(--radius-full);
            background: linear-gradient(180deg, var(--accent), var(--accent-hover));
            flex-shrink: 0;
        }}
        .section-heading--large::before {{
            height: 1.35em;
        }}
        .section-heading--tight {{
            margin: 0.15rem 0 0.35rem;
        }}
        .section-heading--large {{
            font-size: clamp(1.5rem, 4vw, 2.125rem);
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: var(--text);
            margin: 0.25rem 0 0.5rem;
        }}
        .ai-dashboard-top {{
            margin-bottom: 0;
        }}
        .ai-dashboard-top + [data-testid="stVerticalBlock"],
        .ai-dashboard-top ~ div {{
            margin-top: 0;
        }}
        .chart-tagline {{
            text-align: center;
            font-size: 0.8125rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--accent);
            margin: 0 0 var(--space-md);
            opacity: 0.9;
        }}
        .chart-bitcoin-logo {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .chart-bitcoin-logo--above {{
            margin: 0 0 var(--space-xs);
        }}
        .chart-bitcoin-logo--below {{
            margin: var(--space-md) 0 var(--space-lg);
        }}
        .chart-bitcoin-logo__svg {{
            width: 72px;
            height: 72px;
            filter: drop-shadow(0 6px 18px rgba(247, 147, 26, 0.35));
        }}
        .chart-bitcoin-brand {{
            text-align: center;
            margin: 0 0 var(--space-xl);
        }}
        .chart-bitcoin-brand__symbol {{
            font-size: 3.25rem;
            font-weight: 700;
            line-height: 1;
            color: var(--accent);
        }}
        .chart-bitcoin-brand__name {{
            margin-top: 0.35rem;
            font-size: 1.875rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            color: var(--text);
        }}
        .chart-bitcoin-brand__email {{
            display: inline-block;
            margin-top: 0.75rem;
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-decoration: none;
        }}
        .chart-bitcoin-brand__email:hover {{
            color: var(--accent);
            text-decoration: underline;
        }}

        /* ── Cards ── */
        .card-wrap {{
            height: 100%;
            display: flex;
        }}
        .card-wrap .card {{
            flex: 1;
            width: 100%;
        }}
        .card {{
            position: relative;
            overflow: hidden;
            background: linear-gradient(160deg, rgba(38, 24, 14, 0.96) 0%, rgba(22, 14, 9, 0.98) 100%);
            border: 1px solid rgba(247, 147, 26, 0.16);
            border-radius: var(--radius);
            padding: clamp(1rem, 2.5vw, 1.25rem) clamp(1rem, 2.5vw, 1.375rem);
            box-sizing: border-box;
            transition: transform 0.25s var(--ease-out), box-shadow 0.25s var(--ease-out), border-color 0.25s var(--ease-out);
        }}
        .card--elevated {{
            box-shadow: var(--shadow);
        }}
        .card--elevated:hover {{
            box-shadow: var(--shadow-md);
            transform: translateY(-3px);
            border-color: rgba(247, 147, 26, 0.32);
        }}
        .card__accent {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            opacity: 0.55;
        }}
        .card__accent--long {{ background: linear-gradient(90deg, transparent, var(--long), transparent); opacity: 1; }}
        .card__accent--short {{ background: linear-gradient(90deg, transparent, var(--short), transparent); opacity: 1; }}
        .card__accent--wait {{ background: linear-gradient(90deg, transparent, var(--wait), transparent); opacity: 1; }}
        .card--metric {{
            min-height: 6.5rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
        }}
        .card--component {{
            min-height: 9rem;
            margin-bottom: var(--space-sm);
        }}
        .card--tone-long {{ border-left: 3px solid var(--long); }}
        .card--tone-short {{ border-left: 3px solid var(--short); }}
        .card--tone-wait {{ border-left: 3px solid var(--wait); }}
        .card__label {{
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }}
        .card__value {{
            font-size: clamp(1.125rem, 2.8vw, 1.5rem);
            font-weight: 700;
            color: var(--text);
            line-height: 1.2;
            letter-spacing: -0.02em;
        }}
        .card--tone-long .card__value {{ color: var(--long); }}
        .card--tone-short .card__value {{ color: var(--short); }}
        .card--tone-wait .card__value {{ color: var(--wait); }}
        .card__suffix {{
            font-size: 0.6em;
            font-weight: 600;
            color: var(--text-muted);
        }}
        .card__detail {{
            font-size: 0.8125rem;
            color: var(--text-secondary);
            line-height: 1.55;
            margin: 0.375rem 0 0;
        }}
        .card--prose {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            line-height: 1.75;
            white-space: pre-wrap;
        }}

        /* ── Recommendation panel ── */
        .rec-panel {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.25rem 1.375rem;
            box-shadow: var(--shadow);
            min-height: 18rem;
            display: flex;
            flex-direction: column;
            gap: var(--space-md);
            align-items: stretch;
        }}
        .rec-panel--long {{ border-top: 4px solid var(--long); }}
        .rec-panel--short {{ border-top: 4px solid var(--short); }}
        .rec-panel--wait {{ border-top: 4px solid var(--wait); }}
        .signal-badge {{
            display: flex;
            align-items: center;
            justify-content: center;
            align-self: center;
            width: 100%;
            max-width: 16rem;
            padding: 0.85rem 1.25rem;
            border-radius: var(--radius-sm);
            font-size: clamp(1.75rem, 4vw, 2.25rem);
            font-weight: 800;
            letter-spacing: 0.14em;
            text-align: center;
        }}
        .signal-badge--long {{
            color: var(--long);
            background: var(--long-bg);
            border: 2px solid var(--long-border);
            box-shadow: 0 8px 24px rgba(5, 150, 105, 0.15);
        }}
        .signal-badge--short {{
            color: var(--short);
            background: var(--short-bg);
            border: 2px solid var(--short-border);
            box-shadow: 0 8px 24px rgba(220, 38, 38, 0.15);
        }}
        .signal-badge--wait {{
            color: var(--wait);
            background: var(--wait-bg);
            border: 2px solid var(--wait-border);
            box-shadow: 0 8px 24px rgba(217, 119, 6, 0.15);
        }}
        .signal-hero {{
            text-align: center;
            margin: 0 0 var(--space-sm);
            padding: 0;
        }}
        .signal-hero--panel {{
            background: linear-gradient(145deg, rgba(42, 26, 14, 0.85) 0%, rgba(24, 16, 10, 0.95) 100%);
            border: 1px solid rgba(247, 147, 26, 0.2);
            border-radius: var(--radius);
            padding: 1.25rem 1rem 1rem;
            box-shadow: var(--shadow-md);
            margin-bottom: var(--space-md);
        }}
        .signal-hero__row {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: clamp(1rem, 4vw, 2.5rem);
            flex-wrap: wrap;
        }}
        .signal-hero__stat {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.2rem;
            min-width: 7rem;
        }}
        .signal-hero__stat-label {{
            font-size: 0.625rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-muted);
        }}
        .signal-hero__stat-value {{
            font-size: clamp(1.125rem, 2.5vw, 1.5rem);
            font-weight: 800;
            color: var(--text);
            letter-spacing: -0.02em;
        }}
        .signal-hero__stat-suffix {{
            font-size: 0.55em;
            font-weight: 600;
            color: var(--text-muted);
        }}
        .signal-hero__stat--score .signal-hero__stat-value {{
            color: var(--accent);
        }}
        .signal-badge--hero {{
            flex-direction: column;
            gap: 0.35rem;
            max-width: 14rem;
            margin: 0 auto;
            padding: 1.1rem 1.5rem;
            font-size: clamp(2rem, 5vw, 2.75rem);
        }}
        .signal-badge__symbol {{
            font-size: 1.35em;
            line-height: 1;
        }}
        .signal-badge__label {{
            line-height: 1.1;
        }}
        .signal-hero__confidence {{
            margin: 0.4rem 0 0;
            font-size: 0.8125rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: var(--text-muted);
        }}
        .signal-hero__insight {{
            margin: 0.35rem auto 0;
            max-width: 36rem;
            font-size: 0.9375rem;
            line-height: 1.6;
            color: var(--text-secondary);
        }}
        .signal-hero__trader {{
            margin: 0.5rem auto 0;
            max-width: 36rem;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--accent);
        }}
        .rec-panel__badge {{
            display: none;
        }}
        .rec-panel__insight {{
            font-size: 0.9375rem;
            color: var(--text-secondary);
            line-height: 1.65;
            margin: 0;
            text-align: center;
        }}
        .rec-panel__conf-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.375rem;
        }}
        .rec-panel__conf-value {{
            font-size: 0.8125rem;
            font-weight: 600;
            color: var(--text);
        }}

        .signal-summary {{
            margin-top: 1rem;
            text-align: left;
            display: flex;
            flex-direction: column;
            gap: 0.625rem;
            width: 100%;
        }}
        .signal-summary__heading {{
            font-size: 0.6875rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-bottom: 0.125rem;
        }}
        .signal-summary__row {{
            padding: 0.75rem 0.875rem;
            background: var(--surface-alt);
            border-radius: var(--radius-sm);
            border: 1px solid var(--border);
        }}
        .signal-summary__label {{
            font-size: 0.6875rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            margin-bottom: 0.25rem;
        }}
        .signal-summary__text {{
            font-size: 0.875rem;
            line-height: 1.55;
            color: var(--text-secondary);
            margin: 0;
        }}

        .risk-alert {{
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
            padding: 0.75rem 0.875rem;
            border-radius: var(--radius-sm);
            background: var(--wait-bg);
            border: 1px solid var(--wait-border);
            color: var(--wait);
            font-size: 0.8125rem;
            line-height: 1.45;
        }}
        .risk-alert strong {{
            font-size: 0.875rem;
            font-weight: 700;
        }}
        .risk-alert--banner {{
            margin-bottom: var(--space-md);
        }}

        /* ── Progress bars ── */
        .progress-track {{
            background: var(--surface-alt);
            border-radius: var(--radius-sm);
            height: 5px;
            overflow: hidden;
        }}
        .progress-track--lg {{ height: 8px; }}
        .progress-fill {{
            height: 100%;
            border-radius: var(--radius-sm);
            transition: width 0.4s ease;
        }}
        .progress-fill--long {{ background: var(--long); }}
        .progress-fill--short {{ background: var(--short); }}
        .progress-fill--wait {{ background: var(--wait); }}

        /* ── State panels ── */
        .state-panel {{
            text-align: center;
            background: var(--surface);
            border-radius: var(--radius);
            padding: 2.5rem 1.5rem;
            border: 1px dashed var(--border);
        }}
        .state-panel--compact {{ padding: 1.5rem; }}
        .state-panel--error {{
            text-align: left;
            border: 1px solid var(--error-border);
            background: var(--error-bg);
            color: var(--error-text);
        }}
        .state-panel__icon {{ font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.7; }}
        .state-panel__title {{ font-size: 1rem; font-weight: 600; margin-bottom: 0.25rem; }}
        .state-panel__desc {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            line-height: 1.6;
            max-width: 28rem;
            margin: 0 auto;
        }}
        .state-panel--welcome {{
            padding: 2rem 1.5rem;
        }}
        .state-panel--logo-only {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 1.5rem 1rem;
        }}
        .state-panel--welcome .chart-bitcoin-logo__svg {{
            width: 112px;
            height: 112px;
        }}
        .state-panel--error .state-panel__desc {{ color: var(--error-text); margin: 0; }}

        /* ── Brand footer ── */
        .brand-footer {{
            text-align: center;
            padding: clamp(1rem, 3vw, 1.5rem);
            margin-top: var(--space-lg);
        }}
        .brand-footer__disclaimer {{
            font-size: 0.8125rem;
            font-weight: 600;
            color: var(--text-secondary);
            margin: 0 0 0.375rem;
        }}
        .brand-footer__meta {{
            font-size: 0.75rem;
            color: var(--text-muted);
            margin: 0.375rem 0 0;
        }}

        .brand-footer__meta--muted {{
            color: var(--text-muted);
            font-weight: 400;
        }}

        /* ── Data Hub ── */
        .hub-panel {{ width: 100%; }}
        .hub-summary__grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: var(--space-md);
        }}
        .hub-summary__value {{
            font-size: 0.9375rem;
            font-weight: 700;
            color: var(--text);
            margin-top: 0.35rem;
        }}
        .hub-source-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: var(--space-sm);
        }}
        .hub-source {{
            padding: 0.875rem 1rem;
            min-height: 5.5rem;
        }}
        .hub-source__head {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            margin-bottom: 0.35rem;
        }}
        .hub-source__name {{
            font-weight: 600;
            color: var(--text);
            font-size: 0.875rem;
        }}
        .hub-source__meta {{
            font-size: 0.75rem;
            color: var(--text-muted);
        }}
        .hub-source__error {{
            margin-top: 0.35rem;
            font-size: 0.6875rem;
            color: var(--text-secondary);
            line-height: 1.4;
        }}
        .hub-status {{
            font-size: 0.625rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            padding: 0.2rem 0.45rem;
            border-radius: var(--radius-full);
        }}
        .hub-status--online {{ background: var(--long-bg); color: var(--long); }}
        .hub-status--degraded {{ background: var(--wait-bg); color: var(--wait); }}
        .hub-status--offline {{ background: var(--short-bg); color: var(--short); }}
        .hub-status--placeholder {{ background: var(--surface-alt); color: var(--text-muted); }}

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {{
            background: var(--surface);
            border-right: 1px solid var(--border);
        }}
        .sidebar-label {{
            font-size: 0.6875rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            margin-bottom: 0.75rem;
        }}

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.35rem;
            background: rgba(18, 12, 8, 0.85);
            border: 1px solid rgba(247, 147, 26, 0.16);
            border-radius: var(--radius);
            padding: 0.4rem;
            margin-bottom: var(--space-lg);
            overflow-x: auto;
            overflow-y: hidden;
            flex-wrap: nowrap;
            scrollbar-width: none;
            -webkit-overflow-scrolling: touch;
        }}
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
            display: none;
        }}
        .stTabs [data-baseweb="tab"] {{
            font-family: var(--font);
            font-size: clamp(0.75rem, 2vw, 0.8125rem);
            font-weight: 600;
            letter-spacing: 0.03em;
            color: var(--text-secondary);
            padding: 0.6rem clamp(0.75rem, 2.5vw, 1.125rem);
            border-radius: calc(var(--radius-sm) - 2px);
            border: 1px solid transparent;
            background: transparent;
            white-space: nowrap;
            flex-shrink: 0;
            min-height: 40px;
            transition: color 0.2s var(--ease-out), background 0.2s var(--ease-out), box-shadow 0.2s var(--ease-out);
        }}
        .stTabs [data-baseweb="tab"]:hover {{
            color: var(--text);
            background: rgba(247, 147, 26, 0.1);
        }}
        .stTabs [aria-selected="true"] {{
            color: #fff !important;
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%) !important;
            border-color: rgba(255, 255, 255, 0.14) !important;
            box-shadow: 0 6px 18px rgba(247, 147, 26, 0.38) !important;
        }}
        .stTabs [data-baseweb="tab-panel"] {{
            padding-top: 0.35rem;
        }}
        .stTabs [data-baseweb="tab-highlight"] {{
            display: none !important;
        }}

        .chart-frame {{
            border-radius: var(--radius-lg);
            overflow: hidden;
            border: 1px solid rgba(247, 147, 26, 0.22);
            box-shadow: var(--shadow-lg);
            background: #0a0604;
        }}
        @media (max-width: 768px) {{
            .chart-frame {{
                border-radius: var(--radius);
            }}
        }}

        /* ── Buttons ── */
        .stButton > button {{
            min-height: 46px !important;
            border-radius: var(--radius-sm) !important;
            font-family: var(--font) !important;
            font-weight: 700 !important;
            letter-spacing: 0.02em !important;
            transition: transform 0.2s var(--ease-out), box-shadow 0.2s var(--ease-out), background 0.2s var(--ease-out) !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
        }}
        .stButton > button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"] {{
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent-hover) 100%) !important;
            color: #fff !important;
            border: none !important;
            box-shadow: 0 6px 20px rgba(247, 147, 26, 0.38) !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            background: linear-gradient(135deg, var(--accent-hover) 0%, #ffc04d 100%) !important;
            box-shadow: 0 8px 24px rgba(247, 147, 26, 0.45) !important;
        }}

        form[data-testid="stForm"] {{
            background: linear-gradient(160deg, rgba(34, 22, 14, 0.9) 0%, rgba(18, 12, 8, 0.95) 100%);
            border: 1px solid rgba(247, 147, 26, 0.2);
            border-radius: var(--radius-lg);
            padding: clamp(1.25rem, 4vw, 2rem);
            box-shadow: var(--shadow-md);
        }}
        form[data-testid="stForm"] [data-testid="stTextInput"] input {{
            background: rgba(8, 6, 4, 0.65) !important;
            border: 1px solid rgba(247, 147, 26, 0.22) !important;
            color: var(--text) !important;
        }}
        form[data-testid="stForm"] [data-testid="stTextInput"] input:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px rgba(247, 147, 26, 0.18) !important;
        }}

        [data-testid="stExpander"] {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
        }}

        [data-testid="stSelectbox"] label,
        [data-testid="stTextInput"] label,
        [data-testid="stSlider"] label,
        [data-testid="stNumberInput"] label,
        [data-testid="stToggle"] label {{
            font-size: 0.8125rem !important;
            color: var(--text-secondary) !important;
        }}

        [data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {{
            gap: 0.35rem;
        }}

        div[data-testid="stPlotlyChart"] {{
            margin-top: 0.25rem;
            margin-bottom: 0.25rem;
        }}

        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        /* Hide Streamlit Deploy button in the top header */
        [data-testid="stDeployButton"],
        .stAppDeployButton {{
            display: none !important;
            visibility: hidden !important;
        }}
        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        @media (max-width: 768px) {{
            .premium-nav__inner {{
                flex-direction: column;
                align-items: flex-start;
                gap: var(--space-md);
            }}
            .premium-nav__right {{
                flex-direction: row;
                align-items: center;
                justify-content: space-between;
                width: 100%;
                padding-top: 0.5rem;
                border-top: 1px solid rgba(255, 255, 255, 0.06);
            }}
            .premium-nav__updated {{
                text-align: left;
                max-width: none;
            }}
            .premium-nav__title {{
                white-space: normal;
            }}
            .rec-panel {{ min-height: auto; }}
            .hub-summary__grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .status-grid,
            .source-status-grid,
            .risk-panel__grid {{
                grid-template-columns: 1fr;
            }}
            .signal-hero__row {{
                flex-direction: column;
                gap: var(--space-md);
            }}
            .signal-badge--hero {{
                max-width: 100%;
            }}
            .overview-signal-only {{
                min-height: 12rem;
            }}
            .card--metric {{
                min-height: 5.5rem;
            }}
            [data-testid="column"] {{
                min-width: calc(50% - 0.5rem) !important;
            }}
        }}
        @media (max-width: 540px) {{
            [data-testid="column"] {{ min-width: 100% !important; }}
            .hub-summary__grid {{ grid-template-columns: 1fr; }}
            .chart-bitcoin-logo__svg {{
                width: 56px;
                height: 56px;
            }}
            .chart-bitcoin-brand__symbol {{
                font-size: 2.5rem;
            }}
            .chart-bitcoin-brand__name {{
                font-size: 1.5rem;
            }}
            .chart-bitcoin-brand__email {{
                font-size: 0.9375rem;
                word-break: break-all;
            }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            .progress-fill {{ transition: none; }}
            .status-dot--live {{ animation: none; }}
            .premium-nav__logo:hover {{ transform: none; }}
            .card:hover, .card--elevated:hover, .rec-panel:hover {{ transform: none; }}
        }}

        /* ── AI dashboard panels ── */
        .status-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: var(--space-md);
        }}
        .source-status-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: var(--space-sm);
        }}
        .source-pill {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            padding: 0.75rem 0.875rem;
        }}
        .source-pill__name {{
            font-size: 0.8125rem;
            font-weight: 600;
            color: var(--text);
        }}
        .trade-quality {{
            text-align: center;
            padding: 1.25rem;
        }}
        .trade-quality__grade {{
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1.1;
            margin: 0.25rem 0;
        }}
        .trade-quality__score {{
            font-size: 1rem;
            color: var(--text-secondary);
            margin-bottom: 0.35rem;
        }}
        .trade-quality__stars {{
            font-size: 1.25rem;
            letter-spacing: 0.15em;
            color: #fbbf24;
        }}
        .checklist__list {{
            list-style: none;
            margin: 0.5rem 0 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        .checklist__item {{
            display: flex;
            gap: 0.625rem;
            align-items: flex-start;
            font-size: 0.875rem;
            line-height: 1.5;
            color: var(--text-secondary);
            padding: 0.5rem 0.625rem;
            border-radius: var(--radius-sm);
            background: rgba(255, 255, 255, 0.02);
        }}
        .checklist--positive .checklist__icon {{ color: var(--long); font-weight: 700; }}
        .checklist--negative .checklist__icon {{ color: var(--wait); font-weight: 700; }}
        .news-panel__summary {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin: 0.35rem 0 0.75rem;
        }}
        .news-panel__list {{
            list-style: none;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        .news-item {{
            font-size: 0.8125rem;
            line-height: 1.45;
            color: var(--text-secondary);
            padding: 0.5rem 0;
            border-top: 1px solid var(--border);
        }}
        .news-item__source {{
            display: block;
            font-size: 0.6875rem;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 0.15rem;
        }}
        .news-item--positive {{ border-left: 3px solid var(--long); padding-left: 0.5rem; }}
        .news-item--negative {{ border-left: 3px solid var(--short); padding-left: 0.5rem; }}
        .risk-panel__grid {{
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: var(--space-md);
        }}
        .placeholder-row {{
            padding: 0.5rem 0;
            border-top: 1px solid var(--border);
        }}
        .card__value--sm {{
            font-size: 1.05rem !important;
        }}

        /* ── Overview tab ── */
        .overview-tab [data-testid="column"],
        .overview-tab [data-testid="stVerticalBlock"],
        .overview-tab [data-testid="stPlotlyChart"],
        .overview-tab [data-testid="stPlotlyChart"] > div,
        .overview-tab .js-plotly-plot,
        .overview-tab .plot-container {{
            background: transparent !important;
        }}
        .overview-tab .card,
        .overview-tab .rec-panel {{
            background: rgba(42, 26, 14, 0.72) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(247, 147, 26, 0.2) !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        }}
        .overview-tab .rec-panel {{
            min-height: auto;
        }}
        .overview-signal-only {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 18rem;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0;
        }}
        .overview-tab [data-testid="stHtml"] {{
            background: transparent !important;
        }}
        .overview-tab .progress-track {{
            background: rgba(255, 255, 255, 0.08) !important;
        }}

        /* ── Login gate ── */
        .login-gate {{
            display: flex;
            justify-content: center;
            margin: 1rem 0 1.25rem;
        }}
        /* Hide legacy login title panel / st.html white sandbox if it still appears */
        .login-gate__panel,
        .login-gate__title,
        .login-gate__subtitle,
        .login-gate__product,
        [data-testid="stHtml"]:empty {{
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            max-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            border: none !important;
            background: transparent !important;
        }}
        [data-testid="stHtml"] {{
            background: transparent !important;
        }}
        [data-testid="stHtml"] iframe {{
            background: transparent !important;
        }}
        .login-gate--below {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            margin: 2rem auto 1rem;
        }}
        .chart-bitcoin-logo--login {{
            display: flex;
            justify-content: center;
            margin: 2rem auto 1rem;
        }}
        .chart-bitcoin-logo--login .chart-bitcoin-logo__svg {{
            width: 220px;
            height: 220px;
            filter: drop-shadow(0 12px 32px rgba(247, 147, 26, 0.5));
        }}
        .login-gate--below .chart-bitcoin-logo {{
            margin: 0;
        }}
        .login-gate--below .chart-bitcoin-logo__svg {{
            width: 220px;
            height: 220px;
            filter: drop-shadow(0 12px 32px rgba(247, 147, 26, 0.5));
        }}
        .login-purchase {{
            width: 100%;
            max-width: 28rem;
            margin: 1.25rem auto 0;
            padding: clamp(1.125rem, 3vw, 1.5rem) !important;
            text-align: left;
        }}
        .login-purchase__title {{
            font-size: clamp(1.05rem, 2.8vw, 1.25rem);
            font-weight: 800;
            color: var(--text);
            margin: 0 0 0.75rem;
            letter-spacing: 0.02em;
        }}
        .login-purchase__price {{
            font-size: 1.0625rem;
            color: var(--accent);
            margin: 0 0 0.5rem;
        }}
        .login-purchase__price strong {{
            font-weight: 800;
        }}
        .login-purchase__line {{
            font-size: 0.9375rem;
            line-height: 1.55;
            color: var(--text-secondary);
            margin: 0 0 0.625rem;
        }}
        .login-purchase__wallet-block {{
            margin: 0.75rem 0;
            padding: 0.875rem 1rem;
            background: #ffffff !important;
            border: 2px solid #f7931a;
            border-radius: var(--radius-sm);
        }}
        .login-purchase__label {{
            display: block;
            font-size: 0.6875rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #5c3d1e !important;
            margin-bottom: 0.5rem;
        }}
        .login-purchase__wallet,
        .login-purchase__wallet-block code {{
            display: block;
            font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
            font-size: clamp(0.8125rem, 2.4vw, 0.9375rem);
            font-weight: 700;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            background: transparent !important;
            word-break: break-all;
            line-height: 1.5;
            user-select: all;
        }}
        .login-purchase__email {{
            color: var(--accent);
            font-weight: 600;
            text-decoration: none;
        }}
        .login-purchase__email:hover {{
            text-decoration: underline;
        }}
        .login-purchase__note {{
            font-size: 0.875rem;
            line-height: 1.55;
            color: var(--text-muted);
            margin: 0.75rem 0 0;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(247, 147, 26, 0.14);
        }}
        {'''
        [data-testid="stTextInput"] input {{
            min-height: 3.75rem !important;
            font-size: 1.25rem !important;
            padding: 1rem 1.25rem !important;
            border-radius: 0.75rem !important;
        }}
        [data-testid="stTextInput"] label {{
            font-size: 1rem !important;
            margin-bottom: 0.5rem !important;
        }}
        form[data-testid="stForm"] [data-testid="stFormSubmitButton"] > button {{
            min-height: 3.25rem !important;
            font-size: 1.0625rem !important;
        }}
        ''' if hide_sidebar else ''}
        {f'[data-testid="stSidebar"] {{ display: none !important; }}' if hide_sidebar else ''}
        {f'[data-testid="collapsedControl"] {{ display: none !important; }}' if hide_sidebar else ''}
        </style>
        """,
        unsafe_allow_html=True,
    )
```

---

<a id="file-src-ui-theme-py"></a>
## File: `src\ui\theme.py`


```python
"""Design tokens and theme palettes."""

from __future__ import annotations

APP_VERSION = "1.0"

BRAND = {
    "author_he": "אופיר קדוש",
    "author_en": "Ofir Kadosh",
    "since_year": "2026",
    "product": "AlphaBTC",
    "website": "https://alphabtctrading.com",
    "website_label": "alphabtctrading.com",
}


def brand_caption() -> str:
    """Author line shown under the app title."""
    return "AlphaBTC Private Project ( Don't bring anyone )"


# Bitcoin brand colors
BITCOIN_ORANGE = "#F7931A"
BITCOIN_ORANGE_DARK = "#E8820C"
BITCOIN_ORANGE_LIGHT = "#FFB84D"
BITCOIN_GOLD = "#F2A900"
BITCOIN_CREAM = "#FFF4E6"
BITCOIN_CREAM_SURFACE = "#FFFAF3"

LIGHT_PALETTE = {
    "bg": "#FFF4E6",
    "surface": "#FFFAF3",
    "surface_alt": "#FFEED9",
    "border": "#F5D5A8",
    "text": "#1A1108",
    "text_secondary": "#6B4423",
    "text_muted": "#9A7349",
    "accent": BITCOIN_ORANGE,
    "accent_hover": BITCOIN_ORANGE_DARK,
    "accent_soft": "#FFE8CC",
    "long": "#059669",
    "long_bg": "#ecfdf5",
    "long_border": "#a7f3d0",
    "short": "#dc2626",
    "short_bg": "#fef2f2",
    "short_border": "#fecaca",
    "wait": BITCOIN_GOLD,
    "wait_bg": "#FFF8E7",
    "wait_border": "#F5D58A",
    "error_bg": "#fef2f2",
    "error_border": "#fecaca",
    "error_text": "#991b1b",
    "heatmap_mid": BITCOIN_GOLD,
    "chart_grid": "#F5D5A8",
}

DARK_PALETTE = {
    "bg": "#080604",
    "surface": "#16100a",
    "surface_alt": "#22160e",
    "border": "#3d2a18",
    "text": "#FFF9F2",
    "text_secondary": "#E0B88A",
    "text_muted": "#A67C52",
    "accent": BITCOIN_ORANGE,
    "accent_hover": BITCOIN_ORANGE_LIGHT,
    "accent_soft": "rgba(247, 147, 26, 0.16)",
    "long": "#34d399",
    "long_bg": "rgba(6, 78, 59, 0.42)",
    "long_border": "#065f46",
    "short": "#f87171",
    "short_bg": "rgba(69, 10, 10, 0.42)",
    "short_border": "#7f1d1d",
    "wait": BITCOIN_GOLD,
    "wait_bg": "rgba(61, 46, 10, 0.5)",
    "wait_border": "#78550F",
    "error_bg": "#450a0a",
    "error_border": "#7f1d1d",
    "error_text": "#fecaca",
    "heatmap_mid": BITCOIN_ORANGE,
    "chart_grid": "#3d2818",
}

SPACING = {
    "xs": "0.5rem",
    "sm": "0.875rem",
    "md": "1.25rem",
    "lg": "1.75rem",
    "xl": "2.5rem",
}
RADIUS = {"sm": "12px", "md": "16px", "lg": "20px", "full": "999px"}
SHADOW = {
    "sm": "0 2px 10px rgba(0, 0, 0, 0.22), 0 1px 3px rgba(0, 0, 0, 0.14)",
    "md": "0 14px 36px rgba(0, 0, 0, 0.32), 0 0 0 1px rgba(247, 147, 26, 0.08)",
    "lg": "0 24px 56px rgba(0, 0, 0, 0.42), 0 0 0 1px rgba(247, 147, 26, 0.12)",
}
FONT = {
    "sans": "'Inter', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
    "display": "'Inter', 'Segoe UI', system-ui, sans-serif",
}

RECOMMENDATION_STYLE: dict[str, dict[str, str]] = {
    "long": {"label": "LONG", "symbol": "▲", "tone": "long"},
    "short": {"label": "SHORT", "symbol": "▼", "tone": "short"},
    "wait": {"label": "WAIT", "symbol": "◆", "tone": "wait"},
}

PLOTLY_CONFIG = {"displayModeBar": False, "responsive": True}


def get_palette(dark: bool = False) -> dict[str, str]:
    return DARK_PALETTE if dark else LIGHT_PALETTE


def score_tone(score: float) -> str:
    if score >= 62:
        return "long"
    if score <= 38:
        return "short"
    return "wait"


def score_color(score: float, dark: bool = False) -> str:
    palette = get_palette(dark)
    return palette[score_tone(score)]


def gauge_steps(dark: bool = False) -> list[dict]:
    palette = get_palette(dark)
    return [
        {"range": [0, 38], "color": palette["short_bg"]},
        {"range": [38, 62], "color": palette["wait_bg"]},
        {"range": [62, 100], "color": palette["long_bg"]},
    ]


def confidence_percent(confidence: str) -> int:
    return {"High": 85, "Medium": 62, "Low": 38}.get(confidence, 50)


def chart_layout(palette: dict[str, str]) -> dict:
    return {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {
            "family": "Inter, system-ui, sans-serif",
            "color": palette["text_secondary"],
            "size": 12,
        },
        "margin": {"l": 12, "r": 12, "t": 44, "b": 12},
        "xaxis": {"gridcolor": palette["chart_grid"], "zerolinecolor": palette["chart_grid"]},
        "yaxis": {"gridcolor": palette["chart_grid"], "zerolinecolor": palette["chart_grid"]},
    }
```

---

<a id="file-src-ui-time_utils-py"></a>
## File: `src\ui\time_utils.py`


```python
"""Datetime helpers for session state and UI display."""

from __future__ import annotations

from datetime import datetime


def normalize_last_updated(value: object) -> datetime | None:
    """Return a datetime from session state, or None if missing or invalid."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    return None


def format_last_updated(value: object) -> str:
    """Format timestamp for display; safe when value is None or invalid."""
    dt = normalize_last_updated(value)
    if dt is None:
        return "Not updated yet"
    return dt.strftime("%b %d, %Y · %H:%M UTC")
```

---

<a id="file-src-ui-tradingview-py"></a>
## File: `src\ui\tradingview.py`


```python
"""TradingView BTCUSDT chart embed for Streamlit."""

from __future__ import annotations

import html
import time

import streamlit.components.v1 as components

from src.ui.sidebar import AUTO_REFRESH_SECONDS

INTERVAL_MAP = {
    "1m": "1",
    "15m": "15",
    "1h": "60",
    "4h": "240",
    "1d": "D",
}

CHART_REFRESH_SECONDS = AUTO_REFRESH_SECONDS


def render_tradingview_chart(
    *,
    symbol: str = "BINANCE:BTCUSDT",
    interval: str = "1m",
    height: int | None = None,
    dark: bool = True,
    refresh_seconds: int = CHART_REFRESH_SECONDS,
    chart_id: str = "btc-live-chart",
) -> None:
    """Embed a live TradingView chart that reloads on a fixed interval."""
    chart_height = height if height is not None else 520
    tv_interval = INTERVAL_MAP.get(interval, "60")
    theme = "dark" if dark else "light"
    safe_chart_id = html.escape(chart_id, quote=True)

    iframe_src = (
        "https://s.tradingview.com/widgetembed/?"
        f"symbol={symbol}&interval={tv_interval}&hidesidetoolbar=0&"
        f"symboledit=0&saveimage=0&toolbarbg=f1f3f6&studies=[]&"
        f"theme={theme}&style=1&timezone=Etc%2FUTC&withdateranges=1&"
        "hidelegend=0&hidevolume=0&allow_symbol_change=0"
    )
    cache_bust = int(time.time() // max(refresh_seconds, 1))
    initial_src = f"{iframe_src}&_={cache_bust}"
    safe_src = html.escape(initial_src, quote=True)
    safe_base = html.escape(iframe_src, quote=True)

    components.html(
        f"""
        <div class="chart-frame" style="width:100%;height:{chart_height}px;overflow:hidden;">
            <iframe
                id="{safe_chart_id}"
                src="{safe_src}"
                style="width:100%;height:100%;border:0;"
                allow="fullscreen"
                loading="lazy"
            ></iframe>
        </div>
        <script>
            (function () {{
                var refreshMs = {int(refresh_seconds) * 1000};
                var baseSrc = "{safe_base}";
                var chartId = "{safe_chart_id}";
                setInterval(function () {{
                    var frame = document.getElementById(chartId);
                    if (!frame) return;
                    frame.src = baseSrc + "&_=" + Date.now();
                }}, refreshMs);
            }})();
        </script>
        """,
        height=chart_height + 8,
        scrolling=False,
    )
```

---
