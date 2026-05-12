# PRD: TechBridge — PM Technical Fluency Platform
**Status**: Draft | **Date**: 2026-05-12

## Problem Statement

Product managers at B2B SaaS companies regularly feel technically outmatched in engineering conversations — unable to evaluate estimates, contribute to design reviews, or write requirements that engineers trust. Existing learning tools (Codecademy, bootcamps) teach programming, not PM-engineering collaboration. The gap is context-specific: PMs need technical fluency in their workflows, not the ability to code. This erodes PM-engineer trust, slows decision-making, and limits PM career growth.

## Goals & Success Metrics

| Goal | Metric | Baseline | Target |
|------|--------|----------|--------|
| PMs feel more confident in technical conversations | Self-reported confidence score (1–5) | 2.3 (survey) | 3.8 at 30 days |
| PMs use TechBridge in their actual workflow | Weekly active users | 0 | 40% of signups WAU at 8 weeks |
| Product retains PMs past the novelty phase | 8-week retention | 0 | 55% |
| Engineering managers notice the difference | EM satisfaction with PM technical fluency | [NEEDS BASELINE: EM survey] | +1 point on 5-pt scale |

## Non-Goals

- We are not building a coding bootcamp or teaching PMs to write production code
- We are not building team-level analytics or manager dashboards in v1
- We are not integrating with GitHub, Jira, or Linear in v1
- We are not issuing certifications or badges in v1

## User Stories

1. As a **mid-level PM**, I want to **understand what an engineer means when they say "we need to refactor the auth layer"**, so that **I can ask the right questions and make an informed trade-off decision**.
2. As a **PM preparing for an architecture review**, I want to **get a plain-language briefing on the system components being discussed**, so that **I can participate meaningfully rather than just listening**.
3. As a **senior PM**, I want to **know whether a 3-sprint estimate is reasonable for a given feature**, so that **I can advocate for the right scope with stakeholders without undermining my engineers**.
4. As a **PM writing acceptance criteria**, I want **guidance on what technical details to include**, so that **engineers don't need to come back to me with clarifying questions**.
5. As a **junior PM new to the team**, I want **a guided path through the technical concepts most relevant to my product area**, so that **I can onboard faster and feel credible sooner**.

## Requirements (MoSCoW)

**Must have**:
- Contextual explanation engine: PM pastes in a Slack message, design doc excerpt, or ticket description and gets a plain-language explanation of the technical content
- Concept library: 50+ PM-specific technical concepts explained in PM terms (not developer terms) — e.g., "what is a database index and why does your engineer care about it"
- Workflow guides: step-by-step guides for the 5 most common technically-heavy PM workflows (sprint estimation, architecture review, incident debrief, technical debt triage, writing technical requirements)
- Mobile-friendly web app (PMs read on their phones before meetings)

**Should have**:
- "Before this meeting" prep mode: PM describes the meeting (e.g., "architecture review for new auth system") and gets a 5-minute prep brief
- Saved concepts: PMs can bookmark explanations for review
- Confidence tracker: simple self-reported before/after confidence score per concept

**Could have**:
- Community Q&A: PMs ask questions and get answers from a moderated PM community
- "Explain this to a non-technical stakeholder" reverse mode: PM understands something technical and wants help explaining it up
- Team invites: PM invites their engineering manager to see the prep briefs they're generating

**Won't have**:
- Coding exercises or assessments
- Integration with engineering tools (v1)
- Certification or credentialing

## Open Questions

1. **Where does the content come from?** Claude-generated with PM editorial review, or human-written by former engineers who became PMs? Answer affects quality, cost, and scalability. Owner: CPO. Target: before design starts.
2. **Freemium vs. paid-only?** If PMs pay personally, price sensitivity is high. If companies buy, we need a team/admin layer we're not building in v1. Owner: CEO + PM. Target: before launch.
3. **How do we measure "technical fluency improvement" honestly?** Self-reported confidence scores are gameable. Behavioral proxy (frequency of technical questions asked, PM-written requirement quality) is better but harder. Owner: Data Science. Target: before instrumentation is built.

## Dependencies

| Dependency | Team | Status |
|-----------|------|--------|
| Claude API access for explanation engine | Platform | Confirmed |
| Content review process for concept library | Editorial / PM | TBD — needs resourcing |
| Design system availability | Design | Confirmed — use existing |
