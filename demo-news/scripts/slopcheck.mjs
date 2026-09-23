// Slop check for editors - repurposed from JobsScraper/slopdetector (heuristic-only, zero deps).
// Usage: npm run slop  (fails CI if any article scores >= 60 "Likely raw AI output")
import fs from 'node:fs';
import path from 'node:path';
import { analyze } from './slop/analyzer.mjs';

const dir = 'src/content/news';
let worst = 0;
for (const f of fs.readdirSync(dir)) {
  if (!f.endsWith('.md')) continue;
  const raw = fs.readFileSync(path.join(dir, f), 'utf8');
  const body = raw.replace(/^---[\s\S]*?---/, '');
  const r = analyze(body);
  const flag = r.score >= 60 ? 'FAIL' : r.score >= 40 ? 'WARN' : 'OK';
  console.log(`${flag} ${f} => ${r.score} (${r.grade}) em:${r.signals.emDashes.weightedCount} buzz:${r.signals.buzzwords.count} phrases:${r.signals.phrases.count}`);
  if (r.matches.length && r.score >= 40) console.log('   tells: ' + r.matches.slice(0, 4).map((m) => m.term).join(' / '));
  worst = Math.max(worst, r.score);
}
if (worst >= 60) { console.error('Slop gate failed. Edit flagged files, then re-run npm run slop.'); process.exit(1); }
console.log('Slop gate passed. Worst score: ' + worst);
