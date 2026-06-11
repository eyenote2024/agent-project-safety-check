# Agent Project Safety Check

A small pre-publish safety checker for projects built with coding agents such as Codex, Claude Code, Cursor, and similar tools.

It helps maintainers catch common privacy and repository hygiene problems before pushing a project to GitHub:

- sensitive files such as `.env`, key JSON files, and token files
- `.gitignore` rules that do not cover common secret patterns
- missing `AGENTS.md` guidance for coding agents
- public-readiness items that are easy to forget during fast agent-assisted work

The checker only reports file paths and rule status. It does not print secret values.

## Why

Agent-assisted development makes it easy to generate a working project quickly. It also makes it easy to accidentally publish local configuration, API keys, private paths, or project-specific instructions.

This repository provides a lightweight safety pass that maintainers can run before sharing a project or accepting agent-generated changes.

## Quick Start

Run against the current folder:

```bash
python3 agent_project_safety_check.py .
```

Run against another project:

```bash
python3 agent_project_safety_check.py /path/to/project
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

Exit codes:

- `0`: no high-risk issue found
- `1`: high-risk issue found
- `2`: invalid usage or path

## What It Checks

### Sensitive File Names

The checker flags common secret-bearing file names and extensions:

- `.env`, `.env.local`, `.env.production`
- `*.env`
- `*key*.json`
- `*keys.json`
- `*secret*`
- `*token*`
- `google-cloud-key.json`
- `gcp-oauth.keys.json`

It skips dependency and build folders such as `node_modules`, `.git`, `dist`, `build`, `.next`, and common cache folders.

### Git Ignore Coverage

It checks whether `.gitignore` contains common protections:

```gitignore
.env
.env.*
*.env
*key*.json
*keys.json
*secret*
*token*
```

### Agent Guidance

It checks whether the project has an `AGENTS.md` file. A template is included at:

```text
templates/AGENTS.md
```

## Example Output

```text
Agent Project Safety Check
Target: /example/project

[HIGH] Sensitive-looking files found:
  - .env.local
  - config/google-cloud-key.json

[MEDIUM] Missing .gitignore patterns:
  - .env.*
  - *key*.json

[LOW] Missing AGENTS.md

Result: review needed before publishing.
```

## Public Repository Checklist

Before making a repository public:

- remove real `.env` files and key JSON files from the working tree
- make sure `.gitignore` blocks common secret file patterns
- use `env.example` for variable names without real values
- remove private client names, private local paths, and unpublished business details
- add a license
- add basic install and usage instructions
- run this checker again

## Scope

This is a helper, not a complete security scanner. It focuses on simple, high-signal checks that are useful before publishing a coding-agent project.

## License

MIT
