import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

function escapeXml(unsafe: string): string {
  return unsafe.replace(/[<>&'"]/g, (c) => {
    switch (c) {
      case '<': return '&lt;';
      case '>': return '&gt;';
      case '&': return '&amp;';
      case '\'': return '&apos;';
      case '"': return '&quot;';
      default: return c;
    }
  });
}

export const GET: APIRoute = async ({ site }) => {
  const base = (site?.toString() ?? 'https://rentfreenews.com').replace(/\/$/, '');
  const allPosts = await getCollection('news');

  // Sort newest first
  const sorted = allPosts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  // Filter entries published within the last 48 hours
  const now = Date.now();
  const fortyEightHoursAgo = now - 48 * 60 * 60 * 1000;
  let recent = sorted.filter((p) => p.data.pubDate.getTime() >= fortyEightHoursAgo);

  // Fallback to the 10 most recent articles if fewer than 10 were published in last 48 hours
  if (recent.length < 10) {
    recent = sorted.slice(0, 10);
  }

  const items = recent.map((p) => {
    const loc = `${base}/${p.slug}/`;
    const pubDate = p.data.pubDate.toISOString();
    const title = escapeXml(p.data.title);

    return `  <url>
    <loc>${loc}</loc>
    <news:news>
      <news:publication>
        <news:name>RentFreeNews</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:publication_date>${pubDate}</news:publication_date>
      <news:title>${title}</news:title>
    </news:news>
  </url>`;
  }).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
${items}
</urlset>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'X-Content-Type-Options': 'nosniff'
    }
  });
};

