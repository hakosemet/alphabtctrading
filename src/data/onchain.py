"""On-chain data placeholders for future API integrations."""

from __future__ import annotations

from datetime import datetime, timezone

from src.data.hub_models import SourceInfo


class OnChainProvider:
    name = "On-Chain"

    def fetch(self) -> tuple[dict, SourceInfo]:
        payload = {
            "exchange_inflows": {"status": "placeholder", "value": None, "provider": "future API"},
            "exchange_outflows": {"status": "placeholder", "value": None, "provider": "future API"},
            "whale_transactions": {"status": "placeholder", "value": None, "provider": "future API"},
            "active_addresses": {"status": "placeholder", "value": None, "provider": "future API"},
            "miner_flows": {"status": "placeholder", "value": None, "provider": "future API"},
            "stablecoin_flows": {"status": "placeholder", "value": None, "provider": "future API"},
        }
        info = SourceInfo(
            name=self.name,
            status="placeholder",
            last_updated=datetime.now(timezone.utc),
            error="On-chain APIs not yet connected",
            fields=list(payload.keys()),
        )
        return payload, info
