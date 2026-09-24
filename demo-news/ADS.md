# Ads implementation runbook — Rent Free News

Follow this document **when AdSense (or another network) approves the site**. Nothing here needs doing before approval.

## Current state (2026-09-24)

- Placeholder ad boxes removed from all 5 spots (homepage ×2, articles ×3). `AdSlot.astro` component kept, unused.
- `public/ads.txt` **deleted on purpose** — a placeholder `pub-0000000000000000` line risks rejection for a mismatched publisher ID. Do not recreate it until you have a real `ca-pub-…`.
- Site ships with zero ad code. That is correct until approval.

---

## Phase 1 — Before applying (do these first)

1. **GSC Domain property verified + sitemap submitted** — AdSense review leans on it. Not optional.
2. Content floor: aim for **15–20 original articles** spread across all 4 categories (we launch with 10 — add a handful). Every article keeps its sources + verdict (already enforced by the CMS).
3. Required pages all exist ✅ — `/about/` `/privacy/` `/terms/` `/contact/` `/corrections/` `/dmca/`.
4. Apply at **adsense.google.com → Add site → `rentfreenews.com`**. Review runs ~2 days to 2 weeks.

## Phase 2 — Approval day, in order

### 1. Grab the publisher ID

AdSense → Settings → Account information → `ca-pub-XXXXXXXXXXXXXXXX` (16 digits).

### 2. Recreate `public/ads.txt`

Create the file back with the **exact line AdSense's UI gives you** (AdSense → Sites → your site → the "ads.txt" prompt → Copy):

```
google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
```

Commit + push (Actions auto-deploys). Verify at `https://rentfreenews.com/ads.txt`. AdSense shows "ads.txt found" (green) within ~24h.

### 3. Site-level snippet

AdSense → Ads → Overview → get the snippet and paste it into `src/layouts/Layout.astro`, inside `<head>`:

```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
```

If you enable **Auto ads** (AdSense → Ads → By site → toggle Auto ads ON), stop here — Google places units itself. The manual path below is recommended instead: a reading-heavy fact-check site wants predictable, non-intrusive placement.

### 4. Manual ad units (recommended path)

In AdSense → Ads → By ad unit → **+ New ad unit → Display ad**, create three and name them to match the slots:

| Unit name | Goes in | Format |
|---|---|---|
| `rfn-home-leaderboard` | homepage, between hero and "Top checks" | Responsive display, ~728×90 shape |
| `rfn-article-inline` | article, after "Why it matters" | Responsive display |
| `rfn-sidebar-300` | both sidebars | 300×250 shape |

Record each unit's slot ID. Then rewrite `src/components/AdSlot.astro`:

```astro
---
interface Props { slot?: string; }
const { slot = 'in-article' } = Astro.props;
const slotIds: Record<string, string> = {
  'leaderboard': 'SLOT_ID_HOME',        // rfn-home-leaderboard
  'article-top': 'SLOT_ID_ARTICLE',     // rfn-article-inline
  'article-mid': 'SLOT_ID_ARTICLE',     // reuse the inline unit
  'sidebar-300x250': 'SLOT_ID_SIDEBAR', // rfn-sidebar-300
};
const adSlot = slotIds[slot];
---
<div class="my-4">
  <div class="text-[10px] font-bold uppercase tracking-[0.2em] text-zinc-400">Advertisement</div>
  <ins class="adsbygoogle"
       style="display:block"
       data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
       data-ad-slot={adSlot}
       data-ad-format="auto"
       data-full-width-responsive="true"></ins>
</div>
<script is:inline>(adsbygoogle = window.adsbygoogle || []).push({});</script>
```

### 5. Re-add the 5 usages at the exact former spots

Add `import AdSlot from '../components/AdSlot.astro';` back to both pages, then:

| Slot prop | File | Exact location |
|---|---|---|
| `leaderboard` | `src/pages/index.astro` | after the hero bento grid (`</div>` closing `pt-5 grid lg:grid-cols-3`), before the "Top checks" `SectionHeader`. Wrap: `<div class="mt-4">…</div>` |
| `sidebar-300x250` | `src/pages/index.astro` | in `<aside>`, between the "Most read" card and the "Why trust us" card |
| `article-top` | `src/pages/[slug].astro` | after the "Why it matters" section, before `<Content />`. Wrap: `<div class="mt-4">…</div>` |
| `article-mid` | `src/pages/[slug].astro` | after the "Reader discussion" section, before the `<Newsletter />` block. Wrap: `<div class="mt-4">…</div>` |
| `sidebar-300x250` | `src/pages/[slug].astro` | in `<aside>`, after the "Related in …" card (last child) |

Build + spot-check two pages, then push.

## Placement rules (keep these on every future edit)

- **Max 5 display ads per page** (home 2, article 3) — matches Google's ad-density guidance.
- **Nothing above the fold on mobile that pushes the headline down** — if PageSpeed LCP regresses after launch, hide `article-top` on small screens (`hidden sm:block`) before deleting it.
- **Never ads on** `/admin/`, `/search/`, or the 404 — they're noindex; AdSlot only ever existed on content templates, keep it that way.
- **Never inside** the claim box, verdict pill, or Sources list — `/advertise/` promises "verdicts are never for sale"; don't break it.
- "Advertisement" label stays (AdSlot renders it; AdSense adds its own too).

## Compliance (ban prevention)

- Never click your own ads, no exchange/traffic schemes.
- **EEA + UK traffic needs consent** before personalized ads: enable AdSense's consent tool (AdSense → Privacy & messaging) or a certified CMP. Do this the same day ads go live.
- Add one paragraph to `/privacy/`: Google AdSense, DoubleClick cookie, ad partners, link to Google's Ads Settings + the EU user-opt-out page.
- Leave Cloudflare's managed robots.txt content-signals block alone.

## Phase 3 — Verify after enabling

1. AdSense → Sites → status **Ready** + ads.txt green.
2. Incognito → open an article → View Source → `adsbygoogle.js` present; the `<ins>` renders (Google house ads are normal the first days).
3. GSC → Manual actions: none. AdSense → Policy center: clean.
4. PageSpeed Insights on `/` and one article: LCP still under 2.5s. If not, apply the mobile-hide fix above.

## Scaling up (bigger networks — same ads.txt file)

Add lines **below** the AdSense line, never delete a live network's line while still serving it:

| Network | Traffic bar | Notes |
|---|---|---|
| Mediavine **Journey** | 10k sessions/mo | realistic first upgrade; apply at mediavine.com/journey |
| Mediavine (full) | 50k sessions/mo | |
| Raptive | 100k uniques/mo | |
| Ezoic | no minimum | AI placement, lower RPMs |

Each network's dashboard gives its exact `ads.txt` line — paste it, push, done.

## Rollback

Delete `public/ads.txt`, remove the Layout snippet, remove the `<AdSlot>` usages → push. Site returns to zero-ad state.
