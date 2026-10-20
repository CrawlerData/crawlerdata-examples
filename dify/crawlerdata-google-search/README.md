# CrawlerData Google Search (Dify tool plugin)

Live Google results for your Dify apps, workflows and agents:

- **Google Search**: top organic results, Google's AI Overview with the pages it cites (when Google shows one), and related questions.
- **Google News**: recent articles with source, date and link.

## Setup

1. Create an API key at https://app.crawlerdata.com. New accounts with a verified work email get 50 free credits. One request costs 1 credit, and failed requests are not charged.
2. Install the plugin, open **Tools → CrawlerData → Authorize**, and paste the key.
3. Add the tool to a workflow, chatflow or agent.

## Connection requirements

- Outbound HTTPS from the Dify plugin daemon to `https://api.crawlerdata.com` (port 443). No inbound connections, no other hosts.
- A CrawlerData API key, entered once as the plugin credential `api_key`.
- Each tool call is one request: 1 credit. Failed requests are not charged.

## Contact and source

- Website: https://crawlerdata.com · API reference: https://crawlerdata.com/apis/google-search-api
- Source: https://github.com/CrawlerData/crawlerdata-examples/tree/main/dify/crawlerdata-google-search
- Support: contact@crawlerdata.com

See [PRIVACY.md](PRIVACY.md) for how requests are handled.
