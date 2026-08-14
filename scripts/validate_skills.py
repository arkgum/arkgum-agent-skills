#!/usr/bin/env python3
"""Static validation for the public Agent Skills collection."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
CATALOG_PATH = ROOT / "catalog.json"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SECRET_PATTERNS = {
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[opsu]_[A-Za-z0-9]{20,}\b"),
    "Google API key": re.compile(r"\bAIza[A-Za-z0-9_-]{20,}\b"),
    "private NotebookLM URL": re.compile(r"notebooklm\.google\.com/notebook/[0-9a-f-]{20,}", re.I),
    "macOS personal path": re.compile(r"/Users/[^/<>{}\s]+/"),
    "Windows personal path": re.compile(r"[A-Za-z]:\\Users\\[^\\<>{}\s]+\\"),
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")

    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("missing closing YAML frontmatter delimiter") from error

    metadata: dict[str, str] = {}
    index = 1
    while index < end:
        line = lines[index]
        if not line or line.startswith((" ", "\t")):
            index += 1
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value in {">", ">-", "|", "|-"}:
            chunks: list[str] = []
            index += 1
            while index < end and (not lines[index] or lines[index].startswith((" ", "\t"))):
                stripped = lines[index].strip()
                if stripped:
                    chunks.append(stripped)
                index += 1
            metadata[key] = " ".join(chunks)
            continue
        metadata[key] = value.strip("\"'")
        index += 1
    return metadata


def validate_markdown_links(skill_dir: Path, errors: list[str]) -> None:
    for markdown_path in skill_dir.rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or re.match(r"^(?:https?://|mailto:)", target):
                continue
            resolved = (markdown_path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{markdown_path.relative_to(ROOT)}: broken local link {raw_target!r}")


def validate_sensitive_content(skill_dir: Path, errors: list[str]) -> None:
    for path in skill_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".mp3", ".mp4", ".zip"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)}: possible {label}")


def main() -> int:
    errors: list[str] = []
    if not SKILLS_DIR.is_dir():
        errors.append("skills directory is missing")
        skill_dirs: list[Path] = []
    else:
        skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())

    discovered: set[str] = set()
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_dir.relative_to(ROOT)}: SKILL.md is missing")
            continue
        try:
            metadata = parse_frontmatter(skill_md)
        except ValueError as error:
            errors.append(f"{skill_md.relative_to(ROOT)}: {error}")
            continue

        extra_keys = set(metadata) - {"name", "description"}
        if extra_keys:
            errors.append(f"{skill_md.relative_to(ROOT)}: unsupported frontmatter keys {sorted(extra_keys)}")

        name = metadata.get("name", "")
        description = metadata.get("description", "")
        if name != skill_dir.name:
            errors.append(f"{skill_md.relative_to(ROOT)}: name {name!r} does not match directory")
        if not NAME_RE.fullmatch(name) or len(name) > 64:
            errors.append(f"{skill_md.relative_to(ROOT)}: invalid skill name {name!r}")
        if len(description) < 40:
            errors.append(f"{skill_md.relative_to(ROOT)}: description is too short")
        discovered.add(name)
        validate_markdown_links(skill_dir, errors)
        validate_sensitive_content(skill_dir, errors)

    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        catalog_names = {entry["name"] for entry in catalog.get("skills", [])}
        if catalog_names != discovered:
            errors.append(
                "catalog skill names differ from discovered skills: "
                f"catalog={sorted(catalog_names)}, discovered={sorted(discovered)}"
            )
        for entry in catalog.get("skills", []):
            expected_path = f"skills/{entry['name']}"
            if entry.get("path") != expected_path:
                errors.append(f"catalog: {entry['name']} has path {entry.get('path')!r}, expected {expected_path!r}")
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        errors.append(f"catalog.json: {error}")

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(discovered)} skills: {', '.join(sorted(discovered))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
