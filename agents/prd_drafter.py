"""
PRD Drafter Agent
Takes a feature brief, Jira ticket, or rough idea and produces a structured
PRD draft with problem statement, goals, user stories, success metrics,
and open questions.

Usage:
    python prd_drafter.py --brief "build a weekly email digest for managers"
    python prd_drafter.py --file ticket.txt
    python prd_drafter.py --brief "..." --context context.md --output prd.md
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPT = """You are a senior product manager writing a structured PRD.

Given a feature brief, ticket description, or rough idea, produce a complete
PRD draft in this format:

# PRD: [Feature Name]

**Author**: [infer from context or leave blank]
**Status**: Draft
**Last Updated**: [today's date]
**Target Release**: [infer or leave as TBD]

---

## Problem Statement
[2-3 sentences. What pain does this solve? For whom? What evidence suggests it matters?
If evidence isn't provided, write: "[NEEDS DATA: what evidence would validate this problem]"]

## Goals
- [Measurable outcome 1 — tie to an OKR or metric where possible]
- [Measurable outcome 2]
- [Measurable outcome 3]

## Non-Goals
- [What this explicitly does NOT do in v1]
- [Scope boundary that might otherwise be assumed]

## User Stories
1. As a **[user type]**, I want to **[action]**, so that **[outcome]**.
2. As a **[user type]**, I want to **[action]**, so that **[outcome]**.
3. As a **[user type]**, I want to **[action]**, so that **[outcome]**.

## Proposed Solution
[Describe the solution clearly enough for design and engineering to start.
Not a full spec — just clear enough that scope is unambiguous.]

## Success Metrics
| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|-------------------|
| [Primary metric] | [Current value or TBD] | [Goal] | [How measured] |
| [Secondary metric] | | | |

## Open Questions
1. [Question that needs an answer before engineering starts]
2. [Question that needs an answer before engineering starts]
3. [Question that needs an answer before engineering starts]

## Dependencies
| Dependency | Team / System | Status |
|-----------|--------------|--------|
| [Dependency] | [Owner] | Confirmed / TBD |

---

Rules:
- Mark any section where input is insufficient with [NEEDS INPUT: what's missing]
- Non-Goals section is mandatory — if none are obvious, derive them from the solution
- Every success metric must have a measurement method
- Open Questions must be genuine blockers, not rhetorical
- Keep the problem statement factual — do not assume user sentiment not in the brief"""


def draft_prd(
    brief: str,
    context: str = "",
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    user_content = f"Write a PRD for the following:\n\n{brief}"
    if context:
        user_content += f"\n\nAdditional context:\n{context}"

    print("Drafting PRD...\n")
    print("=" * 60)

    result = []

    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=2500,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_content}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print("\n" + "=" * 60)

    if output_file:
        Path(output_file).write_text("".join(result))
        print(f"\nPRD saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Draft a PRD from a brief or ticket")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--brief", help="Feature brief as text")
    group.add_argument("--file", help="Path to ticket or brief file")
    parser.add_argument(
        "--context",
        help="Path to additional context file (CLAUDE.md, OKRs, prior research)",
    )
    parser.add_argument("--output", help="Save PRD to this markdown file")
    args = parser.parse_args()

    if args.brief:
        brief = args.brief
    else:
        brief = Path(args.file).read_text()
        print(f"Loaded brief from: {args.file}\n")

    context = ""
    if args.context:
        context = Path(args.context).read_text()
        print(f"Loaded context from: {args.context}\n")

    draft_prd(brief, context=context, output_file=args.output)


if __name__ == "__main__":
    main()
