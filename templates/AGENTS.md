# Project Agent Rules

These rules are for coding agents working in this repository.

## Language and Tone

- Keep explanations direct and practical.
- Use the repository's existing naming and structure.
- Do not add broad rewrites unless the task asks for them.

## Safety

- Do not print or commit `.env` values, API keys, OAuth secrets, service-role keys, or private key JSON files.
- If a secret-looking file exists, report its path only.
- Keep real credentials in local env files, platform environment variables, keychains, or another approved secret store.
- Use `env.example` for variable names without real values.

## File Changes

- Read nearby files before editing.
- Keep changes scoped to the requested task.
- Do not leave temporary files, debug dumps, generated caches, or local build artifacts.
- Do not use destructive git commands unless the user explicitly asks for them.

## Before Publishing

- Run `python3 agent_project_safety_check.py .`.
- Confirm `.gitignore` blocks common secret file patterns.
- Confirm the README does not expose private paths, client names, or unpublished plans.
