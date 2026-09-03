# NOTICE — 벤더링 출처

이 스킬의 `references/`와 `scripts/`는 아래 공개 스킬에서 발췌·복제했다. 전역 설치 대신 벤더링한 이유: 원본들은 독립 진입점으로 설계돼 있어 자동 발동 설명문이 넓고(우리 스킬·superpowers 브레인스토밍·gstack spec과 트리거 충돌), 상호 모순(랜딩 페이지 미학 vs 제품 UI)과 대화형 게이트(끝에 사용자 질문)를 품고 있다. 필요한 절만 역할·순간별로 심는 편이 컨텍스트 10분의 1로 같은 효과를 낸다.

| 대상 | 출처 | 커밋 | 라이선스 | 형태 |
|---|---|---|---|---|
| references/craft-floor.md | pbakaus/impeccable `plugin/skills/impeccable/reference/craft-floor.md` | 5a7e283 (2026-09-03) | Apache-2.0 | verbatim + 예외 절 |
| references/operate-mode.md | pbakaus/impeccable `reference/operate.md` | 5a7e283 | Apache-2.0 | verbatim |
| references/brief-template.md | pbakaus/impeccable `reference/shape.md` §Phase 3 | 5a7e283 | Apache-2.0 | 발췌·번역 |
| references/review-template.md | pbakaus/impeccable `reference/critique.md` 휴리스틱·인지부하·P0~P3 | 5a7e283 | Apache-2.0 | 발췌·번역 |
| references/feedback-translation.md | pbakaus/impeccable `reference/polish.md` · `distill.md` · `quieter.md` · `bolder.md` | 5a7e283 | Apache-2.0 | 발췌·번역 |
| references/motion-decisions.md | emilkowalski/skills `skills/animate` · `review-animations` · `emil-design-eng` | d23d7f8 (2026-08-21) | 레포 LICENSE 참조 | 발췌(표·값 원문) |
| references/round-rules.md | jakubkrehel/skills `skills/variant` · emilkowalski/skills `skills/prototype` · mattpocock/skills `skills/engineering/prototype/UI.md` · gstack `design-shotgun` 반수렴 지시문 | 267330e · d23d7f8 · 6654f6b | 레포 LICENSE / MIT | 합본·번역 |
| references/thesis-divergence.md | anthropics/knowledge-work-plugins `product-management/skills/product-brainstorming` | f30dc63 (2026-09-02) | 레포 LICENSE 참조 | 발췌·번역 |
| references/decision-record.md | owl-listener/designer-skills `designer-toolkit/skills/design-rationale` | 20e34c4 (2026-08-08) | 레포 LICENSE 참조 | 발췌·번역 |
| scripts/detect.mjs · scripts/detector/ · scripts/lib/ · scripts/data/ | pbakaus/impeccable `plugin/skills/impeccable/scripts/` | 5a7e283 | Apache-2.0 | 복제(결정론 검출기 61규칙) |

검출기는 `htmlparser2 css-select css-tree domutils`가 없으면 정규식 모드로 내려간다(경고 배너 출력, 과소 검출). 정밀 모드가 필요하면 `scripts/`에서 `npm i htmlparser2 css-select css-tree domutils`.

원본 갱신은 커밋을 새로 고정하고 이 표를 갱신한다. 원본을 전역 설치하지 않는다.
