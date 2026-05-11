# PM Anti-Patterns

Common patterns that look like good product management but reliably produce bad outcomes. Most of these are well-intentioned. That's what makes them hard to catch.

---

## 1. The Solution in a Problem's Clothing

**What it looks like**  
The product brief says: "Users need a way to export their data to CSV." The team treats this as a problem statement and builds a CSV export.

**What's actually happening**  
A solution has been mistaken for a problem. "Users need X" is almost always a disguised feature request. The actual problem is downstream: users are doing something with that CSV that Pulse should probably help with directly.

**Why it happens**  
Customer requests are phrased as solutions. Sales escalations are phrased as solutions. It takes active effort to push past "what do you want?" to "what are you trying to accomplish?"

**The fix**  
Before scoping any feature, require a one-sentence problem statement that doesn't mention the proposed solution. "Users can't analyze team performance data in context with their other business metrics" is a problem. "Users need CSV export" is not.

---

## 2. Roadmap as Commitment

**What it looks like**  
The Q3 roadmap is shared with the company in April. By August, two of the five items haven't shipped, one shipped late, and one was descoped mid-quarter. The PM spends the back half of the quarter managing expectations.

**What's actually happening**  
The roadmap was shared as a commitment when it should have been shared as a plan. Plans change; commitments are supposed to hold.

**Why it happens**  
Stakeholders want certainty. PMs feel pressure to provide it. The quarterly planning meeting creates a deadline for the roadmap document, which creates the illusion that the roadmap is now fixed.

**The fix**  
Share roadmaps with explicit confidence levels: "shipping this quarter" vs. "targeting this quarter" vs. "exploring for next quarter." Treat quarterly roadmaps as bets you're making, not promises you're keeping. Reserve "commitment" language for the 2-week sprint, where scope is actually controllable.

---

## 3. Metric Theater

**What it looks like**  
The team ships a feature and reports that DAU increased 12% in the two weeks after launch. This is cited as evidence the feature worked. The OKR is marked green.

**What's actually happening**  
There's no control group, no accounting for seasonality, and no measurement of whether the right users are more active (or just the wrong ones). The 12% number is probably noise dressed up as signal.

**Why it happens**  
Showing metrics is expected; questioning metrics is uncomfortable. Teams that have shipped hard want the number to mean something. Confirmation bias is powerful.

**The fix**  
Require an A/B test or pre/post cohort analysis with a stated hypothesis before any metric is used as launch evidence. "We expected DAU to increase by X% based on Y users using the feature Z times per week" is a hypothesis. "DAU went up after we launched" is not evidence.

---

## 4. The Polite PRD

**What it looks like**  
The PRD has a "Goals" section that says things like "improve the user experience" and "increase engagement." The open questions section is empty. Engineering says the PRD is great.

**What's actually happening**  
The PRD avoided specificity because specificity requires commitment and invites disagreement. A vague PRD gets approved faster. It also produces worse products.

**Why it happens**  
Writing specific, measurable goals means being wrong in public. Writing vague goals means never being wrong. PMs who've been burned by missed targets learn to hedge in planning documents.

**The fix**  
Make vague goals unpublishable by convention. Every goal in a PRD should be a KR-style metric with a baseline and target. Every open question that hasn't been answered is blocking — if it isn't blocking, it isn't open.

---

## 5. Discovery Theater

**What it looks like**  
The team runs 5 customer interviews before the quarterly planning cycle. Insights are presented in an all-hands. The roadmap was already decided. The interviews don't change anything.

**What's actually happening**  
Research is being conducted to validate a decision that's already been made, not to inform a decision that hasn't. This is the most insidious anti-pattern because it looks exactly like good product practice.

**Why it happens**  
Roadmaps are often decided by leadership before research happens, and research is used to build buy-in rather than to generate insight. PMs who know the answer don't run research to find it — they run research to prove it.

**The fix**  
Research should be conducted before priorities are set, not after. If you already know the answer, skip the research and own the decision — pretending to discover what you already knew is worse than just deciding. If you're genuinely uncertain, run research with explicit hypotheses you're willing to be proven wrong on.

---

## 6. The Escalation Spiral

**What it looks like**  
An engineer raises a concern about scope in sprint planning. The PM says "let's take it offline." The offline conversation doesn't happen. The concern resurfaces in the sprint review. An exec asks why the concern wasn't caught earlier.

**What's actually happening**  
A mechanism for surfacing and resolving concerns doesn't exist, so concerns accumulate until they become crises. "Let's take it offline" is often a way of deferring discomfort, not scheduling a resolution.

**Why it happens**  
Sprint planning has a rhythm that resists interruption. Concerns that would break the rhythm get deferred. Deferred concerns compound.

**The fix**  
Name the decision that needs to be made and assign a deadline. "Let's take it offline" becomes "I'll talk to you by EOD Thursday about the timeline impact of that scope change." A named owner and a deadline makes the concern trackable instead of forgettable.

---

## 7. NPS as a Proxy for Product Quality

**What it looks like**  
The quarterly NPS survey comes back at +34. The team celebrates. Product quality is assumed to be high. The survey runs again next quarter.

**What's actually happening**  
NPS measures satisfaction at a moment in time for the subset of users who respond to surveys — typically the most engaged (and therefore most satisfied) users. It's a lagging indicator that smooths over the specific product quality problems that matter.

**Why it happens**  
NPS is a clean single number that's easy to report to execs. It feels like an objective measure of product quality. It isn't.

**The fix**  
Use NPS as a directional signal, not a quality gate. Pair it with: churn data (revealed preference, not stated preference), support ticket themes (what's actually breaking), and feature-specific satisfaction surveys for new launches. An overall NPS of +34 tells you nothing about whether your new onboarding flow is working.

---

## 8. Heroic Shipping

**What it looks like**  
Every quarter, the team ships by working nights and weekends in the final two weeks. Post-mortems cite "underestimation" as the root cause. The next quarter's estimates are slightly higher. The pattern repeats.

**What's actually happening**  
The team has learned that heroic effort at the end of a cycle is expected and normalized. Estimates are made knowing they'll be wrong because being wrong is fine as long as the work gets done eventually.

**Why it happens**  
Heroic shipping is rewarded (everyone praises the team for pulling it off) and underestimation is never penalized. The incentive structure creates the behavior.

**The fix**  
Protect the estimate by protecting the scope. When estimates are exceeded, the right response is "what do we cut?" not "how do we find more time?" Teams that learn scope is flexible will always underestimate; teams that learn scope is fixed will estimate honestly.

---

## 9. The Feature Factory

**What it looks like**  
The team ships 12 features in a quarter. Velocity is celebrated. OKRs are amber — the metrics didn't move as much as expected. Leadership asks for more features next quarter.

**What's actually happening**  
Output is being confused with outcome. Shipping features is not product management — moving metrics is. A team that ships 12 features and moves no metrics is worse than a team that ships 3 features that collectively change user behavior.

**Why it happens**  
Features are visible and countable. Metric movement is invisible until it isn't. Shipped features provide closure; outcomes require patience.

**The fix**  
Tie quarterly goals to outcomes, not outputs. "Ship digest, onboarding, and SSO" is an output goal. "WAU 32% → 42%" is an outcome goal. Outcome goals force the team to ask, before and after, whether what they're building is actually doing what they expected.

---

## 10. The Loudest Customer Problem

**What it looks like**  
A large enterprise customer complains loudly that they need feature X. The feature gets prioritized. It ships. The enterprise customer is satisfied. Four other customers quietly churn because you didn't ship feature Y, which would have helped all of them.

**What's actually happening**  
Priority is being set by vocal customers rather than by the distribution of customer needs. Large customers have more access to PMs and more weight in conversations. Quiet customers just leave.

**Why it happens**  
Customer conversations are vivid and personal; churn data is abstract. It's much easier to respond to a specific request from a specific person than to respond to a signal in a retention cohort table.

**The fix**  
Triage feature requests against the customer population, not the customer voice. "How many accounts have this problem?" is the first question. "How loudly has this been requested?" is largely irrelevant to prioritization. Use churn interview data, NPS verbatims, and support ticket volume as the passive signal from customers who aren't calling you.
