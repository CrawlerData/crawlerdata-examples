from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._client import run_job


class GoogleNewsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials.get("api_key")
        if not api_key:
            yield self.create_text_message("A CrawlerData API key is required.")
            return
        query = tool_parameters.get("query", "")
        country = (tool_parameters.get("country") or "us").lower()
        limit = int(tool_parameters.get("max_results") or 8)
        try:
            data = run_job(api_key, "google-news", {"query": query, "country": country})
        except RuntimeError as e:
            yield self.create_text_message(str(e))
            return

        items = [
            {"title": n.get("title") or "", "source": n.get("source") or "", "date": n.get("date") or "", "link": n.get("link") or "", "snippet": n.get("snippet") or ""}
            for n in (data.get("news_results") or [])[:limit]
        ]
        lines = [f"{i}. {n['title']} ({n['source']}, {n['date']})\n   {n['link']}\n   {n['snippet']}".rstrip() for i, n in enumerate(items, 1)]
        yield self.create_text_message("\n\n".join(lines) or "No news found.")
        yield self.create_json_message({"query": query, "news_results": items})
