# 도로시펫 광주점 분양 SEO 사이트 — 매장 2,500

dorothypet.co.kr 의 **광주점**(광주광역시 남구 서문대로 801(주월동) 2층 · 010-8544-8584) 기준 매장 홍보 키워드 페이지. 대구점 사이트(`C:\side_Prj\dorothypet_dg_prj`)를 복사해 데이터만 광주로 바꿨다(2026-11-24). 코드 구조 설명·사실 근거·디자인은 부산 사이트(`C:\side_Prj\dorothypet_prj`) SITE.md 와 같고, 여기에는 다른 점만 적는다.

## 키워드 (`keywords/`, 키워드 시트가 첫 시트)

- `도로시펫_광주_1000.xlsx` — 사용자 원본 791(`raw/광주 도로시펫 키워드 791개.csv`, 노출·클릭 포함, 그대로) + 추가 209(`scripts/base_keywords.py`). 추가 축: 광주×분양 어휘 20 · 구×어휘 17 · 동네×강아지분양·고양이분양 46 · 전남 시·군×어휘 28 · 광주○○분양(원본 클릭 많은 견종 순) 51 · 광주○○ 47.
- `도로시펫_광주_2500.xlsx` — 위 1,000 + 확장 1,500(`scripts/expand_keywords.py`, 대구점과 같은 축을 광주권 지명으로): 견종×패턴 574 · 동네×분양 어휘 269 · 나주·광양·화순·담양×견종 분양 159 · 동네×짧은 어휘 237 · 견종×종류별 패턴 261.
- 추가·확장 1,709개는 검색량을 재지 않았다(빈칸).
- 원본 791 확인: 중복 0. 견종·종류를 못 잡는 37개(도로시펫·펫샵·오타 표기 등)는 일반 강아지/고양이 페이지로 만든다. 호텔·미용 6개(광주애견호텔 등)와 용품 2개는 원본이라 페이지는 만들되 그 서비스를 한다고 쓰지 않는다. 전북 6개(전주·남원·정읍)도 원본이라 동네 사실을 붙였다.
- 동네 49곳(`scripts/build_regions.py` PLACE): 광주 + 5개 구 + 광주 동네 26곳(주월동·봉선동·상무지구·첨단·수완동 등) + 전남 14곳(순천·목포·여수·나주·광양·담양·화순·장성·함평·해남·무안·영광·남악·빛가람) + 전북 3곳. '운천'은 상무1동, '효천'은 효덕동, '상무지구'는 치평동 세대 수를 쓴다.

```bash
python -I scripts/build_regions.py      # data/regions.json
python -I scripts/base_keywords.py      # 791 → 1,000 CSV + 엑셀
python -I scripts/expand_keywords.py    # 확장 1,500 CSV
python -I scripts/select_keywords.py    # → data/pages.json + 2,500 엑셀
python -I -X utf8 scripts/make_og.py --force   # public/og (저장소에 포함 — Actions 에 윈도 글꼴이 없어 로컬에서 만든다)
npx next build                          # → out/
npx tsx scripts/x_check.ts
python -I ~/.claude/skills/site-launch/scripts/check_all.py C:/side_Prj/dorothypet_gj_prj
```
`node_modules` 는 부산 프로젝트로 junction.

## 대구점 사이트와 다른 점

- `lib/site.ts`: 광주점 주소·전화(공식 사이트 지점 안내), STORE(광주 남구 주월동, 먼 지역 = 전남·전북), 지점 목록은 광주점·부산본점·대구점 순.
- 블로그 없음(`app/blog`·`lib/blog.ts` 삭제, 메뉴·사이트맵·RSS·llms 에서 뺌). 대구 글을 복사하지 않으려고.
- 소유확인 코드 없음(`app/layout.tsx` verification 삭제 — 받으면 넣는다).
- 매장 사진 없음 → 견종·대표 사진(대구와 같음). 사업자 정보 비어 있어 하단에 상호·주소만.

## 확인 필요 (사용자)

- [x] 도메인 dorothypetgwangju.co.kr (2026-11-24 사용자 결정)
- [x] GitHub 저장소 https://github.com/Jeongdonghwan/drtgwangju_prj.git (2026-11-24) — main 푸시마다 Actions 가 빌드해 deploy 브랜치로. 서버 폴더 `/var/www/dorothypet_gj`
- [ ] 서치어드바이저·서치콘솔 소유확인 코드
- [ ] 광주점 사업자 정보(상호·대표·사업자번호), 매장 사진
- [ ] 광주점 전화 010-8544-8584 가 상담 전화로 맞는지(공식 사이트 지점 안내 번호)
- [ ] 호텔·미용 키워드 6개를 남길지(원본에 있어 만들었지만 그 서비스 안내는 없음)

## 규칙 맞춤 (2026-11-25, composer-patterns §5-4 · post-launch)

- 번호 절 문단 200~260자(공백 제외): `lib/ray.ts` EXTRA(절마다 3벌, 매장 절차 안의 사실)로 모자라면 한 문장 더, 넘치면 끝에서 둘째 문장부터 뺀다. 2,500쪽 200~246자.
- 키워드가 품종 이름 그대로('먼치킨')면 본문에 이름이 30회 넘게 들어가 §5-4(8~20회)를 넘었다 → 절 문단 안 두 번째부터 '이 아이'로(86쪽 → 4쪽).
- 화면 '최종 수정' 줄 + WebPage dateModified(키워드 페이지에 datePublished 없음), sitemap lastmod = `lib/site.ts` UPDATED(2026-11-25). 본문·title 을 바꾸면 UPDATED 를 올린다.
- 나눠 열기(post-launch 고정 규칙): `data/drip.json` 오픈일 2026-11-25, 2일마다 625쪽씩 4묶음(11-25 625 · 11-27 1,250 · 11-29 1,875 · 12-01 2,500). 순서 = pages.json(원본 791 클릭순 → 추가 → 확장). Actions 가 매일 06:00 KST 빌드하면서 연다. 점검은 `OPEN_WAVE=4`. 배포 때 안 열린 키워드 og 는 뺀다(deploy.sh).
- 전화번호 뒤 조사 '(으)로' 를 끝자리로 고름(010-8544-8584로).
- check_all 7·8번 게이트용 `data/site-pages.json`(select_keywords.py 가 같이 만든다).
- 측정(2026-11-25, 전체 2,500쪽 빌드): check_all SEO 구조·중복 문서·AI 티·화면 버그·답 페이지 틀·제목 규칙·본문 규칙 통과, FAQ·Q&A 미달(/qna/ 없음 — 대구·부산과 같음). 본문 1,970~2,348자, 내부링크 12~16, FAQ 4, 대구 사이트와 같은 주소 같은 문장 평균 25%.
