#!/usr/bin/env python3
"""Regenerate or verify the content-addressed order-eleven certificate manifest.

The manifest content-addresses every Lean source of this package, the generator that produced its
row leaves, and the exact `finitegeom` revision the package resolves, so that a reader can check
that the sealed sources are the ones the trust fact was derived from.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"
GENERATOR = ROOT / "scripts" / "generate-q11-a5-point-action.py"
ROOTS = ["RelativeConicArcs.Gates.ClebschRigidityTrust"]
REV_RE = re.compile(
    r'\[\[require\]\]\s+name\s*=\s*"finitegeom".*?rev\s*=\s*"([0-9a-f]{40})"',
    re.DOTALL,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def module_name(path: Path) -> str:
    return ".".join(path.relative_to(ROOT).with_suffix("").parts)


def render(source_commit: str) -> dict[str, object]:
    lakefile = (ROOT / "lakefile.toml").read_text(encoding="utf-8")
    rev_match = REV_RE.search(lakefile)
    if rev_match is None:
        raise SystemExit("finitegeom dependency revision is missing from lakefile.toml")

    lean_files = sorted((ROOT / "RelativeConicArcs").rglob("*.lean"))
    sources = [
        {
            "bytes": path.stat().st_size,
            "module": module_name(path),
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(path),
        }
        for path in lean_files
    ]
    return {
        "schema_version": 1,
        "dependency": {
            "repository": "https://github.com/tavisrudd/finitegeom",
            "commit": rev_match.group(1),
        },
        "module_count": len(sources),
        "roots": ROOTS,
        "sources": sources,
        "generator": {
            "bytes": GENERATOR.stat().st_size,
            "path": str(GENERATOR.relative_to(ROOT)),
            "sha256": sha256(GENERATOR),
        },
        "source_commit": source_commit,
    }


def serialize(manifest: dict[str, object]) -> str:
    return json.dumps(manifest, indent=2) + "\n"


def lean_sources_unchanged_since(commit: str) -> bool:
    """Has any Lean source moved since the commit the manifest names?

    Verification compares against the recorded source commit rather than `HEAD`.  Sealing is itself
    committed, so the seal always lands one commit after the sources it describes; deriving the
    expected commit from `HEAD` would make the check permanently red the moment it was published.
    What matters is that the Lean sources have not moved since the recorded commit, which is
    exactly what this asks.
    """
    result = subprocess.run(
        ["git", "diff", "--quiet", commit, "HEAD", "--", "RelativeConicArcs"],
        cwd=ROOT,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        expected = render(git_head())
        MANIFEST.write_text(serialize(expected), encoding="utf-8")
        print(f"wrote {MANIFEST.relative_to(ROOT)} ({expected['module_count']} modules)")
        return 0

    if not MANIFEST.is_file():
        print("MANIFEST.json is missing")
        return 1
    recorded = json.loads(MANIFEST.read_text(encoding="utf-8"))
    source_commit = recorded.get("source_commit", "")
    if MANIFEST.read_text(encoding="utf-8") != serialize(render(source_commit)):
        print("MANIFEST.json is stale")
        return 1
    if not lean_sources_unchanged_since(source_commit):
        print(f"Lean sources have changed since the sealed commit {source_commit}")
        return 1
    print(f"MANIFEST.json ok ({recorded['module_count']} modules)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
