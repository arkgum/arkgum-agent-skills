# Public launch checklist

Use this checklist when publishing or promoting a release.

## Repository setup

- [x] Public repository named `arkgum-agent-skills`.
- [x] Description explains the outcome, not merely “a collection of prompts”.
- [x] Topics include `agent-skills`, `codex`, `claude-code`, `notebooklm`, and `content-creation`.
- [ ] Upload `assets/social-preview.png` in GitHub repository settings as the social preview.
- [x] `README.md`, license, contribution guide, security policy, and code of conduct are visible.
- [x] GitHub Actions validation is green.
- [x] A `v0.1.0` release explains what each launch skill enables.
- [ ] The repository is pinned on the `arkgum` profile.

## Discovery

- [ ] Confirm `npx skills add arkgum/arkgum-agent-skills --list` discovers the published skill.
- [ ] Install one skill through the CLI from a clean environment.
- [ ] Check whether the repository has appeared on [skills.sh](https://skills.sh/) after real installs.
- [ ] Add a skills.sh install-count badge only after the repository is indexed.
- [x] Add the GitHub topics `agent-skills`, `codex-skills`, and `claude-code-skills`.

## Launch content

- [ ] Record a short before/after demo of one concrete workflow.
- [ ] Publish one visual showing input → artifacts → final handoff.
- [ ] Write a launch post around the problem solved, not the number of files in the repository.
- [ ] Link directly to one installation command.
- [ ] Ask early users for one reproducible example or issue, not generic feedback.

## Ongoing credibility

- [ ] Keep the catalog small and curated.
- [ ] Publish changelog entries and tagged releases.
- [ ] Answer issues with reproducible artifacts.
- [ ] Add skills only after removing personal defaults and undocumented dependencies.
- [ ] Never inflate stars, installs, testimonials, or compatibility claims.
