"""
title: CrawlerData Google Search
author: CrawlerData
author_url: https://crawlerdata.com
git_url: https://github.com/CrawlerData/crawlerdata-examples
description: Live Google results for your model: web search with the AI Overview and its cited sources, plus Google News. Needs a CrawlerData API key (50 free credits on sign-up, 1 credit per request).
required_open_webui_version: 0.5.0
requirements: requests
version: 0.1.0
license: MIT
"""

import asyncio
from typing import Any, Awaitable, Callable, Optional

import requests
from pydantic import BaseModel, Field

API_URL = "https://api.crawlerdata.com/v1/jobs"


class Tools:
    class Valves(BaseModel):
        CRAWLERDATA_API_KEY: str = Field(
            default="",
            description="API key from https://app.crawlerdata.com (new accounts get 50 free credits).",
        )
        COUNTRY: str = Field(default="us", description="Two-letter country code for the results, e.g. us, gb, de.")
        MAX_RESULTS: int = Field(default=8, description="Maximum organic results or news items to return.")

    def __init__(self):
        self.valves = self.Valves()

    def _request(self, endpoint: str, params: dict) -> dict:
        if not self.valves.CRAWLERDATA_API_KEY:
            raise RuntimeError("Set CRAWLERDATA_API_KEY in this tool's settings (get a key at https://app.crawlerdata.com).")
        res = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {self.valves.CRAWLERDATA_API_KEY}"},
            json={"endpoint": endpoint, "params": params, "queue": "live"},
            timeout=120,
        )
        if res.status_code == 401:
            raise RuntimeError("The CrawlerData API key was rejected.")
        if res.status_code == 402:
            raise RuntimeError("Out of CrawlerData credits. Top up at https://app.crawlerdata.com.")
        res.raise_for_status()
        return res.json().get("result") or {}

    async def _status(self, emitter: Optional[Callable[[dict], Awaitable[None]]], text: str, done: bool) -> None:
        if emitter:
            await emitter({"type": "status", "data": {"description": text, "done": done}})

    async def google_search(
        self,
        query: str,
        __event_emitter__: Optional[Callable[[dict], Awaitable[None]]] = None,
    ) -> str:
        """
        Search Google and return the top results, Google's AI Overview with the pages it cites (when Google shows one),
        and related questions. Use for current facts, recent events, or anything you are unsure about.
        :param query: The search query.
        :return: Text summary of the Google results.
        """
        await self._status(__event_emitter__, f"Searching Google for: {query}", False)
        try:
            data = await asyncio.to_thread(self._request, "google-search", {"query": query, "country": self.valves.COUNTRY})
        except Exception as e:  # shown to the model so it can tell the user
            await self._status(__event_emitter__, "Google search failed", True)
            return f"Google search failed: {e}"

        lines: list[str] = []
        overview: Any = data.get("ai_overview")
        if isinstance(overview, dict) and overview.get("text"):
            lines.append("Google AI Overview:\n" + overview["text"].strip())
            sources = [s for s in overview.get("sources") or [] if s.get("link")]
            if sources:
                lines.append("AI Overview sources:\n" + "\n".join(f"- {s.get('title') or ''} {s['link']}" for s in sources[:6]))
        organic = data.get("organic_results") or []
        for i, r in enumerate(organic[: self.valves.MAX_RESULTS], 1):
            lines.append(f"{i}. {r.get('title') or ''}\n   {r.get('link') or ''}\n   {r.get('snippet') or ''}".rstrip())
        related = [q.get("question") for q in data.get("people_also_ask") or [] if q.get("question")]
        if related:
            lines.append("Related questions: " + "; ".join(related[:5]))

        await self._status(__event_emitter__, f"Found {len(organic)} Google results", True)
        return "\n\n".join(lines) or "No results."

    async def google_news(
        self,
        query: str,
        __event_emitter__: Optional[Callable[[dict], Awaitable[None]]] = None,
    ) -> str:
        """
        Search Google News for recent articles about a topic. Use for breaking news and anything from the last days.
        :param query: The news topic.
        :return: Text list of recent articles with source and date.
        """
        await self._status(__event_emitter__, f"Searching Google News for: {query}", False)
        try:
            data = await asyncio.to_thread(self._request, "google-news", {"query": query, "country": self.valves.COUNTRY})
        except Exception as e:
            await self._status(__event_emitter__, "Google News search failed", True)
            return f"Google News search failed: {e}"

        items = data.get("news_results") or []
        lines = [
            f"{i}. {n.get('title') or ''} ({n.get('source') or ''}, {n.get('date') or ''})\n   {n.get('link') or ''}\n   {n.get('snippet') or ''}".rstrip()
            for i, n in enumerate(items[: self.valves.MAX_RESULTS], 1)
        ]
        await self._status(__event_emitter__, f"Found {len(items)} news articles", True)
        return "\n\n".join(lines) or "No news found."
