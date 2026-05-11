"""
Stakeholder Updater Agent
Takes project status and produces audience-tailored stakeholder updates:
exec summaries, team check-ins, customer-facing updates, or board briefings.

Usage:
    python stakeholder_updater.py --status status.txt --audience exec
    python stakeholder_updater.py --status "sprint 24 done, shipped digest..." --audience team
    python stakeholder_updater.py --status status.md --audience all --output updates.md
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPTS = {
    "exec": """You are a product leader writing a concise executive update.

Given project status, produce an executive update in this format:

# Executive Update — [Product / Initiative] — [Date]

## Status: [Green / Yellow / Red]

[One sentence on why this status. Green = on track. Yellow = at risk but manageable. Red = needs exec decision.]

---

## This Week

[3-5 bullets. Each bullet is an outcome, not a task. "Shipped X which enables Y" not "completed work on X".]

- **[Area]**: [Outcome and its business significance]

---

## Next 2 Weeks

[3 bullets max. What's coming and what decision or dependency could change it.]

- [Item]: [Expected outcome, owner, any dependency]

---

## Risks & Asks

| Risk | Impact | Ask |
|------|--------|-----|
| [Risk] | [Business impact if unresolved] | [Specific ask from exec — decision, resource, unblock] |

[If no asks: "No asks this week."]

---

## Metrics Snapshot

| Metric | Last Week | This Week | Target | Trend |
|--------|----------|-----------|--------|-------|
| [KPI] | [value] | [value] | [goal] | ↑ / ↓ / → |

---

Rules:
- Total length: max 1 page
- No technical jargon
- Every risk must have a specific ask — vague "FYI" risks are noise
- If status is Yellow or Red, lead with the risk, not the wins""",

    "team": """You are a PM writing a team-facing sprint or weekly update.

Given project status, produce a team update in this format:

# Team Update — [Sprint / Week] — [Date]

## What We Shipped

[Bullets — specific, with ticket IDs if available. Celebrate the work.]

- [Feature / fix]: [what it does, why it matters, who owns it]

---

## What's In Flight

| Item | Owner | Status | Blocked? |
|------|-------|--------|---------|
| [ticket/feature] | [name] | On track / At risk / Blocked | [blocker if any] |

---

## Blockers

[If any blockers, list them with owner and resolution path. If none: "No blockers."]

---

## Decisions Made This Week

[Decisions that affect the team — record them so they're not re-litigated]

- **[Decision]**: [What was decided, who made it, rationale in one sentence]

---

## Heads Up — Coming Next Sprint

[3 bullets so the team isn't surprised]

- [Item]: [what to expect, what's needed from whom]

---

## Shoutouts

[Optional — specific recognition for people who went above and beyond]

---

Rules:
- Use names — team updates build trust when they're personal, not corporate
- Blockers need owners and resolution paths, not just descriptions
- Decisions section is mandatory — the team deserves to know why things changed""",

    "customer": """You are a customer success writer producing a customer-facing update.

Given project status, produce a customer update in this format:

# [Product] Update — [Month / Quarter]

Hi [Customer name or "Team"],

[1 sentence on why you're reaching out — routine update, milestone, or something specific to them.]

---

## What's New

[2-4 bullets on shipped features or improvements that matter to this customer.]

- **[Feature]**: [What it does and how to access it. Plain language, no jargon.]

---

## What's Coming

[2-3 bullets on what's next — only commit to things that are on the roadmap]

- **[Q date]**: [Feature / improvement expected]

---

## Open Items From You

| Item | Status | ETA |
|------|--------|-----|
| [Request or issue] | In progress / Resolved / On roadmap | [date if known] |

---

## Questions or Feedback?

[Call to action — book a call, reply to this email, or reach out to CSM]

---

Rules:
- Never over-commit on timelines — use "targeting Q3" not "shipping July 15"
- Open items table is mandatory if there are any outstanding customer requests
- Tone: warm, direct, professional — not corporate or stiff
- Under 300 words total""",

    "board": """You are a product leader producing a board-level briefing section.

Given product status, produce a board briefing in this format:

# Product Update — Board Briefing — [Quarter / Date]

## Summary
[3 sentences. Where we are, where we're going, and the one thing the board needs to know.]

---

## Key Metrics

| Metric | [Last Quarter] | [This Quarter] | Target | YoY |
|--------|---------------|---------------|--------|-----|
| [North Star] | [value] | [value] | [goal] | [%] |
| [Revenue / ARR] | | | | |
| [Retention] | | | | |

---

## Strategic Progress

For each major strategic initiative:

**[Initiative]**: [1 sentence on progress. Ahead / On track / Behind. Implication.]

---

## Risks for Board Awareness

| Risk | Likelihood | Revenue Impact | Mitigation |
|------|-----------|---------------|-----------|
| [risk] | High/Med/Low | [$range] | [what we're doing] |

---

## Competitive Landscape

[1-3 bullets on material competitive moves since the last board meeting and our response]

---

## Ask of the Board

[Specific asks — introductions, strategic guidance, resource decisions. Never vague.]

---

Rules:
- Board members have 5 minutes for this section — respect that
- Every number needs a comparison point (vs. last quarter, vs. plan, vs. competition)
- Risks section must be honest — boards hate surprises more than bad news
- "Ask of the Board" is mandatory — if you have no ask, you're underusing the board""",
}


def write_update(
    status: str,
    audience: str,
    project: str = "",
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    audiences = list(SYSTEM_PROMPTS.keys()) if audience == "all" else [audience]
    all_results = []

    for aud in audiences:
        system_prompt = SYSTEM_PROMPTS[aud]
        user_content = f"Write a stakeholder update based on the following status:\n\n{status}"
        if project:
            user_content += f"\n\nProject / product: {project}"

        if len(audiences) > 1:
            print(f"\n{'=' * 60}")
            print(f"AUDIENCE: {aud.upper()}")
            print("=" * 60)
        else:
            print(f"Writing {aud} update...\n")
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
        print(f"\nUpdates saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate audience-tailored stakeholder updates"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--status", help="Project status as text")
    group.add_argument("--file", help="Path to status file")
    parser.add_argument(
        "--audience",
        choices=["exec", "team", "customer", "board", "all"],
        default="exec",
        help="Target audience (default: exec)",
    )
    parser.add_argument("--project", help="Project or product name")
    parser.add_argument("--output", help="Save updates to this markdown file")
    args = parser.parse_args()

    if args.status:
        status = args.status
    else:
        status = Path(args.file).read_text()
        print(f"Loaded status from: {args.file}\n")

    write_update(
        status,
        audience=args.audience,
        project=args.project or "",
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
