---
title: "DeckCraft: Can a Pure-Rust Reimplementation Replace Microsoft PowerPoint?"
seoTitle: "DeckCraft: Open-Source Rust PowerPoint Alternative"
excerpt: "An open-source clean-room reimplementation of Microsoft PowerPoint in pure Rust promises native PPTX editing without Microsoft 365 cloud bloat."
description: "DeckCraft builds an open-source Microsoft PowerPoint alternative in pure Rust. We benchmark its engine, memory footprint, and PPTX fidelity."
category: 'Lab Tested'
tags: ['Rust', 'PowerPoint', 'Open Source', 'Presentation']
author: 'Wasim'
authorRole: 'Contributing Writer'
pubDate: '2026-10-16 08:00'
heroImage: '/images/deckcraft-rust-powerpoint.jpg'
heroAlt: 'Stark editorial illustration of a speaker presenting slide architecture with red-orange accent.'
claim: 'DeckCraft is an open-source, clean-room reimplementation of Microsoft PowerPoint in pure Rust that matches native PPTX workflows without subscriptions.'
claimSource: 'GitHub trending repositories and open-source discussion forums, 2026'
verdict: 'True with context'
primarySource: 'DeckCraft v0.1 repository architecture and test benchmarks'
primarySourceUrl: 'https://github.com/storytold/deckcraft'
whyItMatters: 'Corporate presentations rely heavily on proprietary Microsoft Office subscriptions. A standalone, memory-safe engine offers an exit ramp from software lock-in.'
sources:
  - title: 'DeckCraft GitHub Repository'
    url: 'https://github.com/storytold/deckcraft'
    publisher: 'Storytold / ArtCraft'
  - title: 'ArtCraft Official Portal'
    url: 'https://getartcraft.com/'
    publisher: 'Storytold'
---

**Short answer:** DeckCraft delivers a working, zero-telemetry desktop presentation app written entirely from scratch in pure Rust. It loads and renders PPTX files natively, avoids web wrappers like Electron, and runs offline without telemetry. However, it remains in alpha: advanced collaboration and legacy visual effects still require Microsoft 365.

## 1. What the open-source project provides

The project repository on [GitHub](https://github.com/storytold/deckcraft) describes DeckCraft as:

> "Presentations and slide shows: an open-source, clean-room reimplementation of Microsoft PowerPoint in pure Rust. Part of the ArtCraft Crafting Apps."

Unlike typical desktop software that packages a web browser inside an Electron shell, DeckCraft is written in 100% native Rust. It splits its codebase across 24 modular crates containing roughly 202,000 lines of Rust code and over 1,600 automated tests. The graphical interface relies on immediate-mode rendering via the `egui` library, running directly against the host GPU.

The app supports standard slide layouts, master slides, speaker notes, custom shapes, connectors, and full-screen presenter display. It reads and writes standard `.pptx` archives using an XML parser that retains unknown proprietary tags. This design choice prevents file corruption when a slide deck round-trips between DeckCraft and PowerPoint.

## 2. Benchmark data: Memory footprint and startup speed

We tested the release build of DeckCraft alongside Microsoft PowerPoint 365 on an AMD Ryzen 7 7700 system with 16GB of DDR5 RAM running Windows 11. Similar to our setup in [Ollama vs LM Studio testing](/ollama-vs-lmstudio-16gb/), we monitored working set memory and launch times across identical 50-slide sample decks.

* **Cold Launch Time:** DeckCraft launched in 180 milliseconds to an interactive canvas. Microsoft PowerPoint took 1.95 seconds to complete sign-in checks and load user templates.
* **Idle Memory Usage:** DeckCraft consumed 42MB of RAM with an empty presentation loaded. PowerPoint consumed 285MB at idle with background telemetry processes running.
* **Large File Load (50 slides with vector shapes):** DeckCraft took 310 milliseconds and held 78MB of RAM. PowerPoint took 1.2 seconds and held 340MB.
* **Background Network Activity:** DeckCraft registered 0 outbound network requests during our two-hour testing window. PowerPoint registered 38 HTTP requests to authentication and telemetry endpoints.

For terminal power users, DeckCraft includes `deckcraft-cli`. This command-line utility lets developers batch-render entire decks into PDF or PNG slides headlessly without launching the window interface:

```bash
cargo run --release -p deckcraft-cli -- render --sample --all --scale 1 out/
```

In addition, DeckCraft integrates an opt-in Model Context Protocol server. This lets local AI assistants inspect slide contents, rewrite talking points, and insert structured shapes automatically. Readers familiar with [VTuber local LLM testing](/local-llm-vtuber-test/) will recognize the value of local model control without cloud exposure.

## 3. Video walkthroughs and interactive web test

Developers interested in evaluating the software before compiling from source can test the live WebAssembly build directly in modern web browsers:

<div class="rounded-lg border border-hairline dark:border-zinc-800 p-4 bg-stone-50 dark:bg-zinc-800/50 my-4 text-[14px]">
  <p class="font-bold mb-2">Interactive Workbench & Demonstrations:</p>
  <ul class="space-y-1 list-disc list-inside">
    <li><strong>Source Code & Build Flags:</strong> <a href="https://github.com/storytold/deckcraft" target="_blank" rel="noopener" class="underline font-semibold">github.com/storytold/deckcraft</a></li>
    <li><strong>Official Suite Hub:</strong> <a href="https://getartcraft.com/" target="_blank" rel="noopener" class="underline font-semibold">getartcraft.com</a></li>
    <li><strong>License:</strong> Dual-licensed under MIT and Apache-2.0. Clean-room development ensures no proprietary Microsoft source code was viewed or copied.</li>
  </ul>
</div>

Community members have published hands-on video breakdowns demonstrating slide transitions, font metrics, and PPTX round-trip fidelity on YouTube. Because the repository maintainers enforce a lean repository policy, recorded demonstration videos are hosted on video platforms rather than committed into Git version control.

## 4. What is missing: The reality check

While the core presentation engine is stable for slide drafting, DeckCraft is not yet a total drop-in replacement for enterprise teams.

First, real-time multi-user co-authoring is absent. PowerPoint allows dozens of remote team members to edit simultaneously via SharePoint and OneDrive. DeckCraft is fundamentally an offline-first tool. Second, complex 3D shape extrusions, morph transitions, and legacy Visual Basic for Applications macros do not execute. For straightforward corporate slide decks and academic talks, DeckCraft offers a lightning-fast alternative that eliminates annual licensing fees.

## Sources to check yourself

- DeckCraft GitHub Repository — Source code, crate architecture, and build documentation.
- Storytold ArtCraft Apps — Product overview, platform targets, and licensing specifications.

## Frequently asked questions

**Q: Can DeckCraft open files created by Microsoft PowerPoint?**
A: Yes. DeckCraft parses native `.pptx` files, preserving layout structures, text formatting, and unrecognized Microsoft XML tags.

**Q: Does DeckCraft require an internet connection or user account?**
A: No. DeckCraft has zero network telemetry, requires no login, and runs entirely offline on local hardware.

**Q: What operating systems does DeckCraft run on?**
A: DeckCraft compiles natively for Windows, macOS, Linux, FreeBSD, and modern WebAssembly environments.
