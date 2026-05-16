# Pulse Product Roadmap

> **Forward-looking statement**: This roadmap reflects current plans and priorities and is subject to change. Items in the `exploring` and `in design` phases may be significantly altered or dropped. Nothing here is a commitment to ship.

**Last updated**: Q2 2026  
**North star**: Digest-active WAU → 52% (from 38%)  
**Tracking**: Features move left-to-right through phases. Click any item for the full spec.

---

## How to Read This

| Label type | Values |
|-----------|--------|
| **Phase** | `exploring` → `in design` → `preview` → `beta` → `ga` |
| **Quarter** | `Q2-2026` `Q3-2026` `Q4-2026` `future` |
| **Area** | `digest` `onboarding` `analytics` `integrations` `admin` `platform` |
| **Plan** | `starter` `team` `enterprise` |

Items are listed under their *current* phase. Quarter labels show *target GA quarter*, not when the work starts.

---

## Exploring

> Early signal gathering. No spec exists yet. May not ship.

---

**Mobile digest push notification**
`exploring` · `Q4-2026` · `digest` · `team` `enterprise`

Engineering managers are often away from their desk on Monday morning. A native push on iOS/Android could increase digest open rate by surfacing the summary without requiring email open. Exploring whether the open-rate delta justifies a native app investment.

*Questions we're answering*: Does low open rate reflect email-channel fatigue or timing? Would push notifications cannibalize email opens or add net new engagement? What's the build cost vs. a deep-link from email?

---

**Org-level rollup view**
`exploring` · `future` · `analytics` · `enterprise`

Directors managing 4+ teams have no way to see cross-team health without context-switching between individual manager views. This would be Pulse's first multi-team surface. Significant scope — requires a new data model and a new persona (director vs. manager).

*Known constraint*: This is explicitly out of scope for our ICP (team-scoped, not org-scoped). Only pursuing if enterprise expansion becomes a Q3 strategic priority.

---

**Slack digest delivery**
`exploring` · `Q3-2026` · `digest` · `integrations` · `team` `enterprise`

Some managers don't use email as a primary work surface. A Slack DM version of the weekly digest could improve open rate among Slack-native orgs. Exploring whether this fragments engagement or grows it.

---

## In Design

> Spec in progress. Eng has not started. Designs may exist.

---

**Digest personalization — signal weighting**
`in design` · `Q2-2026` · `digest` · `team` `enterprise`

Currently the digest surfaces the same four signals for every manager. Research shows managers differ in what they act on — some prioritize PR cycle time, others focus on blocked engineers. This feature lets managers reorder or suppress digest sections based on their role and team context.

*Design question*: Explicit preference-setting (settings screen) vs. implicit learning from click behavior. Leaning toward explicit for v1 to avoid cold-start problem.

*Success gate*: Insight click-through rate +8pp within 4 weeks of enabling personalization.

---

**Onboarding checklist — guided first week**
`in design` · `Q2-2026` · `onboarding` · `starter` `team` `enterprise`

TTV is 8 days. Target is 3. Root cause: managers connect tools but don't know what to look at first. A guided checklist (connect Jira → view first sprint report → set your team baseline → receive first digest) should compress time-to-first-insight.

*Constraint*: Checklist must be dismissible after step 2 — we've seen in research that forced flows create drop-off rather than reduce it.

*Owner*: Jordan (PM), Priya (design), 1 FE

---

**Sprint predictability trend card**
`in design` · `Q3-2026` · `analytics` · `team` `enterprise`

Managers ask "are we getting more or less predictable over time?" but today Pulse only shows the current sprint's predictability ratio. A 4-sprint trend line with a plain-English interpretation ("your team is improving — 3 of the last 4 sprints hit plan") would be a high-value addition to the digest.

---

## Preview

> Feature is live for a subset of accounts. Gathering signal before broad rollout.

---

**Digest recommendation engine v2**
`preview` · `Q2-2026` · `digest` · `team` `enterprise`

Upgraded the recommendation logic from rule-based to model-based. V2 surfaces the most actionable recommendation per manager based on their team's current pattern — not just the most-recently-triggered rule. In preview with 8 enterprise accounts since April 28.

*Current signal*: Recommendation action rate 14% → 22% in preview cohort (target: 20%). On track.

*Rollout plan*: GA after 3 more weeks of preview if action rate holds above 20% with no guardrail degradation.

---

**GitHub PR aging alert**
`preview` · `Q2-2026` · `integrations` · `starter` `team` `enterprise`

PRs open for 5+ days surface in the digest with the author and age. In preview with 12 accounts since May 5. Early signal: managers who see the alert resolve the PR within 48 hours 67% of the time.

*Open issue*: False-positive rate on draft PRs is ~18%. Filtering draft PRs before GA.

---

## Beta

> Feature is available to all accounts that opt in. Approaching GA quality.

---

**Custom digest schedule**
`beta` · `Q2-2026` · `digest` · `team` `enterprise`

Managers can now change their digest delivery day/time. Default remains Monday 7am. Beta since April 14 with 34 accounts opted in. Unsubscribe rate unchanged. Engineering managers at companies with Friday sprint closes are scheduling for Monday EOD.

*GA criteria*: 4 more weeks of stability + support ticket volume < 2 per week related to schedule changes.

---

**Jira custom workflow support**
`beta` · `Q2-2026` · `integrations` · `team` `enterprise`

Teams using non-standard Jira workflows (custom columns, sub-task-as-story patterns) previously required manual configuration. Beta adds auto-detection of workflow structure and maps it to Pulse's sprint model without manual setup.

*Known gap*: 3-level hierarchy (Epic → Story → Sub-task as Story) still requires manual override. Targeting fix before GA.

---

## GA — Q2 2026

> Shipped to all eligible accounts. No further changes unless a bug is found.

---

**Weekly digest v1**  `ga` · `Q1-2026` · `digest` · `starter` `team` `enterprise`

Monday morning email summary: sprint predictability trend, top open PRs by age, blocked/idle engineer flags, one prioritized recommendation. Shipped to 100% of accounts March 3, 2026.

*Outcome*: Digest-active WAU +11pp (38% → 49%). Open rate 73% (target: 75%). 30-day retention 64% → 76%.

---

**Slack integration — team health alerts**  `ga` · `Q1-2026` · `integrations` · `team` `enterprise`

Real-time Slack DM when a team health threshold is breached (e.g., 3+ engineers with no commits for 2 days; sprint scope increase >20%). Shipped February 10, 2026.

---

**SSO / SAML**  `ga` · `Q1-2026` · `admin` · `enterprise`

SAML 2.0 support with Okta, Azure AD, and Google Workspace. Required for enterprise procurement. Shipped January 22, 2026.

---

## Roadmap by Quarter

| Feature | Phase | Q2-2026 | Q3-2026 | Q4-2026 |
|---------|-------|:-------:|:-------:|:-------:|
| Digest personalization | In Design | GA | | |
| Onboarding checklist | In Design | GA | | |
| Recommendation engine v2 | Preview | GA | | |
| GitHub PR aging alert | Preview | GA | | |
| Custom digest schedule | Beta | GA | | |
| Jira custom workflow | Beta | GA | | |
| Sprint predictability trend | In Design | | GA | |
| Slack digest delivery | Exploring | | Preview | GA |
| Mobile push notification | Exploring | | | Preview |
| Org-level rollup | Exploring | | | Exploring |

---

## What We're Not Building (and Why)

| Request | Decision | Rationale |
|---------|----------|-----------|
| Executive dashboard / org rollup | No — this quarter | Out of ICP. Directors are not our buyer. Would dilute manager-first focus. Revisit if enterprise motion expands. |
| Mobile app | No — this year | Open rate problem is timing + channel, not device. Solving with push notifications first (exploring). Native app is a 6-month build for uncertain lift. |
| Two-way Jira write-back | No | Creates liability for incorrect writes. Pulse is read-only on purpose — we surface, we don't mutate. |
| Team mood / sentiment surveys | Deprioritized | Legal and HR risk in some jurisdictions. Not differentiated from existing survey tools. |
| Public API | Q4-2026 or later | Enterprise demand is real but premature. Shipping one integration (Slack, GitHub, Jira) properly beats a general API shipped half-baked. |

---

## Labels Reference

### Release Phases

| Phase | Meaning |
|-------|---------|
| `exploring` | Signal gathering. No commitment. May not ship. |
| `in design` | Spec in progress. Eng not yet started. |
| `preview` | Live for select accounts. Gathering signal. |
| `beta` | Available to all opt-in accounts. Approaching GA quality. |
| `ga` | Shipped to all eligible accounts. |

### Plan Tiers

| Label | Accounts |
|-------|---------|
| `starter` | Teams up to 15 engineers, self-serve |
| `team` | Teams up to 50 engineers, includes Slack integration |
| `enterprise` | 50+ engineers, SSO, custom workflows, priority support |
