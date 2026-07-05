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
