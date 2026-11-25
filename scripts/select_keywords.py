"""도로시펫 광주점 키워드 → data/pages.json + keywords/도로시펫_광주_2500.xlsx

  python -I scripts/select_keywords.py
raw/도로시펫 키워드 - 광주 1000개.csv (사용자 원본 791 + 추가 209, scripts/base_keywords.py) + 확장 1,500(expand_keywords.py) = 2,500.
노출·클릭은 사용자가 준 광주 원본 791개의 값. 엑셀은 요약 시트 없이 키워드 시트가 첫 시트.
"""
import csv, json, os, re, sys
import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'raw', '도로시펫 키워드 - 광주 1000개.csv')
EXPAND = os.path.join(ROOT, 'raw', '도로시펫 키워드 - 광주 확장 1500개.csv')  # scripts/expand_keywords.py (2026-11-16, +1,000)


def slug(kw):
    return re.sub(r'\s+', '-', kw.strip())


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    rows = [r for r in list(csv.reader(open(SRC, encoding='utf-8-sig')))[1:] if r and r[0].strip()]
    if os.path.exists(EXPAND): rows += [r for r in list(csv.reader(open(EXPAND, encoding='utf-8-sig')))[1:] if r and r[0].strip()]
    n = lambda v: int(re.sub(r'\D', '', v or '') or 0)
    store, seen = [], set()
    for r in rows:
        kw = r[0].strip()
        assert kw not in seen, kw
        seen.add(kw)
        store.append(dict(kw=kw, slug=slug(kw), set='store', impressions=n(r[1]), clicks=n(r[2]), dupRows=0, added=bool(r[4].strip()) if len(r) > 4 else False, note=r[4].strip() if len(r) > 4 else '', src=r[3].strip() if len(r) > 3 else ''))
    assert len(store) in (1000, 2000, 2500), len(store)
    json.dump({'store': store, 'franchise': []}, open(os.path.join(ROOT, 'data', 'pages.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    json.dump({'_note': 'check_all 7·8번 게이트용 — pages.json store 의 slug', 'pages': [{'slug': p['slug'], 'kw': p['kw']} for p in store]}, open(os.path.join(ROOT, 'data', 'site-pages.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)

    wb = openpyxl.Workbook(); ws = wb.active; ws.title = '키워드'
    ws.append(['키워드', 'URL', '노출수', '클릭수', '비고'])
    for p in store:
        ws.append([p['kw'], f"/{p['slug']}/", p['impressions'] or None, p['clicks'] or None, p['note'] or '원본 791'])
    for col, w in zip('ABCDE', (28, 32, 10, 10, 18)): ws.column_dimensions[col].width = w
    os.makedirs(os.path.join(ROOT, 'keywords'), exist_ok=True)
    wb.save(os.path.join(ROOT, 'keywords', '도로시펫_광주_2500.xlsx'))
    print(f'매장 {len(store)} (원본 {sum(1 for p in store if not p["added"])} · 추가 {sum(1 for p in store if p["added"])})')


if __name__ == '__main__':
    main()
