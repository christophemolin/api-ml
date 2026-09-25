// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://api-ml.info',
  trailingSlash: 'ignore',
  integrations: [sitemap()],
});
