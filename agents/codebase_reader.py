"""
Codebase Reader Agent
Walks a local directory, reads the key files, and produces a structured
codebase analysis: architecture map, component breakdown, data model,
and quality signals.

Usage:
    python codebase_reader.py --path ./my-project
    python codebase_reader.py --path ./my-project --mode onboarding
    python codebase_reader.py --path ./my-project --file src/services/digest.py
    python codebase_reader.py --path ./my-project --output codebase-report.md

Modes: full | architecture | onboarding | file
"""

import anthropic
import argparse
import os
from pathlib import Path


# Files to always read when present (orientation layer)
ANCHOR_FILES = [
    "README.md",
    "README.rst",
    "readme.md",
    "package.json",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "go.mod",
    "Cargo.toml",
    "pom.xml",
    "build.gradle",
    "Makefile",
    "docker-compose.yml",
    "docker-compose.yaml",
    ".env.example",
    "requirements.txt",
    "Pipfile",
]

# Directories to skip entirely
SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".pytest_cache", ".mypy_cache",
    "dist", "build", ".next", ".nuxt", "coverage", ".coverage", "venv",
    ".venv", "env", ".env", "vendor", ".idea", ".vscode", "target",
    "out", ".cache", "tmp", "temp", "logs", ".tox",
}

# Extensions to include when walking the tree
CODE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".kt",
    ".rb", ".php", ".cs", ".cpp", ".c", ".h", ".swift", ".scala",
    ".sql", ".graphql", ".proto", ".yaml", ".yml", ".toml", ".json",
    ".md", ".sh", ".bash",
}

# Max file size to read (skip very large files)
MAX_FILE_BYTES = 50_000
# Max total content sent to the model
MAX_TOTAL_BYTES = 150_000


def collect_anchor_files(root: Path) -> list[tuple[str, str]]:
    collected = []
    for name in ANCHOR_FILES:
        fp = root / name
        if fp.exists() and fp.is_file():
            try:
                content = fp.read_text(errors="replace")
                collected.append((str(fp.relative_to(root)), content[:MAX_FILE_BYTES]))
            except Exception:
                pass
    return collected


def walk_codebase(root: Path, max_bytes: int = MAX_TOTAL_BYTES) -> list[tuple[str, str]]:
    files = []
    total = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skipped directories in-place
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]

        for fname in sorted(filenames):
            fp = Path(dirpath) / fname
            if fp.suffix not in CODE_EXTENSIONS:
                continue
            if fp.stat().st_size > MAX_FILE_BYTES:
                files.append((str(fp.relative_to(root)), f"[file too large to read — {fp.stat().st_size // 1024}KB]"))
                continue
            try:
                content = fp.read_text(errors="replace")
                rel = str(fp.relative_to(root))
                files.append((rel, content))
                total += len(content)
                if total >= max_bytes:
                    files.append(("...", f"[truncated — reached {max_bytes // 1024}KB limit]"))
                    return files
            except Exception:
                pass

    return files


def format_files(files: list[tuple[str, str]]) -> str:
    parts = []
    for path, content in files:
        parts.append(f"### {path}\n```\n{content}\n```")
    return "\n\n".join(parts)


def build_tree(root: Path, max_depth: int = 3) -> str:
    lines = [root.name + "/"]

    def _walk(path: Path, prefix: str, depth: int) -> None:
        if depth > max_depth:
            return
        try:
            entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
        except PermissionError:
            return
        entries = [e for e in entries if e.name not in SKIP_DIRS and not e.name.startswith(".")]
        for i, entry in enumerate(entries):
            connector = "└── " if i == len(entries) - 1 else "├── "
            lines.append(prefix + connector + entry.name + ("/" if entry.is_dir() else ""))
            if entry.is_dir():
                extension = "    " if i == len(entries) - 1 else "│   "
                _walk(entry, prefix + extension, depth + 1)

    _walk(root, "", 1)
    return "\n".join(lines)


SYSTEM_PROMPTS = {
    "full": """You are a senior software engineer producing a complete codebase analysis.

Given the contents of a codebase, produce a full analysis in this format:

# Codebase Analysis: [Project Name]

**Date**: [today]

---

## What It Is

[2-3 sentences. What this project does, who it's for, and what problem it solves.]

---

## Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Language | [lang + version] | |
| Framework | [framework] | |
| Database | [db] | |
| Infrastructure | [cloud/docker/etc] | |
| Testing | [framework] | |
| Key dependencies | [notable libs] | [why notable] |

---

## Directory Structure

[Explain what each top-level directory is responsible for. Use the tree provided.]

---

## Architecture

[Describe how the system fits together. Include a text diagram of the main flow.]

```
[Entry point]
    ↓
[Layer]
    ↓
[Layer]
    ↓
[Data store / external]
```

**Key components**:
| Component | File(s) | Responsibility |
|-----------|---------|---------------|
| [name] | [path] | [what it does] |

---

## Data Model

[Key entities, their fields, and relationships. Note any non-obvious design decisions.]

---

## API Surface

[List routes, endpoints, or public interfaces. Note auth requirements.]

---

## Quality Signals

| Signal | Assessment | Notes |
|--------|-----------|-------|
| Test coverage | [Good / Partial / Minimal / None] | [observations] |
| Error handling | [Consistent / Inconsistent / Minimal] | |
| Logging | [Structured / Unstructured / Minimal] | |
| Security | [No obvious issues / Issues found] | [list any issues] |
| Tech debt | [Low / Medium / High] | [hotspots] |

---

## Notable Patterns

[Any interesting or non-obvious patterns in the codebase worth knowing about]

---

## Risks & Recommendations

| Issue | Severity | Recommendation |
|-------|---------|---------------|
| [issue] | High/Med/Low | [specific action] |

---

## Where to Start Reading

If someone is new to this codebase, read these files in this order:
1. [file] — [why]
2. [file] — [why]
3. [file] — [why]""",

    "architecture": """You are a principal engineer producing an architecture one-pager.

Given codebase contents, produce a concise architecture summary:

# Architecture: [Project Name]

## What It Does
[2 sentences. Plain language.]

## Tech Stack
[Bullet list: language, framework, database, infra, key deps]

## Architecture Diagram
```
[text diagram showing how components connect]
```

## Components
| Component | File(s) | Responsibility |
|-----------|---------|---------------|
| [name] | [path] | [one sentence] |

## Data Flow
[Step-by-step: how a request enters and what happens to it]

## External Dependencies
[Third-party APIs, services, or systems this relies on]

## Open Questions / Risks
[What's unclear or concerning about the architecture]""",

    "onboarding": """You are a senior engineer writing an onboarding guide for a new team member.

Given codebase contents, produce a practical onboarding guide:

# Onboarding Guide: [Project Name]

## What Is This?
[1 paragraph. What it does and why it exists.]

## How to Run It

```bash
# Step-by-step setup commands
```

## The Mental Model

[Explain how the system works conceptually — before diving into code. What's the main loop? What's the core abstraction?]

## Where Things Live

| I want to... | Look in... |
|-------------|-----------|
| [common task] | [file or directory] |
| [common task] | [file or directory] |
| [common task] | [file or directory] |

## Read This First

Ordered reading list for getting up to speed:
1. [file] — [what you'll learn]
2. [file] — [what you'll learn]
3. [file] — [what you'll learn]

## Common Tasks

### [Task — e.g., "Add a new API endpoint"]
1. [Step]
2. [Step]
3. [Step]

### [Task — e.g., "Add a database migration"]
[Steps]

## Gotchas

Things that will trip you up if you don't know them:

- **[Gotcha]**: [explanation and what to do instead]
- **[Gotcha]**: [explanation]

## How to Test

```bash
# Test commands
```

## Who to Ask

[Based on the codebase, infer likely owners by area — or leave as [Fill in]]""",

    "file": """You are a senior engineer explaining a specific file or module.

Given the file content and its codebase context, produce a focused explanation:

# File Explanation: [filename]

## Purpose

[What this file is responsible for. Why it exists.]

## How It Fits In

[What calls this file / module, and what it calls. Its place in the architecture.]

## Key Functions / Classes

For each important function or class:

### `[name]([params])`

**Does**: [plain language explanation]
**Called by**: [callers if identifiable]
**Calls**: [dependencies]
**Edge cases**: [failure modes, null handling, unexpected inputs]

## Non-Obvious Things

[Anything a reader would find surprising, confusing, or easy to misuse]

## Improvement Opportunities

[Specific things that could be refactored, better tested, or documented]""",
}


def analyze(
    root: Path,
    mode: str,
    specific_file: str | None = None,
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    print(f"Reading codebase at: {root}\n")

    # Build directory tree
    tree = build_tree(root)

    if specific_file and mode == "file":
        # Single file mode
        fp = root / specific_file
        if not fp.exists():
            print(f"File not found: {specific_file}")
            raise SystemExit(1)
        file_content = fp.read_text(errors="replace")
        # Also collect anchor files for context
        anchor = collect_anchor_files(root)
        context = f"Directory tree:\n```\n{tree}\n```\n\n"
        context += format_files(anchor[:3])  # README + package.json for context
        context += f"\n\n### Target file: {specific_file}\n```\n{file_content}\n```"
        user_content = f"Explain this file in the context of the codebase:\n\n{context}"
    else:
        # Walk the full codebase
        anchor_files = collect_anchor_files(root)
        anchor_set = {name for name, _ in anchor_files}

        # Walk remaining files
        all_files = walk_codebase(root)
        other_files = [(p, c) for p, c in all_files if p not in anchor_set]

        # Anchor files first, then the rest
        ordered = anchor_files + other_files

        context = f"Directory tree:\n```\n{tree}\n```\n\n"
        context += format_files(ordered)

        task_map = {
            "full": "Produce a complete codebase analysis",
            "architecture": "Produce an architecture one-pager",
            "onboarding": "Produce an onboarding guide for a new engineer",
        }
        task = task_map.get(mode, "Analyse this codebase")
        user_content = f"{task}:\n\n{context}"

    system = SYSTEM_PROMPTS[mode]

    print(f"Analysing [{mode} mode]...\n")
    print("=" * 60)

    result = []
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_content}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print("\n" + "=" * 60)

    if output_file:
        Path(output_file).write_text("".join(result))
        print(f"\nReport saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Read and analyse a codebase — produces architecture maps, onboarding guides, or file explanations"
    )
    parser.add_argument(
        "--path", required=True, help="Path to the root of the codebase"
    )
    parser.add_argument(
        "--mode",
        choices=["full", "architecture", "onboarding", "file"],
        default="full",
        help="Type of analysis (default: full)",
    )
    parser.add_argument(
        "--file",
        help="Specific file to explain (relative to --path). Requires --mode file.",
    )
    parser.add_argument(
        "--output", help="Save the report to this markdown file"
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Directory not found: {root}")
        raise SystemExit(1)

    if args.file and args.mode != "file":
        print("--file requires --mode file")
        raise SystemExit(1)

    analyze(root, mode=args.mode, specific_file=args.file, output_file=args.output)


if __name__ == "__main__":
    main()
