// Render-completeness guard. Astro can silently truncate pages at build time
// (green build, broken HTML) when exotic markup appears in expressions —
// e.g. a fragment `{cond && <>...</>}` or a raw & inside an href={...}.
// This runs as part of `npm run build` and fails LOUDLY if any article
// is missing its body sections, so a truncated deploy can never ship.
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const dist = join(process.cwd(), 'dist');
// Directories that are not articles (archives, tooling, assets).
const SKIP_DIRS = new Set(['category', 'author', 'rss', 'search', 'admin', 'images', '_astro']);
// Standalone utility pages: real pages, but they legitimately lack article sections.
const UTILITY = new Set(['about', 'advertise', 'contact', 'corrections', 'dmca', 'privacy', 'terms']);

let failures = 0;
const fail = (msg) => { console.error(`verify-render: FAIL — ${msg}`); failures++; };

// Homepage must carry exactly one h1 (sr-only brand statement).
const home = readFileSync(join(dist, 'index.html'), 'utf8');
const homeH1 = (home.match(/<h1[ >]/g) || []).length;
if (homeH1 !== 1) fail(`homepage has ${homeH1} <h1> tags (expected 1)`);

for (const name of readdirSync(dist)) {
  const idx = join(dist, name, 'index.html');
  try { if (!statSync(idx).isFile()) continue; } catch { continue; }
  if (SKIP_DIRS.has(name)) continue;
  const html = readFileSync(idx, 'utf8');
  if (!/<h1[ >]/.test(html)) fail(`${name}: missing <h1>`);
  if (UTILITY.has(name)) continue;
  // Article completeness: body sections that must survive the build.
  for (const marker of ['How we checked', 'Reader discussion', 'Keep reading']) {
    if (!html.includes(marker)) fail(`${name}: missing article section "${marker}" (truncated render?)`);
  }
  if ((html.match(/<h2[ >]/g) || []).length < 1) fail(`${name}: missing <h2>`);
}

if (failures > 0) {
  console.error(`verify-render: ${failures} problem(s) — refusing to ship.`);
  process.exit(1);
}
console.log('verify-render: all pages complete.');
