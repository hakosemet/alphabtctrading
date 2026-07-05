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
