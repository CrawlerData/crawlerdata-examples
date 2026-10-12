"""Google Search API: one live request. Set CRAWLERDATA_API_KEY first."""
import json
import os

import requests

res = requests.post(
    "https://api.crawlerdata.com/v1/jobs",
    headers={"Authorization": f"Bearer {os.environ['CRAWLERDATA_API_KEY']}"},
    json={
        "endpoint": "google-search",
        "params": {
            "query": "best crm software",
            "country": "us",
            "device": "desktop",
        },
        "queue": "live",
    },
    timeout=200,
)
res.raise_for_status()
data = res.json()
print(data["job"]["status"], data["job"].get("credits"))
print(json.dumps(data.get("result"), indent=2)[:2000])
