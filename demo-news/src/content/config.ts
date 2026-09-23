import { defineCollection, z } from 'astro:content';

const news = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    excerpt: z.string(),
    category: z.string(), // e.g. Exposed, Rankings, Country Files, Tech Tests
    tags: z.array(z.string()).default([]),
    author: z.string().default('Rent Free Desk'),
    authorRole: z.string().default('Fact-check Desk'),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
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
