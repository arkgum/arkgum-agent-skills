# Contributing

Thanks for helping improve Arkgum Agent Skills.

## Good contributions

- Reproducible bug reports with the agent, platform, prompt, and observed output.
- Compatibility fixes that preserve the skill's core workflow.
- Clearer safety boundaries, failure handling, or dependency documentation.
- Deterministic scripts for logic that agents otherwise recreate repeatedly.
- Focused new skills with a specific trigger and verifiable handoff.

## Before opening a pull request

1. Create or update one focused skill.
2. Keep installable files under `skills/<skill-name>/`.
3. Update `README.md`, `catalog.json`, and `CHANGELOG.md` when behavior or catalog entries change.
4. Remove credentials, private URLs, personal paths, and account-specific defaults.
5. Run the static checks documented in `AGENTS.md`.
6. Explain the real task that motivated the change and attach non-sensitive output artifacts when useful.

## New skill checklist

- [ ] The folder and frontmatter `name` match and use lowercase hyphen-case.
- [ ] The `description` explains what the skill does and when it should trigger.
- [ ] `SKILL.md` is concise and imperative.
- [ ] Optional detail is moved to `references/`.
- [ ] Repeated logic is implemented in `scripts/` or `tools/`.
- [ ] External dependencies and permissions are documented.
- [ ] The skill contains no user-specific paths, IDs, credentials, or paid-service assumptions.
- [ ] Example prompts are realistic and do not promise unsupported results.

## Pull requests

Keep pull requests small enough to review. Describe:

- the problem;
- the behavior before and after;
- the affected agents or services;
- how the change was validated;
- any remaining limitation.

By contributing, you agree that your contribution is licensed under the repository's MIT License.
