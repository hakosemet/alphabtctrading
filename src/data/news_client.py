"""Crypto news RSS client with simple headline sentiment."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

try:
    import feedparser
except ImportError:
    feedparser = None

from src.analysis.sentiment import analyze_headline_sentiment, summarize_sentiment
from src.data.hub_models import SourceInfo

RSS_FEEDS: dict[str, str] = {
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "Cointelegraph": "https://cointelegraph.com/rss",
    "Bitcoin Magazine": "https://bitcoinmagazine.com/.rss/full/",
}


class NewsClient:
    name = "News RSS"

    def __init__(self, timeout: float = 12.0, max_items: int = 15) -> None:
        self.timeout = timeout
        self.max_items = max_items

    def fetch(self) -> tuple[dict[str, Any], SourceInfo]:
        headlines: list[dict[str, Any]] = []
        errors: list[str] = []

        if feedparser is None:
            data = {
                "status": "offline",
                "headlines": [],
                "summary": summarize_sentiment([]),
                "error": "feedparser not installed",
            }
            info = SourceInfo(
                name=self.name,
                status="offline",
                last_updated=datetime.now(timezone.utc),
                error="feedparser not installed",
                fields=["headlines", "sentiment"],
            )
            return data, info

        for source, url in RSS_FEEDS.items():
            try:
                parsed = feedparser.parse(url, request_headers={"User-Agent": "btc-market-analyzer/1.0"})
                for entry in (parsed.entries or [])[: self.max_items // len(RSS_FEEDS) + 3]:
                    title = str(getattr(entry, "title", "") or "").strip()
                    if not title:
                        continue
                    sentiment = analyze_headline_sentiment(title)
                    headlines.append(
                        {
                            "source": source,
                            "title": title,
                            "link": getattr(entry, "link", ""),
                            "sentiment": sentiment,
                        }
                    )
            except Exception as exc:
                errors.append(f"{source}: {exc}")

        headlines = headlines[: self.max_items]
        summary = summarize_sentiment(headlines)

        if headlines:
            status = "online"
            source_status = "online"
            error = "; ".join(errors) if errors else None
        else:
            status = "offline"
            source_status = "offline"
            error = "; ".join(errors) if errors else "No headlines fetched"

        data = {
            "status": status,
            "headlines": headlines,
            "summary": summary,
            "feeds": list(RSS_FEEDS.keys()),
            "error": error,
        }
        info = SourceInfo(
            name=self.name,
            status=source_status,
            last_updated=datetime.now(timezone.utc),
            error=error if source_status != "online" else None,
            fields=["headlines", "sentiment"],
        )
        return data, info
