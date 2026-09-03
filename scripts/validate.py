#!/usr/bin/env python3
"""Repository validation — what CI runs. Standard library only; needs `node` for the detector smoke test.

Checks:
  1. every skills/*/SKILL.md has YAML frontmatter with `name` (== folder name, [a-z0-9-]) and a
     non-empty `description`; the frontmatter block is at most 1024 characters (Agent Skills spec)
  2. every `references/<file>.md` a SKILL.md mentions exists next to it
  3. every source row in a skill's NOTICE.md table names a repository that appears as a heading in
     the root THIRD_PARTY_LICENSES.md
  4. the vendored detector runs on tests/fixtures/smoke.html and prints a JSON array
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
FAIL: list[str] = []


def fail(msg: str) -> None:
    FAIL.append(msg)
    print(f"  FAIL  {msg}")


def ok(msg: str) -> None:
    print(f"  ok    {msg}")


def parse_frontmatter(text: str) -> tuple[dict[str, str], int]:
    """Minimal YAML subset: `key: value` and `key: >-` / `key: |` folded blocks."""
    if not text.startswith("---"):
        return {}, 0
    end = text.find("\n---", 3)
    if end < 0:
        return {}, 0
    block = text[4:end]
    data: dict[str, str] = {}
    key = None
    folded: list[str] = []
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m and not line.startswith(" "):
            if key and folded:
                data[key] = " ".join(s.strip() for s in folded).strip()
            key, val = m.group(1), m.group(2).strip()
            folded = []
            if val in (">-", ">", "|", "|-"):
                continue
            data[key] = val
            key = None
        elif key is not None:
            folded.append(line)
    if key and folded:
        data[key] = " ".join(s.strip() for s in folded).strip()
    return data, len(block) + 8


def check_frontmatter() -> None:
    print("frontmatter")
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        md = skill_dir / "SKILL.md"
        if not md.exists():
            fail(f"{skill_dir.name}: SKILL.md missing")
            continue
        data, size = parse_frontmatter(md.read_text(encoding="utf-8"))
        name = data.get("name", "")
        desc = data.get("description", "")
        if not name:
            fail(f"{skill_dir.name}: frontmatter has no name")
        elif name != skill_dir.name:
            fail(f"{skill_dir.name}: name '{name}' != folder name")
        elif not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
            fail(f"{skill_dir.name}: name must be lowercase letters, digits, hyphens")
        if not desc:
            fail(f"{skill_dir.name}: description missing or empty")
        if size > 1024:
            fail(f"{skill_dir.name}: frontmatter is {size} chars (> 1024)")
        if name == skill_dir.name and desc and size <= 1024:
            ok(f"{skill_dir.name} ({size} chars)")


def check_references() -> None:
    print("references")
    pat = re.compile(r"`?references/([A-Za-z0-9_.-]+\.md)`?")
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        md = skill_dir / "SKILL.md"
        if not md.exists():
            continue
        text = md.read_text(encoding="utf-8")
        missing = sorted({m for m in pat.findall(text) if not (skill_dir / "references" / m).exists()})
        if missing:
            fail(f"{skill_dir.name}: referenced but missing: {', '.join(missing)}")
        else:
            n = len(set(pat.findall(text)))
            ok(f"{skill_dir.name} ({n} referenced files exist)")


def check_provenance() -> None:
    print("provenance")
    third = ROOT / "THIRD_PARTY_LICENSES.md"
    if not third.exists():
        fail("THIRD_PARTY_LICENSES.md missing")
        return
    headings = re.findall(r"^## (https://github\.com/[^\s@]+)", third.read_text(encoding="utf-8"), re.M)
    known = {h.rstrip("/") for h in headings}
    for notice in sorted(SKILLS.glob("*/NOTICE.md")):
        text = notice.read_text(encoding="utf-8")
        sources = set()
        for row in text.splitlines():
            if not row.startswith("|") or row.startswith("| 대상") or row.startswith("|---"):
                continue
            cells = [c.strip() for c in row.strip("|").split("|")]
            if len(cells) < 2:
                continue
            for repo in re.findall(r"\b([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\b(?= `| ·|$)", cells[1]):
                if "/" in repo and not repo.endswith(".md"):
                    sources.add(repo)
        missing = sorted(s for s in sources if f"https://github.com/{s}" not in known)
        if missing:
            fail(f"{notice.parent.name}/NOTICE.md sources without license text: {', '.join(missing)}")
        else:
            ok(f"{notice.parent.name}/NOTICE.md ({len(sources)} sources covered)")


def check_no_private_identifiers() -> None:
    """Skill bodies must not depend on the author's machine or employer: no absolute home paths,
    no internal ticket ids, no company/product tokens listed below."""
    print("private identifiers")
    import re as _re
    # Structural patterns only. Employer/product tokens live in an untracked local file so the
    # public validator never names them: one token per line in scripts/private-tokens.local
    parts = [r"/Users/[A-Za-z]", r"/home/[A-Za-z]", r"~/Desktop", r"\b[A-Z]{3,6}-\d{2,5}\b",
             r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}"]
    local = ROOT / "scripts" / "private-tokens.local"
    if local.exists():
        parts += [_re.escape(tok.strip()) for tok in local.read_text(encoding="utf-8").splitlines() if tok.strip()]
    pat = _re.compile("|".join(parts))
    hits = []
    for path in sorted(SKILLS.rglob("*")):
        if not path.is_file() or path.suffix not in (".md", ".html", ".json", ".txt", ".py", ".mjs", ".js"):
            continue
        if any(part in ("detector", "lib", "data") for part in path.relative_to(SKILLS).parts):
            continue
        try:
            for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if pat.search(line):
                    hits.append(f"{path.relative_to(ROOT)}:{i}")
        except UnicodeDecodeError:
            continue
    if hits:
        fail("private identifiers found: " + ", ".join(hits[:12]) + (" …" if len(hits) > 12 else ""))
    else:
        ok("no absolute home paths, ticket ids, or employer tokens in skills/")


def check_detector() -> None:
    print("detector smoke test")
    det = SKILLS / "design-variant-rounds" / "scripts" / "detect.mjs"
    fixture = ROOT / "tests" / "fixtures" / "smoke.html"
    if not det.exists():
        ok("no detector vendored — skipped")
        return
    if not fixture.exists():
        fail("tests/fixtures/smoke.html missing")
        return
    try:
        proc = subprocess.run(
            ["node", str(det), "--json", "--no-config", str(fixture)],
            capture_output=True, text=True, timeout=120,
        )
    except FileNotFoundError:
        fail("node not found")
        return
    if proc.returncode not in (0, 2):
        fail(f"detector exit {proc.returncode}: {proc.stderr.strip()[:200]}")
        return
    try:
        findings = json.loads(proc.stdout)
    except json.JSONDecodeError:
        fail(f"detector output is not JSON: {proc.stdout[:120]!r}")
        return
    if not isinstance(findings, list):
        fail("detector output is not a JSON array")
        return
    names = sorted({f.get("antipattern", "?") for f in findings})
    ok(f"{len(findings)} findings on fixture ({', '.join(names) or 'none'})")


def main() -> int:
    check_frontmatter()
    check_references()
    check_provenance()
    check_no_private_identifiers()
    check_detector()
    print()
    if FAIL:
        print(f"{len(FAIL)} check(s) failed")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
