# PRD: Bridge — Technical Translator for PMs

**Author**: Jordan (PM) | **Date**: May 2026 | **Status**: Draft  
**Eng lead**: Sam | **Design lead**: Priya | **Jira Epic**: PULSE-BRIDGE-001

---

## Problem Statement

Product managers at mid-market B2B SaaS companies spend significant time in meetings, Slack threads, and GitHub PRs where they encounter technical language they don't fully understand — yet admitting confusion creates friction with engineering teams and erodes credibility. In discovery interviews with 24 PMs (March 2026), 19 reported that they regularly nod along to technical explanations they don't understand, then spend 20–40 minutes afterward trying to decode the content privately using generic AI tools, Google, or by asking a sympathetic engineer. This translation tax slows decision-making, produces requirements documents with subtle misalignments, and quietly degrades PM-engineering trust over time.

---

## Goals & Success Metrics

| Goal | Metric | Baseline | Target |
|------|--------|----------|--------|
| PMs adopt Bridge as a regular part of their workflow | Weekly active PMs (opened Bridge and ran at least one query) | 0 (new product) | 1,200 WAU at 90 days post-launch |
| Explanations are accurate and useful | Explanation quality rating (thumbs up/down + optional 1–5 stars, collected inline) | 0 (new product) | ≥ 4.1 / 5.0 average; < 8% thumbs-down rate |
| Bridge meaningfully reduces the time PMs spend confused | Time-to-understanding (self-reported, sampled via in-product prompt: "Did this resolve your question?") | ~28 min (discovery benchmark, DIY methods) | ≤ 5 min median |
| PMs trust Bridge's output enough to act on it externally | "Forwarded to engineer" rate (user clicks "Share explanation" or copies output within 60 sec of reading it) | 0 (new product) | 22% of sessions result in a forward or copy action |

**Primary success metric**: Weekly active PMs who return two or more weeks in a row (retained WAU). A tool PMs use once is a novelty; one they return to is infrastructure.

---

## Non-Goals (v1)

1. **Generating technical documentation or specs on behalf of PMs.** Bridge explains; it does not produce. v1 is a translator, not a writer. If PMs want AI-assisted spec writing, that is a separate product surface with different quality requirements. Conflating the two in v1 risks scope creep and muddies the core value prop.

2. **Real-time transcription or meeting assistance.** Integrating with Zoom or Google Meet to translate jargon spoken aloud in engineering standups is technically feasible but requires audio permissions, latency handling, and a materially different UX. This is a v2 consideration after we validate the core paste-and-explain workflow.

3. **Code review or code quality feedback.** Bridge is for PMs, not engineers. If a PM pastes a code snippet, Bridge explains what it does in plain English — it does not evaluate whether the code is well-written, suggest refactors, or flag bugs. Adding a code-quality layer would confuse the target user and compete with GitHub Copilot and Sourcegraph on their home turf.

4. **Org-level or team-scoped knowledge bases.** v1 explanations are stateless — Bridge explains the content you paste without reference to your company's specific tech stack, architecture decisions, or internal terminology. Building a persistent knowledge layer (e.g., "at Acme Corp, 'the pipeline' refers to the ETL job that runs at 3am") is a high-value v2 feature that requires data modeling and privacy review not scoped for this release.

5. **Integration with Jira, GitHub, or Slack as a native plugin.** v1 ships as a standalone web app (and optionally a Chrome extension for paste workflows). Native plugin integrations with each tool require separate API approval processes, platform review cycles, and ongoing maintenance. We will validate demand via the standalone product before committing to integration engineering.

6. **Automated glossary building or "learn from your corrections."** PMs will sometimes disagree with Bridge's explanations. v1 captures that feedback (thumbs down + optional comment) for model improvement, but does not expose a user-facing glossary editor or let users teach Bridge custom definitions. That feedback loop is a v2 feature once we have enough correction signal to model well.

---

## User Stories

1. **The PR comment PM.** As a PM who received a GitHub PR review comment referencing "N+1 queries" and "missing index," I want to paste that comment into Bridge and get a plain-English explanation of what the engineers are debating and why it matters for our sprint timeline, so that I can participate meaningfully in the discussion instead of waiting for someone to summarize it for me in Slack.

2. **The architecture meeting PM.** As a PM preparing to sit in on a backend architecture review about migrating from a monolith to microservices, I want Bridge to explain the core trade-offs in 90 seconds before the meeting, so that I can ask informed questions instead of nodding politely and pretending to take notes.

3. **The requirements writer.** As a PM drafting acceptance criteria for a feature that requires an API change, I want Bridge to help me understand what "idempotent endpoint" and "rate limiting" mean in context, so that my requirements doc doesn't contain subtle misunderstandings that waste engineering time during sprint planning.

4. **The sales-assist PM.** As a PM who has been looped into a sales call where a technical prospect is asking about our "data residency guarantees" and "SOC 2 Type II controls," I want Bridge to give me a confidence-calibrated explanation of what those terms mean and what questions I should ask our security team before the call, so that I don't embarrass myself or over-promise to the prospect.

5. **The async PM.** As a PM working across time zones whose engineering team is in Bangalore, I want to paste a Slack thread containing a debate about "eventual consistency vs. strong consistency" and get an explanation I can understand at 9am my time without waking anyone up, so that I can unblock my own understanding and make a product decision before the daily sync.

---

## Requirements (MoSCoW)

### Must Have

- [ ] **Paste any technical content and receive a plain-English explanation within 10 seconds.**  
  Why (from research): 19 of 24 interviewed PMs said their current workaround (Google, generic AI, asking an engineer) takes 20–40 minutes and often fails. A sub-10-second response is the threshold that makes Bridge feel like a tool, not a process. Latency above 30 seconds caused abandonment in prototype testing.

- [ ] **Context-aware explanations that understand the user is a PM, not an engineer.**  
  Why (from research): Generic AI tools (ChatGPT, Claude.ai) were reported as "too technical" or "still confusing" by 14 of 19 PMs who tried them. The explanation register matters — Bridge must default to "smart non-technical adult" framing, not "computer science peer review." This is achieved via system prompt design and onboarding calibration, not a toggle.

- [ ] **"Go deeper" toggle that reveals a more technical follow-up layer on demand.**  
  Why (from research): 8 of 24 interviewed PMs described themselves as "technical enough to want more" but didn't want technical depth by default. The toggle preserves the default simplicity for non-technical PMs while giving technically-inclined PMs a path to more. Without it, Bridge either over-explains (alienates) or under-explains (fails the curious).

- [ ] **Confidence indicator on each explanation (e.g., "High confidence," "Medium — this term has multiple meanings in context," "Low — the input was ambiguous").**  
  Why (from research): The "forwarded to engineer" use case — a PM sharing Bridge's output directly in Slack or a doc — requires that PMs know when to trust the output and when to verify. Without a confidence signal, PMs either over-trust (and forward incorrect explanations) or under-trust (and don't use Bridge for sharing at all). This is the feature that separates Bridge from ChatGPT in user perception.

- [ ] **Conversation mode: follow-up questions within the same context window.**  
  Why (from research): 16 of 24 PMs said their confusion is iterative — "I understand the first explanation but then I have a follow-up." A stateless Q&A tool that resets after each answer forces PMs to re-paste context and re-explain their situation. Conversation mode is the minimum bar for Bridge to feel like a knowledgeable colleague rather than a search engine.

### Should Have

- [ ] **Onboarding calibration flow (3–5 questions about PM's technical background) to tune explanation depth automatically.**  
  Reduces the need to manually adjust every session. Lower-priority than core flow but significantly improves Day 1 experience and reduces thumbs-down rate from over/under-explaining.

- [ ] **"Share explanation" button that generates a clean, shareable version of the explanation** (stripped of UI chrome, formatted for Slack or email).  
  Directly supports the "forwarded to engineer" success metric. Deprioritized from Must Have because raw copy-paste covers the use case at launch; the formatted share is a polish layer.

- [ ] **Input type detection** — Bridge recognizes whether the pasted content is a GitHub PR comment, a Jira ticket description, a Slack message, or a generic technical paragraph, and frames the explanation accordingly.  
  Improves explanation quality without requiring user effort. Deferred from Must Have because v1 can deliver acceptable quality without it; this is a quality-of-life improvement.

- [ ] **Explanation history** — the last 20 explanations are saved per user session (not persisted cross-session in v1).  
  PMs frequently return to the same thread or ticket. Without history, they re-paste the same content. Session-scoped history is the minimum useful version.

- [ ] **Mobile-responsive layout.**  
  PMs encounter technical jargon on their phones (Slack notifications, email). Mobile-responsive is table stakes for any web tool in 2026 but is deprioritized from Must Have because the primary workflow (paste from desktop) is desktop-first.

### Could Have

- [ ] **Browser extension with right-click-to-explain** — select any text on any page, right-click, and get a Bridge explanation in a popover.  
  High user delight, low discovery friction, but adds a separate deployment and review surface (Chrome Web Store). Post-launch if core product shows retention.

- [ ] **Jira and GitHub read-only integration** — Bridge fetches ticket or PR content directly from a URL instead of requiring manual paste.  
  Removes one step from the workflow. Requires API credential storage and OAuth flows. Valuable but not blocking validation.

- [ ] **Weekly "Technical Concept of the Week" digest for Bridge users** — one concept explained in Bridge's voice, delivered via email.  
  Brand-building, engagement driver, and positions Bridge as a learning tool, not just a lookup tool. Low engineering cost (editorial-driven), medium marketing cost.

- [ ] **Explanation rating breakdown by concept category** (infrastructure, security, data, frontend, APIs) to help Bridge's model improve by domain.

### Won't Have (v1)

- [ ] Real-time meeting transcription and live translation (see Non-Goals)
- [ ] Code quality review or engineering feedback (see Non-Goals)
- [ ] Persistent org-level knowledge base (see Non-Goals)
- [ ] Native Jira / GitHub / Slack plugin (see Non-Goals)
- [ ] User-editable glossary (see Non-Goals)
- [ ] Audio or video input

---

## Open Questions

| # | Question | Owner | Target Date | Consequence if Unresolved |
|---|----------|-------|-------------|--------------------------|
| 1 | What is the right confidence threshold model? How do we determine "High" vs. "Medium" vs. "Low" confidence programmatically — is this based on LLM log-prob, input ambiguity scoring, or a heuristic we label manually? | Sam (Eng) | June 6, 2026 | If unresolved, confidence indicator ships as a static label or is cut from v1 — losing the key differentiator from ChatGPT in user perception. |
| 2 | Do we need legal review of the "forwarded to engineer" share feature? If a PM shares a Bridge explanation of a security concept with an engineer and it's subtly wrong, what is our liability exposure? | Jordan (PM) + Legal | June 13, 2026 | If unresolved, "Share explanation" feature may need to ship with a disclaimer footer, which reduces perceived confidence and may suppress the forwarding behavior we're trying to measure. |
| 3 | What is the onboarding calibration question set? We have a hypothesis for 5 questions (role, technical background, primary tools, most common confusion contexts, prior AI tool use) but have not validated with users whether this feels invasive or helpful at sign-up. | Priya (Design) | June 6, 2026 | If unresolved, onboarding ships without calibration and defaults to a middle-ground explanation register that may feel generic to both technical and non-technical PMs. Impacts quality rating in first 30 days. |
| 4 | How do we handle inputs that are not technical? If a PM pastes a legal clause, a financial model, or a marketing brief, does Bridge explain it, decline, or redirect? We need a defined out-of-scope content policy. | Jordan (PM) | May 30, 2026 | If unresolved, Bridge either fails visibly (confusing error) or explains non-technical content (scope creep that muddies the product identity and dilutes model performance). |
| 5 | What model do we use at launch, and what is the cost-per-query at 1,200 WAU assuming 8 queries/session? At current API pricing, 1,200 WAU × 8 queries × estimated token volume puts us at ~$14K–$22K/month. Is that within unit economics for the pricing tier we're planning? | Sam (Eng) + Alex (Data) | June 6, 2026 | If unresolved, we may launch at a price point that is structurally unprofitable or be forced to rate-limit heavy users in a way that damages the experience for our best users. |
| 6 | Should conversation mode use a persistent server-side context window or a client-side accumulated prompt? Server-side is better UX (survives tab refresh) but adds session storage infrastructure. Client-side is simpler but fragile. | Sam (Eng) | June 13, 2026 | If unresolved, conversation mode ships in the simpler client-side form, which is acceptable for v1 but creates a noticeable regression if the user refreshes mid-conversation. |
