"""News and sentiment placeholders for future API integrations."""

from __future__ import annotations

from datetime import datetime, timezone

from src.data.hub_models import SourceInfo


class NewsSentimentProvider:
    name = "News & Sentiment"

    def fetch(self) -> tuple[dict, dict, SourceInfo]:
        news = {
            "headlines": {"status": "placeholder", "items": [], "provider": "future crypto news API"},
            "macro_events": {"status": "placeholder", "items": [], "provider": "future macro calendar API"},
        }
        sentiment = {
            "fear_greed_index": {"status": "placeholder", "value": None, "provider": "future Fear & Greed API"},
            "social_sentiment": {"status": "placeholder", "value": None, "provider": "future social sentiment API"},
        }
        info = SourceInfo(
            name=self.name,
            status="placeholder",
            last_updated=datetime.now(timezone.utc),
            error="News and sentiment APIs not yet connected",
            fields=["headlines", "macro_events", "fear_greed_index", "social_sentiment"],
        )
        return news, sentiment, info
