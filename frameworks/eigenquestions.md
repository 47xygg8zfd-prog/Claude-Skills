# Eigenquestions

## What It Is

An eigenquestion is the question whose answer determines the answers to most other questions in a problem space. The term comes from linear algebra (eigenvectors are the vectors that define the fundamental directions of a transformation) and was popularized in PM circles by Shreyas Doshi.

The insight: in any complex product or strategy problem, there are usually 1-3 questions that act as load-bearing walls. If you answer those, many other questions resolve themselves. If you don't answer those, no amount of analysis elsewhere makes progress.

Most product discussions spend time on derivative questions — questions whose answers depend on a prior question that hasn't been resolved. Finding the eigenquestion means finding the prior question.

---

## When to Use It

- Strategy debates that keep cycling without resolution
- Roadmap planning where the team can't align on priorities
- Disagreements between stakeholders that feel intractable
- Any situation where "it depends" is the honest answer — it depends on what?
- Before a quarterly planning cycle, to identify what needs to be decided first

---

## How to Apply It

### Step 1: List the questions in the room
Write down every question the team is debating. Don't filter — capture the surface-level questions as stated.

### Step 2: Ask "what does the answer to this depend on?"
For each question, push one level deeper. If the answer to Question A depends on answering Question B first, then B is more fundamental than A.

### Step 3: Find the dependencies
Draw the dependency graph. Questions at the bottom of the dependency tree — the ones everything else depends on — are your eigenquestion candidates.

### Step 4: Test the eigenquestion
A true eigenquestion has this property: if you could answer it right now, most of the other questions would resolve or become obviously answerable. Ask: "If we knew the answer to this, which other questions would we be able to answer?"

### Step 5: Direct energy there
Stop debating derivative questions. Put all your research, data gathering, and decision-making energy into the eigenquestion first.

---

## Worked Example: Pulse Q3 Planning

**Surface-level questions in the room:**
- Should we build a mobile app?
- Should we add SSO?
- Should we build a weekly digest?
- Should we invest in custom dashboards?
- Should we build API access?

**Pushing one level deeper:**
- Mobile app: "Is low engagement a device problem or a habit problem?"
- Digest: "Is low engagement because users don't have a pull mechanism, or because the product doesn't have enough value?"
- SSO: "Is enterprise growth blocked by missing features, or by sales capacity?"

**The eigenquestion:**
> **Is low engagement (68% of users log in < 2×/week) a habit formation problem or a product value problem?**

If it's a **habit formation problem**: the solution is passive delivery (digest). Build the digest.  
If it's a **product value problem**: passive delivery won't help — the user tries it and still doesn't find value. The solution is deeper features (custom dashboards, API).

This single question determines whether the digest is the right bet or a distraction.

**How it was answered:** Customer research. 7/8 interview participants said they know the value is there — they just don't remember to check. That's a habit problem, not a value problem.

**Result:** The digest is the right Q3 bet. Mobile, custom dashboards, and API move to later cycles.

---

## Common Mistakes

**Mistaking a complicated question for the eigenquestion.**  
Hard questions aren't always load-bearing. The eigenquestion is the one everything else depends on — not the one that requires the most research.

**Having two eigenquestions when there's actually one.**  
Push further. If you have two candidate eigenquestions, ask: does answering one of them determine the answer to the other?

**Answering the eigenquestion with the wrong method.**  
Once you've found the eigenquestion, the method for answering it matters enormously. A strategy question answered by a survey will produce noise. A product question answered by a board discussion will produce politics. Match the question to the right evidence type.

**Using eigenquestions as a reason to delay.**  
"We can't decide anything until we answer the eigenquestion" becomes an excuse for inaction. Set a deadline for resolving the eigenquestion. If you can't get clean data, make your best judgment and note the assumption.

---

## Connections

- Use with **[Pre-Mortem](pre-mortem.md)** to find eigenquestions about risk: "What's the question whose answer determines whether this project fails?"
- Use with **[Playing to Win](playing-to-win.md)** to find the strategic eigenquestion: "What's the question whose answer determines which of our strategic choices is correct?"
- The `customer-research-synthesis` skill is often the right tool for answering eigenquestions about user behavior
- The `feature-prioritization` skill makes more sense after the eigenquestion is answered — prioritizing before you've resolved the load-bearing question produces a roadmap built on sand
