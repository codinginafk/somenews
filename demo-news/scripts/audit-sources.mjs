// Rigid source audit. Reads the ACTUAL frontmatter schema (sources[] +
// primarySourceUrl), not body markdown. Classifies every source URL by
// specificity so generic-homepage "citations" can't hide behind a link tag.
import { readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import matter from 'gray-matter';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const NEWS = join(ROOT, 'src', 'content', 'news');
const OUT = process.env.TEMP
  ? join(process.env.TEMP, 'opencode', 'source-audit.json')
  : join(ROOT, 'source-audit.json');

const GENERIC = new Set([
  '/', '/news', '/world', '/business', '/technology', '/tech', '/politics',
  '/sports', '/entertainment', '/health', '/science', '/money', '/latest',
  '/india', '/us', '/uk', '/en', '/home', '/index.html',
]);

function classify(raw) {
  let u;
  try { u = new URL(String(raw).trim()); } catch { return 'invalid'; }
  if (!/^https?:$/.test(u.protocol)) return 'invalid';
  const p = (u.pathname.replace(/\/+$/, '') || '/').toLowerCase();
  if (u.search) {
    if (/[?&](q|s|query|search)=/i.test(u.search)) return 'search';
    return 'deep';
  }
  if (p === '/' || GENERIC.has(p)) return 'homepage';
  const segs = p.split('/').filter(Boolean);
  if (segs.length === 0) return 'homepage';
  // Single-segment content pages such as /apps or /book are not homepages;
  // root paths and known section hubs are caught above.
  return 'deep';
}

const files = readdirSync(NEWS).filter(f => f.endsWith('.md')).sort();
const rows = [];
const urlCounts = new Map();
const domainCounts = new Map();
let badEncoding = [];

for (const f of files) {
  const raw = readFileSync(join(NEWS, f), 'utf8');
  const { data, content } = matter(raw);
  const sources = Array.isArray(data.sources) ? data.sources : [];
  const classes = sources.map(s => classify(s?.url));
  const primaryClass = data.primarySourceUrl ? classify(data.primarySourceUrl) : 'none';
  const deep = classes.filter(c => c === 'deep').length;
  const home = classes.filter(c => c === 'homepage').length;
  const search = classes.filter(c => c === 'search').length;
  const invalid = classes.filter(c => c === 'invalid').length;

  for (const s of sources) {
    const u = String(s?.url || '').trim();
    urlCounts.set(u, (urlCounts.get(u) || 0) + 1);
    try { domainCounts.set(new URL(u).hostname.replace(/^www\./, ''), (domainCounts.get(new URL(u).hostname.replace(/^www\./, '')) || 0) + 1); } catch {}
  }

  const text = [data.title, data.seoTitle, data.verdict, data.primarySource, ...sources.map(s => s?.title)].join(' ');
  if (text.includes('\uFFFD')) badEncoding.push(f);

  rows.push({
    slug: f.replace(/\.md$/, ''),
    title: data.title,
    sources: sources.length,
    deep, home, search, invalid,
    primaryClass,
    primarySource: data.primarySource || null,
    primarySourceUrl: data.primarySourceUrl || null,
    bodyLinks: (content.match(/\]\((https?:\/\/[^)]+)\)/g) || []).length,
    htmlLinks: (content.match(/<a\s[^>]*href=["']https?:\/\//gi) || []).length,
  });
}

const sum = (k) => rows.reduce((a, r) => a + r[k], 0);
const articlesWith = (pred) => rows.filter(pred).length;
const allHomepage = rows.filter(r => r.sources > 0 && r.deep === 0 && r.search === 0);
const zeroDeepNoPrimary = rows.filter(r => r.deep === 0 && r.primaryClass !== 'deep');
const noSources = rows.filter(r => r.sources === 0);
const thinSources = rows.filter(r => r.sources > 0 && r.sources < 3);
const duplicateUrls = [...urlCounts.entries()].filter(([, n]) => n > 1).sort((a, b) => b[1] - a[1]);

const report = {
  generatedAt: new Date().toISOString(),
  totals: {
    articles: rows.length,
    sourceEntries: sum('sources'),
    deep: sum('deep'), homepage: sum('home'), search: sum('search'), invalid: sum('invalid'),
    articlesZeroSources: noSources.length,
    articlesUnder3Sources: thinSources.length,
    articlesAllHomepageSources: allHomepage.length,
    articlesZeroDeepAndNoDeepPrimary: zeroDeepNoPrimary.length,
    uniqueSourceUrls: urlCounts.size,
    duplicateSourceUrls: duplicateUrls.length,
    badEncoding: badEncoding.length,
  },
  topDomains: [...domainCounts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 20),
  duplicateUrls: duplicateUrls.slice(0, 30),
  noSources: noSources.map(r => r.slug),
  allHomepage: allHomepage.map(r => r.slug),
  zeroDeepNoPrimary: zeroDeepNoPrimary.map(r => r.slug),
  badEncoding,
  rows,
};

writeFileSync(OUT, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report.totals, null, 2));
console.log('top domains:', report.topDomains.slice(0, 10));
console.log('duplicate URLs:', report.duplicateUrls.slice(0, 10));
console.log('zero sources:', noSources.length, noSources.map(r => r.slug).slice(0, 10));
console.log('all-homepage sources:', allHomepage.length, allHomepage.map(r => r.slug).slice(0, 15));
console.log('written:', OUT);
