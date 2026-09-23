# Rent Free News — Demo News Theme (Astro + Decap CMS)

Fast, beautiful, editor-friendly. Brand: Rent Free News (rentfreenews.com) — claims vs data.

## What you got
- Homepage: live ticker + hero-plus-grid (BBC/Guardian pattern) + trending rail + category blocks + VTuber spotlight
- Article page: claim box, verdict box, quote box (permission), sources/method box, ad slots (no CLS), NewsArticle schema
- `/admin/` → Decap CMS for editors (no code). Git-based, free.
- SEO: sitemap, rss.xml, canonical, OG, NewsArticle JSON-LD
- CI/CD: `.github/workflows/deploy.yml` → Cloudflare Pages on push to main

## Run it
```powershell
cd demo-news
npm install
npm run dev
# open http://localhost:4321
# editors: http://localhost:4321/admin/ (with local_backend: true + `npx decap-server`)
```

## CMS choice for prod
- **Demo / 1-5 editors:** Decap (this) — free, commits MD to `src/content/news/`, CI rebuilds in ~40s.
- **Scale / real-time collab:** migrate to Sanity — same Astro components, replace `getCollection` with Sanity fetch. Keep Decap file as fallback.
- **Sentry (you asked “sentry or decap”):** Sentry ≠ CMS. Sentry = error tracking. Add `@sentry/astro` later for prod monitoring. Decap = editor login. You need both, different jobs.

## Add Sentry (optional, 2 min)
```
npm i @sentry/astro
# astro.config.mjs: import sentry from '@sentry/astro'; integrations: [sentry({ dsn: process.env.SENTRY_DSN })]
```

## Deploy (canonical host = **rentfreenews.com**, never www)
1. Register `rentfreenews.com` + point DNS at Cloudflare
2. Cloudflare DNS: apex + `www` → Pages project
3. Pages → Functions/Redirects: `https://www.rentfreenews.com/*` → `https://rentfreenews.com/$1` **301**
4. Push GitHub `main` → Pages builds `npm run build`, output `dist`
5. Security: `public/_headers` (HSTS, nosniff, frame deny); protect `/admin/*` with Cloudflare Access (SSO/PIN for editors only)
6. GSC: **Domain property** `rentfreenews.com` (not URL-prefix) → submit sitemap; Ahrefs/Semrush: add only `https://rentfreenews.com`
7. robots + sitemap already non-www. Do not add a second GSC property for www.

## Backlink hub + DA/DR funnel (praveentechworld.com, pctoolshub.com)
- Original datasets/tables journalists cite; free “how to read X” explainers
- Always link out to primary sources; short quotes + linkback only (DMCA page live)
- Contextual deep links to praveentechworld.com / pctoolshub.com from matching stories (1–2 per post, in body) — never sitewide footer spam
- Corrections + author pages + NewsArticle schema for E-E-A-T
- Submit to Google News Publisher once on domain + 20+ posts

## Next to make it earn
- Replace AdSlot placeholders with Mediavine Journey script via Partytown
- Add `/ads.txt`, GA4, Search Console, News Publisher Center
- 10 articles → apply AdSense → newsletter Beehiiv
