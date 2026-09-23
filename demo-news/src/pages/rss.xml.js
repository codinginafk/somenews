import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = (await getCollection('news')).sort((a,b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
  return rss({
    title: 'Rent Free News — Claims vs Data',
    description: 'Viral claims checked against primary data + creator tests.',
    site: context.site ?? 'https://rentfreenews.com',
    items: posts.map(p => ({
      title: p.data.title,
      description: p.data.excerpt,
      pubDate: p.data.pubDate,
      link: `/${p.slug}/`,
    })),
  });
}
