# Contributing

Thanks for looking. This library is small on purpose; a few principles keep it that way.

## Non-negotiable principles

A change that breaks one of these is a regression, however useful it looks:

1. **Extract, don't invoke.** When a skill needs a rule from another public skill, it
   vendors the exact section into `references/` with the source repo, commit, and
   license in a `NOTICE.md`, and the license text in `THIRD_PARTY_LICENSES.md`. It never
   tells the agent to load the other skill wholesale. Whole-skill loads bring
   contradictory directives, interactive gates that stall inside worker loops, and
   ten times the context for the same effect.
2. **One rule, one owner, one moment.** Every rule in a skill names which role applies it
   (worker, coordinator, planner) and at which step. A rule that "everyone should keep
   in mind" belongs nowhere.
3. **Skill bodies are harness-neutral.** Commands for launching workers, sending
   follow-up messages, waiting, and taking screenshots live in `references/harness-*.md`.
   The body says *what* ("send the feedback to the same worker"), the adapter says *how*.
4. **A skill is verified before it is tagged.** Each skill documents its scenarios and
   assertions in `evals/README.md` (the concrete set is author-local). A change is accepted when the new version is run against the previous snapshot on the
   same prompts and graded by an agent that has not read the skill. Untested edits are
   not merged, including "just a wording change".

## Development

```bash
python3 scripts/validate.py
```

This is what CI runs: frontmatter validity for every `skills/*/SKILL.md`, existence of
every referenced `references/*.md`, provenance consistency between each skill's
`NOTICE.md` and the root `THIRD_PARTY_LICENSES.md`, and a smoke test of the vendored
detector. It needs only Python 3 and Node.

To run a skill's evals, follow the loop described in
`skills/<name>/evals/README.md`. The eval workspace stays outside the repository.

## Pull requests

- Keep changes surgical; touch only what the change requires. Match the surrounding
  style; don't refactor unrelated text.
- If you change a skill's behavior, re-run its evals and paste the before/after pass
  counts in the PR description.
- If you re-vendor an extract, bump the commit in the skill's `NOTICE.md` and refresh
  the license text in `THIRD_PARTY_LICENSES.md` in the same PR.
- Bump `plugin.json`/`marketplace.json` versions and add a `CHANGELOG.md` entry with the
  change; tags follow the version.

## Reporting bugs

Use the issue templates. Because the same skill runs under different harnesses, always
name the **harness** (Orca, Claude Code, Codex, Cursor, other) and the **skill**; that
context is usually most of the diagnosis.

## License

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
