/**
 * analyzer.mjs — deterministic AI-slop fingerprint engine.
 *
 * Pure JS, zero dependencies, instant. Produces an ordinal 0-100 score from
 * documented stylistic tells. This is NOT a calibrated probability of
 * authorship — it ranks "how much does this text LOOK like raw AI output".
 *
 * Signals (with caps):
 *   tier1 buzzwords      20   "delve", "tapestry", "seamless", ...
 *   tier2 repeats         8   legitimate words overused (repeated >= 3x)
 *   tell phrases         15   "in today's fast-paced world", ...
 *   weak openers          5   "Certainly,", "let me walk you through"
 *   em/en dashes         10   ~73% of GPT-4 long-form vs ~12% human (Guo et al.)
 *   "actually" fillers    5   documented overuse word
 *   burstiness (CV)      20   human > 0.4, AI < 0.2 (Aletheia thresholds)
 *   lexical diversity    10   low TTR = generic padding
 *   trigram repetition    5   formulaic n-gram reuse
 *   rhythm runs           5   long stretches of same-length sentences
 *   typography tells      5   curly quotes, ellipsis, nbsp
 *   bold-bullet formula   5   "**Word:** explanation" repetition
 */

import {
  BUZZWORDS_TIER1,
  BUZZWORDS_TIER2,
  TELL_PHRASES,
  WEAK_OPENERS,
  FILLER_WORDS,
  TYPOGRAPHY_TELLS,
} from "./wordlists.mjs";

const PER_300 = 300;
const MAX_MATCHES = 60;

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export function stripCodeBlocks(text) {
  // Fenced code blocks (``` or ~~~) are non-prose and excluded from scoring.
  const blocks = text.match(/```[\s\S]*?```|~~~[\s\S]*?~~~/g) || [];
  const stripped = text.replace(/```[\s\S]*?```|~~~[\s\S]*?~~~/g, " ").replace(/\n{3,}/g, "\n\n");
  return { text: stripped, codeBlocks: blocks.length, codeChars: blocks.join("").length };
}

export function extractStats(text) {
  const normalized = text.replace(/\r/g, "").replace(/[\t ]+/g, " ").trim();
  const words = normalized.split(/\s+/).filter((w) => w.length > 0);
  const wordCount = words.length;

  const sentences = normalized
    .split(/[.!?…]+(?:\s+)?(?=[A-Z0-9"“'(])|\n+|[.!?…]+$/g)
    .map((s) => s.trim().replace(/^[-*•\d.)]+\s*/, ""))
    .filter((s) => s.split(/\s+/).filter((w) => w.length > 0).length >= 1);

  const sentenceLengths = sentences.map(
    (s) => s.split(/\s+/).filter((w) => w.length > 0).length
  );

  const paragraphs = normalized.split(/\n\s*\n/).filter((p) => p.trim().length > 0);
  const lines = normalized.split(/\n/);

  return { text: normalized, lower: normalized.toLowerCase(), words, wordCount, sentences, sentenceLengths, paragraphs, lines };
}

function per300(count, wordCount) {
  return wordCount > 0 ? (count / wordCount) * PER_300 : 0;
}

function collectMatches(stats) {
  const { text, lower } = stats;
  const matches = []; // { category, term, hint, start, end, weight }

  const wordRegex = (word) => new RegExp(`\\b${escapeRegex(word)}\\b`, "g");

  for (const { word, hint } of BUZZWORDS_TIER1) {
    const re = wordRegex(word);
    let m;
    while ((m = re.exec(lower)) !== null) {
      matches.push({ category: "buzzword", term: word, hint, start: m.index, end: m.index + word.length, weight: 1 });
    }
  }

  // tier2: only counts when the SAME word is used repeatedly (>= 3x)
  const tier2Counts = new Map();
  for (const { word, hint } of BUZZWORDS_TIER2) {
    const re = wordRegex(word);
    let m;
    while ((m = re.exec(lower)) !== null) {
      const key = word;
      tier2Counts.set(key, (tier2Counts.get(key) || 0) + 1);
      matches.push({ category: "buzzword-repeat", term: word, hint, start: m.index, end: m.index + word.length, weight: 0.5, repeatedOnly: true });
    }
  }

  const phraseRegex = (p) => new RegExp(`(?<![\\w])${escapeRegex(p)}(?![\\w])`, "gi");

  for (const { phrase, hint } of TELL_PHRASES) {
    const re = phraseRegex(phrase);
    let m;
    while ((m = re.exec(text)) !== null) {
      matches.push({ category: "phrase", term: phrase, hint, start: m.index, end: m.index + phrase.length, weight: 2 });
    }
  }

  for (const { phrase, hint } of WEAK_OPENERS) {
    const re = phraseRegex(phrase);
    let m;
    while ((m = re.exec(text)) !== null) {
      matches.push({ category: "opener", term: phrase, hint, start: m.index, end: m.index + phrase.length, weight: 2 });
    }
  }

  for (const word of FILLER_WORDS) {
    const re = wordRegex(word);
    let m;
    while ((m = re.exec(lower)) !== null) {
      matches.push({ category: "filler", term: word, hint: `"${word}" is a documented overuse word - cut it 90% of the time.`, start: m.index, end: m.index + word.length, weight: 0.8 });
    }
  }

  // typography tells
  for (const { char, name, hint } of TYPOGRAPHY_TELLS) {
    let idx = text.indexOf(char);
    while (idx !== -1) {
      matches.push({ category: "typography", term: name, hint, start: idx, end: idx + char.length, weight: 0 });
      idx = text.indexOf(char, idx + 1);
      if (idx > 200000) break;
    }
  }

  // de-dupe overlapping matches (keep the longer, earlier term)
  matches.sort((a, b) => (a.start - b.start) || (b.end - a.end));
  const kept = [];
  let lastEnd = -1;
  for (const m of matches) {
    if (m.start >= lastEnd) {
      kept.push(m);
      lastEnd = m.end;
    } else if (kept.length && m.end > kept[kept.length - 1].end && m.start === kept[kept.length - 1].start) {
      kept.pop();
      kept.push(m);
      lastEnd = m.end;
    }
  }

  return kept;
}

function contextAround(text, start, end, pad = 70) {
  const from = Math.max(0, start - pad);
  const to = Math.min(text.length, end + pad);
  const prefix = from > 0 ? "..." : "";
  const suffix = to < text.length ? "..." : "";
  return (prefix + text.slice(from, to) + suffix).replace(/\s+/g, " ").trim();
}

function scoreBurstiness(stats) {
  const { sentenceLengths, wordCount } = stats;
  if (sentenceLengths.length < 3) {
    return { points: 0, cv: 0, mean: 0, sd: 0, short: true, note: "Too few sentences to judge rhythm." };
  }
  const mean = sentenceLengths.reduce((a, b) => a + b, 0) / sentenceLengths.length;
  const variance = sentenceLengths.reduce((a, b) => a + (b - mean) ** 2, 0) / sentenceLengths.length;
  const sd = Math.sqrt(variance);
  const cv = mean > 0 ? sd / mean : 0;

  let points;
  if (cv < 0.2) points = 20;
  else if (cv < 0.3) points = 16;
  else if (cv < 0.4) points = 10;
  else if (cv < 0.5) points = 4;
  else points = 0;

  const short = sentenceLengths.length < 8 || wordCount < 80;
  if (short) points = Math.round(points / 2);

  return { points, cv: +cv.toFixed(3), mean: +mean.toFixed(1), sd: +sd.toFixed(1), short, note: short ? "Text too short - rhythm signal halved." : "" };
}

function scoreLexicalDiversity(stats) {
  const { words, wordCount } = stats;
  if (wordCount < 50) return { points: 0, ttr: 0, short: true, note: "Too short to judge vocabulary range." };
  const unique = new Set(words.map((w) => w.toLowerCase())).size;
  const ttr = unique / wordCount;
  let points;
  if (ttr < 0.35) points = 10;
  else if (ttr < 0.45) points = 7;
  else if (ttr < 0.55) points = 4;
  else points = 1;
  return { points, ttr: +ttr.toFixed(3), short: false, note: "" };
}

function scoreTrigramRepetition(stats) {
  const { words, wordCount } = stats;
  if (wordCount < 40) return { points: 0, repeated: 0, surplus: 0 };
  const trigrams = new Map();
  const lower = words.map((w) => w.toLowerCase());
  for (let i = 0; i < lower.length - 2; i++) {
    const t = `${lower[i]} ${lower[i + 1]} ${lower[i + 2]}`;
    trigrams.set(t, (trigrams.get(t) || 0) + 1);
  }
  let surplus = 0;
  let repeated = 0;
  for (const [t, f] of trigrams) {
    if (f > 1) {
      surplus += f - 1;
      repeated++;
    }
  }
  const per500 = wordCount > 0 ? (surplus / wordCount) * 500 : 0;
  return { points: Math.min(5, per500 * 1.5), repeated, surplus, per500: +per500.toFixed(2) };
}

function scoreRhythmRuns(stats) {
  const { sentenceLengths } = stats;
  if (sentenceLengths.length < 8) return { points: 0, longestRun: 0 };
  let longestRun = 1;
  let run = 1;
  for (let i = 1; i < sentenceLengths.length; i++) {
    if (Math.abs(sentenceLengths[i] - sentenceLengths[i - 1]) <= 4) {
      run++;
      longestRun = Math.max(longestRun, run);
    } else {
      run = 1;
    }
  }
  const points = longestRun >= 4 ? Math.min(5, (longestRun - 3) * 0.6) : 0;
  return { points, longestRun };
}

function scoreBoldBullets(stats) {
  const { lines, wordCount } = stats;
  const re = /^\s*(?:[-*•]?\s*)?\*\*[^*]{1,40}\*\*\s*:?/;
  let count = 0;
  for (const line of lines) {
    if (re.test(line)) count++;
  }
  return { points: Math.min(5, per300(count, wordCount) * 2), count, per300: +per300(count, wordCount).toFixed(2) };
}

function scoreTypography(stats) {
  const { text, wordCount } = stats;
  let points = 0;
  const found = [];
  for (const { char, name } of TYPOGRAPHY_TELLS) {
    const count = text.split(char).length - 1;
    if (count > 0) {
      found.push({ name, count });
      if (char === "—") points += Math.min(3, count * 0.8);
      else if (char === "…" || char === "\u00a0") points += Math.min(1.5, count * 0.3);
      else points += Math.min(1.5, count * 0.2);
    }
  }
  return { points: Math.min(5, points), found, per300: +per300(found.reduce((a, f) => a + f.count, 0), wordCount).toFixed(2) };
}

export function analyze(text, preparedInfo = {}) {
  const stats = extractStats(text);
  const { wordCount } = stats;
  const short = wordCount < 40;
  const codeBlocks = preparedInfo.codeBlocks || 0;

  const kept = collectMatches(stats);
  const deduped = short
    ? kept
    : kept.filter((m) => m.category !== "buzzword-repeat" || kept.filter((x) => x.category === "buzzword-repeat" && x.term === m.term).length >= 3);

  const weighted = deduped.reduce((acc, m) => acc + m.weight, 0);
  const per300w = per300(weighted, wordCount);

  const byCategory = {};
  for (const m of deduped) {
    if (!byCategory[m.category]) byCategory[m.category] = [];
    byCategory[m.category].push(m);
  }

  const tier1 = byCategory.buzzword || [];
  const tier2 = byCategory["buzzword-repeat"] || [];
  const phrases = byCategory.phrase || [];
  const openers = byCategory.opener || [];
  const fillers = byCategory.filler || [];
  const typo = byCategory.typography || [];

  const t1per300 = per300(tier1.length, wordCount);
  const buzzPoints = Math.min(20, t1per300 * 5);

  const tier2Per300 = per300(tier2.length, wordCount);
  const tier2Points = wordCount < 40 ? 0 : Math.min(8, tier2Per300 * 2);

  const phrasePer300 = per300(phrases.length, wordCount);
  const phrasePoints = Math.min(15, phrasePer300 * 6);

  const openerPer300 = per300(openers.length, wordCount);
  const openerPoints = Math.min(5, openerPer300 * 3);

  const fillerPer500 = wordCount > 0 ? (fillers.length / wordCount) * 500 : 0;
  const fillerPoints = Math.min(5, fillerPer500 * 2.5);

  const emDashes = stats.text.split("—").length - 1 + (stats.text.split("–").length - 1) * 0.5 + (stats.text.match(/---/g) || []).length;
  const emPer300 = per300(emDashes, wordCount);
  const emPoints = Math.min(10, emPer300 * 4);

  const burst = scoreBurstiness(stats);
  const ttr = scoreLexicalDiversity(stats);
  const tri = scoreTrigramRepetition(stats);
  const rhythm = scoreRhythmRuns(stats);
  const bullets = scoreBoldBullets(stats);
  const typoInfo = scoreTypography(stats);

  const score = Math.min(100, Math.round(
    buzzPoints + tier2Points + phrasePoints + openerPoints + fillerPoints +
    emPoints + burst.points + ttr.points + tri.points + rhythm.points +
    bullets.points + typoInfo.points
  ));

  const grade =
    score <= 19 ? "Human-sounding" :
    score <= 39 ? "Mostly human, minor tells" :
    score <= 59 ? "AI-assisted (edited)" :
    score <= 79 ? "Likely raw AI output" :
    "AI slop";

  const matchList = deduped
    .slice(0, MAX_MATCHES)
    .map((m) => ({
      category: m.category,
      term: m.term,
      hint: m.hint,
      context: contextAround(stats.text, m.start, m.end),
    }));

  const humanize = buildHumanizeList({
    emPoints, emPer300, fillerPoints, fillerPer500, buzzPoints, tier1,
    phrases, openers, burst, ttr, tri, rhythm, bullets, typoInfo,
  });

  return {
    meta: {
      words: wordCount,
      sentences: stats.sentences.length,
      paragraphs: stats.paragraphs.length,
      chars: stats.text.length,
      short,
      codeBlocks,
      detectedType: codeBlocks > 0 && wordCount < 40 ? "code" : "prose",
    },
    score,
    grade,
    signals: {
      buzzwords: { points: +buzzPoints.toFixed(1), count: tier1.length, per300: +t1per300.toFixed(2) },
      repeatedWords: { points: +tier2Points.toFixed(1), count: tier2.length, per300: +tier2Per300.toFixed(2) },
      phrases: { points: +phrasePoints.toFixed(1), count: phrases.length, per300: +phrasePer300.toFixed(2) },
      openers: { points: +openerPoints.toFixed(1), count: openers.length, per300: +openerPer300.toFixed(2) },
      fillers: { points: +fillerPoints.toFixed(1), count: fillers.length, per500: +fillerPer500.toFixed(2) },
      emDashes: { points: +emPoints.toFixed(1), weightedCount: emDashes, per300: +emPer300.toFixed(2) },
      burstiness: burst,
      lexicalDiversity: ttr,
      repetition: tri,
      rhythm: rhythm,
      boldBullets: bullets,
      typography: typoInfo,
    },
    matches: matchList,
    humanize,
  };
}

function buildHumanizeList(s) {
  const items = [];
  if (s.emPoints >= 4 && s.emPer300 >= 0.8) {
    items.push({ action: "Replace em dashes", detail: "Swap every \"—\" for \" - \" (space hyphen space). The em dash is the single most common AI tell." });
  }
  if (s.fillerPoints >= 2.5 && s.fillerPer500 >= 1) {
    items.push({ action: "Cut \"actually\"", detail: "Remove \"actually\" - it adds nothing 90% of the time." });
  }
  if (s.tier1.length > 0) {
    const top = [...new Set(s.tier1.map((m) => m.term))].slice(0, 8).join(", ");
    items.push({ action: "Cut AI buzzwords", detail: `Found: ${top}. Replace each with plain language (see hints under each match).` });
  }
  if (s.phrases.length > 0) {
    const top = [...new Set(s.phrases.map((m) => m.term))].slice(0, 5).join(", ");
    items.push({ action: "Remove stock phrases", detail: `Found: ${top}. These clichés are the fastest way readers spot AI writing.` });
  }
  if (s.openers.length > 0) {
    items.push({ action: "Cut chat-style openers", detail: "\"Certainly,\", \"Let me walk you through\" etc. make it read like a chatbot answer." });
  }
  if (s.burst.points >= 8) {
    items.push({ action: "Vary sentence length", detail: `Sentence rhythm is too flat (CV ${s.burst.cv}). Mix in short punchy sentences between long ones. Aim for CV above 0.4.` });
  }
  if (s.ttr.points >= 7) {
    items.push({ action: "Add specific detail", detail: `Vocabulary range is narrow (TTR ${s.ttr.ttr}). Add real numbers, names, examples, first-hand observations.` });
  }
  if (s.tri.points >= 3) {
    items.push({ action: "Rewrite repeated phrasing", detail: `${s.tri.repeated} trigrams repeat. Reuse of the same 3-word constructions is a formulaic-AI signature.` });
  }
  if (s.rhythm.points >= 3) {
    items.push({ action: "Break the rhythm", detail: `${s.rhythm.longestRun} consecutive sentences are nearly the same length. Break the pattern.` });
  }
  if (s.bullets.points >= 3) {
    items.push({ action: "Vary bullet formatting", detail: "The bold-word-colon bullet formula (**Term:** text) is an AI habit. Mix in plain sentences." });
  }
  if (s.typoInfo.found.length > 0) {
    items.push({ action: "Straighten typography", detail: "Curly quotes, ellipses and non-breaking spaces are typeset-data tells. Use plain characters." });
  }
  if (items.length === 0) {
    items.push({ action: "Keep the voice", detail: "No major tells found. Keep the specific detail and natural rhythm." });
  }
  items.push({
    action: "Add what a model cannot know",
    detail: "Numbers from your own tests, mistakes you made, screenshots, first-hand observations. One verifiable specific beats an hour of paraphrasing.",
  });
  items.push({
    action: "Proofread for substance, not style",
    detail: "Check for misarticulated ideas, hallucinations, and overly wordy sentences. A detector measures style; Google and readers measure whether it is true and useful.",
  });
  return items;
}
