# Skill: Roadmap

## Trigger Phrases
- "build a roadmap"
- "roadmap for Q3"
- "sequence these features"
- "what should we build when"
- "roadmap tradeoffs"
- "capacity planning"
- "what if we delay"
- "prioritize the roadmap"

## Description
Build and maintain product roadmaps. Use when the user needs to produce a quarterly roadmap, sequence features against OKRs, allocate capacity across teams, model "what-if" scenarios (what if we delay X?), or communicate roadmap tradeoffs to stakeholders.

## Behavior

### The Four Roadmap Questions (always answer all four)

Every roadmap output must address:
1. **What are we trying to achieve?** — link to OKRs; if there's no OKR, there's no roadmap item
2. **What are we building?** — named features with requirement IDs, not vague themes
3. **When are we building it?** — time-boxed quarters or explicit "not yet" with criteria
4. **What are we NOT building?** — a roadmap without a "no" list is a wish list

---

### Mode 1: Quarterly Roadmap

Produce a table. Every row must have a value in every column — blanks signal a feature that isn't ready to be on the roadmap.

| Quarter | Theme | Features (Req IDs) | Teams | Capacity (pts) | OKR | Gate to Advance |
|---------|----|-----|-----|--------|-----|------|
| Q1 | [Theme] | [Feature — REQ-001] | [Eng, Design] | [N pts] | [OKR KR] | [e.g., discovery complete] |

**Capacity rules**: Use the team's known velocity from CLAUDE.md. Never assign more than 80% of capacity to roadmap items — leave 20% for bugs, tech debt, and unplanned work.

After the table, add a **Not Building (This Quarter)** section: features that were considered and explicitly deferred, with a one-sentence reason for each.

---

### Mode 2: Now / Next / Later

Use this format when dates are uncertain or the team needs a horizon-based view rather than hard quarters.

| Column | Who it's for | What goes here |
|--------|-------------|----------------|
| **Now** | Active sprint / current quarter | Committed, resourced, in-flight |
| **Next** | Following quarter | Validated, sequenced, team aware |
| **Later** | Beyond that | Directional, not committed |

For each feature include: feature name, OKR it serves, and a **why now/next/later** rationale (one sentence). "Later" is not a graveyard — every item there must have explicit criteria for what would move it to Next.

---

### Mode 3: Scenario Modeling ("What if we delay X?")

When asked to model a delay or scope change, produce:

**Scenario: Delay [Feature X] by [N quarters]**

| Dimension | Impact |
|-----------|--------|
| OKR impact | Which KRs slip and by how much |
| Dependency impact | What other features or teams are blocked |
| Capacity freed | What else could be pulled forward |
| Risk | What gets worse if we wait |
| Recommendation | Ship on time / delay / descope / split |

State the recommendation directly. Don't hedge — the PM can override it, but give a clear starting position.

---

### Roadmap Quality Rules

- Every feature must trace to an OKR. No OKR = no roadmap slot.
- No feature ships without a "why now" rationale. "We've talked about this for a while" is not a rationale.
- Capacity is always constrained. If the roadmap requires more than available velocity, flag the overload explicitly and ask which items to cut or defer.
- "Later" items must have written advancement criteria, not just good intentions.
- A roadmap that can't say no is not a strategy — it's a backlog sorted by who asked loudest.

## Output Style
- Tables first, narrative below
- Flag capacity overloads and missing OKR links as explicit warnings, not footnotes
- When modeling tradeoffs, quantify impact on KRs wherever possible

## Customization Tips
- Add your sprint velocity and team composition from CLAUDE.md so capacity is auto-populated
- Add your OKRs to CLAUDE.md so every roadmap item is automatically checked against them
- Specify your preferred roadmap horizon (quarterly, semi-annual, rolling 6-week)
