// Single source of truth for verdict display.
// §4 of AGENTS.md defines the legal set; this maps any drifted legacy string
// onto a tone so the UI can never render a ragged or inconsistent chip.
export type VerdictTone = 'false' | 'misleading' | 'context' | 'true' | 'neutral';

export interface VerdictChip {
  label: string;
  tone: VerdictTone;
}

const CANON: VerdictChip[] = [
  { label: 'False', tone: 'false' },
  { label: 'Misleading', tone: 'misleading' },
  { label: 'Missing context', tone: 'context' },
  { label: 'True with context', tone: 'true' },
  { label: 'Explainer', tone: 'neutral' },
];

// Order matters: check the severe prefixes before the softer `True with context`.
const MATCHERS: Array<[RegExp, VerdictChip]> = [
  [/^\s*false\b/i, CANON[0]],
  [/^\s*misleading\b/i, CANON[1]],
  [/^\s*missing context\b/i, CANON[2]],
  [/^\s*true with context\b/i, CANON[3]],
  [/^\s*true\b/i, CANON[3]],
  [/^\s*(lab result|field brief|explainer)\b/i, CANON[4]],
];

/** Normalise any verdict string (legacy or canonical) into a chip. */
export function verdictChip(raw?: string | null): VerdictChip | null {
  if (!raw) return null;
  for (const [re, chip] of MATCHERS) {
    if (re.test(raw)) return chip;
  }
  return { label: raw.trim(), tone: 'neutral' };
}

/** Tailwind classes per tone. Kept here so every surface styles chips identically. */
export function chipClass(tone: VerdictTone): string {
  switch (tone) {
    case 'false':
      return 'bg-red-100 text-red-800 border-red-200 dark:bg-red-950/50 dark:text-red-300 dark:border-red-900';
    case 'misleading':
      return 'bg-orange-100 text-orange-900 border-orange-200 dark:bg-orange-950/50 dark:text-orange-300 dark:border-orange-900';
    case 'context':
      return 'bg-amber-100 text-amber-900 border-amber-200 dark:bg-amber-950/50 dark:text-amber-300 dark:border-amber-900';
    case 'true':
      return 'bg-emerald-100 text-emerald-800 border-emerald-200 dark:bg-emerald-950/50 dark:text-emerald-300 dark:border-emerald-900';
    default:
      return 'bg-zinc-100 text-zinc-600 border-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:border-zinc-700';
  }
}

/** Weight for "worth your time" ranking: sharper verdicts earn more attention. */
export function verdictWeight(raw?: string | null): number {
  switch (verdictChip(raw)?.tone) {
    case 'false': return 4;
    case 'misleading': return 3;
    case 'context': return 2;
    case 'true': return 2;
    default: return 1;
  }
}

/**
 * Freshness label that never overstates recency.
 * Editors may publish `YYYY-MM-DD` (date only) or `YYYY-MM-DD HH:MM` (with time).
 * A date-only value parses to exactly midnight UTC, so we treat that as "no
 * clock time given" and fall back to a date instead of inventing "2h ago".
 */
export function timeAgo(d: Date, now: Date = new Date()): string {
  const hasClock = d.getUTCHours() !== 0 || d.getUTCMinutes() !== 0;
  const hours = (now.getTime() - d.getTime()) / 36e5;
  if (hasClock && hours >= 0 && hours < 24) {
    if (hours < 1) return `${Math.max(1, Math.round(hours * 60))}m ago`;
    return `${Math.round(hours)}h ago`;
  }
  const days = Math.floor((now.getTime() - d.getTime()) / 864e5);
  if (!hasClock && days <= 1) return 'Today';
  // Pinned to UTC because pubDate is stored with a Z suffix: formatting in the
  // builder's local zone would render a different day than production for any
  // article published late in the UTC day.
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', timeZone: 'UTC' });
}