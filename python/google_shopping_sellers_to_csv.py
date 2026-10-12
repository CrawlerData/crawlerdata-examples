# Scrape every seller's price for a Google Shopping product into a CSV.
# Usage: CRAWLERDATA_API_KEY=... python google_shopping_sellers_to_csv.py "sony wh-1000xm5" us
# Walkthrough: https://crawlerdata.com/blog/scrape-google-shopping-prices-python

import csv
import os
import sys
import time

import requests

API_URL = "https://api.crawlerdata.com/v1/jobs"
API_KEY = os.environ["CRAWLERDATA_API_KEY"]
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


class CrawlerDataError(Exception):
    pass


def run_job(endpoint, params, retries=2):
    """Run one live job and return its result. Retries failed jobs and 429/5xx."""
    body = {"endpoint": endpoint, "params": params, "queue": "live"}
    error = None
    for attempt in range(retries + 1):
        try:
            resp = requests.post(API_URL, json=body, headers=HEADERS, timeout=200)
        except requests.RequestException as exc:
            error = f"network error: {exc}"
        else:
            if resp.status_code in (400, 401, 402):
                # Bad params, bad key or no credits: retrying will not help.
                raise CrawlerDataError(f"HTTP {resp.status_code}: {resp.json()['error']['message']}")
            if resp.status_code == 429 or resp.status_code >= 500:
                error = f"HTTP {resp.status_code}"
            else:
                resp.raise_for_status()
                data = resp.json()
                if data["job"]["status"] == "completed":
                    return data["result"]
                error = data["job"]["error"]  # failed jobs cost 0 credits
        if attempt < retries:
            time.sleep(5 * 2 ** attempt)
    raise CrawlerDataError(f"{endpoint} failed after {retries + 1} attempts: {error}")


def search(query, country="us"):
    result = run_job("google-shopping-search", {"query": query, "country": country})
    return result.get("shopping_results", [])


def sellers(product_id, country="us"):
    result = run_job("google-shopping-product", {"product_id": product_id, "country": country})
    if result.get("error"):
        raise CrawlerDataError(f"{product_id}: {result['error']}")
    return result


def value(money):
    return money["value"] if money else None


def write_csv(path, result):
    fields = ["position", "merchant", "merchant_rating", "price", "shipping",
              "total_price", "currency", "availability", "delivery", "offer_title"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for s in result["sellers"]:
            writer.writerow({
                "position": s["position"],
                "merchant": s["merchant"],
                "merchant_rating": s["merchant_rating"],
                "price": value(s["price"]),
                "shipping": value(s["shipping"]),
                "total_price": value(s["total_price"]),
                "currency": (s["total_price"] or s["price"] or {}).get("currency"),
                "availability": s["availability"],
                "delivery": s["delivery"],
                "offer_title": s["offer_title"],
            })


def main():
    query = sys.argv[1]
    country = sys.argv[2] if len(sys.argv) > 2 else "us"

    products = search(query, country)
    if not products:
        sys.exit(f"No Google Shopping results for {query!r} in {country}")
    for p in products[:5]:
        price = p["price"]["raw"] if p["price"] else "n/a"
        print(f'{p["position"]:>2}  {p["product_id"]}  {price:>10}  {p["title"][:60]}')

    product = products[0]
    result = sellers(product["product_id"], country)
    path = f'sellers_{product["product_id"]}_{country}.csv'
    write_csv(path, result)
    print(f'\n{result["sellers_count"]} sellers for "{result["product"]["title"]}" -> {path}')


if __name__ == "__main__":
    main()
