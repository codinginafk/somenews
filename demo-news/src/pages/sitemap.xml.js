import { getCollection } from 'astro:content';

export async function GET({ site }) {
  const base = (site?.toString() ?? 'https://rentfreenews.com').replace(/\/$/, '');
  const posts = (await getCollection('news')).sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
  const statics = ['/', '/about/', '/contact/', '/corrections/', '/advertise/', '/privacy/', '/terms/', '/dmca/', '/category/reality-check/', '/category/by-the-numbers/', '/category/countries/', '/category/lab-tested/'];
  const urls = [
    ...statics.map((p) => ({ loc: base + p, lastmod: new Date().toISOString().slice(0, 10) })),
    ...posts.map((p) => ({ loc: `${base}/${p.slug}/`, lastmod: p.data.updatedDate?.toISOString().slice(0, 10) ?? p.data.pubDate.toISOString().slice(0, 10) })),
  ];
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((u) => `  <url><loc>${u.loc}</loc><lastmod>${u.lastmod}</lastmod></url>`).join('\n')}\n</urlset>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
