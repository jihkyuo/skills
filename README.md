<h1 align="center">skills</h1>

<p align="center">
  <strong>A personal library of agent skills, one folder per skill.</strong><br>
  Built to the open <a href="https://agentskills.io">Agent Skills</a> format, so the same skill installs into
  Claude Code, Codex, Cursor, Gemini CLI, Copilot, OpenCode and any other agent the
  <a href="https://skills.sh">skills CLI</a> supports.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/Agent%20Skills-spec-0A7C6E.svg" alt="Agent Skills spec">
  <img src="https://img.shields.io/badge/Claude%20Code-plugin-8A63D2.svg" alt="Claude Code plugin">
  <a href="https://github.com/jihkyuo/skills/actions/workflows/ci.yml"><img src="https://github.com/jihkyuo/skills/actions/workflows/ci.yml/badge.svg" alt="validate"></a>
</p>

---

## Why

Most skill libraries are either a single big methodology (superpowers) or a tool suite
(gstack). This one is a **workbench**: each skill is added on its own, after it has
been run against a baseline and graded, and it stays here only if it measurably changed
what the agent does.

The first skill is the reason the library exists. Design-variant rounds (parallel
design candidates compared on one screen) kept degrading from round two onward: the
variants converged, the quality regressed, and hours of worker time were lost. Measured
across 37 candidates, code similarity between "independent" variants went from 0.12 on
a blank-slate round to 0.74 once copies and pixel gates crept in. The fix was not more
rules but a different engine for every round after the first. That engine, its
rationale, and the benchmark that proves it are what `design-variant-rounds` carries.

## What's inside

| Skill | One line | Harness |
|---|---|---|
| [design-variant-rounds](skills/design-variant-rounds/SKILL.md) | Produce N independent design variants of a screen, component, or information architecture in parallel, compare them on a single page, and iterate in rounds. Rounds after the first run on a **same-author, one-axis, verbatim-feedback** engine so variants improve instead of converging. | Orca · Claude Code · generic (adapters) |
| [socratic](skills/socratic/SKILL.md) | Turn ambiguous material (meeting notes, long specs, policies) into structured understanding and a list of gaps through teach → quiz → grade → re-ask dialogue. | any |
| [orchestration-loop](skills/orchestration-loop/SKILL.md) | Size, assemble, and verify a parallel worker loop for a task of any size. | Orca required |
| [orca-handoff](skills/orca-handoff/SKILL.md) | Transfer ownership of in-progress work to another agent or worktree with a self-contained handoff. | Orca required |

Skill bodies are written in Korean. The format, scripts, and evals are language-neutral.

## Install

**Any agent, via the skills CLI** (creates the right folder for each agent):

```bash
npx skills add jihkyuo/skills@design-variant-rounds -g      # one skill, user-level
npx skills add jihkyuo/skills@design-variant-rounds -p      # one skill, project-level (writes skills-lock.json)
npx skills add jihkyuo/skills --all -g                      # every skill, every supported agent
```

**Claude Code, as a plugin:**

```
/plugin marketplace add jihkyuo/skills
/plugin install jio-skills@jio-skills
```

`design-variant-rounds` expects the Anthropic `frontend-design` skill to be available to
workers (`npx skills add anthropics/skills@frontend-design`), `node` for its detector,
and `python3` for the stage server. Nothing else is required.

## Quickstart

```
# Design variants: say "시안" / "variants" / "show me a few directions", then follow the skill.
# It briefs, disperses N workers, receives, and routes every later round through its engine table.

# Socratic: "이해시켜줘" / "문답으로 파자" on any long document.

# Orchestration loop (Orca): "오케스트레이션으로 굴려서" on any task.

# Handoff (Orca): "핸드오프" / "이 작업 다른 에이전트로 넘겨".
```

## How design-variant-rounds works

Every round after the first is chosen from one table, not improvised:

| Engine | When | Author | Starting point | Freedom | Gates |
|---|---|---|---|---|---|
| **Diverge** | first round · "none of these, start over" | new workers, 3–5 | blank | one thesis per slot | R1 set |
| **Feedback** | "X is good, but here…" · "too complex" · "bland" | **the same author** (kept alive or re-hydrated) | its own file | one named axis, ≤3 variants | R1 set, unchanged |
| **Converge** | grammar settled · "A's X with B's Y" | coordinator | kept variants | one composed candidate | R1 set |
| **Detail** | polish of the chosen candidate | coordinator + live back-and-forth | chosen candidate | single-item surgery | R1 set |

Three rules carry the weight. The coordinator briefs, relays, and reviews but never
builds a shared base or translates feedback into contract clauses. Variants differ on
one named axis and share an identical quality floor that is never traded against the
axis. Gates never grow after round one.

The skill vendors the parts of other skills it needs (impeccable's craft floor and
Operate-mode guidance, Emil Kowalski's motion decisions, the variant-round rules shared
by `variant`/`prototype`/`prototype UI`, Anthropic's product-brainstorming divergence
procedure, a design-rationale template) as **extracts with provenance**, not as skill
invocations. See [PROVENANCE.md](PROVENANCE.md) for why.

## Transparency

- No skill here makes network calls, sends telemetry, or writes outside the stage
  folder it is told to use.
- The only executable is `skills/design-variant-rounds/scripts/detect.mjs`, a vendored
  copy of impeccable's deterministic anti-pattern detector (Apache-2.0). It reads local
  HTML/CSS and prints findings. Without the optional HTML parser packages it runs in
  regex mode and says so.
- Harness-specific commands (Orca, Claude Code's Agent tool, manual sessions) live only
  in `references/harness-*.md`; the skill body is tool-neutral.

## Development

Every skill ships an `evals/README.md` describing its scenarios and objectively
gradable assertions; the concrete eval set stays in the author's workspace because it is
bound to real project stages and local paths. A change to a skill is accepted when the new version is run against
the old snapshot on the same prompts and graded by an agent that has not seen the skill.
For `design-variant-rounds` the baseline (old skill) scored 4/18 and the current version
18/18 across three coordinator-decision scenarios, twice.

```bash
python3 scripts/validate.py          # frontmatter · referenced files · provenance · detector smoke test
```

CI runs the same command on every push and pull request. Contributing? Start with
[CONTRIBUTING.md](CONTRIBUTING.md) — it lists the principles a change must not break.

## License

[MIT](LICENSE) © 지오현 (jihkyuo). Vendored extracts keep their original licenses; the
full texts are in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
