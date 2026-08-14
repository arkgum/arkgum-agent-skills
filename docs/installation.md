# Installation

The recommended installer is the open [`skills`](https://github.com/vercel-labs/skills) CLI. It discovers every `SKILL.md` in this repository and supports multiple AI coding agents.

## Browse before installing

```bash
npx skills add arkgum/arkgum-agent-skills --list
```

## Install one skill

```bash
npx skills add arkgum/arkgum-agent-skills@arkgum-research-to-page
```

Or select it explicitly:

```bash
npx skills add arkgum/arkgum-agent-skills \
  --skill arkgum-research-to-page
```

## Install every skill

```bash
npx skills add arkgum/arkgum-agent-skills --all
```

## Global and agent-specific installation

Install one skill globally for Codex and Claude Code without interactive prompts:

```bash
npx skills add arkgum/arkgum-agent-skills \
  --skill arkgum-research-to-page \
  --agent codex \
  --agent claude-code \
  --global \
  --yes
```

Use `--agent '*'` when you intentionally want to install into every supported agent.

## Manual installation

Clone the repository:

```bash
git clone https://github.com/arkgum/arkgum-agent-skills.git
cd arkgum-agent-skills
```

Copy or symlink only the skills you need.

### Codex

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/arkgum-research-to-page" \
  ~/.codex/skills/arkgum-research-to-page
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/arkgum-research-to-page" \
  ~/.claude/skills/arkgum-research-to-page
```

On Windows, copy the skill directory into the equivalent agent-specific skills directory instead of using the Unix symlink commands.

## Update and remove

```bash
npx skills check
npx skills update
npx skills remove arkgum-research-to-page
```

## Runtime requirements

Installation places the skill instructions and bundled resources into the selected agent. It does not install external services or grant credentials.

### `arkgum-research-to-page`

- Google NotebookLM access.
- A configured NotebookLM MCP integration, or a compatible NotebookLM CLI fallback.
- Python 3 for local run scaffolding and static artifact validation.

## Security note

Agent Skills can instruct an agent to execute scripts, access external services, or create files. Review `SKILL.md` and bundled scripts before installation, keep credentials outside the repository, and grant the narrowest permissions required for the task.
