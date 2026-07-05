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
