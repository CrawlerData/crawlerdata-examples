# Open WebUI tool: CrawlerData Google Search

Gives your Open WebUI models live Google results: web search with Google's AI Overview and the pages it cites, related questions, and Google News.

1. Get an API key at https://app.crawlerdata.com (new accounts with a verified work email get 50 free credits; 1 credit per request).
2. In Open WebUI go to **Workspace → Tools → +**, paste `crawlerdata_google_search.py`, and save.
3. Open the tool's settings (Valves) and set `CRAWLERDATA_API_KEY`. Optionally set `COUNTRY` and `MAX_RESULTS`.
4. Enable the tool for a model or a chat. Functions: `google_search`, `google_news`.

Failed requests are not charged. API reference: https://crawlerdata.com/apis/google-search-api
