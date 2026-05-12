# Discovery Brief: TechBridge — PM Technical Upskilling

## Problem Statement

Product managers at B2B SaaS companies regularly describe feeling like outsiders in technical conversations — unable to challenge engineering estimates, contribute meaningfully to architecture discussions, or independently triage technical debt trade-offs. The available learning paths (bootcamps, online courses) teach programming, not product-engineering collaboration. The gap isn't coding ability; it's technical fluency in PM-specific contexts. This blocks career growth, damages PM-engineer trust, and slows product decisions.

## Opportunity Hypothesis

If we build a contextual technical learning tool designed specifically for PM workflows — reading diffs, understanding system diagrams, estimating complexity, translating technical decisions into business language — then PMs will feel more effective in their roles and engineering teams will collaborate more fluidly with them, because the gap is context-specific, not a general coding problem.

## Assumptions Ranked by Risk

| Assumption | Risk if wrong | How to test |
|-----------|--------------|------------|
| PMs feel blocked by technical gaps in their current job (not just abstractly interested in learning) | Core market doesn't exist — they want this but don't feel urgency | Discovery interviews: ask about the last time a technical gap caused a specific work problem |
| PMs will spend time on this during the workday, not just as personal development | Product must compete for leisure time, not work time — much harder acquisition | Ask directly: "Where would this live in your week?" |
| Engineering managers care about PM technical fluency and would advocate for the tool | No bottom-up distribution channel through eng; reliant solely on PM-direct | Interview EMs: "How does your PM's technical understanding affect your team?" |
| PMs can't get this from their own engineers informally | Existing informal learning is sufficient; no gap to fill | Ask: "How do you currently learn technical concepts? What's missing from that?" |
| Willingness to pay exists at a company level (not just individual) | Individuals love it, no budget path — stays a side project | Probe: "Would your company pay for this? Who holds that budget?" |

## Questions to Answer Before Building

1. **What specific PM workflow creates the most pain?** (PR review? Sprint planning? Architecture review? Writing technical requirements?) — Interview question: "Walk me through the last time a technical conversation went badly for you."
2. **What does "technical enough" look like from an engineering manager's perspective?** — EM interview: "What does a technically fluent PM do differently in your experience?"
3. **What have PMs already tried and why did it fail?** — "Have you ever tried to get more technical? What happened?"
4. **Is this a junior PM problem, a senior PM problem, or both?** — Affects positioning and pricing entirely
5. **Pull vs. push learning**: Do PMs want to study proactively, or do they want contextual help when they're already in a technical conversation?

## Scope Recommendation

- **In scope**: Contextual technical explanations tied to real PM workflows; a "read this PR" or "understand this architecture" guided experience; a library of PM-specific technical concepts (not a full programming course)
- **Out of scope for v1**: Certifications, assessments, team-level analytics, integration with specific engineering tools (Jira, GitHub)

## Recommended Next Step

Conduct 8 discovery interviews: 5 with PMs at B2B SaaS companies (mix of junior/senior), 3 with engineering managers who work closely with PMs. Focus on specific incidents, not opinions. Target completion within 2 weeks before PRD is written.
