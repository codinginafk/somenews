// Full URL Inspection audit via the Search Console API.
// Inspects every article + key site pages and classifies Google's current
// index state. No sampling: 100% of published URLs.
import { readdirSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const NEWS = join(ROOT, 'src', 'content', 'news');
const TOKEN = process.env.GSC_TOKEN;
const SITE = 'sc-domain:rentfreenews.com';
const QUOTA = 'api-proj-1e067';
const OUT = process.env.TEMP
  ? join(process.env.TEMP, 'opencode', 'index-audit.json')
  : join(ROOT, 'index-audit.json');

if (!TOKEN) {
  console.error('GSC_TOKEN not set');
  process.exit(1);
}

const slugs = readdirSync(NEWS).filter(f => f.endsWith('.md')).map(f => f.replace(/\.md$/, '')).sort();
const urls = [
  'https://rentfreenews.com/',
  'https://rentfreenews.com/about/',
  'https://rentfreenews.com/contact/',
  'https://rentfreenews.com/corrections/',
  'https://rentfreenews.com/category/reality-check/',
  'https://rentfreenews.com/category/by-the-numbers/',
  'https://rentfreenews.com/category/countries/',
  'https://rentfreenews.com/category/lab-tested/',
  ...slugs.map(s => `https://rentfreenews.com/${s}/`),
];

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function inspect(url, attempt = 0) {
  const res = await fetch('https://searchconsole.googleapis.com/v1/urlInspection/index:inspect', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      'x-goog-user-project': QUOTA,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ inspectionUrl: url, siteUrl: SITE }),
  });
  if (res.status === 429 && attempt < 3) {
    await sleep(2000 * (attempt + 1));
    return inspect(url, attempt + 1);
  }
  const json = await res.json();
  if (!res.ok) return { url, error: json?.error?.message || `HTTP ${res.status}` };
  const i = json.inspectionResult?.indexStatusResult || {};
  return {
    url,
    verdict: i.verdict || null,
    coverageState: i.coverageState || null,
    robotsTxtState: i.robotsTxtState || null,
    indexingState: i.indexingState || null,
    pageFetchState: i.pageFetchState || null,
    lastCrawlTime: i.lastCrawlTime || null,
    googleCanonical: i.googleCanonical || null,
    userCanonical: i.userCanonical || null,
    crawledAs: i.crawledAs || null,
    referringUrls: i.referringUrls || [],
    mobileUsability: json.inspectionResult?.mobileUsabilityResult?.verdict || null,
    richResults: json.inspectionResult?.richResultsResult?.verdict || null,
  };
}

const results = [];
const CONCURRENCY = 5;
for (let i = 0; i < urls.length; i += CONCURRENCY) {
  const chunk = urls.slice(i, i + CONCURRENCY);
  const batch = await Promise.all(chunk.map(u => inspect(u)));
  results.push(...batch);
  writeFileSync(OUT, JSON.stringify({ partial: true, done: results.length, total: urls.length, results }, null, 2));
  console.error(`inspected ${Math.min(i + CONCURRENCY, urls.length)}/${urls.length}`);
  await sleep(120);
}

const byCoverage = {};
const byVerdict = {};
for (const r of results) {
  const c = r.error ? `ERROR: ${r.error}` : (r.coverageState || 'UNKNOWN');
  byCoverage[c] = (byCoverage[c] || 0) + 1;
  const v = r.error ? 'ERROR' : (r.verdict || 'UNKNOWN');
  byVerdict[v] = (byVerdict[v] || 0) + 1;
}

const report = {
  generatedAt: new Date().toISOString(),
  site: SITE,
  total: results.length,
  byVerdict,
  byCoverage,
  results,
};
writeFileSync(OUT, JSON.stringify(report, null, 2));
console.log(JSON.stringify({ total: results.length, byVerdict, byCoverage }, null, 2));
console.log('written:', OUT);
