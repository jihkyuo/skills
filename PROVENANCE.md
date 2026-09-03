# Provenance & Audit

This document records where the content and code in this repository come from, so that
one claim is verifiable: **every third-party piece is named, pinned to a commit, and
shipped with its license; nothing here phones home.**

## Original work

All `SKILL.md` bodies, the harness adapters (`references/harness-*.md`), the eval
scenarios and assertions (`evals/`), the compare-page template
(`assets/compare-template.html`), and `scripts/validate.py` are original to this
repository (MIT, see [LICENSE](LICENSE)).

## Vendored extracts (text)

`skills/design-variant-rounds/references/` carries sections extracted from public skills.
Each file names its source repository, path, commit, and license in a comment on its
first line, and the skill's [`NOTICE.md`](skills/design-variant-rounds/NOTICE.md) tabulates
them. Full license texts are in [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md).

| Source | Used for | License |
|---|---|---|
| pbakaus/impeccable | craft floor, Operate-mode guidance, brief template, critique scoring, feedback procedures | Apache-2.0 |
| emilkowalski/skills | motion decision sequence and review triggers | MIT |
| jakubkrehel/skills · emilkowalski/skills (`prototype`) · mattpocock/skills (`prototype/UI.md`) | variant-round rules (one axis, same harness next round, picker discipline) | MIT |
| anthropics/knowledge-work-plugins | solution-ideation procedure used for thesis divergence | Apache-2.0 |
| owl-listener/designer-skills | design-rationale structure used for decision records | MIT |

Why extracts rather than skill invocations: the sources are independent entry points
with their own personas, output contracts, and interactive gates. Loading several at
once produced contradictory directives (landing-page aesthetics versus product-UI
familiarity), triple redundancy, and gates that wait for a human inside an unattended
worker loop; the extracted sections total about 20 KB against roughly 200 KB for the
whole skills.

## Vendored code

`skills/design-variant-rounds/scripts/detect.mjs` and `scripts/detector/`, `scripts/lib/`,
`scripts/data/` are copied from pbakaus/impeccable
(`plugin/skills/impeccable/scripts/`, commit noted in the skill's `NOTICE.md`), licensed
Apache-2.0. It is a deterministic anti-pattern detector over local HTML/CSS. Without the
optional parser packages (`htmlparser2`, `css-select`, `css-tree`, `domutils`) it falls
back to regex matching and prints a warning saying so. No other third-party code is
bundled.

## Network and telemetry audit

- No skill instructs the agent to call a network service. The only external fetch a
  skill mentions is the optional install of the Anthropic `frontend-design` skill by the
  user.
- `detect.mjs` reads files passed on the command line and writes to stdout only.
- The stage server used during design rounds is Python's `http.server` on localhost,
  started by the coordinator and stopped at the end of a round.
- No hooks are installed by this repository. The `CLAUDE.md` here only delegates to
  `AGENTS.md` for agents working inside this repository.

## Private identifiers

Skill bodies, assets, and design notes are scrubbed of employer-specific references,
local paths, and internal ticket identifiers before publication; `scripts/validate.py`
rejects absolute home paths and ticket-shaped identifiers. Concrete eval sets are bound
to real project stages and stay outside the repository (`evals/README.md` documents
their shape instead).
