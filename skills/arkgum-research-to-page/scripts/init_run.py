#!/usr/bin/env python3
"""Create an isolated artifact workspace for an arkgum-research-to-page run."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path


TRANSLIT = str.maketrans(
    {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e",
        "ё": "e", "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k",
        "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r",
        "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "ts",
        "ч": "ch", "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "",
        "э": "e", "ю": "yu", "я": "ya",
    }
)

ARTIFACTS = {
    "input": "00-input.md",
    "research_plan": "10-research-plan.md",
    "source_manifest": "20-source-manifest.md",
    "grounded_report": "30-grounded-report.md",
    "opportunity_matrix": "40-opportunity-matrix.md",
    "page_brief": "50-page-brief.md",
    "builder_prompt": "60-builder-prompt.md",
    "qa": "70-qa.md",
}


def slugify(value: str) -> str:
    value = value.lower().translate(TRANSLIT)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return (value[:72].strip("-") or "research")


def unique_directory(root: Path, stem: str) -> Path:
    candidate = root / stem
    suffix = 2
    while candidate.exists():
        candidate = root / f"{stem}-{suffix}"
        suffix += 1
    return candidate


def write_markdown(path: Path, title: str, body: str = "") -> None:
    path.write_text(f"# {title}\n\n{body.rstrip()}\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--audience", default="")
    parser.add_argument("--page-goal", default="")
    parser.add_argument("--offer", default="")
    parser.add_argument("--cta", default="")
    parser.add_argument("--builder", default="Google AI Studio Build")
    parser.add_argument("--language", default="ru")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path.home() / "Agent_Work" / "arkgum-research-to-page-runs",
    )
    args = parser.parse_args()

    now = datetime.now().astimezone()
    root = args.output_root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    run_dir = unique_directory(root, f"{now:%Y%m%d-%H%M%S}-{slugify(args.topic)}")
    run_dir.mkdir(parents=False)

    manifest = {
        "version": 1,
        "skill": "arkgum-research-to-page",
        "created_at": now.isoformat(timespec="seconds"),
        "status": "initialized",
        "topic": args.topic.strip(),
        "audience": args.audience.strip(),
        "page_goal": args.page_goal.strip(),
        "offer": args.offer.strip(),
        "cta": args.cta.strip(),
        "builder": args.builder.strip(),
        "language": args.language.strip(),
        "notebook_id": None,
        "notebook_url": None,
        "research_task_ids": [],
        "selected_opportunity": None,
        "unresolved_placeholders": [],
        "artifacts": {key: str(run_dir / name) for key, name in ARTIFACTS.items()},
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    input_body = (
        f"- Тема: {args.topic}\n"
        f"- Аудитория: {args.audience or '[не указана — вывести допущение]'}\n"
        f"- Цель страницы: {args.page_goal or '[не указана]'}\n"
        f"- Оффер: {args.offer or '[не указан]'}\n"
        f"- CTA: {args.cta or '[не указан]'}\n"
        f"- Builder: {args.builder}\n"
        f"- Язык: {args.language}\n\n"
        "## Пользовательские источники\n\n"
        "## Допущения\n\n"
        "## Неразрешённые placeholders\n"
    )
    write_markdown(run_dir / ARTIFACTS["input"], "Входные данные", input_body)

    titles = {
        "research_plan": "План исследования",
        "source_manifest": "Манифест источников",
        "grounded_report": "Grounded research report",
        "opportunity_matrix": "Opportunity matrix",
        "page_brief": "Page brief",
        "builder_prompt": "Builder prompt",
        "qa": "QA",
    }
    for key, title in titles.items():
        write_markdown(run_dir / ARTIFACTS[key], title)

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
