# Skill: Continuous Discovery

## Trigger Phrases
- "build an OST"
- "opportunity solution tree"
- "weekly discovery"
- "assumption test"
- "smallest test for"
- "fake door test"
- "smoke test for assumption"
- "what's the riskiest assumption"
- "next discovery questions"
- "continuous discovery"

## Description
Run ongoing discovery — opportunity solution trees, weekly customer interviews, assumption mapping, assumption tests. Use when the user wants to maintain a discovery cadence, build an OST, map assumptions to risks, spec a smoke/fake-door/concierge test before committing to a full build, or feed retro learnings back into the next discovery cycle.

## Behavior

### 1. What Continuous Discovery Is

Teresa Torres's framework rejects big-bang discovery — the quarterly research project that produces a 60-slide deck, shapes a roadmap for a year, and is never revisited. That approach treats discovery as a phase. It isn't. It's a habit.

Continuous discovery means at least one real customer conversation every week, every sprint, indefinitely. The goal is not to validate a solution you've already decided to build. The goal is to map the opportunity space — to understand the problems, desires, and pain points that exist, so the team can make better bets.

The artifact that holds this work together is the Opportunity Solution Tree. It makes your thinking visible, prevents solution fixation, and gives every interview a clear purpose: which node are you trying to update?

---

### 2. The Opportunity Solution Tree (OST)

The OST is a living document, not a deliverable. It reflects your current best understanding of the problem space and the solutions you're considering. Update it after every interview.

**4-level structure:**

```
[Desired Outcome]
  └── Opportunity 1 (pain/desire in user language, grounded in at least 1 quote)
        └── Solution A  →  Experiment: [assumption being tested]
        └── Solution B  →  Experiment: [assumption being tested]
  └── Opportunity 2
        └── Solution C  →  Experiment: [assumption being tested]
  └── Opportunity 3 (undeveloped — need more interviews)
```

**Rules by level:**

| Level | Rule |
|-------|------|
| Desired Outcome | One metric that matters. Not a laundry list. Must be something you can move. |
| Opportunities | Written in user language ("I can't tell if my team is overwhelmed"), not PM language ("lack of workload visibility"). Must be grounded in at least one interview quote. |
| Solutions | Each solution maps to exactly one opportunity. If a solution addresses two opportunities, split it or re-examine your opportunity framing. |
| Experiments | Each experiment tests exactly one assumption. State the assumption, the test method, and the pass/fail threshold before running it. |

**Assumption table (attach to OST):**

| Assumption | Which solution | Confidence (1–5) | Consequence if wrong | Priority |
|------------|---------------|-------------------|----------------------|----------|
| [e.g. Users check workload daily] | Solution A | 2 | High — invalidates entire solution | Test first |
| [e.g. Managers trust automated scores] | Solution A | 3 | Medium — need redesign | Test second |

Priority = lowest confidence × highest consequence if wrong.

---

### 3. Weekly Interview Cadence

**Minimum viable cadence:** 1 customer conversation per week. If you miss a week, it compounds — two weeks of no interviews is a discovery debt you'll feel in the next sprint planning.

**What to bring into each session:**
- Current OST (printed or open on screen)
- Top 3 open questions — the specific nodes you're trying to update
- 2–3 quotes from the last session to probe deeper

**5 questions to ask in every session** (Torres's habit-forming set):
1. "Tell me about the last time you [job this product serves]."
2. "What made that hard?"
3. "What did you do instead?"
4. "How often does this happen?"
5. "What would change for you if that problem went away?"

These are not a script. They're a fallback. Use them when the conversation stalls or drifts.

**After each session — update the discovery log:**

```
## Discovery Log — [Date] — [Participant type/segment]

**Open questions going in:**
1. [Question]
2. [Question]

**New opportunity nodes:**
- "[Quote]" → maps to Opportunity [X] or creates new node

**Assumption confidence updates:**
- [Assumption]: 2 → 4 (they do this manually, confirmed by workflow description)

**Next session questions:**
1. [Follow-up question seeded by this session]
```

---

### 4. Assumption Testing Before the A/B

Never build before you've tested the riskiest assumption with the cheapest method available. The hierarchy:

| Method | Time | Cost | What it tests | Use when |
|--------|------|------|---------------|----------|
| Interview | 1 hour | Near zero | Desirability, frequency, workarounds | Assumption is about behavior or perception |
| Smoke test | 1–3 days | Low | Demand — will users try to get this? | You need click evidence, not just stated intent |
| Fake door | 3–5 days | Low–medium | Willingness to engage before product exists | Testing a specific entry point or CTA |
| Concierge | 1–2 weeks | Medium | Feasibility + value, manually delivered | You need to learn the workflow before automating it |
| A/B test | 2–8 weeks | High | Impact at scale with statistical confidence | Assumption already validated; optimizing a live feature |

**Before running any test, write this down:**
- Assumption being tested: [exact statement]
- Test method: [which method and why]
- Pass threshold: [e.g. "12 of 20 users click 'Join waitlist' without prompting"]
- Fail threshold: [e.g. "fewer than 6 clicks — kill the solution"]
- What changes on the OST if it passes / if it fails

**Connecting results back to the OST:** A passing experiment raises your confidence on that assumption and may unlock the next experiment. A failing experiment either kills the solution (remove from OST) or reveals a misframed opportunity (update the opportunity node with what you learned).

---

### 5. Feeding Retro Findings Back to Discovery

Retros surface what was wrong with your assumptions — that's discovery signal. Don't let it sit in a Confluence page.

**The loop:**
1. Retro identifies a miss: "We shipped X, but users aren't using it because Y"
2. Y becomes a "Next Discovery Question": "Why is Y actually happening? How often? Who is affected?"
3. Questions seed new or revised opportunity nodes on the OST
4. Next week's interview uses those nodes as the open questions going in

**How to prioritize what to investigate first:**

Use the assumption table. Reprioritize after the retro by asking: which assumption, if we'd tested it earlier, would have changed our decision? Those are your highest-priority discovery questions for the next cycle.

**Retro-to-discovery hand-off table:**

| Retro finding | Type (miss/surprise/confirmation) | Next discovery question | Target OST node | Owner | By when |
|---------------|----------------------------------|------------------------|-----------------|-------|---------|
| [e.g. Managers didn't adopt digest because they use Slack, not email] | Miss | How do managers prefer to receive async summaries? | Opportunity: digest delivery | [PM] | Next interview |
| [e.g. Power users found workaround we didn't anticipate] | Surprise | What need is the workaround serving? | New node TBD | [PM] | Sprint +1 |

Fill this table at the end of every retro. It is the input to the next weekly interview session.
