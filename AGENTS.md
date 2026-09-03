# skills — 에이전트 진입 라우터

> 이 레포 안에서 작업하는 에이전트를 위한 얇은 라우터. 상세는 링크된 파일을 필요할 때만 읽는다.

## 정체성

개인 스킬 라이브러리. 스킬 하나 = `skills/<이름>/` 폴더 하나. 공개 [Agent Skills 규격](https://agentskills.io)을 따르므로 Claude Code 플러그인이면서 동시에 `npx skills add jihkyuo/skills@<이름>`으로 어느 에이전트에나 설치된다. 흔들리면 안 되는 넷은 [CONTRIBUTING.md](CONTRIBUTING.md)의 원칙(발췌·주인 하나·하네스 중립·검증 후 태그)이다.

## 항시 룰

- **외부 스킬은 전역 설치하지 않는다.** 필요한 절만 `references/`에 벤더링하고 `NOTICE.md`(스킬 안)와 `THIRD_PARTY_LICENSES.md`(루트)를 같은 커밋에서 갱신한다. 원본 갱신은 커밋 해시를 새로 고정한다.
- **사내·로컬 의존 0.** 커밋 전 `python3 scripts/validate.py`가 로컬 절대경로·사내 식별자(티켓 ID 등)를 잡는다. 스킬 본문·자산·평가 문서에 특정 회사·제품·경로가 남으면 회귀다.
- **하네스 명령은 `references/harness-*.md`에만.** SKILL.md 본문에 `orca …`, `Agent 도구`, `browse` 같은 도구 이름이 들어가면 회귀다(`scripts/validate.py`가 아직 잡지 않으니 리뷰에서 본다).
- **태그 전 평가.** 스킬 동작을 바꿨으면 `skills/<이름>/evals/README.md`의 시나리오 형태대로 옛 스냅샷 대 새 판을 같은 프롬프트에 돌려 채점한다. 실제 평가 세트와 작업 공간은 `~/.claude/skill-workspaces/<이름>/`(레포 밖) — **실제 무대 경로·사내 문구가 든 평가 세트를 레포에 넣지 않는다.**
- **버전은 세 곳이 같다.** `.claude-plugin/plugin.json` · `marketplace.json` · `CHANGELOG.md` 최신 항목 · git 태그.
- 커밋 메시지는 `type(scope): 요지` (docs · feat · fix · chore). 한국어 요지 허용.

## 명령어

- 검증: `python3 scripts/validate.py` (CI와 동일)
- 검출기 단독: `node skills/design-variant-rounds/scripts/detect.mjs --json --no-config <html>`
- 라이브 설치본 갱신(작성자 기기): `~/.claude/skills/<이름>` 을 레포 폴더의 심볼릭 링크로 두거나 `npx skills add jihkyuo/skills@<이름> -g` 재실행

## 지도

| 무엇 | 어디 |
|---|---|
| 스킬 본문 | `skills/<이름>/SKILL.md` |
| 무거운 참고·하네스 어댑터 | `skills/<이름>/references/` |
| 실행물 | `skills/<이름>/scripts/` |
| 평가 시나리오·단언 | `skills/<이름>/evals/` |
| 출처·라이선스 | `skills/<이름>/NOTICE.md` → `THIRD_PARTY_LICENSES.md` · [PROVENANCE.md](PROVENANCE.md) |
| 변경 이력 | [CHANGELOG.md](CHANGELOG.md) |
