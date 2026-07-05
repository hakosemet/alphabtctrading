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
