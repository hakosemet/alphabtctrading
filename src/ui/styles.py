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
        .login-gate__panel {{
            text-align: center;
            width: 100%;
            max-width: 28rem;
            padding: clamp(1.25rem, 4vw, 2rem) !important;
        }}
        .login-gate__title {{
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--text);
            margin: 0.75rem 0 0.35rem;
        }}
        .login-gate__subtitle {{
            font-size: 0.9375rem;
            color: var(--text-secondary);
            margin: 0 0 0.5rem;
        }}
        .login-gate__panel .chart-bitcoin-logo__svg {{
            width: 96px;
            height: 96px;
        }}
        .login-gate--below {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            margin: 2rem auto 1rem;
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
            padding: 0.75rem 0.875rem;
            background: rgba(8, 6, 4, 0.55);
            border: 1px solid rgba(247, 147, 26, 0.22);
            border-radius: var(--radius-sm);
        }}
        .login-purchase__label {{
            display: block;
            font-size: 0.6875rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--text-muted);
            margin-bottom: 0.35rem;
        }}
        .login-purchase__wallet {{
            display: block;
            font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
            font-size: clamp(0.75rem, 2.2vw, 0.875rem);
            font-weight: 600;
            color: var(--text);
            word-break: break-all;
            line-height: 1.45;
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
