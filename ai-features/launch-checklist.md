# AI Feature Launch Checklist

Run through this before shipping any AI-powered feature to production.

---

## 1. Quality

- [ ] Eval set exists with ≥50 real input examples (not all synthetic)
- [ ] Expected outputs written for all eval examples
- [ ] Pass rate on eval set ≥85% for common cases
- [ ] Pass rate on eval set ≥70% for edge cases
- [ ] Red-teaming session completed — failure modes documented
- [ ] Hallucination rate assessed and acceptable for use case
- [ ] Silent failure modes identified and mitigated (wrong output that looks right)
- [ ] Graceful degradation implemented (what happens when the model fails or times out?)

---

## 2. User Experience

- [ ] Human-in-the-loop level defined: Auto-applied / Suggested / Draft only
- [ ] Loading state handles latency — streaming or skeleton UI implemented
- [ ] Error state defined — user sees a helpful message, not a raw API error
- [ ] Feedback mechanism in place (thumbs up/down, edit tracking, or explicit rating)
- [ ] Output clearly labeled as AI-generated where relevant
- [ ] Undo / revert available if output is auto-applied

---

## 3. Measurement

- [ ] Layer 1 metric defined: pass rate tracking via automated eval on production traffic
- [ ] Layer 2 metric defined: acceptance rate, edit rate, or equivalent
- [ ] Layer 3 metric defined: business outcome tied to an OKR KR
- [ ] A/B test configured (feature ON vs. OFF) — minimum 2-week run planned
- [ ] Dashboard created covering model health, user behavior, and business impact
- [ ] Alerts set for: pass rate drop, latency spike, error rate spike

---

## 4. Cost & Performance

- [ ] Token cost per request estimated
- [ ] Monthly cost projected at current and 12-month usage volume
- [ ] Prompt caching implemented for static context (if applicable)
- [ ] p95 latency measured and within acceptable range for the use case
- [ ] `max_tokens` set to cap output length
- [ ] Rate limit handling implemented (retry logic with exponential backoff)

---

## 5. Safety & Trust

- [ ] PII / sensitive data handling reviewed — is user data sent to the model API? Is that acceptable per your privacy policy?
- [ ] Prompt injection risks assessed for any feature that takes user input as part of the prompt
- [ ] Output filtering in place for any user-visible content (block harmful outputs)
- [ ] Logging in place for all model inputs and outputs (required for debugging, may require consent)
- [ ] Data retention policy for logged AI inputs/outputs defined

---

## 6. Rollout

- [ ] Feature flag configured — can be turned off without a deploy
- [ ] Rollout plan defined: % of users, by what criteria (plan tier, cohort, geography)
- [ ] Rollback criteria defined: what metric threshold triggers an immediate rollback?
- [ ] On-call runbook updated with AI feature failure modes and responses
- [ ] CS team briefed: what the feature does, what errors users might see, how to handle feedback

---

## 7. Post-Launch

- [ ] Week 1 review scheduled: pass rate, acceptance rate, cost vs. projection
- [ ] Week 4 review scheduled: A/B test readout, business impact assessment
- [ ] Eval set update process defined: how will you add new examples as you discover edge cases?
- [ ] Prompt version control in place: can you roll back to a previous prompt if quality regresses?

---

## Sign-off

| Role | Reviewer | Sign-off |
|------|----------|----------|
| PM | | ☐ |
| Eng lead | | ☐ |
| Design | | ☐ |
| Security / Legal (if PII) | | ☐ |
