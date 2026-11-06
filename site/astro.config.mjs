// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://senrecep.github.io',
  base: '/yontu',
  trailingSlash: 'always',
  output: 'static',
  build: { format: 'directory' },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/404'),
      i18n: {
        defaultLocale: 'tr',
        locales: { tr: 'tr-TR', en: 'en-US' },
      },
    }),
  ],
});
