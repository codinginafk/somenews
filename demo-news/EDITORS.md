# Rent Free News — Editor Guide (for Yash)

One page. If it isn't here, ask Praveen before guessing.

## How publishing works
1. **Edit** a file in `demo-news/src/content/news/` — either on github.com (open file → pencil icon → Commit) or via `rentfreenews.com/admin/` (Decap).
2. **Pushing to `main` auto-deploys.** GitHub Actions builds the site and publishes to Cloudflare Pages (~1 min).
3. **Green build or it didn't happen.** If the Actions run goes red, the deploy is blocked — tell Praveen, don't push more on top.

## New article checklist (copy the template in `AGENTS.md` §5)
- [ ] Filename: `kebab-case-slug.md` (lowercase, words separated by `-`, no dates/numbers). **Never rename a published file** — renaming breaks the URL (see Slug rule).
- [ ] `title` (page H1) — clear claim-vs-data headline.
- [ ] `seoTitle` — **≤ 60 characters**, written for Google (keyword first).
- [ ] `description` — **≤ 155 characters**, one compelling sentence (falls back to excerpt).
- [ ] `excerpt` — 1–2 sentences shown on cards.
- [ ] `category` — exactly one of: `Reality Check`, `By the Numbers`, `Countries`, `Lab Tested`.
- [ ] `tags` — 2–4, lowercase except proper nouns (`uk`, `crime stats`).
- [ ] `author` — follow the rotation (oldest→newest by date): odd article → **Diyan** (Staff Writer); even → alternate **Yash** (Contributing Writer). Next up: Diyan. Never use desk names.
- [ ] `pubDate` — `YYYY-MM-DD`.
- [ ] `claim`, `claimSource`, `verdict` — fill for fact-checks (`verdict` from: `True with context`, `Misleading — Missing Context`, `False — with context`, `Missing Context`, `Explainer`).
- [ ] `primarySource` + `primarySourceUrl` (real link), `whyItMatters` (1–2 sentences), `sources` (2+ real links).
- [ ] `heroImage` — reuse a file from `public/images/` (e.g. `/images/country-uk.svg`) + `heroAlt` describing it in plain words.
- [ ] Body: **bold `**Short answer:**` paragraph first**, then **3+ `##` sections**, 800+ words target.
- [ ] **2+ links to our own articles** (e.g. `/finland-happiest-bangladesh-reality/`), and every outside link must actually open (click each one).
- [ ] FAQ (`## Frequently asked questions`, 2–4 Q&As) when readers would naturally ask follow-ups.

## House rules (top 10)
1. Every number needs a named source with a working link. No "studies show".
2. Quote the claim fairly before knocking it down. Steelman, then check.
3. Short answer first, methodology second, verdict always visible.
4. No `###` sub-heads — flatten to `##`.
5. No `#` H1 inside the body — the title is the H1.
6. Corrections go in the article visibly + bump `updatedDate: YYYY-MM-DD`. Never silently rewrite.
7. Keep AI-tells out: em-dashes sparingly (never in headlines), no "delve / landscape / additionally / in today's fast-paced".
8. Run `npm run slop` if you have the repo locally — stay under 40 (60 = blocked).
9. Dates always `YYYY-MM-DD`. Strings with `:` or quotes go in `"double quotes"`.
10. When in doubt, shorter + more sources beats longer + fewer.

## Images
- Reuse `public/images/*.svg`. New image only if none fits — keep it small, SVG preferred.
- `heroAlt` is mandatory whenever `heroImage` is set (≤ 125 chars, describe don't stuff keywords).

## Slug rule (important)
Published URL = filename. **Do not rename a published article's file.** If a slug MUST change: keep a 301 from old → new (add a line to `public/_redirects`, format inside that file), update every internal link to it, rebuild green. When unsure — ask first.

## Don't touch (ever — ask Praveen)
`.github/`, `public/_headers`, `public/robots.txt`, `public/_redirects` (except adding a 301 line), `astro.config.mjs`, `src/layouts/`, `src/components/` (except reading), `scripts/`, `package.json`.

## Help
- Your AI companion has the full detailed rulebook: **`AGENTS.md`** (same folder as this file). Point it there first.
- Human questions / access / anything red in Actions → Praveen.
