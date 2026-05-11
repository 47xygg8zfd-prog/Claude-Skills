"""
Engineering Team Orchestrator
Takes a ticket or PRD and runs all four engineering specialists in sequence:
tech lead → backend → frontend → QA. Each specialist's output feeds the next.

Usage:
    python eng_team.py --ticket "build the weekly digest email service"
    python eng_team.py --prd prd.md --output-dir ./digest-eng/
    python eng_team.py --ticket "..." --role backend   # run a single specialist
"""

import anthropic
import argparse
from pathlib import Path


client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

ROLES = ["tech_lead", "backend", "frontend", "qa"]

SYSTEM_PROMPTS = {
    "tech_lead": """You are a staff-level tech lead doing an initial ticket review.

Produce a concise tech lead brief (not a full architecture doc — that comes later):

# Tech Lead Brief: [Feature]

## Complexity Assessment
**Size**: Small / Medium / Large / XL
**Effort**: [X engineer-weeks]
**Risk**: Low / Medium / High — [one sentence on the biggest risk]

## Recommended Approach
[3-5 bullet points on the implementation strategy. Enough for backend and frontend to plan independently.]

## Key Decisions Made
- [Decision]: [rationale]
- [Decision]: [rationale]

## What Backend Owns
[Specific list — APIs, services, data model changes]

## What Frontend Owns
[Specific list — components, flows, API integration]

## Shared Concerns
- [Authentication / authorization approach]
- [Error handling contract between frontend and backend]
- [Analytics events to fire and where]

## Definition of Done
- [ ] [Technical requirement]
- [ ] [Technical requirement]
- [ ] All tests green, no regressions""",

    "backend": """You are a senior backend engineer given a ticket and tech lead brief.

Produce a focused backend implementation plan:

# Backend Plan: [Feature]

## Scope
[What backend is building — 2-3 bullets]

## API Contracts

For each endpoint:
`[METHOD] /api/v1/[path]` — [one-sentence purpose]
- Request: `{ [field]: [type] }`
- Response: `{ [field]: [type] }`
- Errors: 400 ([condition]), 404 ([condition]), 500 (log + safe message)

## Data Model Changes

```sql
-- New table or ALTER TABLE
[SQL]
```

## Core Logic (step-by-step)
1. [Validate input]
2. [DB operation]
3. [Business logic]
4. [Side effect — event, email, cache bust]
5. [Return response]

## Error & Resilience
- [Failure scenario]: [behavior]
- Idempotency: [is this endpoint safe to call twice?]

## Test Cases
- [happy path]: expect [result]
- [edge case]: expect [result]
- [error case]: expect [status + message]

## Implementation Order
1. Migration
2. Repository / service layer
3. Controller / route
4. Tests""",

    "frontend": """You are a senior frontend engineer given a ticket and backend API contracts.

Produce a focused frontend implementation plan:

# Frontend Plan: [Feature]

## Component Tree
```
<[FeatureRoot]>
  ├── <[ComponentA]>   ← new
  └── <[ComponentB]>   ← modified
```

## Key Components

For each new component:
**`<[ComponentName]>`** — [one-line responsibility]
- Props: `{ [prop]: [type] }`
- States: loading | empty | error | populated
- On [event]: [behavior]

## API Integration

Hook: `use[Feature]()` in `src/hooks/`
- Fetches: `GET /api/v1/[path]`
- Mutates: `POST /api/v1/[path]`
- Error handling: [toast / inline / redirect]

## State Management
**Approach**: [local / Context / store]
**Why**: [one sentence]

## Accessibility
- Keyboard: [tab order, focus management]
- ARIA: [labels and roles needed]

## Implementation Order
1. Static component (hardcoded data)
2. Hook + real API
3. Error / loading / empty states
4. Accessibility
5. Tests""",

    "qa": """You are a senior QA engineer given a feature spec and implementation plans.

Produce a focused test plan:

# QA Test Plan: [Feature]

## P0 Test Cases (blocking)

| TC | Scenario | Steps (abbreviated) | Expected |
|----|---------|-------------------|---------|
| TC-01 | Happy path | [key steps] | [result] |
| TC-02 | [Critical error] | [trigger] | [safe behavior] |

## P1 Test Cases (high priority)

| TC | Scenario | Expected |
|----|---------|---------|
| TC-03 | [Edge case] | [result] |
| TC-04 | [Concurrent action] | [result] |

## Regression Checks
- [ ] [Adjacent feature]: [specific thing to verify]
- [ ] [Adjacent feature]: [specific thing to verify]

## Accessibility Checks
- [ ] Keyboard-only navigation completes main flow
- [ ] Screen reader announces [key state change]

## Go/No-Go
**Ship when**: All P0 pass, all P1 pass or documented, no data-loss bugs
**Block when**: Any P0 failure, any data loss""",
}


def run_specialist(role: str, content: str) -> str:
    system = SYSTEM_PROMPTS[role]
    label = role.replace("_", " ").upper()

    print(f"\n{'━' * 60}")
    print(f"  SPECIALIST: {label}")
    print(f"{'━' * 60}\n")

    result = []
    with client.messages.stream(
        model=MODEL,
        max_tokens=2000,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": content}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print()
    return "".join(result)


def run_eng_team(
    ticket: str,
    role_filter: str | None = None,
    output_dir: str | None = None,
) -> None:
    roles_to_run = [role_filter] if role_filter else ROLES
    outputs: dict[str, str] = {}

    print(f"\nEngineering Team starting — {len(roles_to_run)} specialist(s)\n")

    for role in roles_to_run:
        if role == "tech_lead":
            content = f"Ticket / feature:\n\n{ticket}"
        elif role == "backend":
            tl = outputs.get("tech_lead", "")
            content = f"Ticket:\n{ticket}\n\nTech lead brief:\n{tl}"
        elif role == "frontend":
            tl = outputs.get("tech_lead", "")
            be = outputs.get("backend", "")
            content = f"Ticket:\n{ticket}\n\nTech lead brief:\n{tl}\n\nBackend API contracts:\n{be}"
        elif role == "qa":
            combined = "\n\n".join(
                f"[{r.upper()}]\n{outputs[r]}" for r in outputs if outputs[r]
            )
            content = f"Ticket:\n{ticket}\n\nImplementation plans:\n{combined}"
        else:
            content = f"Ticket:\n{ticket}"

        result = run_specialist(role, content)
        outputs[role] = result

        if output_dir:
            out_path = Path(output_dir)
            out_path.mkdir(parents=True, exist_ok=True)
            (out_path / f"{role}.md").write_text(result)
            print(f"\n  → Saved to {out_path / f'{role}.md'}")

    print(f"\n{'━' * 60}")
    print(f"  Engineering Team complete — {len(roles_to_run)} specialist(s) run")
    if output_dir:
        print(f"  Outputs saved to: {output_dir}")
    print(f"{'━' * 60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Run the full engineering team on a ticket (tech lead → backend → frontend → QA)"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ticket", help="Ticket or feature description as text")
    group.add_argument("--prd", help="Path to PRD file")
    parser.add_argument(
        "--role",
        choices=ROLES,
        help="Run a single specialist instead of the full team",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save each specialist's output as a markdown file",
    )
    args = parser.parse_args()

    if args.ticket:
        ticket = args.ticket
    else:
        ticket = Path(args.prd).read_text()
        print(f"Loaded PRD from: {args.prd}\n")

    run_eng_team(ticket, role_filter=args.role, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
