# Google Shopping price tracker for Google Sheets

Track the lowest Google Shopping price for your products, straight from a spreadsheet. One Apps Script file adds a **CrawlerData** menu to Google Sheets: list your products, click **Check prices now**, and every check appends the lowest total price (price + shipping) across all sellers, the merchant offering it and the seller count to a History sheet. Turn on the daily check and you have a price history without any server.

> Uses the CrawlerData API, so you need an API key: [sign up](https://app.crawlerdata.com/register) for 50 free credits. Each product check costs 1 credit per 10 sellers returned (rounded up). Failed requests are not charged.

## Setup

1. Open your spreadsheet and go to **Extensions → Apps Script**.
2. Replace the editor contents with [`price-tracker.gs`](price-tracker.gs) and click **Save**.
3. Reload the spreadsheet. A **CrawlerData** menu appears (the first run asks you to authorize the script).
4. **CrawlerData → Set API key** and paste your key.
5. Add a sheet named **Products** with these headers in row 1:

| product_id | country | label |
|---|---|---|
| 11726664398501807381 | us | Sony WH-1000XM5 |
| 7580511071886337697 | us | Samsung Galaxy Buds3 FE |

6. **CrawlerData → Check prices now.** Results land in the **History** sheet:

| checked_at | label | product_id | country | lowest_total | currency | merchant | sellers_count | title | note |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-14 05:00 | Sony WH-1000XM5 | 11726664398501807381 | us | 191.53 | USD | eBay - firesale-deals | 22 | Sony WH-1000XM5 Noise Canceling Wireless Headphones | |

7. Optional: **CrawlerData → Check every day at 7:00** to build a daily price history (**Stop daily checks** turns it off).

## Finding product IDs

`product_id` is the Google Shopping product ID. Get it from the [Google Shopping scraper](https://github.com/CrawlerData/google-shopping-scraper) (every result has one) or from the `gpcid:` value in a Google Shopping URL. `country` is a two-letter code such as `us`, `gb`, `de`, `fr` or `au`.

## Ideas

- Add a chart on the History sheet (Insert → Chart, filtered by label) to see price trends.
- Use conditional formatting to highlight when `lowest_total` drops below your own price.
- For hundreds of products or minute-level schedules, use the async queue with a webhook instead: see the [API docs](https://app.crawlerdata.com/docs).
