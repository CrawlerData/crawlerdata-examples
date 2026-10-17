import requests

API_URL = "https://api.crawlerdata.com/v1/jobs"


def run_job(api_key: str, endpoint: str, params: dict) -> dict:
    """One live CrawlerData request; returns the `result` object. Raises RuntimeError with a readable message."""
    try:
        res = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={"endpoint": endpoint, "params": params, "queue": "live"},
            timeout=120,
        )
    except requests.RequestException as e:
        raise RuntimeError(f"Could not reach CrawlerData: {e}")
    if res.status_code == 401:
        raise RuntimeError("The CrawlerData API key was rejected.")
    if res.status_code == 402:
        raise RuntimeError("Out of CrawlerData credits. Top up at https://app.crawlerdata.com.")
    if not res.ok:
        raise RuntimeError(f"CrawlerData returned HTTP {res.status_code}.")
    return res.json().get("result") or {}
