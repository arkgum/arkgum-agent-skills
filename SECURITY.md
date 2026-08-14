# Security policy

Agent Skills can instruct an AI agent to execute scripts, access files, call external services, and create or modify artifacts. Treat every skill as executable workflow code.

## Supported versions

Security fixes are applied to the latest release on the `main` branch.

## Reporting a vulnerability

Do not open a public issue for credentials exposure, command injection, unsafe file operations, permission escalation, or other exploitable behavior.

Use GitHub's **Security → Report a vulnerability** flow for this repository. Include:

- the affected skill and version or commit;
- the agent and operating system;
- minimal reproduction steps;
- the impact;
- a suggested mitigation, if known.

Do not include real credentials or private user data in the report. Replace them with clearly marked test values.

## Scope

Security reports may cover:

- unsafe shell construction or path handling;
- accidental credential or personal-data persistence;
- actions performed without explicit authorization;
- dependency or installer confusion that causes an unintended skill to execute;
- prompt-injection paths that bypass documented safety gates.

Availability problems in third-party services should be reported to those providers unless this repository handles the failure unsafely.
