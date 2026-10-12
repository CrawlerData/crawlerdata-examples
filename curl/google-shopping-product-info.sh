#!/bin/sh
# Google Shopping Product API: one live request. Set CRAWLERDATA_API_KEY first.
curl -sS -X POST https://api.crawlerdata.com/v1/jobs \n  -H "Authorization: Bearer $CRAWLERDATA_API_KEY" \n  -H "Content-Type: application/json" \n  -d '{"endpoint":"google-shopping-product-info","params":{"product_id":"14580532573920022357","country":"us"},"queue":"live"}'
