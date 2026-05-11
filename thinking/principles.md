# PM Principles

These are the beliefs I've formed about product decision-making — not rules I follow, but positions I've arrived at through experience and argument. I hold them strongly enough to act on them and loosely enough to update when I'm wrong.

---

## On problems

**Start with the problem, not the solution.**  
The most common source of bad product decisions is treating a solution as a given. "We need to build X" is not a product brief — it's a hypothesis that X is the best way to solve some problem. State the problem first. Let the solution emerge.

**The customer's stated problem is usually real. Their stated solution usually isn't.**  
"We need a way to export this to Excel" is a real signal. It means someone is doing downstream work you haven't accounted for. The right response is to understand that downstream work, not to build an Excel export. Sometimes the export is right. Often there's a better answer.

**A problem worth solving is specific enough to be falsified.**  
"Users are frustrated" is not a problem statement — it's a mood. "New users who complete onboarding but don't return within 7 days cite 'I couldn't find my team's data' as the primary reason" is a problem. If you can't imagine evidence that would prove your problem statement wrong, it isn't specific enough.

---

## On prioritization

**Opportunity cost is the most underused concept in product.**  
Every feature you build is a feature you didn't build. The question isn't "is this worth doing?" — it's "is this the most valuable thing we could do with this capacity right now?" Teams that forget this end up with full roadmaps and stalled metrics.

**Consensus is a bad prioritization method.**  
Roadmaps built by committee produce local optima — everyone's top priority gets a token commitment, nothing gets enough investment to actually move. Someone has to make the call. The PM's job is to make it with evidence, explain the reasoning, and commit.

**Deprioritizing is a product decision, not a failure.**  
The most important sentence in a roadmap presentation is "here's what we're not doing and why." Teams that can articulate their cuts are teams that understand their constraints. Teams that can't are teams that will surprise stakeholders every quarter.

---

## On data

**Data answers "what." It rarely answers "why" or "what next."**  
A dashboard can tell you that WAU dropped 18% last week. It cannot tell you whether that's a product problem, a marketing problem, a seasonal effect, or a data pipeline issue. The PM's job is to generate hypotheses and design the investigation — not just read the chart.

**Most A/B tests are underpowered.**  
A two-week test with 3,000 users detecting a 5% lift has approximately a coin-flip chance of being statistically valid. Before running an experiment, calculate the required sample size. If you don't have enough traffic to detect the effect size you care about, either run the test longer or accept that you're making a judgment call — which is fine, as long as you know that's what you're doing.

**Absence of evidence is not evidence of absence.**  
No one complained about the bug in the checkout flow. The flow has a 34% drop-off rate. These facts coexist because most users don't report problems — they just leave. Don't use support ticket volume as a proxy for product quality.

**Be suspicious of metrics that only go up.**  
Any metric that has never gone in the wrong direction is probably not measuring the right thing, is being measured wrong, or is being gamed. Good product metrics are uncomfortable sometimes.

---

## On decisions

**Most decisions are reversible. Treat them that way.**  
Jeff Bezos's two-door metaphor is right. The majority of product decisions — feature flags, copy changes, pricing experiments, UI tweaks — can be undone. The cost of moving fast on reversible decisions is low; the cost of treating them like irreversible decisions is high. Reserve deliberation for the decisions that genuinely can't be undone.

**Disagreement and commitment are compatible.**  
It's appropriate to say "I think we're making a mistake here, and I want that on record — and I'm fully committed to making this work." Silence in the meeting followed by disengagement after is not. If you disagree, say so. Then execute like you voted for it.

**Speed of decision is itself a product quality.**  
A product team that takes three weeks to make a scope decision has slower velocity than one that takes three days — regardless of what's in the sprint. Indecision is a decision to delay. Name it.

**Don't let perfect be the enemy of shipped.**  
There is a version of every feature that is clearly not ready to ship and a version that is clearly good enough. The PM's job is to find the second version and protect it from scope creep toward the first. Perfection is infinite; a release date is finite.

---

## On people

**Your job is to make the team right, not to be right.**  
The best product outcome comes from the best collective thinking, not from the PM's individual judgment. If an engineer has a better idea than what's in the PRD, that's a win. Create conditions where good ideas can surface from anywhere.

**Engineers are not velocity machines.**  
The people building your product have intuitions about users, constraints, and technical debt that no PRD captures. The best engineers will tell you when something is wrong, overscoped, or technically unsound — if you've built the relationship where that's safe to do. That relationship is worth protecting.

**Stakeholder trust is infrastructure.**  
You build it slowly through accurate forecasts, honest status updates, and delivered commitments. You lose it fast through surprises. Every "we're actually going to miss that date" that a stakeholder hears from you before they hear it from elsewhere is a deposit. Every surprise is a withdrawal. Most PMs are running a deficit without knowing it.

---

## On instinct

**Intuition is pattern-matching on past data you haven't surfaced yet.**  
When something feels wrong about a product decision and you can't explain why, that's worth investigating — not overriding. The feeling is usually pointing at a real constraint, past failure, or missing assumption. Find it.

**Strong opinions, loosely held — but actually loosely held.**  
Most PMs are good at the first part. Few are good at the second. "Loosely held" means genuinely updating when you see contradicting evidence, not rationalizing why the new data doesn't count. If you haven't changed a significant product opinion in the last 6 months, you're probably not actually looking.
