"""사용자 원본 791개 + 추가 209개 → raw/도로시펫 키워드 - 광주 1000개.csv + keywords/도로시펫_광주_1000.xlsx (2026-11-24)

  python -I scripts/base_keywords.py
원본: raw/광주 도로시펫 키워드 791개.csv (키워드·노출수·클릭수 — 사용자 제공). 791개는 그대로 둔다.
추가 209(검색량 측정 안 함, 원본에 이미 있는 꼴만 넓힌다 — 앞에서부터 채우고 1,000에서 끊음):
 1. 광주 × 분양 어휘(원본에 빠진 것)          2. 광주 5개 구 × 강아지분양·고양이분양·애견분양·펫샵
 3. 광주 동네 × 강아지분양·고양이분양          4. 전남 시·군 × 강아지분양·고양이분양·애견분양·펫샵
 5. 광주○○분양 — 원본에서 클릭이 많은 견종부터          6. 광주○○ — 같은 순서(1,000이 찰 때까지)
엑셀은 요약 시트 없이 키워드 시트가 첫 시트.
"""
import csv, json, os, sys
from collections import defaultdict
import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'raw', '광주 도로시펫 키워드 791개.csv')
OUT = os.path.join(ROOT, 'raw', '도로시펫 키워드 - 광주 1000개.csv')
TARGET = 1000
CITY_WORDS = ['강아지분양가', '고양이분양가', '강아지입양', '고양이입양', '반려견분양', '반려묘분양', '강아지분양가격', '고양이분양가격', '애견샵', '고양이분양샵',
              '강아지분양소', '새끼강아지분양', '새끼고양이분양', '아기강아지분양', '아기고양이분양', '중형견분양', '강아지분양하는곳', '고양이분양하는곳', '분양샵', '강아지펫샵']
GU = ['광산구', '북구', '서구', '남구', '동구']
GU_WORDS = ['강아지분양', '고양이분양', '애견분양', '펫샵']
DONG = ['주월동', '봉선동', '진월동', '백운동', '효천', '상무지구', '풍암동', '금호동', '화정동', '운천', '용봉동', '운암동', '문흥동', '일곡동', '양산동', '두암동',
        '첨단', '수완동', '수완지구', '송정', '신창동', '운남동', '월곡동', '충장로', '학동', '계림동']
DONG_WORDS = ['강아지분양', '고양이분양']
JN = ['순천', '목포', '여수', '나주', '광양', '담양', '화순', '장성', '함평', '해남', '무안', '영광', '남악']


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    rows = [r for r in list(csv.reader(open(SRC, encoding='utf-8-sig')))[1:] if r and r[0].strip()]
    have = {r[0].replace(' ', '') for r in rows}
    assert len(have) == len(rows) == 791
    bd = json.load(open(os.path.join(ROOT, 'data', 'breeds.json'), encoding='utf-8'))
    alias = sorted(bd['alias'], key=len, reverse=True)
    by_id = {b['id']: b for b in bd['breeds']}
    clicks = defaultdict(int)
    for r in rows:
        hit = next((a for a in alias if a in r[0]), None)
        if hit and bd['alias'][hit] in by_id: clicks[bd['alias'][hit]] += int(r[2] or 0)
    added, how = [], {}

    def add(kw, axis):
        if kw in have or len(rows) + len(added) >= TARGET: return
        have.add(kw); added.append(kw); how[axis] = how.get(axis, 0) + 1

    for w in CITY_WORDS: add(f'광주{w}', '광주×어휘')
    for w in GU_WORDS:
        for g in GU: add(f'광주{g}{w}' if g != '광산구' else f'{g}{w}', '구×어휘')
    for w in DONG_WORDS:
        for d in DONG: add(f'{d}{w}', '동네×어휘')
    for w in GU_WORDS:
        for c in JN: add(f'{c}{w}', '전남×어휘')
    for bid, _ in sorted(clicks.items(), key=lambda x: -x[1]):
        b = by_id[bid]
        if 'special' in (b['site'] or ''): continue
        add(f"광주{(b['siteName'] or b['name']).replace(' ', '')}분양", '광주견종분양')
    for bid, _ in sorted(clicks.items(), key=lambda x: -x[1]):
        b = by_id[bid]
        if 'special' in (b['site'] or ''): continue
        add(f"광주{(b['siteName'] or b['name']).replace(' ', '')}", '광주견종')
    assert len(rows) + len(added) == TARGET, (len(rows) + len(added), how)

    with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(['검색어', '노출수', '클릭수', '원본 키워드', '비고'])
        for r in rows: w.writerow([r[0].strip(), r[1], r[2], '', ''])
        for k in added: w.writerow([k, '', '', '', '추가(2026-11-24)'])
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = '키워드'
    ws.append(['키워드', '노출수', '클릭수', '구분'])
    for r in rows: ws.append([r[0].strip(), int(r[1] or 0), int(r[2] or 0), '원본 791'])
    for k in added: ws.append([k, None, None, '추가'])
    for col, wd in zip('ABCD', (28, 10, 10, 12)): ws.column_dimensions[col].width = wd
    os.makedirs(os.path.join(ROOT, 'keywords'), exist_ok=True)
    wb.save(os.path.join(ROOT, 'keywords', '도로시펫_광주_1000.xlsx'))
    print(f'원본 {len(rows)} + 추가 {len(added)}: ' + ' · '.join(f'{a} {n}' for a, n in how.items()))


if __name__ == '__main__':
    main()
