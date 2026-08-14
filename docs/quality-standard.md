# Skill quality standard

Every skill published here should pass the following bar.

## Triggering

- The directory name and frontmatter `name` match.
- The `description` says both what the skill does and when it should trigger.
- The skill is narrow enough to have a clear success condition.

## Instructions

- `SKILL.md` contains the essential workflow, boundaries, failure handling, and handoff.
- Detailed variants live in `references/` and are loaded only when needed.
- User-facing repository documentation stays at the repository root, not inside each skill.

## Reproducibility

- Repeated or fragile logic lives in `scripts/` or `tools/`.
- Prompts, manifests, and QA artifacts are saved before irreversible generation steps.
- Outputs are written outside the installed skill directory.

## Safety

- No credentials, cookies, tokens, private URLs, or personal absolute paths.
- External writes, publication, deletion, paid generation, and account changes require explicit authorization.
- Dependencies and required permissions are documented.

## Verification

- Bundled code is syntactically valid.
- Relative Markdown links resolve inside the skill.
- QA checks validate the actual deliverables, not only the presence of files.
- Factual claims distinguish evidence, inference, and unknowns.

## Portability

- A skill follows the open Agent Skills directory structure.
- Agent-specific metadata is optional and cannot replace `SKILL.md`.
- Platform-specific assumptions are explicit rather than silently embedded.
