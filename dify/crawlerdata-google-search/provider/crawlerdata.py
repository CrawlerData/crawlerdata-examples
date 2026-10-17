from typing import Any

import requests
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

API_URL = "https://api.crawlerdata.com/v1/jobs"


class CrawlerDataProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = credentials.get("api_key")
        if not api_key:
            raise ToolProviderCredentialValidationError("A CrawlerData API key is required.")
        try:
            # Cheapest real check: one autocomplete request (1 credit).
            res = requests.post(
                API_URL,
                headers={"Authorization": f"Bearer {api_key}"},
                json={"endpoint": "google-autocomplete", "params": {"query": "test", "country": "us"}, "queue": "live"},
                timeout=60,
            )
        except requests.RequestException as e:
            raise ToolProviderCredentialValidationError(f"Could not reach CrawlerData: {e}")
        if res.status_code == 401:
            raise ToolProviderCredentialValidationError("The CrawlerData API key was rejected.")
        if res.status_code == 402:
            raise ToolProviderCredentialValidationError("This CrawlerData account is out of credits.")
        if not res.ok:
            raise ToolProviderCredentialValidationError(f"CrawlerData returned HTTP {res.status_code}.")
