# Repository instructions

This repository publishes portable Agent Skills. Keep changes focused, reviewable, and safe for public installation.

## Skill contract

- Store installable skills under `skills/<skill-name>/`.
- Require `SKILL.md` with only `name` and `description` in YAML frontmatter.
- Match the directory name to the frontmatter `name`.
- Keep `SKILL.md` concise; move optional detail to one-level-deep `references/` files.
- Put repeated or fragile logic in `scripts/` or `tools/`.
- Do not add `README.md`, changelogs, or installation guides inside individual skill directories.
- Write generated task artifacts outside the installed skill directory.

## Public-safety contract

- Never commit credentials, cookies, tokens, private URLs, personal absolute paths, or account identifiers.
- Replace personal defaults with inputs, documented examples, or explicit placeholders.
- Document external tools and permissions in the root installation guide and catalog.
- Require explicit authorization for publication, deletion, paid generation, purchases, account changes, and other consequential external actions.

## Repository maintenance

- Update `README.md` and `catalog.json` when skills are added, removed, or renamed.
- Update `CHANGELOG.md` for user-visible changes.
- Keep examples realistic and free of unverifiable performance claims.
- Run the repository validator and Python syntax compilation before proposing a release.
