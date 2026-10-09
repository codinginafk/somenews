// Single source of truth for verdict display.
// §4 of AGENTS.md defines the legal set; this maps any drifted legacy string
// onto a tone so the UI can never render a ragged or inconsistent verdict.
// v2: verdict renders ONLY as one bold line under the article dek — never on
// cards, lists, rails or the homepage. `Explainer` (neutral) renders no line.
export type VerdictTone = 'false' | 'misleading' | 'context' | 'true' | 'neutral';

// Order matters: check the severe prefixes before the softer `True with context`.
const MATCHERS: Array<[RegExp, VerdictTone]> = [
  [/^\s*false\b/i, 'false'],
  [/^\s*misleading\b/i, 'misleading'],
  [/^\s*missing context\b/i, 'context'],
  [/^\s*true with context\b/i, 'true'],
  [/^\s*true\b/i, 'true'],
  [/^\s*(lab result|field brief|explainer)\b/i, 'neutral'],
];

function toneOf(raw?: string | null): VerdictTone | null {
  if (!raw) return null;
  for (const [re, tone] of MATCHERS) {
    if (re.test(raw)) return tone;
  }
  return 'neutral';
}

const PHRASES: Record<VerdictTone, string> = {
  false: 'false alarm.',
  misleading: 'misleading.',
  context: 'missing context.',
  true: 'true, with context.',
  neutral: '',
};

/** One-line verdict for the article dek. `Explainer` and stray values → null. */
export function verdictLine(raw?: string | null): { phrase: string; tone: VerdictTone } | null {
  const tone = toneOf(raw);
  if (!tone || tone === 'neutral' || !PHRASES[tone]) return null;
  return { phrase: PHRASES[tone], tone };
}

/** Tailwind text classes per tone for the verdict phrase (light + dark). */
export function toneTextClass(tone: VerdictTone): string {
  switch (tone) {
    case 'false':
      return 'text-red-600 dark:text-red-400';
    case 'misleading':
      return 'text-orange-600 dark:text-orange-400';
    case 'context':
      return 'text-amber-700 dark:text-amber-400';
    case 'true':
      return 'text-emerald-600 dark:text-emerald-400';
    default:
      return '';
  }
}

/** Weight for "worth your time" ranking: sharper verdicts earn more attention. */
export function verdictWeight(raw?: string | null): number {
  switch (toneOf(raw)) {
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
