# Sample Report

```text
Agent Project Safety Check
Target: /example/project

[HIGH] Sensitive-looking files found:
  - .env.local
  - config/google-cloud-key.json

[MEDIUM] Missing .gitignore patterns:
  - .env.*
  - *key*.json

[LOW] Missing AGENTS.md:
  - Add agent-facing project rules so coding agents handle the repo safely.

Result: review needed before publishing.
```
