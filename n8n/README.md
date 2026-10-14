# n8n workflow templates

Ready-to-import n8n workflows built on the CrawlerData API. In n8n: **Workflows → Import from file**, pick a JSON file, then add your credentials.

> Uses the CrawlerData API, so you need an API key: [sign up](https://app.crawlerdata.com/register) for 50 free credits.

| Workflow | What it does | Credits per run |
|---|---|---|
| [`google-shopping-prices-to-google-sheets.json`](google-shopping-prices-to-google-sheets.json) | Every day, searches Google Shopping for your products and appends the top 5 offers (merchant, price, product ID) to a Google Sheet. | 1 per search |
| [`daily-rank-tracker-to-google-sheets.json`](daily-rank-tracker-to-google-sheets.json) | Daily rank tracker: your domain's organic position per keyword, country and device, plus whether Google's AI Overview cites you. One row per keyword in a Google Sheet. | 1 per keyword |
| [`ai-overview-monitor-to-slack.json`](ai-overview-monitor-to-slack.json) | Every morning, checks your keywords for a Google AI Overview and posts to Slack whether it cites your domain, with the sources it cites. | 1 per keyword |

## Credentials

1. **CrawlerData API key**: create an *HTTP Header Auth* credential named `CrawlerData API key` with header name `Authorization` and value `Bearer YOUR_API_KEY`, and select it in the CrawlerData node.
2. **Google Sheets** (sheet workflows): connect your Google account in the *Append to Google Sheets* node and paste your spreadsheet URL. The sheet tab names are `Prices` and `Rankings`; the columns are created from the data.
3. **Slack** (AI Overview monitor): create an [incoming webhook](https://api.slack.com/messaging/webhooks) for your channel and paste its URL into the *Post to Slack* node.

Edit the list in the first Code node (products, keywords, countries, your domain), click **Test workflow**, then activate it to run on the schedule.

## Sample output

Rank tracker row:

```json
{ "date": "2026-10-14", "keyword": "running shoes", "country": "us", "device": "mobile", "domain": "nike.com",
  "position": 2, "url": "https://www.nike.com/w/running-shoes-37v7jzy7ok", "ai_overview": "yes", "ai_overview_cites_you": "yes" }
```

AI Overview report in Slack:

```
Google AI Overview report, 2026-10-14
• best crm for small business (us): AI Overview does not cite hubspot.com ❌ (sources: slack.com, uschamber.com, fayedigital.com, reddit.com)
• running shoes (us): AI Overview cites nike.com ✅ (sources: nike.com, adidas.com, amazon.com)
```
