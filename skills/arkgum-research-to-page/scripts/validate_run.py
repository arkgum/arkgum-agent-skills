#!/usr/bin/env python3
"""Perform static completeness checks for a research-to-page run directory."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_FILES = {
    "00-input.md": 80,
    "10-research-plan.md": 120,
    "20-source-manifest.md": 180,
    "30-grounded-report.md": 600,
    "40-opportunity-matrix.md": 400,
    "50-page-brief.md": 400,
    "60-builder-prompt.md": 500,
    "70-qa.md": 300,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()

    run_dir = args.run_dir.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = run_dir / "manifest.json"

    if not manifest_path.is_file():
        print("ERROR: manifest.json is missing")
        return 1

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: invalid manifest.json: {exc}")
        return 1

    if manifest.get("skill") != "arkgum-research-to-page":
        errors.append("manifest.skill is not arkgum-research-to-page")
    if not str(manifest.get("topic") or "").strip():
        errors.append("manifest.topic is empty")
    if not str(manifest.get("notebook_id") or "").strip():
        errors.append("manifest.notebook_id is empty")
    if manifest.get("status") != "complete":
        warnings.append(f"manifest.status is {manifest.get('status')!r}, not 'complete'")

    contents: dict[str, str] = {}
    for filename, minimum in REQUIRED_FILES.items():
        path = run_dir / filename
        if not path.is_file():
            errors.append(f"missing {filename}")
            continue
        text = path.read_text(encoding="utf-8").strip()
        contents[filename] = text
        if len(text) < minimum:
            errors.append(f"{filename} is too short ({len(text)} < {minimum} chars)")
        if re.search(r"\b(?:TODO|TBD)\b", text, flags=re.IGNORECASE):
            errors.append(f"{filename} contains TODO/TBD")

    citation_text = "\n".join(
        contents.get(name, "")
        for name in ("20-source-manifest.md", "30-grounded-report.md", "40-opportunity-matrix.md")
    )
    if not re.search(r"https?://|источник|source|citation|цитат", citation_text, re.IGNORECASE):
        errors.append("no citation or source markers found in grounded artifacts")

    builder = contents.get("60-builder-prompt.md", "")
    builder_checks = {
        "responsive/mobile": r"responsive|mobile|мобил|адаптив",
        "SEO": r"\bSEO\b|поисков",
        "accessibility": r"accessib|доступност",
        "CTA": r"\bCTA\b|призыв",
        "acceptance criteria": r"acceptance|критери[ийя] готовност",
    }
    for label, pattern in builder_checks.items():
        if builder and not re.search(pattern, builder, re.IGNORECASE):
            errors.append(f"builder prompt lacks {label}")

    qa = contents.get("70-qa.md", "")
    if qa and not re.search(r"\bPASS\b|\bFAIL\b", qa):
        errors.append("70-qa.md has no PASS/FAIL results")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"Validation passed: {len(REQUIRED_FILES)} artifacts checked, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
