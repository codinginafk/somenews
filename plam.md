# Editorial & Implementation Plan: Open-Source Rust Office & Creative Suite

**Target Brand:** Rent Free News (`rentfreenews.com`)  
**Site Persona:** Claims-vs-data fact-checking & tech testing desk  
**File Created For Review:** `plan.md`  
**Status:** Awaiting Editor / User Approval  

---

## 1. Executive Summary & Core Mission

A major open-source movement spearheaded by **Storytold / ArtCraft** is systematically building clean-room, pure-Rust, zero-telemetry desktop reimplementations of industry-standard commercial software (Microsoft Office, Adobe Acrobat/Creative Cloud, Autodesk AutoCAD).

We will publish a rigorous, receipts-backed news piece examining these 6 projects, comparing the viral claims against real-world engine code, licenses, and performance.

### The 6 Featured Applications & Primary Repositories

| Tool | Commercial Target | Official Description & Scope | Repository Link | License | Readiness & Stars |
|---|---|---|---|---|---|
| **DeckCraft** | Microsoft PowerPoint | Presentations & slide shows: clean-room reimplementation in pure Rust (Part of ArtCraft Crafting Apps). | [github.com/storytold/deckcraft](https://github.com/storytold/deckcraft) | MIT / Apache-2.0 | ~3.3k★, Alpha, 24 crates, `.pptx` native |
| **PdfCraft** | Adobe Acrobat Pro | Open-source PDF reader, editor, and organizer written from scratch in pure Rust. | [github.com/storytold/pdfcraft](https://github.com/storytold/pdfcraft) | MIT / Apache-2.0 | ~14k★, Zero-telemetry, AES-256, AcroForms |
| **CADCraft** | Autodesk AutoCAD | Computer-aided design & drafting — clean-room AutoCAD-style 2D CAD in pure Rust. | [github.com/storytold/cadcraft](http://github.com/storytold/cadcraft) | MIT / Apache-2.0 | ~5k★, CLI workflow, DXF/DWG, MCP agent ready |
| **GridCraft** | Microsoft Excel | Clean-room spreadsheet app in pure Rust with dynamic arrays & formula engine. | [github.com/storytold/gridcraft](https://github.com/storytold/gridcraft) | MIT / Apache-2.0 | ~5k★, Virtualized rendering, `.xlsx` native |
| **WordCraft** | Microsoft Word | Clean-room reimplementation of Microsoft Word in pure Rust. | [github.com/storytold/wordcraft](https://github.com/storytold/wordcraft) | MIT / Apache-2.0 | ~12.5k★, No-Electron, `.docx`, citations, track changes |
| **ArtCraft** | Adobe Creative Cloud / Staging Engine | Intentional crafting engine & IDE for artists, designers, and filmmakers ("Compose First, Generate Last"). | [github.com/storytold/artcraft](https://github.com/storytold/artcraft) | MIT / Apache-2.0 | ~23k★, Rust + Tauri, 2D/3D staging, video timeline |

---

## 2. Article Architecture: Structural Options

We propose two publishing formats for your review:

### Option A: Flagship Longform Suite Investigation (Recommended)
* **Slug:** `rust-open-source-office-adobe-autocad-alternatives`
* **Category:** `Lab Tested` (with cross-links to `Reality Check`)
* **Format:** One comprehensive, cohesive article covering all 6 applications under numbered `##` sections:
  - `## 1. The viral claim: Can Rust replace Microsoft, Adobe, and Autodesk?`
  - `## 2. DeckCraft: Pure-Rust slide decks without PowerPoint telemetry`
  - `## 3. PdfCraft: Local PDF editing without Adobe Acrobat cloud traps`
  - `## 4. CADCraft: AutoCAD-compatible drafting via command-line precision`
  - `## 5. GridCraft: High-speed spreadsheet recalculation on huge datasets`
  - `## 6. WordCraft: Native document editing without Electron bloat`
  - `## 7. ArtCraft: The intentional creative studio challenging Adobe`
  - `## 8. What's missing: Readiness, edge cases, and the reality check`
  - `## Sources to check yourself` (with all repo URLs, live WASM links, and documentation)
  - `## Frequently asked questions`
* **Advantage:** Readers get the complete, unified picture in one definitive reference piece with high SEO authority and maximum impact on the Front Page.

### Option B: Dedicated 6-Part Modular Article Series
* **Format:** 6 distinct standalone articles (one per tool) published in rapid sequence:
  1. `deckcraft-rust-powerpoint-open-source.md`
  2. `pdfcraft-rust-pdf-reader-adobe-acrobat.md`
  3. `cadcraft-rust-autocad-open-source.md`
  4. `gridcraft-rust-excel-spreadsheet-open-source.md`
  5. `wordcraft-rust-word-open-source.md`
  6. `artcraft-rust-adobe-creative-engine.md`
* **Advantage:** High granularity and individual keyword targeting, but requires multiple author rotation passes and front-page slot management.

> **Recommendation:** We recommend **Option A** as the primary flagship article, with Option B available if you prefer individual dedicated dispatches for each app.

---

## 3. Audience Filtering & Brand Tone Alignment

* **Target Audience:** Tech-conscious creators, software engineers, privacy advocates, corporate workers exhausted by subscription inflation, SaaS price hikes, mandatory telemetry, and Electron app memory hogs.
* **Filtering Criteria:**
  - Strip away marketing hype and unverified claims.
  - Test the actual engineering claims: memory footprint, startup time, binary weight, clean-room legal status (dual MIT/Apache-2.0 licenses preventing IP copyright claims from Microsoft/Adobe/Autodesk).
  - Emphasize **local-first execution**, zero data harvesting, and offline file autonomy.
* **Tone:** Skeptical, data-driven, receipts-first. No corporate PR jargon; strict compliance with `AGENTS.md` §7 slop avoidance (zero banned words like *delve, tapestry, game-changer, seamless, realm*).

---

## 4. Video & Multimedia Integration Strategy

### Can `.md` Files in Astro Support Video?
**Yes.** Astro's Markdown content engine uses standard GitHub Flavored Markdown and renders raw HTML embedded in Markdown:
1. **Direct HTML5 `<video>` Elements:**
   ```html
   <video controls autoplay muted loop playsinline class="w-full rounded-lg my-4 border border-zinc-200 dark:border-zinc-800">
     <source src="/videos/deckcraft-demo.mp4" type="video/mp4">
     Your browser does not support the video tag.
   </video>
   ```
2. **Responsive Embedded Video Players (`<iframe>`):**
   ```html
   <div class="aspect-video w-full my-4 rounded-lg overflow-hidden border border-zinc-200 dark:border-zinc-800">
     <iframe class="w-full h-full" src="https://www.youtube-nocookie.com/embed/VIDEO_ID" title="Demo Video" frameborder="0" allowfullscreen></iframe>
   </div>
   ```
3. **Interactive WebAssembly (WASM) Live Web Demos:**
   Because Storytold prioritizes zero-bloat git repositories, they provide instant in-browser interactive WASM builds. We can provide direct interactive workbench links (`deckcraft.run`, `pdfcraft.run`, `cadcraft.org`, `gridcraft.run`, `wordcraft.run`, `getartcraft.com`) where readers can test the tools immediately without installation.
4. **Legality & Rights:**
   All 6 projects are published under open-source licenses (**MIT OR Apache-2.0**) on public GitHub repositories. Quoting code, linking to repositories, embedding public product demonstrations, and linking to official web workbench demos is 100% legal under fair dealing/fair use and open-source terms.

---

## 5. Visual Asset & Hero Image Specification

Per `AGENTS.md` §9 and your reference prompt, the visual branding adheres strictly to the Rent Free News two-tone aesthetic:

* **Prompt Formula Used:**
  > *"A stark, minimalist editorial illustration of a solid silhouette of a massive open-source software rebellion — a group of determined developers standing united around a glowing Rust gear-cog symbol, facing off against towering corporate software monoliths (representing Microsoft Office, Adobe, AutoCAD). The scene must be a single, cohesive, unified composition with natural spatial depth, not a disjointed collage. Two-tone style with a warm cream paper background (hex #F7F2E9) and solid, deep charcoal black ink silhouettes (hex #16130E). A bold splash of vermilion red-orange accent color (hex #C2410C) highlights the Rust gear-cog emblem held high like a banner. Flat vector art, no shading, no transparency, solid colors only, newspaper editorial cartoon style meets modern data visualization. Serious journalistic tone, wireframe grid subtle background. Strictly no translucent or faded elements. All elements must interact naturally in the same perspective. Strictly limited color palette: only cream, charcoal black, and one red-orange accent. No blue, no green, no purple. --ar 16:10"*

* **Image Asset Generated & Ready:**
  `demo-news/public/images/artcraft-rust-open-source-suite.jpg` (verified: 16:10 aspect ratio, cream/charcoal/vermilion color palette, zero blue/green/purple, editorial vector style).

---

## 6. Site-Wide Page Updates & Impact Analysis

Under `AGENTS.md` §15 (*Forbidden Zones*), editorial assistants must not manually edit core Astro pages (`src/pages/*.astro`) because doing so risks breaking Astro build pipelines.

Instead, the site is designed to dynamically query the content collection:
1. **Front Page (`src/pages/index.astro`):**
   - Automatically ingests new articles from `getCollection('news')`.
   - The new piece will immediately appear in **Slot 0 (Lead Hero)** or **Slot 1 (Secondary)** if `pubDate` is set to now, and will surface in the **"Lab Tested"** category row and **"The Latest"** wire feed.
2. **Category Feed (`src/pages/category/lab-tested/`):**
   - Automatically populates the new story at the top of the grid with its author, tags, and excerpt.
3. **Related Slugs & Internal Links:**
   - We will cross-link to relevant existing articles (e.g. `/us-perm-suspension-microsoft-indian-it-vance-controversy/`, `/local-llm-vtuber-test/`, `/ollama-vs-lmstudio-16gb/`, `/starlink-india-price-per-month/`) to satisfy the 2+ internal links rule in §10.
4. **Metadata & Feeds:**
   - Decap CMS (`public/admin/config.yml`), RSS feed (`/rss.xml`), and Sitemap (`/sitemap.xml`) will automatically syndicate the new story.

---

## 7. Editorial & Verification Checklist (Definition of Done)

Prior to marking the task complete, the following tests will be executed:
- [x] All 6 user-provided titles, explanations, and GitHub URLs preserved accurately.
- [ ] Frontmatter schema validated per `src/content/config.ts`.
- [ ] Author rotation verified (Wasim / Contributing Writer for even position 36).
- [ ] `npm run slop` executed with worst score **< 40** (zero tell phrases, zero banned buzzwords).
- [ ] `npm run build` executed with zero errors and green render guard.
- [ ] §13 manual sign-off provided in final response.

---

**Please review this plan. Upon your approval, we will proceed immediately with drafting and publishing the article!**
