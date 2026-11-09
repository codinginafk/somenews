// Open Graph card generator — one branded 1200×630 PNG per article, plus a
// default brand card for non-article pages.
//
// Scaling model: editors keep uploading exactly ONE image (the hero SVG, or
// none). Every card is DERIVED at build time from that single input:
//   article art -> its category's default art -> generic brand plate
// Artifacts land in dist/og/ and never enter git (CI-only, like the HTML).
// Fonts are committed under scripts/og-assets/ (Libre Franklin, SIL OFL).
//
// Two-pass rasterization: usvg (resvg) can't nest SVG inside <image>, so each
// art SVG is rasterized once (cached per file), then composited into the card
// template. Raster heroes (jpg/png via /uploads/) skip pass one.
import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import matter from 'gray-matter';
import { Resvg } from '@resvg/resvg-js';
import sharp from 'sharp';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const DIST = join(ROOT, 'dist');
const OUT = join(DIST, 'og');
const FONTS = join(ROOT, 'scripts', 'og-assets');

const INK = '#16130e';
const PAPER = '#f7f2e9';
const BRAND = '#c2410c';
const HAIR = '#e3d9c6';
const W = 1200, H = 630;

const CAT_ART = {
  'Reality Check': 'reality-check',
  'By the Numbers': 'by-the-numbers',
  'Countries': 'countries',
  'Lab Tested': 'lab-tested',
};

const xml = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// Char-budget word wrap tuned to the headline face (no font shaping needed)
function wrap(text, maxChars, maxLines) {
  const words = text.replace(/\s+/g, ' ').trim().split(' ');
  const lines = [];
  let line = '';
  for (const w of words) {
    const next = line ? line + ' ' + w : w;
    if (next.length > maxChars && line) { lines.push(line); line = w; }
    else line = next;
  }
  if (line) lines.push(line);
  if (lines.length <= maxLines) return lines;
  const kept = lines.slice(0, maxLines);
  const last = kept[maxLines - 1];
  if (last.length > 8 && kept.join(' ').length < words.join(' ').length) {
    kept[maxLines - 1] = last.slice(0, maxChars - 1).replace(/[\s.,;:!-]+$/, '') + '…';
  }
  return kept;
}

// ---- pass one: art -> raster PNG base64 (cached per absolute path) ----
const artCache = new Map();
function artToDataUri(srcAbs) {
  if (artCache.has(srcAbs)) return artCache.get(srcAbs);
  let dataUri = null;
  const buf = readFileSync(srcAbs);
  const rel = srcAbs.toLowerCase();
  const svgOpts = { fitTo: { mode: 'width', value: 1200 }, shapeRendering: 'geometricPrecision' };
  if (rel.endsWith('.svg')) {
    try {
      const r = new Resvg(buf, svgOpts);
      dataUri = 'data:image/png;base64,' + r.render().asPng().toString('base64');
    } catch (e) { console.error('  art raster fail:', srcAbs, e.message); }
  } else if (/\.(png|jpe?g|webp)$/i.test(rel)) {
    const mime = rel.endsWith('.png') ? 'image/png' : rel.endsWith('.webp') ? 'image/webp' : 'image/jpeg';
    dataUri = 'data:' + mime + ';base64,' + buf.toString('base64');
  }
  artCache.set(srcAbs, dataUri);
  return dataUri;
}

function artSource(category, heroImage) {
  const chain = [];
  // heroImage is site-absolute (/images/x.svg, /uploads/y.png) → demo-news/public
  if (heroImage) chain.push(join(ROOT, 'public', heroImage.replace(/^\//, '')));
  const cat = CAT_ART[category] ?? 'reality-check';
  chain.push(join(ROOT, 'public', 'images', cat + '.svg'));
  for (const p of chain) if (p && existsSync(p)) return { abs: p };
  return null;
}

function cardSvg({ artDataUri, kicker, headline, url }) {
  const titleLines = wrap(headline, 46, 3);
  const headTspans = titleLines
    .map((l, i) => `<tspan x="64" y="${480 + i * 56}">${xml(l)}</tspan>`)
    .join('');
  const art = artDataUri
    ? `<image x="0" y="8" width="1200" height="384" preserveAspectRatio="xMidYMid slice" href="${artDataUri}" />`
    : '';
  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <rect width="${W}" height="${H}" fill="${PAPER}"/>
  ${art}
  <rect x="0" y="0" width="1200" height="8" fill="${BRAND}"/>
  <rect x="0" y="392" width="1200" height="2" fill="${HAIR}"/>
  <text x="64" y="438" font-family="Libre Franklin" font-weight="600" font-size="17" letter-spacing="3.5" fill="${BRAND}">${xml((kicker || 'News').toUpperCase())}</text>
  <text x="1136" y="439" text-anchor="end" font-family="Libre Franklin" font-weight="600" font-size="20" letter-spacing="0" fill="${INK}">rent free news<tspan fill="${BRAND}">.</tspan></text>
  <text font-family="Libre Franklin" font-weight="700" font-size="44" fill="${INK}">${headTspans}</text>
  ${url ? `<text x="64" y="606" font-family="Libre Franklin" font-weight="600" font-size="15" letter-spacing="1" fill="#8a8171">${xml(url)}</text>` : ''}
</svg>`;
}

const fontOpts = {
  font: {
    fontFiles: [join(FONTS, 'LibreFranklin-Bold.ttf'), join(FONTS, 'LibreFranklin-SemiBold.ttf')],
    loadSystemFonts: false,
    defaultFontFamily: 'Libre Franklin',
  },
  fitTo: { mode: 'width', value: W },
  shapeRendering: 'geometricPrecision',
};

// Render + compress. Target: well under ~300KB (WhatsApp ignores heavier
// og:images). Stays PNG throughout so Content-Type matches og:image:type;
// flat brand art collapses to a tiny palette, stepped down only if needed.
async function render(svg) {
  const raw = new Resvg(Buffer.from(svg), fontOpts).render().asPng();
  let out = await sharp(raw).png({ palette: true, quality: 90, compressionLevel: 9 }).toBuffer();
  if (out.length > 260 * 1024) out = await sharp(raw).png({ palette: true, colors: 160, quality: 80, compressionLevel: 9 }).toBuffer();
  if (out.length > 260 * 1024) out = await sharp(raw).png({ palette: true, colors: 96, quality: 70, compressionLevel: 9 }).toBuffer();
  return out;
}

const SITE_URL = 'https://rentfreenews.com';
mkdirSync(OUT, { recursive: true });

// ---- default brand card (non-article pages) ----
const defaultSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <rect width="${W}" height="${H}" fill="${PAPER}"/>
  <rect x="0" y="0" width="1200" height="8" fill="${BRAND}"/>
  <rect x="64" y="250" width="72" height="6" fill="${BRAND}"/>
  <text x="64" y="330" font-family="Libre Franklin" font-weight="700" font-size="68" fill="${INK}">rent free news<tspan fill="${BRAND}">.</tspan></text>
  <text x="64" y="386" font-family="Libre Franklin" font-weight="600" font-size="26" fill="${INK}">Viral claims vs primary data — reality checks with receipts.</text>
  <text x="64" y="446" font-family="Libre Franklin" font-weight="600" font-size="17" letter-spacing="3" fill="${BRAND}">RENTFREENEWS.COM</text>
</svg>`;
writeFileSync(join(OUT, 'default.png'), await render(defaultSvg));
console.log('og: wrote default.png');

// ---- per-article cards ----
const newsDir = join(ROOT, 'src', 'content', 'news');
const files = readdirSync(newsDir).filter(f => f.endsWith('.md'));
let ok = 0, fellBack = 0;
for (const f of files) {
  const slug = f.replace(/\.md$/, '');
  const fm = matter(readFileSync(join(newsDir, f), 'utf8')).data;
  const headline = fm.seoTitle || fm.title || slug;
  const kicker = fm.category || 'News';
  const src = artSource(kicker, fm.heroImage);
  const artDataUri = src ? artToDataUri(src.abs) : null;
  if (!src) fellBack++;
  const svg = cardSvg({ artDataUri, kicker, headline, url: SITE_URL + '/' + slug + '/' });
  writeFileSync(join(OUT, slug + '.png'), await render(svg));
  ok++;
}
console.log(`og: wrote ${ok} article cards (${fellBack} using category fallback), ${artCache.size} unique art renders`);
