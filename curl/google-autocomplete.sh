#!/bin/sh
# Google Autocomplete API: one live request. Set CRAWLERDATA_API_KEY first.
curl -sS -X POST https://api.crawlerdata.com/v1/jobs \n  -H "Authorization: Bearer $CRAWLERDATA_API_KEY" \n  -H "Content-Type: application/json" \n  -d '{"endpoint":"google-autocomplete","params":{"query":"running sho","country":"us"},"queue":"live"}'
