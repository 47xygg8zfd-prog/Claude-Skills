# Example Output: Tech Translation Skill

**Prompt used:** "Engineers said the digest aggregation job needs to be idempotent and we should avoid thundering herd on the email provider. Translate this for me."

---

## Translation: Digest Engineering Concerns

---

### "The job needs to be idempotent"

**What it means in plain language:**  
The engineers want the digest calculation job to be safe to run multiple times without causing problems. If the job runs, fails halfway through, and has to restart — or if it accidentally gets triggered twice — it should produce the same result as if it ran once cleanly.

**Why it matters for you:**  
Without idempotency, a failed job that partially ran could send some managers duplicate emails, or send no email at all, with no clean way to recover. With it, the on-call engineer can simply re-run the job and trust the outcome.

**What to watch for:**  
If there are incidents where the job fails, recovery will be straightforward. No manual cleanup, no "who got the email twice?" support tickets.

---

### "Avoid thundering herd on the email provider"

**What it means in plain language:**  
Right now, every digest email for every manager is scheduled to go out at exactly 9am on Monday. If 18,000 emails all fire at the same millisecond, it's like 18,000 people trying to walk through a revolving door at once — the email provider (SendGrid) gets overwhelmed, some emails fail or get delayed, and we might get rate-limited or flagged as spam.

"Thundering herd" is the term for when a large number of requests all hit a system at the same time, causing it to buckle.

**Why it matters for you:**  
If we don't address this, Monday morning delivery might be unreliable — especially as we scale to more users. Managers expecting a 9am digest might get it at 11am, or not at all.

**What they're proposing:**  
They'll stagger sends across a delivery window (e.g., 8:45–9:15am) so SendGrid receives a steady stream instead of a spike. From a manager's perspective, they'll get the email "around 9am" — functionally identical, technically much safer.

**Your call:**  
Do you want the delivery window to be 15 minutes, 30 minutes, or up to 1 hour? Wider window = safer delivery, but some managers get it slightly later than others. Recommendation: 30-minute window is a reasonable default.
