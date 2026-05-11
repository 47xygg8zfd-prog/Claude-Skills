"""
Engineering Tech Lead Agent
Takes a ticket, PRD, or technical question and produces a tech lead response:
architecture guidance, implementation approach, risks, and review checklist.

Usage:
    python eng_tech_lead.py --ticket "build a digest email service"
    python eng_tech_lead.py --prd prd.md --output tech-plan.md
    python eng_tech_lead.py --question "should we use a job queue or cron for this?"
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPT = """You are a staff-level tech lead reviewing a ticket or technical question.

Produce a tech lead response in this format:

# Tech Lead Review: [Feature / Question]

**Reviewed**: [date]

---

## My Read

[3-5 sentences. Your honest technical take: is the scope right, what's the hard part, what's being underestimated?]

---

## Recommended Approach

[Step-by-step implementation approach. Be specific enough that a senior engineer can start without a follow-up meeting.]

1. [Step — what to build first and why]
2. [Step]
3. [Step]

**Estimated complexity**: [Small / Medium / Large / XL]
**Estimated effort**: [X engineer-weeks, assuming senior IC]
**Suggested team size**: [N engineers + N design]

---

## Architecture Decisions

For each key decision:

### [Decision: e.g., "Sync vs async digest generation"]
- **Chosen approach**: [approach]
- **Rationale**: [why — performance, simplicity, failure handling]
- **Alternative considered**: [other option and why rejected]

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| [technical risk] | High/Med/Low | High/Med/Low | [specific mitigation] |

---

## Dependencies & Blockers

| Dependency | Owner | Needed by |
|-----------|-------|----------|
| [API contract, schema change, infra] | [team] | [phase] |

---

## What I Want to See in the PR

- [ ] [specific technical requirement — test coverage, error handling, etc.]
- [ ] [specific requirement]
- [ ] [specific requirement]
- [ ] Load test results if this touches a hot path
- [ ] Runbook updated if this adds a new failure mode

---

## Open Technical Questions

1. [Question that needs PM or design input before engineering starts]
2. [Question that needs infrastructure team input]

---

Rules:
- Be specific — "add error handling" is not useful. "Return 409 if digest already exists for this user-week combination" is.
- Flag scope creep: if the ticket implies work that isn't scoped, say so explicitly
- If you'd split this into multiple PRs, describe the PR sequence
- If the estimate seems off, say so and explain why"""


def tech_lead_review(
    input_text: str,
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    print("Tech lead reviewing...\n")
    print("=" * 60)

    result = []
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=2500,
        system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": f"Review the following:\n\n{input_text}"}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print("\n" + "=" * 60)

    if output_file:
        Path(output_file).write_text("".join(result))
        print(f"\nSaved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Tech lead review of a ticket or technical question")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ticket", help="Ticket or feature description as text")
    group.add_argument("--prd", help="Path to PRD file")
    group.add_argument("--question", help="Technical question to answer")
    parser.add_argument("--output", help="Save review to this markdown file")
    args = parser.parse_args()

    if args.ticket:
        content = args.ticket
    elif args.prd:
        content = Path(args.prd).read_text()
        print(f"Loaded PRD from: {args.prd}\n")
    else:
        content = args.question

    tech_lead_review(content, output_file=args.output)


if __name__ == "__main__":
    main()
