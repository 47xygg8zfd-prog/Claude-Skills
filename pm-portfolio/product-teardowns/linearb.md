# LinearB Teardown

> **TL;DR**: LinearB is the best Git analytics product on the market — and that's exactly its trap. It measures everything that happens in a pull request and almost nothing that matters to the manager trying to run a healthy team.

---

## What This Product Is Really Optimizing For

LinearB is optimizing for data density and engineering credibility. Every design decision — the Git-first onboarding, the DORA benchmark overlays, the cycle time decomposition into coding/pickup/review/deploy stages — is aimed at one outcome: making an engineering manager feel like they finally have objective signal. The product's implicit promise is "you don't have to guess anymore." That's powerful with a specific buyer: the technical EM who trusts data, distrusts intuition, and wants something defensible to bring to their VP. What LinearB is not optimizing for is what to do next. The dashboard answers "where are we stuck?" brilliantly. It conspicuously never answers "so what should we change?"

---

## Key Metrics & What They Reveal

- **North Star metric**: Cycle time — the time from issue creation to deploy, broken down into coding / pickup / review / deploy stages.
- **How you know**: Every dashboard view leads with cycle time as the primary comparison axis; the entire product is scaffolded around decomposing and optimizing this single metric. The stage breakdown is the core visualization — it's not buried in a submenu, it's the homepage.
- **Input metrics**: PR review turnaround time, time to pickup (how long a PR sits before review starts), rework rate, deployment frequency, and contributor-specific bottleneck identification. These are the sub-metrics the team is actively measuring daily to move the north star.
- **What this tells us**: LinearB is betting that engineering managers care most about delivery speed and believe the path to faster delivery runs through process optimization. They're optimizing for operational efficiency, not business outcomes — they assume that if you fix the engineering process, the business results follow. This positioning leaves them vulnerable to competitors who can connect engineering metrics back to product outcomes or team health.

---

## Jobs to Be Done

| Job type | The job | What users hired before | Why this product wins this job |
|----------|---------|------------------------|-------------------------------|
| Functional | Identify which stage of the delivery pipeline is bottlenecked right now | Eyeballing PR queues manually; asking engineers in standup | Cycle time decomposition by stage is the most granular breakdown in the market — you can see that pickup time is the problem, not review time |
| Emotional | Feel like an objective, data-driven leader rather than someone managing by vibes | Gut feel, retrospective blame, occasional spreadsheets | The DORA benchmark comparison specifically scratches this itch — "elite performer" is a label EMs want to earn |
| Social | Justify process change requests and headcount decisions with real data | Anecdotal arguments in planning meetings | Investment profile and DORA benchmarks give managers a language leadership accepts |

---

## Target Segment

**Primary**: Engineering managers and directors at companies with 30–300+ engineers, shipping continuously, already bought into DORA as a framework. Technical managers comfortable pulling insight from a dashboard without hand-holding.

**Secondary**: VPs of Engineering who want org-level delivery visibility and CTOs who want to benchmark their team against industry standards.

**Explicitly not served**: Managers who aren't Git-native (design-heavy, research-heavy, or stakeholder-intensive teams where the real work doesn't show up in commits). Also not served: managers who want to be told what to do, not just what happened — LinearB assumes you already know how to interpret and act on the data.

---

## Onboarding & The Aha Moment

**Day 1 flow**: Connect GitHub or GitLab org → LinearB maps contributors to engineers → 24–48 hours to pull 90 days of historical data → dashboard populates with cycle time breakdown, open PR queue, and DORA scores. No configuration required for that first view.

**The aha moment**: Seeing your longest PR review lag and highest-rework contributors for the first time. It's visceral — most managers have suspected one of their senior engineers is a bottleneck; LinearB shows them it's true, with receipts.

**Time to aha**: Fast for the first view. But weeks 2–4 require significant configuration work — mapping contributors accurately across repos, filtering bot commits, defining team structures — and the UI doesn't guide this well. The real aha has a long tail.

**What they're betting on**: That technical managers will do the configuration work themselves because the first view is compelling enough. It's a reasonable bet for their target buyer. It's a losing bet for time-poor managers who need the product to do more of the work.

---

## The Growth Loop

```
Manager connects GitHub org (low-friction activation)
      ↓
Sees historical cycle time breakdown in 48 hours (fast aha)
      ↓
Shares dashboard in team standup → engineers see their own PR data
      ↓
WorkerB bot pushes PR reminders into Slack channels
      ↓
Engineers start using the bot daily → managers renew because team is already embedded
      ↓
Team grows → contributor count grows → seat expansion revenue
```

**Loop type**: Product-led with a Slack-embedded viral layer

**Loop strength**: Moderate. The Slack integration (WorkerB) is genuinely sticky because it meets engineers where they already are. But the loop depends on a manager doing enough configuration work to make the data trustworthy — and many drop off before that happens.

**Leakage point**: Weeks 2–4. The first 48 hours are impressive. Then the manager realizes the contributor mapping is messy, the bot is firing on bot commits, and getting clean data requires work LinearB's UI doesn't help with. That's where adoption stalls.

---

## Retention Mechanics

**What brings users back**: The WorkerB Slack bot is the primary retention driver — it surfaces PR queues and review lag in team channels daily, so engineers engage with LinearB data even when the manager doesn't open the dashboard.

**Retention curve shape**: Steep initial engagement (the first week is high), followed by a drop when configuration complexity hits, then a plateau for users who get through setup. The Slack bot is what prevents the plateau from becoming a continued decline.

**The habit they're building**: Daily PR hygiene — engineers reviewing open PRs before standup because WorkerB has already reminded them. It's a useful habit that creates real value, which is why the retention curve stabilizes.

**Churn signals**: Managers who never complete contributor mapping, teams where WorkerB bot messages get muted, accounts where dashboard logins drop to once per sprint instead of weekly.

---

## Monetization & Strategic Alignment

**Model**: Per active contributor tracked, not per manager seat.

**Free tier purpose**: Limited contributor count to establish the product in smaller teams and build the case for expansion as companies hire.

**Upgrade trigger**: Contributor count. As the engineering org grows, the cost scales naturally with the team — no sales conversation needed for expansion.

**Alignment check**: The contributor-based pricing is clever and mostly aligned. Revenue grows with customer team growth, and expansion is automatic. The misalignment: if a manager churns because the product is too configuration-heavy, LinearB loses contributors it could have retained with better onboarding investment. Their monetization model slightly deprioritizes onboarding quality because early-stage teams are small anyway.

---

## Feature Strategy

| Feature | What it does | The strategic bet |
|---------|-------------|------------------|
| Cycle time decomposition | Breaks cycle time into coding / pickup / review / deploy stages | Engineers will care more about fixing the right bottleneck than fixing cycle time as a monolith — specificity creates urgency |
| WorkerB Slack bot | Pushes daily PR reminders and standup summaries into team channels | The product dies if it requires managers to pull data; it survives if it pushes data to where engineers already are |
| Git-to-Jira correlation | Maps git commits to Jira tickets to surface off-roadmap work | Managers don't know how much shadow work their team is doing — making it visible creates a forcing function for prioritization conversations |
| DORA benchmarking | Compares your team's metrics to elite/high/medium/low industry bands | EMs need external benchmarks to justify process change to leadership — "we're in the bottom quartile" is more persuasive than "I think we're slow" |
| Investment profile | Tracks time split across features, tech debt, and bugs | The PM vs. eng tension over tech debt allocation is easier to resolve with data than with arguments |

---

## Weaknesses & Vulnerabilities

**Measurement without prescription**: LinearB tells you your pickup time is in the 40th percentile. It doesn't tell you whether to fix that by changing your PR review norms, reducing WIP, or breaking stories down differently. The product assumes the manager already knows what to do with the data — and many don't. This is a real gap that a recommendation layer could close.

**Git-native blind spots**: Teams where meaningful work doesn't live in Git — design work, research spikes, stakeholder-heavy projects, non-standard Jira workflows — get a systematically incomplete picture. LinearB knows this and accepts it; their ICP is companies where Git is the source of truth. But it's a ceiling on their TAM.

**Configuration tax**: The onboarding investment required to get clean data is real and falls entirely on the manager. LinearB's best-fit customers are technical managers with time to invest in setup. Their worst-fit customers — time-poor managers at fast-growing mid-market companies — are often the ones who need engineering analytics most.

---

## 3 Lessons for Any PM

1. **Embed in existing workflows, don't create new ones**: WorkerB's success is a product lesson. The reason LinearB retains users isn't the dashboard — it's the Slack bot that surfaces data where engineers already are. Every analytics product should ask: where does the user already spend time, and how do we meet them there?

2. **The aha moment should be fast, but the value should deepen**: LinearB's 48-hour historical data pull is the right instinct. Get users to a moment of genuine surprise quickly. But make sure the path from that first aha to sustained value doesn't require a configuration marathon — that's where LinearB leaks.

3. **Pricing architecture is product strategy**: Charging per contributor, not per manager, was a deliberate bet that expansion follows team growth. It's working. When designing monetization, ask whether your pricing unit naturally inflates as customers succeed with your product — if so, you've aligned revenue with value delivery.

---

## If I Were PM Here

LinearB's most exploitable gap is the space between insight and action. The cycle time decomposition is excellent; what's missing is a layer that says "your pickup time crossed a threshold — here are the three process changes teams in similar situations have made, and here's which one worked most often." LinearB has enough aggregate data across their customer base to make those recommendations credible. Building a recommendation engine on top of the metrics layer wouldn't require new data collection — just a new product surface. The metric it would move is activation depth: managers who currently log in once a sprint to look at dashboards would log in weekly to check whether the recommended process change is working. That's the difference between an analytics tool and a tool that actually changes how a team works.
