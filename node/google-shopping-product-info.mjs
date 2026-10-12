// Google Shopping Product API: one live request. Node 18+. Set CRAWLERDATA_API_KEY first.
const res = await fetch('https://api.crawlerdata.com/v1/jobs', {
  method: 'POST',
  headers: { Authorization: `Bearer ${process.env.CRAWLERDATA_API_KEY}`, 'Content-Type': 'application/json' },
  body: JSON.stringify({
    "endpoint": "google-shopping-product-info",
    "params": {
      "product_id": "14580532573920022357",
      "country": "us"
    },
    "queue": "live"
  }),
});
if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
const { job, result } = await res.json();
console.log(job.status, job.credits);
console.log(JSON.stringify(result, null, 2).slice(0, 2000));
