# Agent Project Safety Check Rules

## Scope

This repository is a small public OSS candidate. Keep it privacy-safe and dependency-light.

## Safety

- Never add real `.env` values, API keys, OAuth secrets, service-role keys, private key JSON files, or local private project paths.
- If testing secret detection, use temporary files or documented fake examples only.
- The checker may report sensitive-looking paths, but it must not print file contents.

## Code Style

- Keep the main checker usable with standard `python3`.
- Avoid new dependencies unless there is a clear maintainer benefit.
- Keep output plain text and easy to paste into issues or release checklists.

## Documentation

- README examples must use fake paths and fake filenames only.
- Keep the project focused on pre-publish hygiene for coding-agent repositories.
