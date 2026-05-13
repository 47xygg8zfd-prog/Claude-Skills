# Prioritization Framework: RICE + MoSCoW

RICE is a scoring model. It doesn't make decisions — you do. What it does is force you to make your assumptions explicit, which makes it easier to disagree productively and harder to sneak intuition past stakeholders dressed as analysis.

---

## The RICE Formula

**RICE Score = (Reach × Impact × Confidence) / Effort**

### Reach
**Definition**: How many users will this affect per quarter?

**Practical guidance**: Count unique users, not events. "10,000 events" from 200 users is 200. Use your actual active user count as a denominator and be honest about the segment. A feature that only affects enterprise accounts on a 20-account base is a Reach of 20, not 10,000.

**Common mistake**: Inflating Reach by including users who could theoretically be affected vs. users who will actually encounter this in their normal workflow.

### Impact
**Definition**: How much will this move the needle for each user it reaches?

**Practical guidance**: Use a fixed scale: Massive = 3, High = 2, Medium = 1, Low = 0.5, Minimal = 0.25. Don't invent fractional scores — the false precision costs more than it's worth. Ask: "If a user encounters this feature, does it meaningfully change their behavior or outcome?" If you're not sure, default to 0.5 and revisit after talking to users.

**Common mistake**: Conflating "users will like this" with "this will move the metric."

### Confidence
**Definition**: How confident are you in your Reach and Impact estimates?

**Practical guidance**: Use percentages: 100% = strong data (multiple research sources, quantitative validation), 80% = some data (one user research study, qualitative signal), 50% = hypothesis (informed guess, no direct evidence). If you feel the urge to write 100%, ask yourself what evidence would change your mind. If nothing would, that's a belief, not a confidence score.

**Common mistake**: Using 100% confidence for everything. This makes RICE useless as a comparison tool because it stops penalizing uncertainty.

### Effort
**Definition**: How many person-weeks does this take across the full team?

**Practical guidance**: Include engineering, design, and PM time. A feature that takes Sam's team 2 weeks but requires 3 weeks of Priya's design time is 5 person-weeks, not 2. Don't let Effort become a pure engineering estimate.

---

## Worked Example

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| Slack digest ping | 400 | 2 | 80% | 1 | 640 |
| Sprint predictability alerts | 300 | 3 | 50% | 3 | 150 |
| Custom report builder | 200 | 2 | 50% | 8 | 25 |
| Digest open tracking | 500 | 1 | 100% | 0.5 | 1000 |
| Mobile app (MVP) | 350 | 2 | 50% | 20 | 17.5 |

**The narrative**: Digest open tracking scores highest on RICE — it's low effort, high reach, and we have strong data. Ship it. Slack digest ping scores second and directly supports digest-active WAU, our north star. Worth doing in Q2.

Sprint predictability alerts score low because confidence is weak — we've heard it from a few customers but haven't validated at scale. The right call is to run a research spike before committing sprint capacity, not to build based on a 150 RICE score.

**When to override the model**: The mobile app scores 17.5. If a key enterprise account makes mobile a contract condition, you build it anyway. RICE reflects averages across your user base — it doesn't capture strategic commitments, competitive responses, or existential risks. When you override RICE, write down why. That's the honest part.

---

## When NOT to Use RICE

- **Clear strategic bet**: If the CEO and board have aligned on a direction, RICE scoring it is theater. Run the project, manage it well.
- **All scores are similar**: If five options score within 10% of each other, you don't have a prioritization problem — you have a strategy problem. Go upstream.
- **Time-sensitive decision**: RICE takes time to do honestly. If you need to decide in 30 minutes, use your judgment and document the rationale.

---

## MoSCoW as a Complement

Use RICE to rank across options. Use MoSCoW to gate within a feature.

RICE tells you which feature to build next. MoSCoW tells you what the smallest useful version of that feature looks like. The two frameworks work together: RICE at the roadmap level, MoSCoW at the scope level. Don't conflate them.
