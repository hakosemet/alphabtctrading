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
    height: int = 520,
    dark: bool = True,
    refresh_seconds: int = CHART_REFRESH_SECONDS,
    chart_id: str = "btc-live-chart",
) -> None:
    """Embed a live TradingView chart that reloads on a fixed interval."""
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
        <div style="width:100%;height:{height}px;overflow:hidden;border-radius:10px;">
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
        height=height + 8,
        scrolling=False,
    )
