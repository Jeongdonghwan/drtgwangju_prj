import type { MetadataRoute } from 'next';
import { SITE_URL, UPDATED } from '../lib/site';
import { STORE_PAGES, storeEncPath } from '../lib/data';

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  const upd = new Date(UPDATED);
  return [
    { url: `${SITE_URL}/`, lastModified: now, changeFrequency: 'weekly', priority: 1 },
    { url: `${SITE_URL}/area/`, lastModified: now, changeFrequency: 'weekly', priority: 0.7 },
    { url: `${SITE_URL}/about/`, lastModified: upd, changeFrequency: 'monthly', priority: 0.7 },
    ...STORE_PAGES.map((p) => ({ url: `${SITE_URL}${storeEncPath(p)}`, lastModified: upd, changeFrequency: 'monthly' as const, priority: 0.7 })),
  ];
}
