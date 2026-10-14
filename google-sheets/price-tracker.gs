/**
 * CrawlerData: Google Shopping price tracker for Google Sheets.
 *
 * Setup (2 minutes):
 *   1. In your spreadsheet: Extensions > Apps Script. Replace the editor contents with this file and save.
 *   2. Reload the spreadsheet. A "CrawlerData" menu appears.
 *   3. CrawlerData > Set API key (get one at https://app.crawlerdata.com, 50 free credits).
 *   4. Add a sheet named "Products" with headers in row 1: product_id | country | label
 *      (product_id is the Google Shopping product ID, e.g. 11726664398501807381; country is us, gb, de...).
 *   5. CrawlerData > Check prices now. Optional: CrawlerData > Check every day at 7:00.
 *
 * Every check appends one row per product to the "History" sheet: the lowest total price
 * (price + shipping) across all Google Shopping sellers, the merchant offering it, and the seller count.
 * Cost: 1 credit per 10 sellers returned per product (rounded up). Failed requests are not charged.
 */
const CRAWLERDATA_API = 'https://api.crawlerdata.com/v1/jobs';
const HISTORY_HEADERS = ['checked_at', 'label', 'product_id', 'country', 'lowest_total', 'currency', 'merchant', 'sellers_count', 'title', 'note'];

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('CrawlerData')
    .addItem('Check prices now', 'checkPrices')
    .addItem('Set API key', 'setApiKey')
    .addItem('Check every day at 7:00', 'installDailyTrigger')
    .addItem('Stop daily checks', 'removeDailyTrigger')
    .addToUi();
}

function setApiKey() {
  const ui = SpreadsheetApp.getUi();
  const res = ui.prompt('CrawlerData API key', 'Paste your API key from app.crawlerdata.com:', ui.ButtonSet.OK_CANCEL);
  if (res.getSelectedButton() !== ui.Button.OK) return;
  PropertiesService.getUserProperties().setProperty('CRAWLERDATA_API_KEY', res.getResponseText().trim());
  ui.alert('Saved. Now add your products to the "Products" sheet and run CrawlerData > Check prices now.');
}

function installDailyTrigger() {
  removeDailyTrigger();
  ScriptApp.newTrigger('checkPrices').timeBased().everyDays(1).atHour(7).create();
  SpreadsheetApp.getActive().toast('Prices will be checked every day around 7:00.');
}

function removeDailyTrigger() {
  ScriptApp.getProjectTriggers()
    .filter(function (t) { return t.getHandlerFunction() === 'checkPrices'; })
    .forEach(function (t) { ScriptApp.deleteTrigger(t); });
}

function checkPrices() {
  const key = PropertiesService.getUserProperties().getProperty('CRAWLERDATA_API_KEY');
  if (!key) throw new Error('Set your API key first: CrawlerData > Set API key');
  const ss = SpreadsheetApp.getActive();
  const products = ss.getSheetByName('Products');
  if (!products) throw new Error('Add a sheet named "Products" with headers: product_id | country | label');
  const history = ss.getSheetByName('History') || ss.insertSheet('History');
  if (history.getLastRow() === 0) history.appendRow(HISTORY_HEADERS);

  const rows = products.getDataRange().getValues().slice(1).filter(function (r) { return String(r[0]).trim(); });
  const checkedAt = Utilities.formatDate(new Date(), ss.getSpreadsheetTimeZone(), 'yyyy-MM-dd HH:mm');
  // Up to 10 products per batch, fetched in parallel. The live queue returns the result in the response.
  for (let i = 0; i < rows.length; i += 10) {
    const batch = rows.slice(i, i + 10);
    const responses = UrlFetchApp.fetchAll(batch.map(function (r) { return buildRequest_(key, r[0], r[1]); }));
    const out = batch.map(function (r, j) {
      let body = null;
      try { body = JSON.parse(responses[j].getContentText()); } catch (e) { /* not JSON */ }
      return historyRow_(checkedAt, r[2], String(r[0]).trim(), String(r[1] || 'us').trim().toLowerCase(), responses[j].getResponseCode(), body);
    });
    history.getRange(history.getLastRow() + 1, 1, out.length, HISTORY_HEADERS.length).setValues(out);
  }
  ss.toast('Checked ' + rows.length + ' product(s). See the History sheet.');
}

function buildRequest_(key, productId, country) {
  return {
    url: CRAWLERDATA_API,
    method: 'post',
    contentType: 'application/json',
    muteHttpExceptions: true,
    headers: { Authorization: 'Bearer ' + key },
    payload: JSON.stringify({
      endpoint: 'google-shopping-product',
      params: { product_id: String(productId).trim(), country: String(country || 'us').trim().toLowerCase() },
      queue: 'live',
    }),
  };
}

/** One History row from an API response (pure function: no Apps Script services used). */
function historyRow_(checkedAt, label, productId, country, httpStatus, body) {
  const row = function (lowest, currency, merchant, count, title, note) {
    return [checkedAt, label || '', productId, country, lowest, currency, merchant, count, title, note];
  };
  if (!body || httpStatus >= 400) {
    const msg = body && body.error && body.error.message ? body.error.message : 'HTTP ' + httpStatus;
    return row('', '', '', '', '', 'error: ' + msg);
  }
  if (!body.job || body.job.status !== 'completed' || !body.result) {
    return row('', '', '', '', '', 'request failed (not charged)');
  }
  const result = body.result;
  if (!result.product) return row('', '', '', 0, '', 'product not found: check the product_id and country');
  const sellers =(result.sellers || []).filter(function (s) { return s.total_price && typeof s.total_price.value === 'number'; });
  if (!sellers.length) return row('', '', '', result.sellers_count || 0, result.product ? result.product.title : '', 'no sellers with a price');
  sellers.sort(function (a, b) { return a.total_price.value - b.total_price.value; });
  const best = sellers[0];
  return row(best.total_price.value, best.total_price.currency, best.merchant, result.sellers_count || sellers.length,
             result.product ? result.product.title : '', '');
}
