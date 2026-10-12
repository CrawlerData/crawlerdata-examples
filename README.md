# CrawlerData API examples

Copy-paste examples for the [CrawlerData API](https://crawlerdata.com): Google Shopping products, sellers and prices, plus Google Search, Images, News, Local and Autocomplete results as JSON.

Each example sends one `live` request to `POST https://api.crawlerdata.com/v1/jobs` and prints the result.

## Setup

1. Create an account at [app.crawlerdata.com](https://app.crawlerdata.com/register). Company emails get free trial credits.
2. Create an API key in the dashboard.
3. Export it:

```sh
export CRAWLERDATA_API_KEY=your_key
```

## Endpoints

| API | `endpoint` | Examples | Reference |
|---|---|---|---|
| Google Shopping API | `google-shopping-search` | [python](python/google_shopping_search.py) · [node](node/google-shopping-search.mjs) · [curl](curl/google-shopping-search.sh) | [docs](https://crawlerdata.com/apis/google-shopping-api) |
| Google Shopping Sellers API | `google-shopping-product` | [python](python/google_shopping_product.py) · [node](node/google-shopping-product.mjs) · [curl](curl/google-shopping-product.sh) | [docs](https://crawlerdata.com/apis/google-shopping-sellers-api) |
| Google Shopping Product API | `google-shopping-product-info` | [python](python/google_shopping_product_info.py) · [node](node/google-shopping-product-info.mjs) · [curl](curl/google-shopping-product-info.sh) | [docs](https://crawlerdata.com/apis/google-shopping-product-api) |
| Google Search API | `google-search` | [python](python/google_search.py) · [node](node/google-search.mjs) · [curl](curl/google-search.sh) | [docs](https://crawlerdata.com/apis/google-search-api) |
| Google Images API | `google-images` | [python](python/google_images.py) · [node](node/google-images.mjs) · [curl](curl/google-images.sh) | [docs](https://crawlerdata.com/apis/google-images-api) |
| Google News API | `google-news` | [python](python/google_news.py) · [node](node/google-news.mjs) · [curl](curl/google-news.sh) | [docs](https://crawlerdata.com/apis/google-news-api) |
| Google Local API | `google-local` | [python](python/google_local.py) · [node](node/google-local.mjs) · [curl](curl/google-local.sh) | [docs](https://crawlerdata.com/apis/google-local-api) |
| Google Autocomplete API | `google-autocomplete` | [python](python/google_autocomplete.py) · [node](node/google-autocomplete.mjs) · [curl](curl/google-autocomplete.sh) | [docs](https://crawlerdata.com/apis/google-autocomplete-api) |

Python examples need `requests` (`pip install requests`). Node examples need Node 18 or newer and no packages.

## Full scripts

- [`python/google_shopping_sellers_to_csv.py`](python/google_shopping_sellers_to_csv.py) searches Google Shopping, picks a product and writes every seller's price, shipping and total to CSV, with retries. Walkthrough: [How to scrape Google Shopping prices with Python](https://crawlerdata.com/blog/scrape-google-shopping-prices-python).

## Request shape

```json
{
  "endpoint": "google-shopping-search",
  "params": { "query": "wireless headphones", "country": "us" },
  "queue": "live"
}
```

- `queue`: `live` returns the result in the same response. `fast` and `regular` are async: poll `GET /v1/jobs/{id}` or pass a `postbackUrl` for a webhook. The price is the same on every queue.
- The response is `{ "job": { "id", "status", "credits", ... }, "result": { ... } }`. Failed jobs cost 0 credits.

## Pricing

1 credit per request, except Google Shopping sellers, which is 1 credit per 10 sellers returned (rounded up, minimum 1). From $1.00 per 1,000 credits down to $0.30 with larger packs, no subscription. See [pricing](https://crawlerdata.com/pricing).

## Links

- [Docs](https://app.crawlerdata.com/docs)
- [Blog](https://crawlerdata.com/blog)
- Questions: contact@crawlerdata.com

## License

MIT
