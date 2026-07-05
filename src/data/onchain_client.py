"""On-chain data client with optional API key providers."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import requests

from src.data.hub_models import SourceInfo

SUPPORTED_PROVIDERS = ("Glassnode", "CryptoQuant", "Arkham")


class OnChainClient:
    name = "On-Chain"

    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout
        self.glassnode_key = os.getenv("GLASSNODE_API_KEY", "").strip()
        self.cryptoquant_key = os.getenv("CRYPTOQUANT_API_KEY", "").strip()
        self.arkham_key = os.getenv("ARKHAM_API_KEY", "").strip()

    def fetch(self) -> tuple[dict[str, Any], SourceInfo]:
        payload: dict[str, Any] = {
            "exchange_inflows": self._field("Glassnode", self.glassnode_key),
            "exchange_outflows": self._field("Glassnode", self.glassnode_key),
            "active_addresses": self._field("Glassnode", self.glassnode_key),
            "miner_flows": self._field("CryptoQuant", self.cryptoquant_key),
            "stablecoin_flows": self._field("CryptoQuant", self.cryptoquant_key),
            "entity_labels": self._field("Arkham", self.arkham_key),
        }

        has_key = any([self.glassnode_key, self.cryptoquant_key, self.arkham_key])
        if has_key:
            payload = self._try_fetch_live(payload)

        if has_key and any(v.get("status") == "online" for v in payload.values()):
            status = "online"
            error = None
        elif has_key:
            status = "offline"
            error = "API keys present but live on-chain fetch failed or unsupported"
        else:
            status = "placeholder"
            error = "Unavailable — add API key (GLASSNODE_API_KEY, CRYPTOQUANT_API_KEY, ARKHAM_API_KEY)"

        info = SourceInfo(
            name=self.name,
            status=status,
            last_updated=datetime.now(timezone.utc),
            error=error,
            fields=list(payload.keys()),
        )
        return payload, info

    @staticmethod
    def _field(provider: str, api_key: str) -> dict[str, Any]:
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
            "message": f"{provider} key detected — live endpoint not wired yet",
        }

    def _try_fetch_live(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self.glassnode_key:
            try:
                response = requests.get(
                    "https://api.glassnode.com/v1/metrics/addresses/active_count",
                    params={"a": "BTC", "api_key": self.glassnode_key, "i": "24h"},
                    timeout=self.timeout,
                )
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        payload["active_addresses"] = {
                            "status": "online",
                            "value": data[-1].get("v"),
                            "provider": "Glassnode",
                        }
            except Exception:
                pass
        return payload
