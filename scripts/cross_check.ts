// 대구점 사이트와 같은 주소(키워드)끼리 같은 문장 비율: npx tsx scripts/cross_check.ts
import { STORE_PAGES } from '../lib/data';
import { composeRay } from '../lib/ray';
import { STORE_PAGES as DG } from '../../dorothypet_dg_prj/lib/data';
import { composeRay as dgRay } from '../../dorothypet_dg_prj/lib/ray';

const set = (c: any) => new Set<string>([c.lead, c.summary, ...c.sections.map((x: any) => x.p), ...c.faq.map((f: any) => f.a)].join(' ').split(/(?<=[.?!])\s+/).map((x: string) => x.trim()).filter((x: string) => x.length > 12));
const dg = new Map(DG.map((p) => [p.slug, p]));
const v: number[] = []; let worst = ['', 0] as [string, number];
for (const p of STORE_PAGES) {
  const q = dg.get(p.slug); if (!q) continue;
  const A = set(composeRay(p)), B = set(dgRay(q)); let n = 0; A.forEach((x) => { if (B.has(x)) n++; });
  const r = n / Math.min(A.size, B.size); v.push(r); if (r > worst[1]) worst = [p.kw, r];
}
console.log(`같은 주소 ${v.length}쪽 · 같은 문장 평균 ${Math.round(100 * v.reduce((a, b) => a + b, 0) / v.length)}% · 최대 ${Math.round(100 * worst[1])}% (${worst[0]})`);
