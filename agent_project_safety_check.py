#!/usr/bin/env python3
"""Pre-publish safety checks for coding-agent projects."""

from __future__ import annotations

import argparse
import fnmatch
import os
from dataclasses import dataclass
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".turbo",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "target",
    "vendor",
}

SENSITIVE_PATTERNS = [
    ".env",
    ".env.*",
    "*.env",
    "*key*.json",
    "*keys.json",
    "*secret*",
    "*token*",
    "google-cloud-key.json",
    "gcp-oauth.keys.json",
]

RECOMMENDED_GITIGNORE = [
    ".env",
    ".env.*",
    "*.env",
    "*key*.json",
    "*keys.json",
    "*secret*",
    "*token*",
]


@dataclass(frozen=True)
class Finding:
    severity: str
    title: str
    items: list[str]


def normalize_path(path: Path) -> str:
    return path.as_posix()


def iter_project_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, dirs, filenames in os.walk(root):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        current_path = Path(current)
        for filename in filenames:
            files.append(current_path / filename)
    return files


def is_sensitive_name(relative_path: str) -> bool:
    name = Path(relative_path).name
    lowered_path = relative_path.lower()
    lowered_name = name.lower()
    return any(
        fnmatch.fnmatch(lowered_name, pattern.lower())
        or fnmatch.fnmatch(lowered_path, pattern.lower())
        for pattern in SENSITIVE_PATTERNS
    )


def read_gitignore_patterns(root: Path) -> set[str]:
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        return set()

    patterns: set[str] = set()
    for line in gitignore.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            patterns.add(stripped)
    return patterns


def check_sensitive_files(root: Path) -> Finding | None:
    sensitive: list[str] = []
    for file_path in iter_project_files(root):
        relative = normalize_path(file_path.relative_to(root))
        if is_sensitive_name(relative):
            sensitive.append(relative)

    if not sensitive:
        return None

    return Finding(
        severity="HIGH",
        title="Sensitive-looking files found",
        items=sorted(sensitive),
    )


def check_gitignore(root: Path) -> Finding | None:
    patterns = read_gitignore_patterns(root)
    if not patterns:
        return Finding(
            severity="MEDIUM",
            title="Missing .gitignore",
            items=["Add a .gitignore with common secret patterns."],
        )

    missing = [pattern for pattern in RECOMMENDED_GITIGNORE if pattern not in patterns]
    if not missing:
        return None

    return Finding(
        severity="MEDIUM",
        title="Missing .gitignore patterns",
        items=missing,
    )


def check_agents_md(root: Path) -> Finding | None:
    if (root / "AGENTS.md").exists():
        return None

    return Finding(
        severity="LOW",
        title="Missing AGENTS.md",
        items=["Add agent-facing project rules so coding agents handle the repo safely."],
    )


def collect_findings(root: Path) -> list[Finding]:
    checks = [
        check_sensitive_files,
        check_gitignore,
        check_agents_md,
    ]
    findings: list[Finding] = []
    for check in checks:
        finding = check(root)
        if finding:
            findings.append(finding)
    return findings


def print_finding(finding: Finding) -> None:
    print(f"[{finding.severity}] {finding.title}:")
    for item in finding.items:
        print(f"  - {item}")
    print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check a coding-agent project before publishing it.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project folder to check. Defaults to the current folder.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.path).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        print(f"Invalid project path: {root}")
        return 2

    print("Agent Project Safety Check")
    print(f"Target: {root}")
    print()

    findings = collect_findings(root)
    if not findings:
        print("No high-signal safety issues found.")
        print("Result: ready for a manual review before publishing.")
        return 0

    for finding in findings:
        print_finding(finding)

    has_high = any(finding.severity == "HIGH" for finding in findings)
    print("Result: review needed before publishing.")
    return 1 if has_high else 0


if __name__ == "__main__":
    raise SystemExit(main())
