"""TTL cache + parallel fetch for slow enrichment feeds (Fear/Greed, news, on-chain, whales)."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, TypeVar

from src.data.cache import TTLCache
from src.data.fear_greed import FearGreedClient
from src.data.hub_models import SourceInfo
from src.data.news_client import NewsClient
from src.data.onchain_client import OnChainClient
from src.data.whale_client import WhaleClient

T = TypeVar("T")

# Shared process cache — avoids duplicate HTTP calls between Streamlit reruns.
_ENRICHMENT_CACHE = TTLCache(default_ttl=120)

# Slower-moving feeds can stay cached longer than the 60s market refresh.
_FEED_TTLS: dict[str, int] = {
    "fear_greed": 300,
    "news": 180,
    "onchain": 600,
    "whale": 600,
}


def _cached_feed(name: str, fetcher: Callable[[], T]) -> T:
    """Return a cached feed payload or fetch and store it with a feed-specific TTL."""
    cached = _ENRICHMENT_CACHE.get(name)
    if cached is not None:
        return cached
    value = fetcher()
    _ENRICHMENT_CACHE.set(name, value, ttl=_FEED_TTLS.get(name, 120))
    return value


def _fetch_fear_greed() -> tuple[dict[str, Any], SourceInfo]:
    return FearGreedClient().fetch()


def _fetch_news() -> tuple[dict[str, Any], SourceInfo]:
    return NewsClient().fetch()


def _fetch_onchain() -> tuple[dict[str, Any], SourceInfo]:
    return OnChainClient().fetch()


def _fetch_whale() -> tuple[dict[str, Any], SourceInfo]:
    return WhaleClient().fetch()


def _safe_feed(
    name: str,
    fetcher: Callable[[], tuple[dict[str, Any], SourceInfo]],
) -> tuple[dict[str, Any], SourceInfo | None, Exception | None]:
    try:
        data, info = _cached_feed(name, fetcher)
        return data, info, None
    except Exception as exc:
        return {}, None, exc


def fetch_enrichment_feeds_parallel() -> dict[str, Any]:
    """Load all enrichment feeds concurrently; one failure does not block the others."""
    jobs = {
        "fear_greed": _fetch_fear_greed,
        "news": _fetch_news,
        "onchain": _fetch_onchain,
        "whale": _fetch_whale,
    }
    results: dict[str, Any] = {
        "fear_data": {},
        "fear_info": None,
        "news_data": {},
        "news_info": None,
        "onchain_data": {},
        "onchain_info": None,
        "whale_data": {},
        "whale_info": None,
        "errors": [],
    }

    with ThreadPoolExecutor(max_workers=4, thread_name_prefix="enrich") as pool:
        future_map = {
            pool.submit(_safe_feed, name, fetcher): name for name, fetcher in jobs.items()
        }
        for future in as_completed(future_map):
            name = future_map[future]
            data, info, error = future.result()
            if name == "fear_greed":
                results["fear_data"] = data
                results["fear_info"] = info
            elif name == "news":
                results["news_data"] = data
                results["news_info"] = info
            elif name == "onchain":
                results["onchain_data"] = data
                results["onchain_info"] = info
            elif name == "whale":
                results["whale_data"] = data
                results["whale_info"] = info
            if error is not None:
                results["errors"].append(f"{name}: {error}")

    return results
