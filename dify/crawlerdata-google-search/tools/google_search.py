from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools._client import run_job


class GoogleSearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials.get("api_key")
        if not api_key:
            yield self.create_text_message("A CrawlerData API key is required.")
            return
        query = tool_parameters.get("query", "")
        country = (tool_parameters.get("country") or "us").lower()
        limit = int(tool_parameters.get("max_results") or 8)
        try:
            data = run_job(api_key, "google-search", {"query": query, "country": country})
        except RuntimeError as e:
            yield self.create_text_message(str(e))
            return

        overview = data.get("ai_overview") if isinstance(data.get("ai_overview"), dict) else {}
        organic = [
            {"position": r.get("position"), "title": r.get("title") or "", "link": r.get("link") or "", "snippet": r.get("snippet") or ""}
            for r in (data.get("organic_results") or [])[:limit]
        ]
        sources = [{"title": s.get("title") or "", "link": s.get("link")} for s in (overview.get("sources") or []) if s.get("link")]
        questions = [q.get("question") for q in (data.get("people_also_ask") or []) if q.get("question")]

        lines = []
        if overview.get("text"):
            lines.append("Google AI Overview:\n" + overview["text"].strip())
            if sources:
                lines.append("AI Overview sources:\n" + "\n".join(f"- {s['title']} {s['link']}" for s in sources[:6]))
        for i, r in enumerate(organic, 1):
            lines.append(f"{i}. {r['title']}\n   {r['link']}\n   {r['snippet']}".rstrip())
        if questions:
            lines.append("Related questions: " + "; ".join(questions[:5]))

        yield self.create_text_message("\n\n".join(lines) or "No results.")
        yield self.create_json_message(
            {
                "query": query,
                "ai_overview": {"text": overview.get("text"), "sources": sources} if overview.get("text") else None,
                "organic_results": organic,
                "related_questions": questions,
            }
        )
