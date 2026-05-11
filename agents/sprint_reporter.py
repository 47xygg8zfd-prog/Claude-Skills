"""
Sprint Reporter Agent
Takes sprint ticket data (from Jira, Linear, or plain text) and produces
a stakeholder-ready status update with status, highlights, blockers, and asks.

Usage:
    python sprint_reporter.py --input tickets.json
    python sprint_reporter.py --text "ticket list as plain text"
    python sprint_reporter.py --input tickets.json --output update.md --audience exec
"""

import anthropic
import argparse
import json
import sys
from pathlib import Path


SYSTEM_PROMPT = """You are a senior product manager writing a concise, accurate
sprint status update for stakeholders.

Given a list of sprint tickets (with titles, status, points, and any notes),
produce a status update in this format:

## Sprint [N] Status Update
**Status**: 🟢 On Track / 🟡 At Risk / 🔴 Blocked
**Date**: [today]

### Summary
[2-3 sentences. What's the overall state? What's the most important thing to know?]

### This Sprint
| Story | Points | Status | Notes |
|-------|--------|--------|-------|
[one row per ticket]

### Completed ✅
[Bullet list of done items with brief description of value delivered]

### In Progress 🔄
[Bullet list with % complete and any risks]

### Blocked / At Risk 🔴
[Bullet list. For each: what's blocked, what's needed, who owns the unblock]

### Metrics This Sprint
[If any metrics were mentioned in the ticket data, summarize them here]

### Asks / Decisions Needed
[Anything stakeholders need to act on, with owner and deadline]

Adapt tone by audience:
- "team": detailed, technical, peer-level
- "exec": brief, outcome-focused, business impact first
- "stakeholder": clear, non-technical, focused on timeline and value

Rules:
- Never fabricate ticket details not in the input
- If status is unclear from input, mark it as [UNKNOWN] and flag it
- Keep the summary to 3 sentences maximum
- Every blocker must have a proposed owner and deadline"""


def generate_report(
    ticket_data: str,
    audience: str = "stakeholder",
    sprint_name: str = "",
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    audience_context = f"Audience: {audience}."
    sprint_context = f"Sprint: {sprint_name}." if sprint_name else ""

    print(f"Generating sprint report for {audience} audience...\n")
    print("=" * 60)

    result = []

    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    f"{audience_context} {sprint_context}\n\n"
                    f"Generate a status update from this sprint data:\n\n{ticket_data}"
                ),
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print("\n" + "=" * 60)

    if output_file:
        Path(output_file).write_text("".join(result))
        print(f"\nOutput saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Generate sprint status update from ticket data")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", help="Path to JSON or text file with ticket data")
    group.add_argument("--text", help="Ticket data as plain text")
    parser.add_argument(
        "--audience",
        choices=["team", "exec", "stakeholder"],
        default="stakeholder",
        help="Target audience for the report (default: stakeholder)",
    )
    parser.add_argument("--sprint", help="Sprint name or number (e.g. 'Sprint 24')")
    parser.add_argument("--output", help="Save output to this markdown file")
    args = parser.parse_args()

    if args.text:
        ticket_data = args.text
    else:
        path = Path(args.input)
        content = path.read_text()
        # Pretty-print JSON if it parses, otherwise use as-is
        try:
            parsed = json.loads(content)
            ticket_data = json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            ticket_data = content
        print(f"Loaded: {path}\n")

    generate_report(
        ticket_data,
        audience=args.audience,
        sprint_name=args.sprint or "",
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
