// Permanent topic hubs. Curated, not generated from tags: a hub is a promise
// that a subject will keep being covered at a stable URL.
export interface TopicGroup {
  title: string;
  slugs: string[];
}

export interface Topic {
  slug: string;
  kicker: string;
  title: string;
  description: string;
  intro: string;
  slugs: string[];
  groups?: TopicGroup[];
}

export const TOPICS: Topic[] = [
  {
    slug: 'open-source-alternatives',
    kicker: 'Permanent guide',
    title: 'Open-source alternatives, tested',
    description: 'Pure-Rust and open-source alternatives to Adobe, Microsoft Office, AutoCAD, Acrobat and GitHub — each checked against its own repository, not a spec sheet.',
    intro: 'These are the tools people actually search for by name. Every piece here goes to the source repository, states what the project really does, and names what it cannot do yet. This guide is updated as the projects change.',
    slugs: [
      'elayadesign-ai-design-skills-open-source-ui',
      'artcraft-rust-creative-engine-adobe-alternative',
      'wordcraft-rust-word-clean-room-alternative',
      'gridcraft-rust-excel-clean-room-alternative',
      'cadcraft-rust-autocad-clean-room-alternative',
      'pdfcraft-rust-pdf-reader-clean-room-alternative',
      'deckcraft-rust-powerpoint-clean-room-alternative',
      'linkswift-javascript-cloud-storage-direct-download',
      'macro-inc-macro-rust-agpl-workspace-mcp',
      'ruview-rust-wifi-spatial-intelligence-open-source',
      'local-llm-vtuber-test',
      'ollama-vs-lmstudio-16gb',
      'xiaolai-craft-of-selfteaching-jupyter-notebook-surge',
    ],
    groups: [
      { title: 'Creative and design', slugs: ['elayadesign-ai-design-skills-open-source-ui', 'artcraft-rust-creative-engine-adobe-alternative', 'pdfcraft-rust-pdf-reader-clean-room-alternative'] },
      { title: 'Office and documents', slugs: ['wordcraft-rust-word-clean-room-alternative', 'gridcraft-rust-excel-clean-room-alternative', 'deckcraft-rust-powerpoint-clean-room-alternative'] },
      { title: 'Developer tools', slugs: ['cadcraft-rust-autocad-clean-room-alternative', 'linkswift-javascript-cloud-storage-direct-download', 'macro-inc-macro-rust-agpl-workspace-mcp', 'ruview-rust-wifi-spatial-intelligence-open-source'] },
      { title: 'Local AI and self-hosting', slugs: ['local-llm-vtuber-test', 'ollama-vs-lmstudio-16gb', 'xiaolai-craft-of-selfteaching-jupyter-notebook-surge'] },
    ],
  },
  {
    slug: 'air-and-pollution-data',
    kicker: 'Permanent guide',
    title: 'Air quality and pollution data',
    description: 'How to read an AQI number, what Diwali air data actually showed, and why a city ranking can be true and misleading at the same time.',
    intro: 'Air stories return every winter. This hub collects the ones that explain the measurement, not just the headline: what was sampled, which index was used, and what the number does not say.',
    slugs: [
      'how-to-read-rankings',
      'delhi-diwali-2026-air-pollution-aqi-severe-smog-data',
      'delhi-post-diwali-pollution-spike-aqi-1331-record',
      'mumbai-rank-1-india-pollution-construction-delhi-comparison',
      'cyclone-arnab-tracker-latest-updates-andhra-odisha',
      'nepal-flood-early-warning-system-telemetry-limits',
      'pooja-samagri-upcycling-home-river-pollution',
    ],
  },
  {
    slug: 'ai-and-automation',
    kicker: 'Permanent guide',
    title: 'AI tools, agents and deepfakes',
    description: 'What an AI agent can actually do, what local models need to run, and how to tell a synthetic clip from a real one.',
    intro: 'A permanent desk for the tools and the claims around them. We check the documentation, the model card and the original video before repeating what a launch post promised.',
    slugs: [
      'instagram-muse-ai-assistant-privacy-debate',
      'local-llm-vtuber-test',
      'ollama-vs-lmstudio-16gb',
      'elayadesign-ai-design-skills-open-source-ui',
      'xiaolai-craft-of-selfteaching-jupyter-notebook-surge',
      'brazil-bricklayer-ai-girlfriend-tiktok-fact-check',
      'microsoft-veo-voluntary-exit-offer-layoffs-fact-check',
    ],
  },
  {
    slug: 'elections-and-rolls',
    kicker: 'Permanent guide',
    title: 'Elections, rolls and the courts',
    description: 'The Special Intensive Revision, the constitutional arithmetic behind seat changes, and what the courts have actually ordered.',
    intro: 'Electoral claims travel fast and the underlying documents are slow. This hub keeps the primary record: court orders, affidavits, division counts and the numbers behind each seat projection.',
    slugs: [
      'supreme-court-cec-gyanesh-kumar-sir-hearing',
      'cjp-protest-crackdown-jantar-mantar-oct-10',
      'cjp-protest-october-2',
      'lok-sabha-850-seats-delimitation-bill-mathematics',
      'rahul-gandhi-acquitted-amit-shah-defamation-case-sultanpur',
      'fightkaro-sansad-showdown-game-facts-check',
    ],
  },
  {
    slug: 'jobs-and-layoffs',
    kicker: 'Permanent guide',
    title: 'Jobs, layoffs and pay',
    description: 'Verified layoff totals, what severance rules actually say, and the difference between a pay hike and an arrears promise.',
    intro: 'Headline job numbers are easy to inflate. Each story here names the filing, the quarter and the definition used, so the next round of announcements can be compared against the same baseline.',
    slugs: [
      'tech-layoffs-2026-intel-oracle-amazon-microsoft-meta-tcs',
      'microsoft-veo-voluntary-exit-offer-layoffs-fact-check',
      'qualcomm-india-layoffs-severance-package-facts',
      'us-perm-suspension-microsoft-indian-it-vance-controversy',
      'bank-strike-deferred-7-day-work-week',
      'central-govt-da-hike-8th-pay-commission-arrears',
      'ex-cognizant-hr-quits-delhi-goa-reality-check',
    ],
  },
  {
    slug: 'himalayan-frontiers',
    kicker: 'Permanent guide',
    title: 'Himalayan frontiers and borderlands',
    description: 'What local communities report along the LAC, the dams planned in the same valleys, and the disaster risks those slopes carry.',
    intro: 'Border stories are usually told from a distance. This hub keeps the local record alongside the satellite imagery, and tracks the projects that change the same ground.',
    slugs: [
      'arunachal-pradesh-china-encroachment-border-citizens-delhi-troops',
      'katon-moyong-arunachal-siang-mega-dam-protest',
      'manipur-kamjong-village-torched-kuki-naga-clashes',
      'manipur-nongshum-ambush-cm-house-body-protest',
      'manipur-thoubal-concert-clashes-curfew-orders',
      'nepal-flash-floods-landslides-glaciers-india-threat',
      'nepal-flood-early-warning-system-telemetry-limits',
    ],
  },
  {
    slug: 'rankings-and-data',
    kicker: 'Permanent guide',
    title: 'Rankings, maps and what the data says',
    description: 'Happiness ladders, safety maps and passport tables read as recipes: who was sampled, what was asked, and which ingredient moved the number.',
    intro: 'A ranking is a claim dressed as a number. This hub keeps the guides that show the denominator, the question wording and the gap between a country and its cell in a table.',
    slugs: [
      'how-to-read-rankings',
      'safest-country-maps-footnote',
      'finland-happiest-bangladesh-reality',
      'dhaka-beyond-rank',
      'passport-lists-recount',
      'sweden-crime-survey-vs-police',
      'britain-crime-claim-vs-data',
      'uk-royal-approval-vs-queen-elizabeth',
    ],
  },
  {
    slug: 'nvidia-and-chips',
    kicker: 'Permanent guide',
    title: 'Nvidia, Jensen Huang and the chip market',
    description: 'Every verified development in one place: the succession rumours, the spy-probe claim, the cargo heist and what the market did.',
    intro: 'A single company now drives a remarkable share of viral technology claims. This hub separates the confirmed from the speculated and keeps the corrections visible.',
    slugs: [
      'jensen-huang-nvidia-scandal-chinese-spy-probe',
      'trump-confirms-fbi-investigating-jensen-huang-nvidia',
      'nvidia-ceo-jensen-huang-resigns-who-can-replace-him',
      'nvidia-gpu-cargo-heist-data-center-chips-stolen',
      'wall-street-stock-market-crash-ai-bubble-midterms',
    ],
  },
];

/** Hubs that contain this article, in priority order. */
export function hubsFor(slug: string): Topic[] {
  return TOPICS.filter((t) => t.slugs.includes(slug));
}
