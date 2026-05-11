# Hard Decisions

Three narratives about product calls that didn't have an obvious right answer. What the situation was, how I reasoned through it, what I decided, and what I'd do differently.

---

## 1. Killing a Feature 3 Weeks Before Launch

**The situation**

We were three weeks from launching a "Team Goals" feature — a way for managers to set and track team OKRs directly inside Pulse. It had been in development for two months. Design was done, engineering was 80% complete, and we'd already told three enterprise prospects it was coming in Q3.

Two weeks before the planned launch, I ran 5 usability tests. The results were bad. Not "needs polish" bad — "wrong mental model" bad. Users consistently tried to attach goals to individual contributors, not to teams. Our data model didn't support that. When they discovered it didn't, 3 of 5 testers said something like "oh, then this doesn't really work for how we use OKRs."

The engineering effort to fix the data model was 4 weeks minimum. We could either: (a) ship what we had and iterate, (b) delay 4 weeks and fix it, or (c) shelve the feature entirely and cut scope.

**How I reasoned through it**

The "ship and iterate" argument was tempting but wrong. This wasn't a polish problem — it was a structural mismatch between the feature's model and how users think. Shipping it would mean 3 enterprise prospects onboarding onto a feature that didn't match their mental model, giving them a bad first impression of a new surface area, and then forcing a migration when we fixed it. The cost of the migration wasn't just engineering time — it was trust.

The "delay 4 weeks" argument was also wrong. We were in Q3. A 4-week delay pushed launch to October, outside our OKR window, and forced the engineering team to context-switch back onto something they thought was done. The sunk cost of 2 months was real but irrelevant to the decision — the question was whether 4 more weeks of investment was worth it right now.

Shelving felt like failure but was the right call. We had a working feature that solved a real problem — just not the way users expected it to be solved. Shipping it would create technical debt, user confusion, and a reputation for launching things that don't quite work.

**What I decided**

I shelved the feature, wrote a one-page postmortem explaining the usability findings to the team and the three prospects, and committed to Q1 delivery with the corrected data model. With the prospects, I was direct: "We ran usability tests and found a structural issue that would make this frustrating to use. We're delaying to fix it rather than ship something you'd be unhappy with."

Two of the three prospects said some version of "thank you for telling us before we launched, not after." The third was annoyed and fair to be annoyed — we'd put it in their decision criteria.

**What I'd do differently**

Run the usability tests at week 4, not week 8. The structural problem was visible in the wireframes. I deferred user testing until engineering was far along because I was worried about the overhead of running sessions mid-build. That's backwards — the cost of a finding at week 4 is a redesign; the cost at week 8 is a shelved feature.

---

## 2. Pushing Back on an Exec's Pet Feature

**The situation**

At the Q2 planning meeting, the VP of Sales asked us to build a "Manager Report Card" — a weekly email to executives summarizing how each manager on their team was performing on Pulse metrics. The ask came with a business justification: two enterprise deals were stalled partly because executives couldn't demonstrate ROI to their CFOs without aggregated data.

On the surface, it seemed reasonable. In practice, I thought it was a mistake.

My concern: Pulse's product-market fit was with managers, not executives. Our NPS from managers was +44. The few times we'd built executive-facing features, engagement was low and support tickets were high — executives would share the report with a manager who'd call us confused about why their "report card" showed a low score during a week they were on vacation.

The VP of Sales had real leverage. Those two deals were worth $240k ARR combined.

**How I reasoned through it**

I separated the business problem from the proposed solution. The business problem — closing two deals that needed executive ROI visibility — was real and urgent. The proposed solution — a Manager Report Card — was one way to solve it, not the only way.

I did two things before the next meeting. First, I called the two prospect contacts directly to understand what their CFOs actually wanted to see. What I found: they didn't need per-manager scorecards. They needed a simple account-level dashboard showing aggregate usage, trend lines, and one-sentence ROI summary. Much smaller scope, no individual manager exposure.

Second, I documented the support cost of our last executive-facing feature — we'd fielded 23 tickets in 6 weeks from a feature used by fewer than 100 executives. I put a rough cost on that: ~$4,200 in CS time.

**What I decided**

I went back to the VP of Sales with a counter-proposal: an executive summary dashboard (1 page, account-level, read-only) that specifically addressed what the two CFOs had asked for. I committed to shipping it in 3 weeks instead of the 6-week estimate for the full report card.

The proposal was accepted. We shipped the dashboard. Both deals closed. One manager report card ticket was filed in the first 90 days.

**What I'd do differently**

I waited too long to engage directly with the prospects. I spent a week internally modeling the tradeoffs before making the two phone calls that immediately clarified what was actually needed. The calls should have been day 1, not day 7. Customer proximity resolves stakeholder debates faster than any internal analysis.

---

## 3. Shipping with a Known Bug

**The situation**

On the Thursday before a Monday launch, QA found a bug: the weekly digest showed incorrect collaboration scores for teams with fewer than 5 members. The score displayed as 0 instead of the correct calculated value.

We had approximately 340 affected teams in the database. Most were on free or starter plans. The bug was in a normalization function — fixable, but the fix required a data migration and a re-run of the aggregation job.

The engineering estimate was 3–4 days to fix properly. That meant delaying the launch to Wednesday at best, or shipping with the bug on Monday.

**How I reasoned through it**

The instinct to delay was strong. Shipping a bug feels like shipping a broken product. But I forced myself to assess the actual impact precisely.

340 teams would see a 0 where a real score should appear. Those teams had 5 or fewer members — nearly all were free-tier accounts or very small starter accounts. The digest was new, so these teams had no baseline expectation to violate. The 0 score was clearly wrong (no team has a 0 collaboration score), which meant it was likely to generate a support ticket rather than silently mislead.

The alternative — delay the full launch by 4+ days — would affect all 18,000 eligible managers who'd been told the digest was launching Monday. We'd already sent an announcement to CS and had two enterprise sales calls scheduled for Tuesday that referenced the launch.

I also looked at the nature of the bug. It was isolated to the score display — it didn't affect delivery, open tracking, or any of the other digest sections. The fix was known and bounded.

**What I decided**

Ship Monday with the bug, fix by Wednesday, do proactive outreach to affected accounts. I wrote the fix ticket with a P0 priority and got a commitment from engineering that it would be live by EOD Wednesday. I also wrote the CS talking points so support was ready if tickets came in.

The launch went live Monday. We received 7 support tickets from affected accounts over 3 days. Engineering shipped the fix Wednesday morning. CS reached out proactively to all 340 affected accounts with a note explaining what had happened and that it was now resolved.

**What I'd do differently**

The bug should have been caught in QA a week earlier, not 4 days before launch. Our QA process tested with fixture data that happened to always have 5+ members. Adding edge case test data — including small teams — to the standard fixture set was an obvious gap. I added it to the Definition of Done for any feature touching aggregation logic after this, but it should have been there already.

The harder question: was shipping with the bug the right call? I still think yes. The impact was limited, the fix was fast, and the alternative was worse. But I've seen this type of reasoning used to rationalize shipping genuinely bad quality. The difference is in the rigor of the impact assessment. "It affects a small segment" only justifies shipping if you've precisely measured the segment and understood the actual harm — not just assumed it's small.
