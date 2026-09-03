# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2026-09-03

### Removed

- **Author-local content that had leaked into the published skill.** The concrete eval set
  (`evals/evals.json`, bound to the author's local stage paths and internal product scenarios)
  and the original compare template (which still carried a product-specific title and hint)
  are gone. `evals/README.md` now documents the scenario shape only; the compare template is a
  generic `SLOTS`/`HINT` scaffold. `orca-handoff`'s working plan was dropped and its design note
  scrubbed of internal ticket ids and repository paths.

### Added

- `scripts/validate.py` now fails on absolute home paths, e-mail addresses, and ticket-shaped
  identifiers anywhere under `skills/`, plus any tokens listed in the untracked
  `scripts/private-tokens.local`. CI runs it.

### Changed

- **History rewritten.** Tags `v0.1.0`–`v0.1.2` pointed at commits containing the removed
  content and were withdrawn; `v0.1.3` is the first tag on the clean history. Earlier entries
  below are kept as a record of what changed, not as reachable tags.
- `design-variant-rounds` description: "portal deploy" (a house term) → "deploy".

## [0.1.2] - 2026-09-03

### Changed

- **`design-variant-rounds` — trigger description narrowed.** It now fires on the intent
  "two or more candidates to compare across rounds", not on the word "시안" (mockup). Single-mockup
  requests (edit, implement, deploy to the portal, check against a PRD, move to `_drafts/`, slice)
  are named as out of scope. Measured with 22 realistic queries against `claude -p`: false triggers
  1/12 → 0/12, true triggers 8/10 → 10/10 (single run per query).
- **Harness adapter selection is now an observable rule**: user override → `orca` binary answering
  `orca orchestration --help` → Agent + follow-up messaging tools → generic.

## [0.1.1] - 2026-09-03

### Added

- Repository scaffolding in the docsherpa/superpowers mold: English README with badges,
  `CONTRIBUTING.md`, `AGENTS.md` entry router (`CLAUDE.md` delegates to it),
  `PROVENANCE.md`, issue templates, and a CI workflow.
- `scripts/validate.py` — stdlib-only checks run locally and in CI: SKILL.md frontmatter
  (name matches folder, description present, ≤ 1024 chars), every `references/*.md` a
  SKILL.md mentions exists, every source in a skill's `NOTICE.md` has its license text in
  `THIRD_PARTY_LICENSES.md`, and a smoke test of the vendored detector on a fixture.

### Changed

- `plugin.json` / `marketplace.json` author metadata now carries the author's name and
  GitHub handle.

## [0.1.0] - 2026-09-03

### Added

- **`design-variant-rounds`** — parallel design-variant rounds with four round engines
  (diverge / feedback / converge / detail). Rewritten from a private skill after
  measuring why rounds after the first degraded (variant code similarity 0.12 → 0.74 as
  copies and pixel gates accumulated). Ships nine vendored references with provenance,
  impeccable's deterministic detector, three harness adapters (Orca, Claude Code, generic),
  and `evals/` with three coordinator-decision scenarios. Baseline (previous skill) 4/18,
  this version 18/18, re-run after the harness split 18/18.
- **`socratic`** — teach → quiz → grade → re-ask dialogue for ambiguous material.
- **`orchestration-loop`** — sizing, assembly, and verification of an Orca worker loop.
- **`orca-handoff`** — ownership-transfer handoff to another agent or worktree.
- MIT license; `THIRD_PARTY_LICENSES.md` with the Apache-2.0 and MIT texts of every
  vendored source.
