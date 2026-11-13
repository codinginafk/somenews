import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// Demo: static output for max speed + free CDN hosting
// For breaking news later: output: 'hybrid' + Cloudflare adapter
export default defineConfig({
  site: 'https://rentfreenews.com',
  output: 'static',
  integrations: [
    tailwind({ applyBaseStyles: true }),
    sitemap({
      filter: (page) =>
        !page.includes('/search') &&
        !page.includes('/404') &&
        !page.includes('/admin'),
    }),
  ],
  markdown: {
    shikiConfig: { theme: 'github-dark' }
  },
  vite: {
    build: { cssMinify: true }
  }
});
