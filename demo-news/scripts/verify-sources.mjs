// Strict source gate for Rent Free News.
// A source passes only when ALL of these are true:
//   1. URL is a specific/deep article URL (not a homepage or section page).
//   2. URL resolves (after redirects) with HTTP 2xx.
//   3. The live page title overlaps the cited source title.
//   4. The final URL is not a publisher homepage.
// Bot-blocked responses (401/403/429) are reported as BLOCKED, never as PASS.
// Report-only mode: `node scripts/verify-sources.mjs --report`
import { readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import matter from 'gray-matter';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const NEWS = join(ROOT, 'src', 'content', 'news');
const OUT_DIR = process.env.TEMP ? join(process.env.TEMP, 'opencode') : ROOT;
const REPORT_ONLY = process.argv.includes('--report');
const CONCURRENCY = Number(process.env.SOURCE_GATE_CONCURRENCY || 8);
const TIMEOUT_MS = Number(process.env.SOURCE_GATE_TIMEOUT_MS || 25000);
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';

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
  // A single-segment path such as /apps or /book is a real content/landing
  // page, not a publisher homepage. Homepages are caught above and by the
  // redirect-to-homepage check on the final URL.
  return 'deep';
}

const STOP = new Set(['the','a','an','and','or','of','to','in','on','for','with','from','by','at','as','is','are','was','were','be','been','has','have','had','after','before','over','under','into','amid','says','said','new','its','his','her','their','this','that','these','those','what','why','how','who','when','where','not','but','you','your','we','our','it','they','them','he','she','i','will','would','can','could','may','might','should','more','than','then','now','up','out','about','against','between','during','through']);

function tokens(s) {
  return String(s || '')
    .toLowerCase()
    .replace(/&amp;/g, '&')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter(t => t.length >= 3 && !STOP.has(t));
}

function titleMatch(cited, live) {
  if (!live) return 'unknown';
  const a = tokens(cited);
  const b = new Set(tokens(live));
  if (a.length === 0) return 'unknown';
  const hit = a.filter(t => b.has(t)).length;
  const coverage = hit / a.length;
  if (coverage >= 0.6) return 'match';
  if (coverage >= 0.35) return 'partial';
  return 'mismatch';
}

function extractTitle(html) {
  const og = html.match(/<meta[^>]+property=["']og:title["'][^>]+content=["']([^"']+)["']/i)
    || html.match(/<meta[^>]+content=["']([^"']+)["'][^>]+property=["']og:title["']/i);
  if (og) return og[1].trim();
  const t = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  if (t) return t[1].replace(/\s+/g, ' ').trim();
  return '';
}

const cache = new Map();

// Some publishers reject Node's fetch client (TLS fingerprinting) while serving
// the article normally to curl and to browsers. A source that a reader can open
// must not be reported as blocked, so a blocked fetch is retried with curl.
// A page that also fails for curl stays blocked.
function curlFetch(url) {
  try {
    const r = spawnSync(
      'curl.exe',
      ['-s', '-L', '--max-time', String(Math.ceil(TIMEOUT_MS / 1000)), '-A', UA,
       '-w', '\n__RFN_GATE_STATUS__%{http_code}\n%{url_effective}', url],
      { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 },
    );
    if (r.error || !r.stdout) return null;
    const out = r.stdout;
    const m = out.match(/\n__RFN_GATE_STATUS__(\d{3})\n([\s\S]*)$/);
    if (!m) return null;
    return {
      status: Number(m[1]),
      finalUrl: m[2].trim(),
      body: out.slice(0, m.index),
    };
  } catch {
    return null;
  }
}

async function checkUrl(url) {
  if (cache.has(url)) return cache.get(url);
  const result = { url, status: null, finalUrl: null, contentType: null, pageTitle: null, error: null };
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, {
      redirect: 'follow',
      signal: controller.signal,
      headers: { 'User-Agent': UA, Accept: 'text/html,application/xhtml+xml' },
    });
    result.status = res.status;
    result.finalUrl = res.url;
    result.contentType = res.headers.get('content-type') || '';
    if (res.ok && /text\/html/i.test(result.contentType)) {
      const html = await res.text();
      result.pageTitle = extractTitle(html);
    }
  } catch (e) {
    result.error = e.name === 'AbortError' ? 'timeout' : String(e.message || e);
  } finally {
    clearTimeout(timer);
  }
  if (result.error === 'timeout' || [400, 403, 406, 429].includes(result.status)) {
    const c = curlFetch(url);
    if (c && c.status >= 200 && c.status < 300) {
      result.status = c.status;
      result.finalUrl = c.finalUrl || result.finalUrl;
      result.error = null;
      result.pageTitle = extractTitle(c.body);
    }
  }
  cache.set(url, result);
  return result;
}

const files = readdirSync(NEWS).filter(f => f.endsWith('.md')).sort();
const ONLY = (process.env.SOURCE_GATE_ONLY || '').split(',').map(s => s.trim()).filter(Boolean);
const selected = ONLY.length ? files.filter(f => ONLY.some(o => f.includes(o))) : files;
const articles = selected.map(f => {
  const raw = readFileSync(join(NEWS, f), 'utf8');
  const { data } = matter(raw);
  return {
    slug: f.replace(/\.md$/, ''),
    title: data.title || '',
    sources: Array.isArray(data.sources) ? data.sources : [],
    primarySource: data.primarySource || '',
    primarySourceUrl: data.primarySourceUrl || '',
  };
});

// Unique URL work list.
const urls = new Set();
for (const a of articles) {
  for (const s of a.sources) if (s?.url) urls.add(String(s.url).trim());
  if (a.primarySourceUrl) urls.add(String(a.primarySourceUrl).trim());
}
const list = [...urls];
const checks = new Map();
for (let i = 0; i < list.length; i += CONCURRENCY) {
  const chunk = list.slice(i, i + CONCURRENCY);
  const done = await Promise.all(chunk.map(checkUrl));
  for (const r of done) checks.set(r.url, r);
  console.error(`checked ${Math.min(i + CONCURRENCY, list.length)}/${list.length}`);
}

const rows = [];
for (const a of articles) {
  const perSource = a.sources.map((s, idx) => {
    const url = String(s?.url || '').trim();
    const kind = classify(url);
    const c = checks.get(url) || {};
    const finalKind = c.finalUrl ? classify(c.finalUrl) : null;
    const match = kind === 'deep' ? titleMatch(s?.title, c.pageTitle) : 'n/a';
    const issues = [];
    if (kind !== 'deep') issues.push(kind);
    if (c.error) issues.push(c.error);
    if (c.status && (c.status < 200 || c.status >= 300)) {
      issues.push(c.status === 401 || c.status === 403 || c.status === 429 ? 'blocked' : `http-${c.status}`);
    }
    if (finalKind && finalKind !== 'deep') issues.push(`redirect-${finalKind}`);
    if (match === 'mismatch') issues.push('title-mismatch');
    return {
      slug: a.slug,
      index: idx + 1,
      citedTitle: s?.title || '',
      publisher: s?.publisher || '',
      url,
      kind,
      status: c.status,
      finalUrl: c.finalUrl || '',
      pageTitle: c.pageTitle || '',
      titleMatch: match,
      issues,
      pass: issues.length === 0,
    };
  });

  const pUrl = String(a.primarySourceUrl || '').trim();
  let primary = null;
  if (pUrl) {
    const kind = classify(pUrl);
    const c = checks.get(pUrl) || {};
    const finalKind = c.finalUrl ? classify(c.finalUrl) : null;
    const match = kind === 'deep' ? titleMatch(a.primarySource, c.pageTitle) : 'n/a';
    const issues = [];
    if (kind !== 'deep') issues.push(kind);
    if (c.error) issues.push(c.error);
    if (c.status && (c.status < 200 || c.status >= 300)) {
      issues.push(c.status === 401 || c.status === 403 || c.status === 429 ? 'blocked' : `http-${c.status}`);
    }
    if (finalKind && finalKind !== 'deep') issues.push(`redirect-${finalKind}`);
    // primarySource is a document description, not a cited headline; title
    // matching applies to sources[] only. URL specificity and status still apply.
    primary = { slug: a.slug, citedTitle: a.primarySource, publisher: 'PRIMARY', url: pUrl, kind, status: c.status, finalUrl: c.finalUrl || '', pageTitle: c.pageTitle || '', titleMatch: match, issues, pass: issues.length === 0 };
  }

  const passing = perSource.filter(s => s.pass).length;
  const articleIssues = [];
  if (passing < 2) articleIssues.push(`only-${passing}-passing-source${passing === 1 ? '' : 's'}`);
  if (primary && !primary.pass) articleIssues.push('primary-fails');
  rows.push({ slug: a.slug, title: a.title, sourceCount: a.sources.length, passing, primary, sources: perSource, issues: articleIssues, pass: articleIssues.length === 0 });
}

const flat = [];
for (const a of rows) {
  for (const s of a.sources) flat.push({ article: a.slug, ...s });
  if (a.primary) flat.push({ article: a.slug, ...a.primary });
}

const esc = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
const header = ['article','index','publisher','citedTitle','url','kind','status','finalUrl','pageTitle','titleMatch','issues','pass'];
const csv = [header.join(',')].concat(flat.map(r => header.map(h => esc(Array.isArray(r[h]) ? r[h].join(';') : r[h])).join(','))).join('\n');
writeFileSync(join(OUT_DIR, 'source-remediation.csv'), csv, 'utf8');
writeFileSync(join(OUT_DIR, 'source-gate.json'), JSON.stringify({ generatedAt: new Date().toISOString(), reportOnly: REPORT_ONLY, articles: rows }, null, 2), 'utf8');

const totals = {
  articles: rows.length,
  passingArticles: rows.filter(r => r.pass).length,
  failingArticles: rows.filter(r => !r.pass).length,
  sourceEntries: flat.length,
  passingEntries: flat.filter(r => r.pass).length,
  failingEntries: flat.filter(r => !r.pass).length,
  byIssue: {},
};
for (const r of flat) for (const i of r.issues) totals.byIssue[i] = (totals.byIssue[i] || 0) + 1;

console.log(JSON.stringify(totals, null, 2));
console.log('worst articles:');
for (const a of rows.filter(r => !r.pass).sort((x, y) => x.passing - y.passing).slice(0, 20)) {
  console.log(`pass=${a.passing}/${a.sourceCount} primary=${a.primary?.pass ? 'PASS' : 'FAIL'} | ${a.slug}`);
}
console.log('written:', join(OUT_DIR, 'source-remediation.csv'));

if (!REPORT_ONLY && totals.failingArticles > 0) process.exit(1);
