import type { Metadata, Viewport } from 'next';
import './globals.css';
import { Header, Footer, StickyBar, JsonLd } from '../components/Common';
import Motion from '../components/Motion';
import { businessJsonLd } from '../lib/jsonld';
import { SITE_URL, BRAND } from '../lib/site';

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: `광주강아지분양 ${BRAND} 광주점 | 강아지·고양이 분양 상담`, template: '%s' },
  description: '도로시펫 광주점 강아지·고양이 분양. 방문 예약 1:1 상담, 동물병원 건강 확인, 계약서, 분양 후 사후관리, 홈딜리버리. 010-8544-8584.',
  robots: { index: true, follow: true },
  alternates: { canonical: '/', types: { 'application/rss+xml': [{ url: '/rss.xml', title: `${BRAND} 분양 안내` }] } },
  icons: { icon: [{ url: '/favicon.ico', sizes: 'any' }, { url: '/icon.png', type: 'image/png', sizes: '192x192' }], apple: '/apple-touch-icon.png' },
};

export const viewport: Viewport = { themeColor: '#ffffff', width: 'device-width', initialScale: 1 };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" />
      </head>
      <body>
        <JsonLd data={businessJsonLd()} />
        <Header />
        {children}
        <Footer />
        <StickyBar />
        <Motion />
      </body>
    </html>
  );
}
