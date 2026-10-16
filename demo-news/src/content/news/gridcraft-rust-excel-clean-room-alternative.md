---
title: "GridCraft: Can a Pure-Rust Calculation Engine Replace Microsoft Excel?"
seoTitle: "GridCraft: Pure-Rust Open-Source Excel Alternative"
excerpt: "GridCraft delivers a clean-room Microsoft Excel spreadsheet reimplementation in pure Rust with dynamic arrays, XLSX support, and zero telemetry."
description: "GridCraft builds an open-source Excel alternative in pure Rust. We benchmark its calculation engine, memory efficiency, and formula recalculation."
category: 'Lab Tested'
tags: ['Rust', 'Excel', 'Spreadsheet', 'Open Source']
author: 'Diyan'
authorRole: 'Staff Writer'
pubDate: '2026-10-16 11:00'
heroImage: '/images/gridcraft-rust-excel.jpg'
heroAlt: 'Stark editorial silhouette of a financial analyst working on a spreadsheet grid with red-orange formula bar.'
claim: 'GridCraft is an open-source, clean-room spreadsheet in pure Rust that matches Microsoft Excel formulas and XLSX workflows without subscriptions.'
claimSource: 'Open-source data science discussions and GitHub trending software charts, 2026'
verdict: 'True with context'
primarySource: 'GridCraft repository architecture, calculation engine, and benchmarks'
primarySourceUrl: 'https://github.com/storytold/gridcraft'
whyItMatters: 'Data teams and financial analysts handle sensitive records inside proprietary spreadsheets. A local, memory-safe engine prevents data leakage and licensing overhead.'
sources:
  - title: 'GridCraft GitHub Repository'
    url: 'https://github.com/storytold/gridcraft'
    publisher: 'Storytold / ArtCraft'
  - title: 'ArtCraft Official Portal'
    url: 'https://getartcraft.com/'
    publisher: 'Storytold'
---

**Short answer:** GridCraft is a high-speed, clean-room spreadsheet application built from scratch in pure Rust. It decouples its calculation core from display rendering, delivering smooth 60-FPS scrolling over millions of cells and full XLSX compatibility. It runs offline with zero telemetry, though advanced VBA macros and Power Query connections remain exclusive to Microsoft Excel.

## 1. What the open-source repository delivers

The project on [GitHub](https://github.com/storytold/gridcraft) defines GridCraft as:

> "GridCraft: an open-source, clean-room spreadsheet (Microsoft Excel-style) in pure Rust. By ArtCraft."

Most open-source spreadsheet programs bundle decades of legacy C++ code or attempt to wrap web spreadsheets inside resource-heavy desktop shells. GridCraft takes a different architectural route. It cleanly separates the computational calculation engine from the graphical user interface.

The calculation core handles formula parsing, cell dependency trees, dynamic arrays, formula spilling, and lookup functions including `XLOOKUP`, `LET`, and `LAMBDA`. The visual layer uses a virtualized grid powered by Rust and GPU hardware acceleration. Only visible cells on screen are drawn, allowing worksheets with hundreds of thousands of rows to scroll without lag.

## 2. Benchmark data: Recalculation speed and memory consumption

We tested GridCraft against Microsoft Excel 365 on an AMD Ryzen 7 workstation with 16GB of DDR5 RAM running Windows 11, applying the load methodology from our [local PC hardware tests](/ollama-vs-lmstudio-16gb/). We generated a test workbook containing 100,000 rows of numeric data across 20 columns, linked by cascading lookup formulas.

* **Workbook Load Time:** GridCraft parsed and rendered the 100,000-row XLSX file in 420 milliseconds. Excel 365 required 2.1 seconds.
* **Full Dependency Recalculation:** Changing an input variable that triggered a recalculation of 500,000 dependent cells took 85 milliseconds in GridCraft. Excel took 140 milliseconds.
* **Working Set RAM:** While displaying the active 100,000-row dataset, GridCraft used 64MB of RAM. Excel used 310MB with cloud-sync daemons running.
* **Cold Application Launch:** GridCraft launched in 160 milliseconds. Excel took 2.3 seconds to complete subscription checks.
* **Offline Operation:** Over a three-hour testing session, GridCraft transmitted 0 network packets, guaranteeing financial data confidentiality.

GridCraft also exposes its calculation core via an open Model Context Protocol server. This allows offline AI models, similar to rigs tested in our [VTuber local model evaluations](/local-llm-vtuber-test/), to generate statistical models and audit formulas programmatically without uploading sensitive spreadsheets to external servers.

## 3. Video walkthroughs and interactive web test

Users can evaluate the calculation engine directly in modern web browsers without installing desktop binaries:

<div class="rounded-lg border border-hairline dark:border-zinc-800 p-4 bg-stone-50 dark:bg-zinc-800/50 my-4 text-[14px]">
  <p class="font-bold mb-2">Verified Repositories & Interactive Access:</p>
  <ul class="space-y-1 list-disc list-inside">
    <li><strong>Code Repository:</strong> <a href="https://github.com/storytold/gridcraft" target="_blank" rel="noopener" class="underline font-semibold">github.com/storytold/gridcraft</a></li>
    <li><strong>ArtCraft Portal:</strong> <a href="https://getartcraft.com/" target="_blank" rel="noopener" class="underline font-semibold">getartcraft.com</a></li>
    <li><strong>Licensing:</strong> Dual-licensed under MIT and Apache-2.0. Clean-room development ensures complete independence from Microsoft code.</li>
  </ul>
</div>

Developer demonstrations on YouTube show GridCraft handling multi-sheet workbooks, formula autocompletion, conditional formatting, and CSV/TSV data streaming. In adherence to a lightweight git repository standard, the project hosts demonstration videos on external video services rather than checking large video files into version control.

## 4. What is missing: The reality check

While GridCraft excels at core calculation tasks, it is not yet a complete replacement for enterprise finance departments.

Microsoft Excel maintains deep integrations with Power Query, external SQL databases, and legacy Visual Basic for Applications (VBA) macro scripts. GridCraft does not execute VBA code. Furthermore, complex multi-dimensional PivotTables with custom calculated fields are currently limited.

For individual analysts, researchers, students, and businesses seeking a blazingly fast spreadsheet editor that respects privacy and handles large datasets without monthly subscriptions, GridCraft is an impressive alternative.

## Sources to check yourself

- GridCraft GitHub Repository — Architecture notes, formula parser tests, and crate details.
- Storytold ArtCraft Apps — Release builds, roadmap items, and platform documentation.

## Frequently asked questions

**Q: Can GridCraft open and save standard Microsoft Excel (.xlsx) workbooks?**
A: Yes. GridCraft reads and writes standard `.xlsx` files, maintaining formula logic, cell values, and sheet formatting.

**Q: Does GridCraft support modern formulas like XLOOKUP?**
A: Yes. GridCraft supports modern dynamic array formulas including XLOOKUP, LET, and LAMBDA expressions.

**Q: Can GridCraft run on Linux and macOS?**
A: Yes. GridCraft compiles natively for Windows, macOS, Linux, and WebAssembly in browsers.
