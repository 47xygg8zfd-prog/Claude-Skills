# HEART Framework

## What It Is

The HEART Framework is a user-centered metrics framework developed by Kerry Rodden and colleagues at Google. It provides a structured approach to defining success metrics for any product surface or feature.

HEART stands for:
- **H**appiness — subjective satisfaction with the product
- **E**ngagement — depth and frequency of interaction
- **A**doption — new users or features being picked up
- **R**etention — returning users and long-term loyalty
- **T**ask Success — efficiency and effectiveness at completing goals

The framework is paired with a **Goals-Signals-Metrics (GSM)** process:
- **Goal**: What is the user trying to accomplish? What does success look like?
- **Signal**: What user behaviors or attitudes indicate progress toward the goal?
- **Metric**: How do you operationalize the signal into a measurable number?

The combination produces metrics that are:
1. Grounded in user goals (not just business goals)
2. Defined before building (not reverse-engineered after launch)
3. Balanced across dimensions (avoiding over-optimization on one axis)

---

## When to Use It

- When launching a new feature or product surface and need to define success metrics
- When a product area has metrics but they feel misaligned with what users actually care about
- During quarterly OKR setting, to ensure KRs capture user value, not just business outputs
- When an A/B test has inconclusive results — HEART helps identify if you're measuring the right thing
- For PM/design alignment: HEART makes "what does success look like?" a structured conversation, not an argument

---

## The Five Dimensions

### Happiness
Measures subjective satisfaction. Typically captured through surveys, NPS, CSAT, or user sentiment.

**Signals**: Users rate the experience positively; users would recommend the feature; users report feeling informed/confident after using it.

**Caution**: Happiness metrics are slow-moving and easy to game (survey timing, population selection). Use as a long-term signal, not a sprint-level metric.

### Engagement
Measures the depth and quality of interaction. High engagement means users are getting real value — not just landing on a page.

**Signals**: Feature used multiple times per session; users explore beyond the default view; users complete more actions per visit over time.

**Caution**: Not all engagement is good engagement. A user spending 30 minutes on error messages is "engaged." Define meaningful engagement actions explicitly.

### Adoption
Measures new uptake — either new users to the product or existing users trying a new feature.

**Signals**: New accounts activated; existing users enabling a feature for the first time; users completing onboarding.

**Caution**: Adoption measures the top of the funnel, not the outcome. High adoption with low retention signals the product isn't delivering on its promise.

### Retention
Measures whether users return. The most important long-term signal of product-market fit.

**Signals**: Users return in week 2, week 4, week 12; users keep feature enabled; cohort retention curves are flat (not declining).

**Caution**: Retention is a lagging indicator — it tells you what happened 30-90 days ago, not what's happening now. Pair with leading indicators (engagement, adoption) for faster feedback.

### Task Success
Measures whether users can accomplish their goals efficiently and correctly.

**Signals**: Users complete the key workflow; error rates are low; time-on-task is decreasing; users don't need support to complete core tasks.

**Caution**: Task success can be high while happiness is low (users can complete the task but find it painful). Monitor both.

---

## The GSM Process

For each HEART dimension you choose to measure, define:

| Level | Question | Example |
|-------|----------|---------|
| **Goal** | What is the user trying to accomplish? | Managers want to understand if their team's performance changed last week |
| **Signal** | What behavior indicates success or failure? | Manager opens digest → clicks through to dashboard → views the metric mentioned |
| **Metric** | How is the signal measured? | Click-through rate from digest CTA; dashboard view rate within 10 minutes of open |

You don't have to measure all five dimensions. Choose the 2-3 most relevant for the feature, and define one metric per dimension.

---

## Worked Example: Pulse Weekly Digest

**Feature**: Weekly email digest delivered to managers on Monday mornings

| Dimension | Goal | Signal | Metric |
|-----------|------|--------|--------|
| **Happiness** | Managers feel informed and in control without logging in daily | Manager rates digest as useful; manager doesn't unsubscribe | Monthly pulse survey: "Is the weekly digest useful?" (1-5); unsubscribe rate |
| **Engagement** | Managers engage with digest content meaningfully | Manager opens digest and clicks through to relevant dashboard | Open rate; CTA click-through rate; dashboard views attributed to digest within 1 hour |
| **Adoption** | Managers who receive the digest start using it regularly | Manager opens at least 3 of first 4 digests received | 4-week adoption rate (opens ≥3/4); % of eligible managers with digest enabled |
| **Retention** | Digest becomes a weekly habit that drives ongoing platform engagement | Manager's WAU increases after digest enrollment | WAU delta: enrolled vs. control group (A/B); 8-week retention rate for enrolled managers |
| **Task Success** | Managers can act on digest insights without friction | Manager clicks through and finds the relevant dashboard section within 2 clicks | Click-to-dashboard success rate; time from open to relevant page view; zero-result click rate (clicked CTA, bounced immediately) |

**Which dimensions to prioritize for launch:**

| Priority | Dimension | Reason |
|----------|-----------|--------|
| Primary | Retention | The digest exists to build WAU habit — retention is the outcome |
| Primary | Engagement | Open + click-through tells us the content is working |
| Secondary | Task Success | Low click-to-dashboard success would indicate a UX problem |
| Quarterly | Happiness | Survey cadence; not a sprint-level metric |
| Quarterly | Adoption | Track enrollment trend; not a weekly concern |

---

## Common Mistakes

**Measuring all five dimensions for every feature.**  
HEART is a menu, not a checklist. Most features warrant 2-3 dimensions, not all five. Choose the dimensions most relevant to the feature's purpose.

**Defining metrics after launch.**  
The GSM process must happen before building — not as a post-launch exercise. Metrics defined before launch drive decisions during build. Metrics defined after launch rationalize decisions already made.

**Confusing engagement with value.**  
High session time, high page views, and high click volume are not inherently good. Each must be grounded in a user goal. A confused user generates high engagement metrics.

**Using happiness as a proxy for quality.**  
A high satisfaction score doesn't mean the product is well-designed. Users often rate familiar-but-broken experiences highly because they've adapted to the workarounds. Pair happiness with task success.

**Ignoring the "T" (Task Success).**  
Task success is the most direct measure of whether users can accomplish what they came to do. It's also the most commonly omitted because it requires usability research or behavioral analysis, not just analytics. Don't skip it.

---

## HEART vs. AARRR

| Framework | Focus | Best For |
|-----------|-------|----------|
| HEART | User goals and experience | Feature-level measurement; user-centered PM teams |
| AARRR (Pirate Metrics) | Business funnel | Growth teams; acquisition and revenue focus |

They're complementary. AARRR maps the business funnel; HEART maps the user experience within each stage. Use AARRR to know where in the funnel the problem is; use HEART to understand why.

---

## Connections

- **[North Star Metric](../pm-skills/north-star-metric/SKILL.md)**: HEART helps define the input metrics that feed the North Star — Retention feeds directly into the NSM for most products
- **[OKR skill](../pm-skills/okrs/SKILL.md)**: HEART dimensions map well to KRs — one KR per dimension ensures OKRs cover user value, not just business output
- **[Opportunity Solution Tree](opportunity-solution-tree.md)**: HEART metrics are the experiments at the bottom of the OST — they validate whether a solution moved a user-centered signal
- The `metrics/` playbook covers the Snowflake SQL to implement HEART engagement, adoption, and retention metrics
