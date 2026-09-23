import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

// Demo: static output for max speed + free CDN hosting
// For breaking news later: output: 'hybrid' + Cloudflare adapter
export default defineConfig({
  site: 'https://rentfreenews.com',
  output: 'static',
  integrations: [
    tailwind({ applyBaseStyles: true }),
  ],
  markdown: {
    shikiConfig: { theme: 'github-dark' }
  },
  vite: {
    build: { cssMinify: true }
  }
});
