# 하네스 어댑터 — Orca

Orca가 있으면 이 어댑터가 기본이다. 워커 터미널이 보여서 기동 확인이 가장 정확하고, 같은 워커에게 후속 메시지를 보내는 것이 명령 하나다. 명령 문법의 정본은 `orca skills get orchestration`(Orca 제공 스킬)이고, 여기 적는 것은 이 시안 라운드에서 쓰는 부분과 실측 지뢰뿐이다.

## 기동

```bash
orca orchestration run-create --objective "<라운드 목적>" --json
orca orchestration task-create --run <run> --spec "<task spec 본문>" --json
orca orchestration worker-start --task <id> --worktree current --agent claude --model <모델> --effort high --json
```

- run id는 `result.run.id`, task id는 `result.task.id`(최상위 `id`는 요청 id).
- `task-create` JSON 출력에 제어문자가 섞일 수 있다. 파싱은 `json.loads(txt, strict=False)`.
- 슬롯 N개는 디스패처 스크립트 하나(`_seed/dispatch.py`)로 돌리고 run/task/dispatch/terminal 핸들을 `_seed/run.json`에 남긴다. 재디스패치는 슬롯 인자로.

## 기동 확인 (생략 금지)

디스패치 약 10초 뒤 `orca terminal read <handle>`:

1. `[Pasted text …]`가 미제출 상태면 `orca terminal send <handle> --enter` (Enter 레이스).
2. 모델 배너·기동 명령 스크롤백으로 지정 모델 확인.
3. 씨드가 요구한 스킬 로드 로그 확인. 없으면 시정 메시지를 `send`.

터미널 tail은 TUI 렌더라 «착지» 같은 문자열을 놓친다. 워커 전사를 볼 때는 `orca orchestration worker-read`(전사 블록 타입은 `tool-call`).

## 대기

`check --wait`는 워커 heartbeat에 조기 종료해 알림 스팸을 만든다. 착지(슬롯 파일 크기가 수 초 간격으로 연속 동일)와 정산(`task-list`의 completed)을 폴링하되 **변화가 있을 때만 stdout 한 줄** 내는 Monitor 스크립트를 쓴다. heartbeat는 전부 소음.

워커는 `review-<slot>-v1.md` 파일 생성을 폴링하며 기다린다. 판정 파일이 곧 게이트다.

## 후속 메시지 (작가 연속)

```bash
orca orchestration send --to <worker> --type status --subject "<제목>" --body "<피드백 task spec>"
```

살아 있는 워커 터미널에 보낸다. 계약 개정도 같은 경로로 라운드 중 통지 가능(작업 큐에 얹힌다). 새 `task-create`가 아니다.

## 릴리스

눈 게이트 판정 전에는 릴리스하지 않는다. 판정 뒤 킵이 없는 슬롯만 릴리스하고, 킵 슬롯은 피드백 라운드까지 유지한다.

## 워커 보고 규약

- v1 착지: `orca orchestration send --type status --subject "v1 착지 <slot>"`.
- 최종: `worker_done` (본문: 논제 · 시그니처 · 실동작 자가 체크 · 못 지킨 계약과 이유).
