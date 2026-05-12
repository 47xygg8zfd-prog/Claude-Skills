# File 18 — Launch Marketing Brief
**Product**: Sentinel — On-Call Intelligence Platform  
**Date**: 2026-05-12  
**Audience for this brief**: Marketing, demand gen, AE team, customer success  
**Launch type**: Soft launch to 5 beta customers, then full launch 2 weeks later

---

## Positioning

**What Sentinel is**:  
Sentinel is the on-call intelligence platform that engineering teams at mid-size B2B SaaS use to eliminate hero dependency — without adding process or changing how engineers work.

**What Sentinel is not**:  
- Not an alerting tool (we don't replace PagerDuty or OpsGenie — we sit on top of them)
- Not an observability platform (not competing with Datadog, Grafana, or New Relic)
- Not an HR or performance management tool
- Not AI-powered (it uses heuristic routing and semantic search — do not say "AI")

**The insight that drives the positioning**:  
On-call burnout is almost never about alert volume alone. It's about the same 1-2 engineers being the only ones who know how to resolve the hard alerts. When those engineers leave or burn out, MTTR spikes and the whole team suffers. Sentinel fixes the knowledge problem, not the alert volume problem.

---

## Target Customer

**Primary**: Engineering managers at mid-size B2B SaaS companies (50–500 engineers)  
**Trigger events** (when they're most receptive):
- Just lost a senior engineer to burnout or a competitor
- MTTR spiked when a key engineer was on PTO and nobody knew what to do
- Post-mortems reveal the same 1-2 people resolving most critical incidents
- Engineering leadership is pushing for on-call rotation health metrics
- Team is growing and institutional knowledge isn't scaling

**Who they are**: They care deeply about their team's wellbeing, they're accountable to uptime SLAs, and they've watched good engineers quit or disengage because of on-call. They are not primarily data people — they need clear signals, not dashboards full of numbers.

**Secondary**: VPs of Engineering who have lost multiple engineers or are preparing for SOC2/uptime commitments that require demonstrable incident management maturity.

---

## Headline Options

Three options — test these in order for A/B on launch email:

**Option A — Pain angle** (recommended for cold outreach and paid):  
> "When your best engineer is on vacation, what happens?"

**Option B — Outcome angle** (recommended for in-app and nurture):  
> "Stop losing your best engineers to on-call."

**Option C — Insight angle** (recommended for content marketing and thought leadership):  
> "On-call shouldn't require a hero."

Supporting subheadline (use with any of the above):  
> Sentinel captures on-call knowledge as it's created, routes the right engineer to every alert, and shows you exactly where your team's on-call risk lives — before someone burns out.

---

## Feature Announcement (In-App / Email) — 100–150 Words

**Subject line options** (see below for full list):

---

**Body copy**:

Sentinel is now available to your team.

We built it for engineering managers who've watched a senior engineer burn out on on-call, or scramble through a 3am incident because the only person who knew the fix was on vacation.

Sentinel does three things:

**Capture runbooks at close.** When an engineer resolves an incident, Sentinel prompts them to document what they did — right then, while the context is fresh. Two minutes. No separate tool.

**Route alerts to the right engineer.** Based on who's resolved similar alerts before, not just who's next in the rotation.

**See your hero dependency.** The Hero Dependency Index shows you which engineers are carrying too much, before they tell you they're leaving.

On-call knowledge shouldn't live in one person's head.

[Get started →]

---

*Word count: 145*

---

## Subject Line Options

**Benefit angle**:  
`Your team's on-call knowledge — captured, organized, and actually useful`

**Pain angle**:  
`What happens when your best engineer burns out?`

**Curiosity angle**:  
`64% of your incidents are handled by one person. Is that sustainable?`

*Notes*: Pain angle performs best in cold sequences with EM/VP Eng titles. Benefit angle performs better for in-app notifications to existing users. Curiosity angle works well for LinkedIn and newsletter content where a specific stat anchors the message.

---

## What Not to Say

Specific language restrictions for all marketing materials, sales decks, and AE conversations:

| Do not say | Why | Say instead |
|------------|-----|-------------|
| "AI-powered" | The routing is heuristic, not ML. Customers will ask about the model and we can't answer. | "intelligent routing," "heuristic-based routing," "experience-based assignment" |
| "Eliminate on-call pain" or "eliminate burnout" | We can reduce hero dependency; we cannot promise to eliminate burnout. Overpromising here will cause churn. | "reduce hero dependency," "distribute on-call knowledge," "lower your team's on-call risk" |
| "Seamless" | Every engineer will tell you changing incident close behavior is not seamless. It's a small friction that's intentional. | "designed to fit your workflow" |
| "Game-changer" | Overused, unspecific, creates skepticism | Name the specific outcome: "reduces MTTR by 30% in the first 60 days" (use only when we have data to back it) |
| "End-to-end incident management" | We don't replace your alerting, observability, or incident comms tools. Positions us incorrectly. | "on-call intelligence layer," "on top of PagerDuty/OpsGenie" |
| "Automatically" (for routing) | Routing makes a suggestion; the engineer or manager accepts it. Nothing is fully automatic. | "suggests the right engineer," "recommends based on past resolutions" |

---

## Sales One-Liner (for AEs)

**For discovery calls and qualification**:

> "Sentinel plugs into PagerDuty or OpsGenie and does three things: captures runbooks at incident close so knowledge doesn't walk out the door, routes alerts to the engineer most likely to resolve them fast, and gives managers a Hero Dependency Index so they can see who's carrying too much on-call before it becomes a retention problem."

**Shorter version for cold email P.S. lines**:

> "Sentinel gives engineering teams runbook capture, experience-based routing, and a burnout risk dashboard — on top of PagerDuty/OpsGenie."

**When asked "what's the ROI"** (until we have hard data from GA):

> "Our beta cohort saw MTTR drop from 47 to 39 minutes in the first 30 days. Our target is 28 minutes at 60 days as runbook coverage grows. We measure it for you."

---

## Launch Messaging Don'ts for the AE Team

- Do not promise features that are on the roadmap but not in MVP (ML routing, Slack bot commands, SCIM provisioning)
- Do not position Sentinel as a replacement for PagerDuty/OpsGenie — we sell alongside them, not against them
- Do not quote MTTR improvement numbers beyond what beta data supports; "up to X%" without context creates expectation problems
- Do not lead with the HDI dashboard in first demos — lead with the runbook capture flow. The HDI is a wow moment, but only after the prospect understands the knowledge problem we're solving.

---

## Beta Launch Checklist

- [ ] In-app announcement modal live in production for beta customers (5 accounts)
- [ ] Launch email sent to beta contacts (engineering manager role, primary contact)
- [ ] CS team briefed on feature set and FAQ for first 2 weeks
- [ ] Feedback channel created (Slack shared channel or in-app feedback widget)
- [ ] AE team has updated one-pager and objection handling doc
- [ ] Public launch blog post drafted (do not publish until full launch in 2 weeks)
- [ ] Pricing page updated to reflect Sentinel as a standalone product (confirm with leadership)
