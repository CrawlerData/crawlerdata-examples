#!/bin/sh
# Google Shopping API: one live request. Set CRAWLERDATA_API_KEY first.
curl -sS -X POST https://api.crawlerdata.com/v1/jobs \n  -H "Authorization: Bearer $CRAWLERDATA_API_KEY" \n  -H "Content-Type: application/json" \n  -d '{"endpoint":"google-shopping-search","params":{"query":"wireless headphones","country":"us"},"queue":"live"}'
