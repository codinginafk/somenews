import { defineCollection, z } from 'astro:content';

// Frontmatter dates are written as `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` with no
// timezone suffix, which the native Date parser would read as the BUILDER's
// local zone — so the same file would mean a different instant on an editor's
// laptop than on the UTC deploy runner. These are house dates, not instants
// observed at a real clock, so they are always interpreted as UTC.
const houseDate = z.preprocess((v) => {
  if (typeof v !== 'string') return v;
  const s = v.trim();
  if (/^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?)?$/.test(s)) {
    const iso = s.replace(' ', 'T');
    return new Date(iso.length === 10 ? `${iso}T00:00:00Z` : `${iso}Z`);
  }
  return v; // already carries an offset or is a real Date
}, z.coerce.date());

const news = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    seoTitle: z.string().optional(), // SERP/social title; falls back to title (H1)
    description: z.string().optional(), // meta description override; falls back to excerpt
    excerpt: z.string(),
    category: z.string(), // e.g. Exposed, Rankings, Country Files, Tech Tests
    tags: z.array(z.string()).default([]),
    author: z.string().default('Diyan'),
    authorRole: z.string().default('Staff Writer'),
    pubDate: houseDate,
    updatedDate: houseDate.optional(),
    heroImage: z.string().optional(),
    heroAlt: z.string().optional(),
    featured: z.boolean().default(false),
    trending: z.boolean().default(false),
    claim: z.string().optional(), // what viral outlet claimed
    claimSource: z.string().optional(),
    verdict: z.string().optional(), // Missing Context / Misleading / False / True with context
    primarySource: z.string().optional(), // e.g. dataset or document checked
    primarySourceUrl: z.string().optional(),
    whyItMatters: z.string().optional(), // 1-2 sentence stakes box
    sources: z.array(z.object({
      title: z.string(),
      url: z.string(),
      publisher: z.string(),
    })).default([]),
  }),
});

export const collections = { news };
