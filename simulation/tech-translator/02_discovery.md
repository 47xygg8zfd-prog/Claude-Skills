# Discovery Brief: Bridge — Technical Translator for PMs

**Author**: PM, Bridge  
**Date**: 2026-05-13  
**Status**: Active Discovery — Interviews in Progress  
**Linked strategy doc**: `01_strategy.md`

---

## Problem Statement

PMs routinely block engineering teams because they don't understand what engineers are saying — or say the wrong thing in response. The gap isn't intelligence, it's vocabulary and context. A PM who confidently writes "just add caching" in a ticket comment, or who hears "we need to refactor the service boundary" and nods along without understanding the implication, creates downstream confusion that costs the whole team time.

### Specific Evidence (Pre-Discovery Signal)

The following data points were gathered from public surveys, analyst reports, and informal PM community interviews conducted in Q1 2026 before formal discovery began. They are directional, not definitive.

| Signal | Stat | Source |
|--------|------|--------|
| Sprint planning vocabulary gaps | **63%** of sprint planning meetings include at least one moment where the PM asks an engineer to explain or re-explain a technical term | Product Ops Community survey, n=214, Feb 2026 |
| Weekly translation tax | Engineers estimate **4.2 hours/week** spent on "translation work" — explaining concepts to PMs, rewriting tickets that reflect a technical misunderstanding, or correcting assumptions in async Slack threads | Informal Slack community poll, Product Engineering Slack, n=87, Jan 2026 |
| Decision reversals with technical root cause | **41%** of product decisions that were significantly revised or walked back within a sprint had a technical misunderstanding identified as a contributing root cause by the engineering lead | Bridge founder interviews with 18 engineering leads, Q4 2025 |
| PM self-reported confidence | Only **29%** of PMs with fewer than 3 years of experience working with engineering teams describe themselves as "confident" when a technical trade-off is discussed in a meeting they're running | Product School survey, n=611, 2025 |
| Current workarounds | **74%** of PMs report using ChatGPT or Google at least once per week to decode a technical term or concept from a Slack message or ticket comment | Bridge founder survey, n=44 PMs, Q1 2026 |

### The Compounding Effect

The problem is not just one misunderstood term. Vocabulary gaps compound: a PM who doesn't understand the difference between synchronous and asynchronous processing writes a ticket that assumes synchronous behavior. The engineer builds to spec, the PM sees the demo and says "wait, why does it lag?" — and the sprint point is lost. The engineer's frustration is not that the PM was wrong; it's that this was entirely preventable, and it happens every other sprint.

---

## Opportunity Hypothesis

**Primary hypothesis**: If a PM can get a reliable, context-aware explanation of a technical concept or trade-off in under 60 seconds — without leaving their current tool (Jira, Linear, Slack) — they will make fewer specification errors, ask better questions in sprint planning, and reduce the back-and-forth that currently costs engineering teams 4+ hours per week.

**Secondary hypothesis**: PMs who use Bridge regularly will develop a persistent, growing vocabulary that reduces their dependence on real-time explanations over time — creating a compounding value loop that increases retention.

**Monetization hypothesis**: Willingness to pay sits with the PM's manager (engineering manager or Head of Product) who experiences the downstream cost of PM-engineer miscommunication as wasted sprint capacity. The PM is the user; the manager is the economic buyer. Pricing should reflect team-level value, not individual-seat value.

---

## Assumptions Ranked by Risk

Assumptions are ranked High / Medium / Low by risk = (likelihood of being wrong) × (impact if wrong).

| # | Assumption | Risk | What would invalidate it |
|---|-----------|------|--------------------------|
| 1 | PMs will reach for Bridge in the moment of confusion rather than defaulting to ChatGPT or asking a teammate | **High** | If habit formation requires more than 2 weeks, or if the Jira/Slack integration has any friction (OAuth errors, slow load), PMs will fall back to existing workarounds |
| 2 | Context-aware explanations (grounded in the specific ticket or message) are meaningfully more useful than generic definitions | **High** | If PMs report that a generic explanation would have been sufficient, Bridge's core differentiation disappears and we're competing with ChatGPT on convenience alone |
| 3 | The engineering manager is willing to pay for a tool that the PM, not the engineer, uses | **High** | If the buyer perceives this as a "PM upskilling" tool rather than an "engineering productivity" tool, the value framing is wrong and sales cycles will stall |
| 4 | LLM explanations will be accurate enough, often enough, that PMs trust them in high-stakes moments (sprint planning, design reviews) | **Medium** | If PMs use Bridge for low-stakes questions only (Slack DMs, personal curiosity) but revert to asking a human for anything consequential, the DAU metric will be misleading |
| 5 | PMs want to reduce their dependence on the "technical PM friend" — they see reliance on a single person as a risk | **Medium** | If PMs are satisfied with the informal network and don't feel the single-point-of-failure risk acutely, the urgency to adopt a tool is lower |
| 6 | The vocabulary gap is consistent enough across PM backgrounds that one product can serve all of them | **Low** | If PMs from engineering backgrounds need fundamentally different content than PMs from design or business backgrounds, personalization costs may exceed Series A budget |
| 7 | Jira and Linear APIs support the context-fetching we need without rate-limiting at our target usage | **Low** | Engineering feasibility check; mitigatable with caching, but must be confirmed before build |

---

## Questions to Answer Before Building

### Must-answer (no-build without these)
1. In what specific workflow moment does the vocabulary gap cause the most pain — sprint planning, ticket writing, Slack async, or design review? (Determines where the integration must live.)
2. How much context does a PM actually have when the confusion occurs — do they have the ticket open, or are they in a meeting? (Determines whether integration-based context fetching is sufficient or whether the PM needs to paste text.)
3. What does "a good explanation" look like to a PM — a definition, a trade-off summary, a "here's how to respond" script, or something else? (Determines output format and prompt architecture.)
4. Who makes the buying decision — the PM, the Head of Product, or the Engineering Manager? What do they need to see to approve a $25/seat/month expense?

### Should-answer (strong-to-have before sprint 1)
5. Are there technical domains where PMs feel more lost than others (e.g., infrastructure and devops vs. frontend vs. data engineering)? (Prioritizes content coverage and model fine-tuning.)
6. How do PMs currently signal confusion in meetings — do they ask questions, or do they stay silent and figure it out later? (Determines whether real-time vs. async is the higher-value surface.)
7. Do PMs feel embarrassed about not understanding technical concepts? Does the shame dynamic affect when and how they'd use a tool like Bridge? (Determines whether the product should be private/invisible or social/shared.)

### Nice-to-know (inform V2 roadmap)
8. Is there a pattern in the types of decisions that get walked back due to technical misunderstanding — e.g., performance-related, security-related, data architecture? (Informs content prioritization for V2.)
9. Do engineering leads want visibility into the explanations their PM is receiving — as a coaching tool or a trust-builder? (Informs whether a manager-facing dashboard belongs on the roadmap.)

---

## Scope Recommendation

Based on pre-discovery signal, the recommended scope for discovery is:

**Interview target**: 12–15 PMs across mid-market B2B SaaS companies, 50–500 employees, team size 5–25 engineers, mix of Jira and Linear shops. Minimum 4 PMs with non-technical backgrounds (design, marketing, business). Minimum 2 PMs who describe themselves as "technical PMs" — to understand where the ceiling of existing fluency sits.

**Exclude from discovery interviews**: PMs at developer-tool companies; PMs with software engineering degrees who write code regularly; PMs at companies with fewer than 5 engineers (the communication dynamic is too different).

**Supplemental research**:
- 2 shadowing sessions in live sprint planning meetings (with consent) to observe vocabulary gaps in real time rather than via recall
- Competitive audit of: ChatGPT, Notion AI, Tettra, Guru, and any PM-focused AI tools launched in the last 12 months
- 3 engineering lead interviews to validate the "translation tax" estimate and understand their perspective on PM vocabulary gaps

**Out of scope for discovery**: Customer journey mapping, pricing research, technical architecture review. These follow green light.

---

## Recommended Next Step

Schedule 12 PM interviews over 2 weeks (6 per week). Use the following screener:
- Works as a PM at a B2B SaaS company, 50–500 employees
- Team includes at least 5 engineers they work with directly
- Uses Jira, Linear, or GitHub Issues to track sprint work
- Has been in the PM role for at least 6 months

Run a 45-minute semi-structured interview. First 20 minutes: storytelling ("tell me about a time a technical discussion in a meeting didn't go the way you expected"). Last 25 minutes: specific workflow questions targeting the must-answer list above.

Synthesis deadline: 5 business days after final interview. Green light decision meeting scheduled for the Friday of week 2.
