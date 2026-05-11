"""
Release Notes Writer Agent
Takes a list of tickets, git log, or changelog and produces audience-tailored
release notes for users, engineering teams, and executives.

Usage:
    python release_notes_writer.py --input tickets.txt --version "2.4.0"
    python release_notes_writer.py --input changelog.md --audience user
    python release_notes_writer.py --input tickets.json --audience all --output release.md
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPTS = {
    "user": """You are a product writer producing customer-facing release notes.

Given a list of tickets, git commits, or a changelog, produce release notes in this format:

# What's New in [Product] — [Version / Date]

[1-sentence summary of the release theme. E.g., "This release focuses on making your weekly workflow faster."]

---

## New Features

### [Feature Name]
[2-3 sentences. What it is, what problem it solves, how to access it. No jargon.]

---

## Improvements

- **[Area]**: [What changed and why it's better. User benefit, not technical detail.]
- **[Area]**: [Same pattern]

---

## Bug Fixes

- Fixed an issue where [symptom the user experienced] in [feature/context].
- Fixed [symptom] when [condition].

---

## Coming Soon

- [Brief teaser of next meaningful feature — 1 sentence]

---

Rules:
- Write for a non-technical user. Never use technical terms without explanation.
- Lead with user benefit, not implementation detail
- Bug fixes: describe the symptom, not the root cause
- Omit internal refactors, infrastructure changes, and dependency updates entirely
- If a ticket is a pure engineering task with no user-visible change, skip it""",

    "engineering": """You are a technical writer producing engineering-facing release notes.

Given a list of tickets, git commits, or a changelog, produce release notes in this format:

# Release Notes — [Version] — [Date]

## Summary
[2-3 sentences covering scope and key changes]

---

## Features Shipped

| Ticket | Feature | Owner | Notes |
|--------|---------|-------|-------|
| [ID] | [Name] | [Team/person] | [Any migration or config needed] |

---

## Bug Fixes

| Ticket | Bug | Root Cause | Fixed In |
|--------|-----|-----------|---------|
| [ID] | [Description] | [Root cause] | [Component / service] |

---

## Breaking Changes

> ⚠️ Action required before upgrading

- **[Change]**: [What broke, what to update, migration path]

---

## Deprecations

- **[API / feature]**: Deprecated in this release. Removal target: [version/date]. Migration: [path]

---

## Infrastructure / Dependencies

- [Dependency update and version, with reason if non-trivial]
- [Config change or environment variable added/changed]

---

## Rollback Instructions

If this release needs to be rolled back:
1. [Step]
2. [Step]
[If no special rollback steps, state: "Standard rollback — redeploy previous image"]

---

Rules:
- Include ticket IDs for every item
- Breaking changes get their own section — never bury them
- Explicitly state if there are no breaking changes: "No breaking changes in this release"
- Include migration guides inline, not as links to docs that may change""",

    "exec": """You are a product leader producing an executive release summary.

Given a list of tickets, git commits, or a changelog, produce a brief executive summary in this format:

# [Product] Release Summary — [Version / Date]

## What Shipped
[3-5 bullets. Each one is a customer-visible outcome, not a technical task. Lead with business impact.]

- **[Feature/fix]**: [Impact — e.g., "Reduces support tickets for X", "Enables upsell to Y accounts"]
- ...

## Business Impact

| Area | Expected Impact | Measurable By |
|------|----------------|--------------|
| [e.g., Activation] | [e.g., Reduces time-to-first-insight] | [e.g., TTV metric in Snowflake] |

## Customer Commitments Delivered

[List any features that were promised to specific accounts or segments. Include account name if appropriate.]

## What's NOT In This Release

[1-3 bullets on notable items that were scoped out or deferred — so execs aren't surprised by customer questions]

## Risks / Watch Items

- [Anything that could generate customer feedback or support volume post-launch]

---

Rules:
- No technical detail. Execs don't need to know the root cause of bugs.
- Frame everything in terms of customer or business outcome
- Keep total length under 1 page
- If a release has no customer-visible changes (pure tech debt), say so explicitly""",
}


def write_release_notes(
    input_text: str,
    audience: str,
    version: str = "",
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    audiences = ["user", "engineering", "exec"] if audience == "all" else [audience]
    all_results = []

    for aud in audiences:
        system_prompt = SYSTEM_PROMPTS[aud]
        user_content = f"Write release notes from the following:\n\n{input_text}"
        if version:
            user_content += f"\n\nVersion / release label: {version}"

        if len(audiences) > 1:
            print(f"\n{'=' * 60}")
            print(f"AUDIENCE: {aud.upper()}")
            print("=" * 60)
        else:
            print(f"Writing {aud} release notes...\n")
            print("=" * 60)

        result = []

        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": user_content}],
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                result.append(text)

        all_results.append(f"## {aud.upper()} AUDIENCE\n\n" + "".join(result))

    print("\n" + "=" * 60)

    if output_file:
        Path(output_file).write_text("\n\n---\n\n".join(all_results))
        print(f"\nRelease notes saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate audience-tailored release notes from tickets or git log"
    )
    parser.add_argument(
        "--input", required=True, help="Path to tickets, git log, or changelog file"
    )
    parser.add_argument(
        "--audience",
        choices=["user", "engineering", "exec", "all"],
        default="all",
        help="Target audience (default: all)",
    )
    parser.add_argument(
        "--version", help="Version or release label (e.g., '2.4.0' or 'May 2026')"
    )
    parser.add_argument("--output", help="Save release notes to this markdown file")
    args = parser.parse_args()

    input_text = Path(args.input).read_text()
    print(f"Loaded input from: {args.input}\n")

    write_release_notes(
        input_text,
        audience=args.audience,
        version=args.version or "",
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
