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
