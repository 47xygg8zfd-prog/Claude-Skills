# Project Constitution — [Project Name]

> **What this is**: A set of immutable principles every agent on this project reads before
> producing output. Fill this in before running the planning orchestrator. Once set,
> these rules override any agent's default behavior. Changing them mid-project requires
> a deliberate decision and a note in the change log below.

---

## Project Identity

**Project name**: [Name]
**One-line description**: [What it does and who it's for]
**Primary user**: [Specific role/persona — not "users", be precise]
**Core job to be done**: [When [situation], I want to [action], so I can [outcome]]

---

## Non-Negotiable Constraints

> Things that cannot change regardless of what any agent recommends.
> If a constraint conflicts with a requirement, the constraint wins.

- [ ] **Stack**: [e.g., Python + FastAPI backend; React frontend; Postgres; no new infrastructure]
- [ ] **Timeline**: [e.g., MVP must be shippable in 6 weeks with a 2-person team]
- [ ] **Budget**: [e.g., infra cost must stay under $500/month at launch]
- [ ] **Compliance**: [e.g., GDPR; SOC 2 Type II; no PII stored without explicit consent]
- [ ] **Integrations**: [e.g., must connect to Jira + GitHub; Slack is optional]
- [ ] **Out of scope**: [e.g., no mobile app; no org-level rollup; no write-back to Jira]

---

## Definition of Done

A feature is "done" when:
1. [ ] Acceptance criteria pass (Given/When/Then)
2. [ ] Unit tests written and passing
3. [ ] No new P0/P1 bugs introduced
4. [ ] Docs updated (if user-facing)
5. [ ] [Add any project-specific criteria]

---

## Quality Bar

**Performance**: [e.g., P95 API response < 500ms; page load < 2s on 4G]
**Reliability**: [e.g., 99.5% uptime; no data loss on failure]
**Security**: [e.g., OWASP Top 10 addressed; no secrets in code; least-privilege IAM]
**Accessibility**: [e.g., WCAG 2.1 AA; keyboard navigable]

---

## Terminology

> Define terms once here so every agent uses them consistently.

| Term | Definition |
|------|-----------|
| [term] | [exact meaning in this project] |
| [term] | [exact meaning in this project] |

---

## Team

| Role | Name | Decision authority |
|------|------|-------------------|
| PM / Driver | [name] | Owns requirements and prioritization |
| Tech Lead | [name] | Owns architecture decisions |
| Designer | [name] | Owns UX and design system |
| QA | [name] | Owns test strategy and release criteria |

---

## Change Log

> Record any changes to this constitution here. Agents treat prior decisions as settled.

| Date | Change | Reason | Decided by |
|------|--------|--------|-----------|
| [date] | Initial constitution | Project kickoff | [name] |
