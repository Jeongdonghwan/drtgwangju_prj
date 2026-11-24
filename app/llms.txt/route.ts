// llms.txt — 사이트 요약과 핵심 페이지 목록 (정적)
import { STORE_PAGES, storeEncPath } from '../../lib/data';
import { SITE_URL, BRAND, BUSINESS, CONTACT } from '../../lib/site';

export const dynamic = 'force-static';

export function GET() {
  const top = [...STORE_PAGES].sort((a, b) => b.impressions - a.impressions).slice(0, 60);
  const lines = [
    `# ${BRAND} 광주점 강아지·고양이 분양`, '',
    `> ${BRAND} 광주점(${BUSINESS.address}) 분양 안내. 예약제 1:1 상담, 동물병원 건강 확인, 계약서, 분양 후 사후관리, 홈딜리버리. 상담 ${CONTACT.phone}. 분양가는 아이마다 달라 상담으로 안내합니다.`, '',
    '## 주요 페이지', `- [광주점 소개](${SITE_URL}/about/)`, `- [전체 분양 안내](${SITE_URL}/area/)`,
    ...top.map((p) => `- [${p.kw}](${SITE_URL}${storeEncPath(p)})`),
    '', '## 사이트맵', `- ${SITE_URL}/sitemap.xml`, '',
  ];
  return new Response(lines.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
}
