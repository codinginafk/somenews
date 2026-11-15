// GA4 report pull for rentfreenews.com.
//
// Usage:
//   node scripts/ga4-report.mjs <PROPERTY_ID> [startDate] [endDate]
//
// Credentials: the service account in
//   %USERPROFILE%\LiveDashboardofSite\gcp-service-account.json
// The service account must be a Viewer on the GA4 property.
//
// The Analytics Data API and Analytics Admin API are enabled on project
// opencode-project-498612. If the token reports "insufficient permissions
// for this property", add the service account
//   praveen-opencode-setup@opencode-project-498612.iam.gserviceaccount.com
// to the property under GA4 > Admin > Property access management.
//
// A numeric property ID is required. GA4 rejects a measurement ID with
// "Invalid property ID". The ID is shown in GA4 under
// Admin > Property Settings > Property ID.

import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';

const KEY = join(homedir(), 'LiveDashboardofSite', 'gcp-service-account.json');
const PROJECT = 'opencode-project-498612';
const SCOPES = 'https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/cloud-platform';

const propertyId = process.argv[2];
if (!propertyId) {
  console.error('Usage: node scripts/ga4-report.mjs <PROPERTY_ID> [startDate] [endDate]');
  process.exit(1);
}
if (!/^\d+$/.test(propertyId)) {
  console.error(`Property ID must be numeric, got "${propertyId}".`);
  process.exit(1);
}
if (!existsSync(KEY)) {
  console.error(`Service account key not found at ${KEY}`);
  process.exit(1);
}

const startDate = process.argv[3] || '2026-09-23';
const endDate = process.argv[4] || '2026-11-13';

const token = execFileSync(
  'gcloud',
  ['auth', 'print-access-token', `--scopes=${SCOPES}`],
  { encoding: 'utf8' },
).trim();

async function call(url, body) {
  const res = await fetch(url, {
    method: body ? 'POST' : 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
      'x-goog-user-project': PROJECT,
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const json = await res.json();
  if (!res.ok) {
    console.error(`ERROR ${res.status}: ${json.error?.message || JSON.stringify(json)}`);
    process.exit(1);
  }
  return json;
}

const base = `https://analyticsdata.googleapis.com/v1beta/properties/${propertyId}`;

const totals = await call(`${base}:runReport`, {
  dateRanges: [{ startDate, endDate }],
  metrics: [
    { name: 'sessions' },
    { name: 'totalUsers' },
    { name: 'newUsers' },
    { name: 'screenPageViews' },
    { name: 'bounceRate' },
    { name: 'averageSessionDuration' },
  ],
  metricAggregations: ['TOTAL'],
});

const t = totals.totals?.[0]?.metricValues || [];
const names = ['sessions', 'totalUsers', 'newUsers', 'screenPageViews', 'bounceRate', 'avgSessionDuration'];
console.log(`\n=== GA4 totals ${startDate} to ${endDate} (property ${propertyId})`);
names.forEach((n, i) => console.log(`  ${n.padEnd(20)} ${t[i]?.value ?? 'n/a'}`));

const daily = await call(`${base}:runReport`, {
  dateRanges: [{ startDate, endDate }],
  dimensions: [{ name: 'date' }],
  metrics: [{ name: 'sessions' }, { name: 'screenPageViews' }],
  orderBys: [{ dimension: { dimensionName: 'date' } }],
  limit: '90',
});
console.log('\n=== daily');
for (const row of daily.rows || []) {
  console.log(`  ${row.dimensionValues[0].value}  sessions=${row.metricValues[0].value}  views=${row.metricValues[1].value}`);
}

const pages = await call(`${base}:runReport`, {
  dateRanges: [{ startDate, endDate }],
  dimensions: [{ name: 'pagePath' }],
  metrics: [{ name: 'screenPageViews' }, { name: 'sessions' }],
  limit: '25',
});
console.log('\n=== top pages by screen views');
for (const row of pages.rows || []) {
  console.log(`  ${String(row.metricValues[0].value).padStart(6)} views  ${String(row.metricValues[1].value).padStart(5)} sess  ${row.dimensionValues[0].value}`);
}

const sources = await call(`${base}:runReport`, {
  dateRanges: [{ startDate, endDate }],
  dimensions: [{ name: 'sessionSource' }, { name: 'sessionMedium' }],
  metrics: [{ name: 'sessions' }],
  limit: '15',
});
console.log('\n=== session source / medium');
for (const row of sources.rows || []) {
  console.log(`  ${String(row.metricValues[0].value).padStart(6)} sess  ${row.dimensionValues.map(d => d.value).join(' / ')}`);
}
