---
title: 'Can Your Laptop Run a 70B Model? The Memory Maths'
seoTitle: "Running a 70B model on one PC: the memory maths"
excerpt: "A 70B model weighs about 42 GB. Here is what the model runners' own documentation says about VRAM, RAM, quantisation and context length, and why the laptop answer is no."
description: "A 70B model weighs about 42 GB. The model runners' own documentation on VRAM, RAM, quantisation and context length, and why the answer on a laptop is no."
category: 'Lab Tested'
tags: ['local LLM', 'VRAM', 'Ollama', 'LM Studio']
author: 'Yash'
authorRole: 'Contributing Writer'
pubDate: '2026-09-19 16:06'
updatedDate: '2026-11-15'
heroImage: '/images/lab-tested.svg'
heroAlt: 'Category artwork showing a terminal benchmark reading tok/s 31.2 stable above a bar chart with one bar marked in vermilion'
claim: 'Any laptop can run a 70B model fine.'
claimSource: 'Viral tech clip'
verdict: 'False — with context'
primarySource: 'Ollama Local FAQ and LM Studio system requirements documentation'
primarySourceUrl: 'https://docs.ollama.com/faq'
whyItMatters: 'Local-model hype promises privacy and zero cost. The memory arithmetic behind that promise is settled, and it is not what the clips suggest.'
sources:
  - title: 'Local FAQ - Ollama'
    url: 'https://docs.ollama.com/faq'
    publisher: 'Ollama'
  - title: 'System Requirements | LM Studio'
    url: 'https://lmstudio.ai/docs/system-requirements'
    publisher: 'LM Studio'
  - title: 'Per-model Defaults | LM Studio'
    url: 'https://lmstudio.ai/docs/app/advanced/per-model'
    publisher: 'LM Studio'
  - title: 'Get started with LM Studio | LM Studio'
    url: 'https://lmstudio.ai/docs/app/basics'
    publisher: 'LM Studio'
  - title: 'Download an LLM | LM Studio'
    url: 'https://lmstudio.ai/docs/app/basics/download-model'
    publisher: 'LM Studio'
---

**Short answer:** No. A 70B model does not fit on a laptop, and the model runners themselves document why. Ollama's own documentation shows a 70B model as a 42 GB download, and its `ollama ps` output describes where a model is loaded, entirely on the GPU, entirely in system memory, or split across both. LM Studio's system requirements ask for at least 16GB of RAM and at least 4GB of dedicated VRAM. A 42 GB weight file cannot sit inside 16GB of system memory, let alone inside a phone or a thin laptop. What changes the answer is not a better laptop. It is quantisation, context length and accepting that part of the model runs on the CPU.

*Correction (2026-11-15): This article previously presented quotes from three unnamed creators and described their hardware and tokens per second. No verifiable source for those quotes, timestamps or creator permissions exists, so they have been removed rather than paraphrased. The article now reports what the model runners publish in their own documentation. The viral claim has been rewritten to the version the record actually addresses, and the two publisher homepage citations have been replaced with five documentation pages.*

## 1. The claim and what it gets wrong

The clip that circulates shows a laptop running a 70-billion-parameter model as if it were nothing special. The claim is not that the machine is fast. It is that the thing works at all, on that machine, at that size.

The documentation does not support it. Three constraints decide whether a model runs locally, and all three are arithmetic rather than opinion: how much memory the weights need, how much of that memory is fast VRAM rather than slow system RAM, and how much context the session has to hold alongside the weights.

## 2. What the weights actually cost

Ollama's FAQ gives the clearest published number. Its example `ollama ps` output lists llama3:70b as a 42 GB model and shows it loaded 100% GPU.

Forty-two gigabytes is the floor for that model, not the headline. And the FAQ documents where a model can live once it is loaded.

The Processor column shows which memory the model was loaded into.
100% GPU means the model was loaded entirely into the GPU.
100% CPU means the model was loaded entirely in system memory.
A split figure such as 48%/52% CPU/GPU means the model was loaded partially onto both.

That third line is the laptop case, and it is the one the clips skip. When the weights do not fit in VRAM, the part that lands on the CPU runs at system memory speed rather than video memory speed. The model still answers. It is simply not the product the clip implies.

The FAQ also documents what happens when a model outgrows one GPU. If the model does not fit entirely on one GPU, then it will be spread across all the available GPUs.

## 3. What the hardware guidance asks for

LM Studio publishes the floor directly.

For macOS, it asks for an Apple Silicon chip, meaning M1, M2, M3 or M4, and macOS 14.0 or newer. It recommends 16GB or more of RAM, and notes that you may still be able to use LM Studio on 8GB Macs if you stick to smaller models and modest context sizes. Intel-based Macs are currently not supported.

For Windows, it supports both x64 and ARM, including Snapdragon X Elite. It requires the AVX2 instruction set for x64 CPUs. It recommends at least 16GB of RAM, noting that LLMs can consume a lot of RAM, and at least 4GB of dedicated VRAM.

For Linux, it supports x64 and ARM64 through an AppImage and asks for Ubuntu 20.04 or newer, with versions newer than 22 not well tested.

Read those numbers against a 42 GB model and the answer is arithmetic. The weights exceed a 16GB laptop's RAM outright, and they exceed 4GB of VRAM by an order of magnitude. The four gigabytes of VRAM in the guidance is for the small models that guidance is aimed at.

## 4. The three levers that actually change the answer

Quantisation is the first lever, and it is why 70B is not the ceiling but is far from the floor. Ollama's FAQ documents that a 70B model can be pulled at a quantised size, and that when a model does not fit the choice becomes which quantisation to use.

The second lever is the context window. By default Ollama uses a context window size of 4096 tokens, overridable with the OLLAMA_CONTEXT_LENGTH environment variable. The FAQ shows the same idea from the other end: parallel request processing for a given model results in increasing the context size by the number of parallel requests, so a 2K context with 4 parallel requests results in an 8K context and additional memory allocation. It also notes that when using GPU inference, new models must be able to completely fit in VRAM to allow concurrent model loads.

Context is memory. Raising it costs you headroom you needed for the weights.

The third lever is the key/value cache. Ollama documents three settings. f16 is high precision and memory usage, and is the default. q8_0 uses approximately half the memory of f16 with a very small loss in precision, usually with no noticeable impact on quality, and is recommended if you are not using f16. q4_0 uses approximately a quarter of the memory of f16 with a small to medium loss in precision that may be more noticeable at higher context sizes. The FAQ also warns that models with a high GQA count may see a larger impact, so the right setting depends on the model and the task.

LM Studio exposes the same levers per model. Its per-model defaults documentation lets you set GPU offload settings for a given model, a particular context size for a given model, and whether to use Flash Attention for a given model. Ollama's FAQ adds that Flash Attention is a feature of most modern models that can significantly reduce memory usage as the context size grows, and that Ollama uses it automatically when the selected backend and devices support it.

So the realistic local setup for a large model on one consumer machine is: a quantised model, a modest context, a reduced cache, and a split load that keeps part of the model on the CPU.

## 5. What this piece does not claim

This is a documentation review, not a benchmark. We are not reporting tokens per second from our own machine, and the earlier version of this article's unsourced tester figures have been removed rather than repeated.

Two things stay open. The documents give requirements and mechanisms, not the exact speed penalty of a CPU split load, which depends on the memory bandwidth of the machine and the size of the layer that lands there. And they do not settle quality: Ollama's own guidance is that the impact of cache quantisation on response quality depends on the model and the task, and that you may need to experiment to find the balance between memory usage and quality.

## 6. The verdict: false, with context

The claim that any laptop can run a 70B model fine is false. A 70B model is about 42 GB of weights, the vendor guidance assumes at least 16GB of RAM and 4GB of dedicated VRAM, and the documented behaviour when a model outgrows VRAM is a split across CPU and GPU that trades speed for the ability to run at all.

The context is that the underlying promise is not empty. Quantisation, cache quantisation, Flash Attention and per-model offload settings have made very large models genuinely runnable on hardware that was not designed for them. A 7B or 13B model at 4-bit, with a sensible context and a reduced cache, is comfortably within what these documents describe for a 16GB machine.

The clips show the end of that range and present it as the start. For a direct comparison of the two runtimes on the same 16GB budget, see our [Ollama versus LM Studio test](/ollama-vs-lmstudio-16gb/), and for more on people running their own tools locally, [the Jupyter self-teaching surge](/xiaolai-craft-of-selfteaching-jupyter-notebook-surge/).

## Sources to check yourself

- [Ollama Local FAQ](https://docs.ollama.com/faq): the 42 GB llama3:70b example, the `ollama ps` processor column, the 4096-token default context, parallel request memory rules, K/V cache quantisation levels and Flash Attention.
- [LM Studio system requirements](https://lmstudio.ai/docs/system-requirements): the Apple Silicon, AVX2, 16GB RAM and 4GB VRAM requirements for macOS, Windows and Linux.
- [LM Studio per-model defaults](https://lmstudio.ai/docs/app/advanced/per-model): setting GPU offload, context size and Flash Attention per model.
- [LM Studio getting started](https://lmstudio.ai/docs/app/basics): the app overview and how models are loaded.
- [LM Studio model downloads](https://lmstudio.ai/docs/app/basics/download-model): where model files come from and what a download contains.

## Frequently asked questions

**Q: How much memory does a 70B model need?**
A: Ollama's documentation lists llama3:70b as a 42 GB model. That is the weight file. Session context and the key/value cache sit on top of it.

**Q: Can I run it on a laptop with 16GB of RAM?**
A: Not entirely. The weights alone are larger than the system memory, so the model has to be split across VRAM and system memory, or partially offloaded to disk. Ollama's FAQ documents the split CPU/GPU state as a normal outcome rather than a failure.

**Q: What is the single most effective setting to change?**
A: Quantisation. Ollama's guidance points at cache quantisation, where q8_0 uses roughly half the memory of f16 and q4_0 roughly a quarter, and at the quantisation of the model itself. Context size is the other big lever, because raising it raises the memory cost directly.

**Q: Does LM Studio need a dedicated GPU?**
A: Its documentation recommends at least 4GB of dedicated VRAM on Windows and at least 16GB of RAM, and it requires AVX2 support for x64 CPUs. On macOS it asks for Apple Silicon, and it notes that Intel-based Macs are currently not supported.
