import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

const MAP = {
  'reality-check': 'Reality Check',
  'by-the-numbers': 'By the Numbers',
  'countries': 'Countries',
  'lab-tested': 'Lab Tested',
};

export async function getStaticPaths() {
  return Object.keys(MAP).map((cat) => ({ params: { cat } }));
}

export async function GET({ params, site }) {
  const label = MAP[params.cat];
  const posts = (await getCollection('news'))
    .filter((p) => p.data.category === label)
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
  return rss({
    title: `Rent Free News — ${label}`,
    description: `Reality checks with receipts: ${label}.`,
    site: site ?? 'https://rentfreenews.com',
    items: posts.map((p) => ({
      title: p.data.title,
      description: p.data.excerpt,
      pubDate: p.data.pubDate,
      link: `/${p.slug}/`,
    })),
  });
}
