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
