# LinearB Teardown

**Category**: Engineering analytics / DORA metrics platform
**Threat level**: High
**One-line**: Git-native engineering intelligence for teams that live in pull requests.

---

## The Problem They Solve

LinearB starts from a specific frustration: engineering managers have no objective signal for what's slowing their team down. Is it code review lag? Deployment frequency? Rework? They're guessing. LinearB connects to GitHub/GitLab, maps cycle time across every stage of the delivery pipeline, and gives managers a dashboard that answers "where are we stuck right now?" It's a metrification play — take the intuition a senior EM develops over years and make it legible in week one.

The segment is precise: engineering managers and directors at companies with 20–200+ engineers, shipping software continuously, already bought into DORA as a framework. These are technical managers who trust data and are comfortable pulling insights from a dashboard. They don't need to be told what to do — they need to see the signal they've been missing.

---

## Day 1 Onboarding

LinearB's onboarding is repo-first. You connect your GitHub or GitLab org, LinearB maps your contributors to engineers, and within 24–48 hours you have historical cycle time data going back 90 days. The aha moment is early and visceral: you can immediately see your longest PR review lag, your highest-rework engineers, your slowest merge paths. No configuration required for that first read. The cost is that setup gets complicated fast — mapping contributors accurately across repos, filtering bot commits, configuring team structures — and that work falls entirely on the manager.

---

## Core Retention Loop

Weekly: managers check cycle time trends after each sprint close. Daily: engineering leads monitor open PR queues and review bottlenecks. The product embeds into existing standups — LinearB's WorkerB Slack bot surfaces blockers and flagged PRs directly in team channels. That Slack integration is their stickiest feature because it puts LinearB data where engineers already are, reducing the "go check the dashboard" friction that kills most analytics tools.

---

## Monetization

Per-seat, per-contributor. Pricing scales with the number of active contributors tracked, not managers. That's a deliberate choice — it aligns their revenue growth with customer team growth, and makes the expansion motion natural as companies hire. Enterprise tier adds SSO, custom integrations, and dedicated CSM. No published pricing; sales-led for teams above ~25 engineers.

---

## Feature Highlights

**Cycle time breakdown** — Not just "cycle time" as a number, but decomposed into coding time, pickup time, review time, deploy time. Tells you exactly which stage is the bottleneck. This is their best feature.

**WorkerB Slack bot** — Automated daily PR reminders and standup summaries pushed to team channels. Reduces review lag without requiring anyone to open the dashboard.

**Git-to-Jira correlation** — Maps git activity to Jira tickets, giving managers a view of actual vs. planned work. Catches scope creep and off-roadmap work automatically.

**DORA benchmark comparisons** — Shows your team's metrics against DORA industry benchmarks (elite / high / medium / low). Useful for justifying investment or process changes to leadership.

**Investment profile** — Tracks how engineering time is split across new features, tech debt, and bugs. Helps managers make the case for refactoring investment.

---

## Weaknesses / Opportunities

LinearB is excellent at measurement and poor at prescription. The dashboard tells you your cycle time is high; it doesn't tell you whether to fix it by changing your PR review process, reducing WIP, or breaking down stories differently. The product assumes the manager already knows what to do with the data — and many don't.

Onboarding is also a real weakness. The first 48 hours are impressive, but weeks 2–4 require significant configuration work that LinearB's UI doesn't guide well. Managers who aren't comfortable in a data tool drop off before they get the full value.

Finally: LinearB is Git-native. Teams using Jira with non-standard workflows, or teams where the work-to-be-done isn't fully represented in Git (design sprints, research, stakeholder-heavy work), get a partial picture at best.

---

## Competitive Counter: How Pulse Wins (and Where It Doesn't)

**Pulse wins on**: Actionable recommendations — Pulse tells you what to do, not just what happened. Manager-first positioning — Pulse is built for the EM running the standup, not the engineering director reviewing dashboards. Onboarding speed — 3 days versus LinearB's longer ramp with configuration overhead.

**LinearB wins on**: Git data depth — their cycle time decomposition is genuinely better than anything Pulse offers today. Slack integration — WorkerB is stickier than Pulse's current notification model. DORA benchmarking — useful for managers who need to justify process investments to leadership.

The honest read: if a manager's primary pain is PR review lag and Git pipeline visibility, LinearB is the better tool. Pulse wins when the manager's pain is broader — "I need to understand whether my team is healthy and what I should focus on this sprint" — because that question requires more than Git data to answer.

---

## If I Were PM at LinearB...

The one thing I'd build next is a **recommendation engine on top of the metrics layer** — something that takes a manager's cycle time breakdown and says "your pickup time is in the bottom quartile; here are three process changes teams like yours have made to fix it." LinearB has the data. They don't yet close the loop from insight to action. That's their biggest vulnerability, and it's exactly where Pulse is attacking.
