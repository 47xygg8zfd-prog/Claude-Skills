# Swarmia Teardown

**Category**: Engineering effectiveness / flow metrics
**Threat level**: Medium
**One-line**: Flow metrics and team health for engineering orgs that want to improve, not just measure.

---

## The Problem They Solve

Swarmia's thesis is that engineering teams fail not because of talent gaps but because of systemic friction — too much WIP, poorly scoped work, interrupted flow. Their product surfaces "flow metrics" (a framework popularized by Mik Kersten's Project to Product book) alongside DORA metrics, and packages them for engineering teams and their managers. The pitch is: see where flow breaks down, fix the system, improve delivery.

The segment sits between LinearB and Allstacks: engineering managers and VPs of Engineering at product-led growth companies (roughly 50–500 engineers), often with a strong engineering culture that values process improvement and invests in developer experience. Swarmia customers tend to be companies already doing retros, running health checks, and thinking about engineering effectiveness as a strategic lever — not just a reporting need.

---

## Day 1 Onboarding

Swarmia connects GitHub and Jira (or Linear), pulls historical data, and surfaces flow metrics within the first session. The onboarding is smoother than LinearB's because Swarmia is more opinionated about defaults — you get a pre-configured dashboard rather than a blank canvas. The tradeoff: less flexibility upfront, but a faster path to a first meaningful view.

Their onboarding explicitly frames the product around "investments" — how is engineering time allocated across new features, quality work, and unplanned work? That framing does useful work: it orients managers toward the right question before they've even configured anything. It's a small UX detail that signals product maturity.

---

## Core Retention Loop

Swarmia's retention is built around the weekly team health check. Managers are nudged to review team health scores — a composite of WIP levels, review cycle times, and deployment frequency — once per week. The product also generates "nudges": lightweight prompts surfaced in Slack when a specific metric crosses a threshold. High WIP? Swarmia tells you. PR sitting unreviewed for 48 hours? Swarmia flags it.

The Slack integration is central to their stickiness, similar to LinearB's WorkerB, but Swarmia's nudges are slightly more actionable — they tell you what crossed a threshold, not just that a threshold was crossed.

---

## Monetization

Per-team, tiered by number of engineers. Swarmia publishes pricing, which is unusual in this space and signals a more product-led sales motion. Starter tier is accessible for small teams; growth and enterprise tiers add integrations, advanced reporting, and SSO. The transparent pricing makes it easier for a manager to expense without going through procurement — a meaningful advantage in the mid-market.

---

## Feature Highlights

**Investment distribution** — Tracks how engineering time breaks down across features, tech debt, bugs, and unplanned work. Backed by the "Project to Product" flow framework. Gives managers a defensible way to argue for tech debt investment.

**Working agreements** — Teams can define explicit norms (e.g., "PRs should be reviewed within 24 hours") and Swarmia tracks adherence. This turns abstract best practices into measurable commitments. Smart.

**Team health overview** — A composite score across multiple dimensions that gives managers a single view of whether their team is in a healthy delivery rhythm. Not as granular as LinearB, but more interpretable for non-data-native managers.

**Automated nudges** — Slack-based alerts tied to specific metric thresholds, with enough context to understand what happened without opening the dashboard.

**GitHub + Linear support** — One of the few tools in this space with strong Linear integration, which matters for companies that have moved off Jira.

---

## Weaknesses / Opportunities

Swarmia's biggest weakness is that it still requires interpretation. The flow metrics framework is powerful, but it's not mainstream knowledge — managers who haven't read Mik Kersten need to be educated before they can use the data. The product does some of this work, but not enough. A manager who opens Swarmia for the first time and sees "flow efficiency: 34%" has no idea whether that's good or bad, or what to do about it.

The working agreements feature is underused because teams have to define their own norms before the tracking is meaningful. That creates a chicken-and-egg problem: the managers who would benefit most from having explicit working agreements are often the ones who haven't defined them yet.

There's also a gap at the individual level — Swarmia is deliberately team-level, which keeps it out of performance management territory, but it means managers can't easily identify where a specific team member is bottlenecked or struggling.

---

## Competitive Counter: How Pulse Wins (and Where It Doesn't)

**Pulse wins on**: Manager-first positioning — Pulse is built for the EM, not the VP or data analyst who interprets Swarmia output. Actionable recommendations — Pulse tells you what to do; Swarmia tells you what's happening and trusts you to figure out the rest. Time-to-value — Pulse's 3-day onboarding beats Swarmia's ramp, especially for teams that aren't already fluent in flow frameworks.

**Swarmia wins on**: Working agreements tracking — this is a genuinely differentiated feature Pulse doesn't have. Flow framework depth — Swarmia's investment distribution model is more rigorous than Pulse's sprint data framing. Published pricing — reduces friction for self-serve and inbound deals.

The competitive risk Swarmia poses is real but specific: they win deals with engineering-culture-forward companies where the manager or VP is already bought into flow frameworks and wants depth over simplicity. That's a narrower buyer than Pulse's ICP. Where Swarmia struggles is with the majority of engineering managers who are time-poor and just want to know what to do this week — that's Pulse's territory.

---

## If I Were PM at Swarmia...

The one thing I'd build next is **opinionated interpretation** — take the flow metrics output and translate it into plain-language recommendations. "Your flow efficiency dropped 12 points this sprint. The cause appears to be a spike in unplanned work. Here's how three similar teams handled it." Swarmia has the data to support this. Right now they surface the signal; they don't close the loop. Whoever builds that layer first wins the mid-market.
