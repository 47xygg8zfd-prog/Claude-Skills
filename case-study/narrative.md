# Case Study: Shipping the Weekly Digest at Pulse

**Product**: Pulse — B2B team analytics for engineering managers  
**Timeline**: Q3 2026 (May–August)  
**PM**: Sarah Kim  
**Result**: WAU increased from 32% to 44% of paid seats within 8 weeks of launch  

---

## The Situation

Pulse gives engineering managers visibility into their team's velocity, responsiveness, and collaboration. The data is valuable. The problem: most managers never look at it.

Going into Q2 planning, our retention data showed a troubling pattern. Accounts with high engagement (3+ logins per week) had 91% 90-day retention. Accounts with low engagement (<2 logins per week) had 58% retention. The gap was 33 points — and 68% of our users were in the low-engagement bucket.

We knew what we needed to move. We didn't yet know why engagement was low or what would fix it.

---

## 1. Discovery — The Problem

**Skills used**: [`customer-research-synthesis`](../pm-skills/customer-research-synthesis/SKILL.md), [`competitive-analysis`](../pm-skills/competitive-analysis/SKILL.md)  
**Example outputs**: [Research synthesis](../examples/customer-research-synthesis-example.md), [Competitive analysis](../examples/competitive-analysis-example.md)

### What we did

I ran 8 customer interviews with engineering managers across our mid-market segment. The goal was simple: understand why they weren't logging in.

I fed the raw notes into the `customer-research-synthesis` skill and got back a structured analysis in minutes instead of hours. The top finding was immediate and clear:

> **Theme 1 (7/8 participants)**: Managers don't log in because there's no pull. They know the data exists — they just don't think to go look at it.

The JTBD statement that came out of synthesis:

> *When I'm starting my week, I want to quickly understand if anything in my team needs my attention, so I can focus my energy on the right problems without spending time digging through dashboards.*

This reframed the problem. It wasn't that managers didn't value Pulse — it was that Pulse required active effort to get value from. The solution wasn't a better dashboard. It was passive delivery.

Meanwhile, I ran a competitive analysis on Teamlytics — our main competitor — and discovered they had just launched a "Manager Digest" feature in beta. This was both a threat and a validation signal: if Teamlytics was betting on passive delivery, we had independent confirmation the insight was real.

**Key decision**: We were solving a habit formation problem, not a product depth problem. That meant the solution needed to find the user, not wait for the user to find it.

---

## 2. Strategy — What to Build

**Skills used**: [`feature-prioritization`](../pm-skills/feature-prioritization/SKILL.md), [`okrs`](../pm-skills/okrs/SKILL.md)  
**Example outputs**: [Feature prioritization](../examples/feature-prioritization-example.md), [OKRs](../examples/okrs-example.md)

### What we did

I had six feature candidates for Q3 competing for the same engineering capacity: weekly digest, mobile app, SSO, custom dashboards, API access, and in-app onboarding. I ran RICE scoring using the `feature-prioritization` skill.

The results were decisive:

| Feature | RICE Score | Recommendation |
|---------|-----------|----------------|
| In-app onboarding | 2,880 | #1 — build Q3 |
| Weekly digest | 1,050 | #2 — build Q3 |
| SSO | 1,200 | #3 — build Q3 (unblocks 4 enterprise deals) |
| Custom dashboards | 360 | Defer to Q4 |
| API access | 150 | Needs more validation |
| Mobile app | 75 | Deprioritize — 94% of sessions are desktop |

The digest wasn't #1 on RICE — onboarding was. But onboarding and the digest were complementary. Users who complete onboarding and receive a digest in their first 30 days form the habit fastest. We committed to both.

With the roadmap set, I used the `okrs` skill to draft Q3 OKRs:

**Objective 1**: Make Pulse a habit managers return to every week  
- KR1: WAU 32% → 42% of paid seats  
- KR2: Manager login frequency 1.8× → 3.5× per week  

**Objective 2**: Turn new users into confident Pulse users in 30 days  
- KR1: Onboarding completion 38% → 65%  
- KR2: Time-to-first-insight 8 days → 3 days  

**Objective 3**: Keep the customers we've earned  
- KR1: 90-day retention 71% → 78%  

**Key decision**: Mobile had the second-highest reach but scored last on RICE because effort was 8 person-months. Presenting the scoring model to the exec team made the deprioritization defensible — it wasn't a gut call, it was math.

---

## 3. Scoping — The PRD

**Skills used**: [`prd`](../pm-skills/prd/SKILL.md)  
**Example output**: [PRD](../examples/prd-example.md)  
**Template**: [PRD template](../templates/prd-template.md)

### What we did

With the research insight and prioritization in hand, I used the `prd` skill to draft the Weekly Digest PRD. The prompt took 2 minutes; the draft took 8 minutes to review and refine.

The PRD had three constraints I was explicit about:
1. **v1 is manager-facing only** — individual contributor digests add scope and complexity without addressing the core retention correlation
2. **Weekly cadence only** — no customization in v1; customization is a nice-to-have that would double the build time
3. **No real-time data** — the digest reflects the previous week; real-time requires a different infrastructure path

The PRD surfaced three open questions that needed answers before engineering kickoff:
1. Should delivery time be configurable per user or set at the admin level?
2. How do we handle managers with multiple teams — one digest or one per team?
3. What's the unsubscribe behavior — 1-click, or login required?

We resolved all three in a single 30-minute design review, which is faster than average because the PRD had already framed the tradeoffs.

**Key decision**: Keeping v1 ruthlessly scoped. Every "what about..." that came up in PRD review went into a "v2 considerations" section rather than expanding scope. This saved approximately 3 weeks of build time.

---

## 4. Planning — Sprint & Forecast

**Skills used**: [`agile-stories`](../pm-skills/agile-stories/SKILL.md), [`agile-ceremonies`](../pm-skills/agile-ceremonies/SKILL.md), [`monte-carlo`](../pm-skills/monte-carlo/SKILL.md)  
**Example outputs**: [Agile stories](../examples/agile-stories-example.md), [Monte Carlo](../examples/monte-carlo-example.md)

### What we did

I used the `agile-stories` skill to break the PRD into sprint-ready tickets. The output was 5 stories totaling 18 points across 2 sprints, with clear acceptance criteria and dependency ordering.

Before sprint planning, I ran a Monte Carlo forecast using the last 4 sprints of velocity data (11, 9, 13, 10 points):

| Confidence | Projected completion |
|------------|---------------------|
| 50% | July 21 |
| 75% | August 4 |
| 85% | August 11 |

The 75% confidence date landed exactly on our August 4 target. I communicated this honestly to stakeholders: "We have a 75% chance of hitting August 4. One slow sprint makes it August 11."

Sprint planning used the `agile-ceremonies` skill to generate a structured agenda. We committed 13 points in Sprint 1 (data aggregation job + email template + admin opt-in), leaving Stories 4 and 5 for Sprint 2.

**Key decision**: Presenting the forecast as a probability distribution instead of a single date changed the stakeholder conversation. Instead of "will you hit August 4?" the question became "what would give us 85% confidence?" — which led to a productive conversation about scope protection rather than deadline pressure.

---

## 5. Build — Staying Aligned

**Skills used**: [`tech-translation`](../pm-skills/tech-translation/SKILL.md), [`stakeholder-updates`](../pm-skills/stakeholder-updates/SKILL.md)  
**Example outputs**: [Tech translation](../examples/tech-translation-example.md), [Stakeholder updates](../examples/stakeholder-updates-example.md)

### What we did

Mid-sprint, two engineering concerns came up that I needed to understand and communicate upward.

**Idempotency**: The team said the aggregation job "needs to be idempotent." I used the `tech-translation` skill to understand the implication for product decisions: a non-idempotent job could send duplicate emails or silently skip managers if the job failed and restarted. The translation made clear this wasn't gold-plating — it was protecting the user experience.

**Thundering herd**: The team flagged that sending 18,000 emails simultaneously at 9am Monday would spike our email provider. Translation: managers would get their digest late or not at all on the first big Monday. We decided to stagger delivery across a 30-minute window.

At week 6, we hit a blocker: our SendGrid contract capped sends at 2,000/week. Full rollout needed 18,000. The contract renewal required CFO approval.

I used the `stakeholder-updates` skill to draft two documents:
1. **Weekly status update** flagging the blocker to the VP Product
2. **Escalation memo** to the CFO with three options, a recommendation, and a decision deadline of May 18

The CFO signed the contract renewal within 48 hours. The memo worked because it came with a clear recommendation and a hard deadline — not just a heads-up.

**Key decision**: Escalating early and in writing. The SendGrid blocker emerged at week 6 of a 12-week quarter. Waiting to raise it in a weekly sync would have cost 2–3 days. The async escalation memo resolved it in 2 days.

---

## 6. Measure — Did It Work?

**Skills used**: [`data-queries`](../pm-skills/data-queries/SKILL.md), [`quicksight-dashboards`](../pm-skills/quicksight-dashboards/SKILL.md)  
**Example outputs**: [Data queries](../examples/data-queries-example.md), [QuickSight dashboards](../examples/quicksight-dashboards-example.md)

### What we did

Before launch I used the `data-queries` skill to write the Snowflake SQL we'd need post-launch:
- WAU by plan tier (to track KR1)
- Digest send volume and delivery status (to monitor launch health)
- Splunk alert for email delivery errors (to catch issues before users did)

I also used the `quicksight-dashboards` skill to design a "Digest Health" dashboard covering three panels: model health (send volume, open rate, CTR), user behavior (adoption by account, engagement trend), and business impact (WAU A/B split).

**Week 1 results**:
- 1,847 emails delivered (capped by SendGrid — full rollout pending contract)
- 41% open rate (industry average: 22%; our target: 45%)
- 18% CTR on the primary CTA

The 41% open rate on week 1, before any optimization, was the strongest signal we'd had that the research was right. Managers wanted this — they just needed it to come to them.

**Week 8 results** (post full rollout):
- WAU: 44% of paid seats (was 32%; target was 42%) ✅ exceeded
- Manager login frequency: 3.2× per week (was 1.8×; target 3.5×) 🟡 close
- Digest open rate: 47% (target 45%) ✅ exceeded

**Key decision**: Instrumenting before launch, not after. The SQL and dashboard were ready on launch day. This meant we had clean data from day 1 and didn't spend the first two weeks arguing about how to measure success.

---

## 7. Launch — Telling the Story

**Skills used**: [`release-notes`](../pm-skills/release-notes/SKILL.md), [`pm-presentations`](../pm-skills/pm-presentations/SKILL.md)  
**Example outputs**: [Release notes](../examples/release-notes-example.md), [PM presentations](../examples/pm-presentations-example.md)

### What we did

For the v2.4 release (digest + SSO + small teams bug fix), I used the `release-notes` skill to produce four versions of the same release:

- **End users**: Friendly, benefit-led — "Your most important insights, delivered every Monday"
- **Internal/eng**: Technical — migration notes, feature flags, known issues
- **Sales & CS**: Talking points and questions to expect ("Does this support SCIM?" → no, Q4)
- **Exec**: 4-bullet summary focused on business outcomes

Writing one release and getting four formats took 15 minutes. Previously this took a half-day of back-and-forth with CS, marketing, and eng.

At mid-quarter (week 6), before the digest had fully launched, I used the `pm-presentations` skill to prepare the exec update. The challenge: retention KRs were lagging, but for a predictable reason — 90-day retention inherently lags 90 days behind engagement work. The exec update needed to tell a coherent story about why the numbers looked soft and why we weren't concerned.

The presentation led with "The one thing": engagement work is on track; retention will follow. It put the ask front-and-center (SendGrid contract) on slide 8, not buried in an appendix.

**Key decision**: Separating the story from the data. The data showed mixed signals mid-quarter. The presentation put those signals in context — which is the PM's job, not the dashboard's.

---

## 8. Reflect — What We Learned

**Skills used**: [`agile-ceremonies`](../pm-skills/agile-ceremonies/SKILL.md), [`okrs`](../pm-skills/okrs/SKILL.md)  
**Example outputs**: [Agile ceremonies](../examples/agile-ceremonies-example.md), [OKRs](../examples/okrs-example.md)

### What we did

Sprint 24 retro (post-digest Sprint 1) surfaced three process improvements:
1. AC must be complete before sprint starts — two days were lost to mid-sprint edge case discovery
2. Design + eng kickoff at sprint start — three revision cycles on the email template happened because design feedback came in async after implementation started
3. Spike story for the SendGrid rate limit question — this was foreseeable and should have been a scoped spike in the prior sprint

Each became a Definition of Ready change we carried into Sprint 25.

End-of-quarter OKR scores:

| Key Result | Score | Note |
|------------|-------|------|
| WAU 32% → 42% | 1.0+ | Hit 44% — target was slightly conservative |
| Login frequency 1.8× → 3.5× | 0.8 | Hit 3.2× — close |
| Onboarding completion 38% → 65% | 0.9 | Hit 61% |
| Time-to-first-insight 8d → 3d | 0.8 | Hit 4 days |
| 90-day retention 71% → 78% | 0.3 | Lags engagement; expect Q4 recovery |
| NPS +28 → +38 | 0.6 | Hit +34 |

Overall quarter: strong on engagement, lagging on retention (expected), mixed on NPS. The Q4 roadmap was set before Q3 ended — custom dashboards and API access moved up based on the engagement data showing that users who engage deeply are the ones who expand.

---

## What This Case Study Demonstrates

| PM Skill | Where It Showed Up |
|----------|--------------------|
| Problem framing | Reframing "low engagement" as a habit formation problem, not a depth problem |
| Prioritization with evidence | RICE scoring that made the mobile deprioritization defensible |
| Scope discipline | Keeping v1 to weekly cadence and manager-only, saving 3 weeks |
| Probabilistic communication | Presenting the forecast as a distribution, not a date |
| Early escalation | Raising the SendGrid blocker in writing, async, with a recommended action |
| Instrumenting before launch | SQL and dashboards ready day 1 |
| Narrative over data | Mid-quarter exec update that put lagging retention in the right context |
| Process improvement | Retro findings turned into Definition of Ready changes that held |

---

## Skills Used

Every skill output referenced in this case study is available in the [`examples/`](../examples/) folder. The skills themselves are in [`pm-skills/`](../pm-skills/). The metrics queries are in [`metrics/`](../metrics/).
