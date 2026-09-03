<!-- 출처(발췌): emilkowalski/skills@d23d7f8 animate/SKILL.md §1~§7 + «Never Ship» · review-animations/SKILL.md 「Aggressive Escalation Triggers」 · emil-design-eng/SKILL.md 「Review Checklist」. 표와 값은 원문 그대로, 절차 설명은 요약. -->

# 모션 결정 — 워커용 4단계, 코디용 grep

이 무대는 제품 UI(Operate 모드)다. 사용자는 «살아 있는 화면»을 요구하지만 제품 UI의 모션은 상태 전달이지 장식이 아니다. **새로 넣는 모션**에만 이 파일을 적용한다. 사용자가 실브라우저에서 «이 손맛·이 열림 팝을 지켜라»고 한 것은 이 파일보다 우선한다.

## 워커: 결정 순서 (순서를 바꾸지 않는다)

### 1. 애니메이션을 넣을 것인가

| 빈도 | 결정 |
|---|---|
| 하루 100회+ (키보드 단축키, 커맨드 팔레트 토글) | 애니메이션 없음. 여기서 멈춘다 |
| 하루 수십 회 (호버, 목록 이동) | 거의 안 보일 정도만, 아니면 없음 |
| 가끔 (모달·드로어·토스트) | 표준 |
| 드묾/첫 경험 (온보딩·완료·축하) | 여기가 «즐거움 예산» |

키보드로 시작된 동작은 판단 대상이 아니라 실격이다. 게이트를 못 넘으면 코드를 쓰지 않고 «즉시 상태 변경»으로 대신한다. 그것도 성공이다.

### 2. 목적을 한 단어로

피드백 · 공간 일관성 · 상태 표시 · 급변 방지 · 설명(마케팅·온보딩만) · 즐거움(드묾 티어만). 이름을 못 붙이면 만들지 않는다. 사용자가 읽거나 조작 중인 데이터는 스타일 때문에 움직이지 않는다.

### 3. 가장 싼 도구

CSS transition(클래스·속성으로 제어하는 상태) → `@starting-style`(마운트 진입) → CSS animation(페이지가 바쁠 때도 매끄러워야 하는 예정 모션) → WAAPI → Motion 라이브러리(스프링·레이아웃·제스처). 페이드 하나에 라이브러리를 넣지 않는다.

### 4. 속성

- `transform`·`opacity`만. `width/height/margin/padding/top/left`는 레이아웃·페인트를 다 태운다(아코디언의 `height`만 용인).
- `scale(0)` 진입 금지. `scale(0.9~0.97)` + `opacity: 0`에서 시작.
- 팝오버·드롭다운·툴팁의 `transform-origin`은 트리거 쪽. 모달은 예외(중앙 유지).
- `translate()`의 퍼센트는 자기 크기 기준. 픽셀 하드코딩보다 우선.

### 5. 곡선과 시간

| 상황 | 이징 |
|---|---|
| 진입·퇴장 | `ease-out` |
| 화면 안 이동·변형 | `ease-in-out` |
| 호버·색 변화 | `ease` |
| 일정한 움직임(마퀴·진행) | `linear` |

UI에 `ease-in` 금지. 시작이 느려 사용자가 가장 주시하는 순간을 지연시킨다. 내장 곡선은 약하다:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
```

| 요소 | 시간 |
|---|---|
| 버튼 눌림 피드백 | 100~160ms |
| 툴팁·작은 팝오버 | 125~200ms |
| 드롭다운·셀렉트 | 150~250ms |
| 모달·드로어 | 200~500ms |

UI 모션은 300ms 아래. 스프링은 드래그 관성·중단 가능한 제스처·«살아 있어야 하는» 요소에만(`{ type: "spring", duration: 0.5, bounce: 0.2 }`, bounce 0.1~0.3).

### 6. 중단과 퇴장

빠르게 반복 트리거되는 것(토스트·토글)은 keyframes가 아니라 transition(현재 값에서 재조준). 들어온 길로 나간다. 사용자가 결정하는 구간은 느리게, 시스템 응답은 빠르게(hold 2s linear / release 200ms ease-out).

### 7. 함께 출하

```css
@media (prefers-reduced-motion: reduce) { .el { animation: fade 0.2s ease; } }
@media (hover: hover) and (pointer: fine) { .el:hover { transform: scale(1.05); } }
```

reduced motion은 «더 적고 부드럽게»이지 0이 아니다.

### 출하 금지 자가 점검

| 절대 | 대신 |
|---|---|
| `transition: all` | 속성 이름을 적는다 |
| `scale(0)` 진입 | `scale(0.95)` + `opacity: 0` |
| UI에 `ease-in` | `ease-out` 또는 강한 커스텀 곡선 |
| 키보드 단축키·100회+/일 동작의 애니메이션 | 없음 |
| 이유 없는 300ms 초과 | 150~250ms |
| 트리거 앵커 팝오버의 `transform-origin: center` | 트리거 쪽 |
| 토스트·토글에 keyframes | transition |
| `width/height/margin/padding/top/left` 애니메이션 | `transform`/`opacity` |
| 게이트 없는 `:hover` 모션 | `@media (hover: hover) and (pointer: fine)` |
| `prefers-reduced-motion` 누락 | 부드러운 변형 |
| 전부 한꺼번에 등장 | 30~80ms 스태거 |

## 코디: 수령 때 grep (기계 검사에 편입)

정규식은 후보를 잡는 것이지 판정이 아니다. 매치를 눈으로 읽고 나서 반려한다.

| 신호 | grep | 판정 메모 |
|---|---|---|
| 무제한 속성 전이 | `transition:\s*all` | 즉시 반려 |
| 무에서 등장 | `scale\(\s*0\s*\)` | 즉시 반려 |
| 느린 시작 | `ease-in\b(?!-out)` | 진입·퇴장에 쓰였으면 반려 |
| 레이아웃 속성 애니메이션 | `transition:[^;]*\b(width\|height\|top\|left\|margin\|padding)\b` | 아코디언 `height`만 용인 |
| 300ms 초과 | `\b([3-9]\d{2}\|\d{4,})ms` | 모달·드로어(≤500) 외엔 이유 확인 |
| 토스트·토글의 keyframes | `@keyframes` 매치 요소가 반복 트리거 대상인지 | 수동 |
| reduced-motion 누락 | `transform` 전이가 있는데 `prefers-reduced-motion` 0회 | 반려 |
| 호버 게이트 누락 | `:hover\s*\{[^}]*transform` 있고 `hover: hover` 0회 | 반려 |
