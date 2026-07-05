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
