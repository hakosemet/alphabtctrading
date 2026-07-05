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
