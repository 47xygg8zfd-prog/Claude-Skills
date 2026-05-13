# Three MVP Options: Bridge — Technical Translator for PMs
**Date:** 2026-05-13
**Author:** PM, Bridge
**Status:** Decision pending — present to CPO and Eng Lead before sprint 1 kickoff

---

## Context

This document follows the full discovery simulation, competitive analysis, devil's advocate review (File 06), and MVP scoping exercise (File 07). Three distinct MVP options are presented below. Each is a coherent, defensible strategic bet — not a good/better/best ranking. The recommendation section makes a decisive call; the decision framework translates that into observable signals so the team can update the decision if discovery findings contradict the current read.

---

## Option A: The Focused Tool ("Deep Explanation, Standalone")

**Strategic bet**: PMs will adopt a best-in-class standalone tool if it's dramatically better than ChatGPT for their specific context.

### What's in
M-01 through M-05: paste and explain, PM-role framing with decision-relevant output, Go Deeper toggle, confidence indicator, conversation mode. Web app only. No integrations, no browser extension, no team features.

### What's out
Browser extension (S-01), explanation history and search (S-02), team sharing (S-03), team glossary (C-01), Jira integration (C-02).

### Timeline
6 weeks to closed beta (15 design partners), 10 weeks to public waitlist launch.

### Pricing
Freemium — 20 free explanations per month, $12/month for unlimited. Free tier is a discovery mechanism, not a long-term growth strategy: it exists to fill the beta with non-design-partner PMs who signed up by choice, not obligation.

### Why this could win
A tool that is genuinely, obviously, demonstrably better than "paste into ChatGPT" for PM-specific technical explanation does not need workflow integration to generate word of mouth. If every explanation ends with a decision-relevant summary and a suggested follow-up question that a PM can bring directly to their tech lead, the value proposition is tangible and repeatable. Focus keeps the team from spreading across browser extension approvals, Jira API constraints, and team authentication infrastructure in the first 10 weeks. Quality goes up when scope goes down.

### Why this could fail
The Devil's Advocate review (File 06, Assumption 1) frames this precisely: a PM who already has ChatGPT open faces a high switching cost to open a new tab with a narrower use case. If the explanation quality difference is not immediately, viscerally obvious — if a PM has to use Bridge for three sessions before they notice the difference — the conversion from free to paid will be too low to sustain the product. Standalone adoption without workflow integration is historically hard for single-purpose tools competing against general-purpose AI. The freemium cap at 20 explanations may also hit before the PM has formed a habit, triggering a paywall at the worst moment.

### Key metric to hit
40% week-4 retention among beta users. This is a high bar for a standalone tool with no workflow integration and no team features. If the standalone web app cannot clear 40% retention, Option A's premise is falsified.

### Recommended if
Discovery interviews reveal that PMs who already use ChatGPT for technical explanations are consistently frustrated by output quality — specifically, that ChatGPT gives them information but not decision framing, and that they've had at least one experience where a confident-sounding ChatGPT answer was wrong in a way that caused a visible problem in a team meeting. If the pain is quality-and-trust, Option A addresses it directly. If the pain is "I don't think to look it up," Option A doesn't help.

---

## Option B: The Browser Extension ("In-Context, Zero Friction")

**Strategic bet**: The winning advantage is zero-switching-cost — explanations appear where PMs already work, so the PM never has to remember to open a separate tool.

### What's in
M-01 (explanation core), M-02 (PM-role framing, decision-relevant output), M-04 (confidence indicator). S-01: browser extension for Jira and Linear, surfacing explanations inline when the PM hovers over or highlights technical terms. Minimal web app as fallback and account management surface only — not the primary product.

### What's out
M-03 (Go Deeper toggle — too complex for an extension overlay UX at launch), M-05 (conversation mode — extension surface is not appropriate for multi-turn Q&A; available in the web app fallback), explanation history and search (S-02), team sharing (S-03), glossary (C-01), Jira auto-suggest (C-02).

### Timeline
8 weeks to closed beta. The extension takes longer than a web app: Chrome Web Store approval (typically 3–7 days), Firefox Add-ons review if included, and the UX complexity of injecting UI into Jira and Linear without breaking the host page's rendering. Plan for two weeks of integration debugging that a web-only build would not require.

### Pricing
$8/month flat. Freemium is not viable for a browser extension: usage caps require tracking explanation counts across pages, which adds state management complexity. A flat low-cost subscription removes this complexity and filters for PMs with genuine intent. Consider a 14-day free trial without a credit card requirement to reduce install friction.

### Why this could win
The Devil's Advocate review (File 06, Assumption 1) identifies the core problem with the standalone tool: PMs don't reach for a separate tool when they hit a confusing technical term, they keep reading and move on, or they open ChatGPT in the same tab they're already in. An extension that surfaces an explanation inline — without a tab switch, without a login, without remembering to check Bridge — removes the friction at the point where it actually exists. If the real failure mode is "I didn't think to look it up" rather than "I looked it up but the explanation was bad," Option B is the correct product. The extension also generates passive data on which technical terms are confusing PMs most frequently across companies, which is a dataset no competitor has and which directly informs C-01 (proactive glossary building) in a later phase.

### Why this could fail
Extension install friction is a real barrier. A PM has to find Bridge, read about it, decide to install it, go through the browser permission grant, and set it up before they get any value at all. The install-to-first-value funnel is longer and lossier than a web app sign-up. Each browser is a separate process: Chrome store approval, Firefox review, Safari extension notarization. Jira's UI has multiple versions (Classic and Next-gen), and Linear's architecture may make DOM injection unreliable. If the extension breaks the host page even once for a user, the uninstall rate will spike and the trust recovery path is difficult. Distribution is also harder without a web app: the standalone web app in Option A can be shared via a link; the extension requires install intent before a PM has seen any value.

### Key metric to hit
Daily active users on the extension, with at least 3 explanations per session. DAU without depth of use means the extension is installed but not integrated into the PM's workflow. Depth without DAU means it's useful on specific days but not habitual. Both must be true.

### Recommended if
Discovery interviews reveal that "I didn't think to look it up" is the dominant failure mode — that PMs encounter confusing technical terms, feel the discomfort in the moment, but do not take any action because opening a new tool feels like too much work given the pressure of the sprint cycle. Also recommended if research shows that PMs who use ChatGPT for technical explanations do so only when they're already in ChatGPT for something else — meaning the barrier is tool-switching, not capability gap.

---

## Option C: The Team Product ("Shared Knowledge, Defensible Moat")

**Strategic bet**: The real value isn't individual explanations — it's shared technical vocabulary across a product team, and that shared vocabulary creates the switching cost that makes Bridge defensible against any well-funded competitor.

### What's in
M-01 through M-05 (full core explanation loop), S-02 (explanation history and search), S-03 (team sharing of saved explanations), C-01 (proactive glossary building from company/team vocabulary). Team workspace with shared glossary, explanation library visible to all PMs in the workspace, and an admin view showing which terms are being looked up most frequently. Web app only at launch — team features require authentication, workspace management, and sharing UX that make the extension impractical in parallel.

### What's out
Browser extension (S-01) at launch — added in a subsequent phase once the team workspace is stable. Jira auto-suggest (C-02) deferred: the Jira integration adds API complexity and is more valuable when the team glossary is populated enough to make auto-suggestions accurate.

### Timeline
12 weeks to closed beta. The additional time reflects the authentication and workspace infrastructure required for team features: invite flows, role management (admin vs. member), shared explanation library with search, glossary contribution and editing UI. This is not complexity for its own sake — each component is required for the team product to function. A team workspace that loses explanations or has unreliable sharing will churn on its first impression.

### Pricing
$25/user/month with a 3-seat minimum. This is a B2B team product, not a PLG individual tool. The 3-seat minimum enforces the team use case and filters out individual PMs who would churn quickly because team sharing requires more than one user. Annual contract preferred; monthly available at a 20% premium. Freemium is not offered — the value of the product is the shared workspace, which requires multiple active users to demonstrate. A single-user free trial obscures the core value.

### Why this could win
Individual AI explanation tools are commoditized the moment a well-capitalized competitor (Notion AI, Atlassian Intelligence, GitHub Copilot for non-developers) ships a similar feature inside a tool PMs already use. The only durable advantage is data and relationship: a glossary that contains your company's specific technical vocabulary, your team's historical explanation decisions, and your new hire onboarding context. That cannot be copied by a generic AI tool, and it creates genuine switching cost — migrating a team glossary with 200 company-specific terms is painful in a way that migrating an individual explanation history is not. The team product also has a natural land-and-expand motion: one PM champion signs up, invites the rest of the product team, and the account grows without a sales call.

### Why this could fail
Team product adoption requires more than one enthusiastic individual: the champion must convince teammates to sign up, the teammates must see value quickly enough to keep using it, and the account must reach a critical mass of shared explanations before the glossary feels useful. This is a longer time-to-value curve than a standalone tool. The 3-seat minimum prevents the "solo PM who just wants explanations" use case, which may cut off the most motivated early adopters. The 12-week timeline also pushes the first design partner session to week 13 at the earliest, which is past the 10-week window the strategy document identifies as the build constraint. An extension waiver from the investor would be needed, or the team needs to accept a later closed beta start.

### Key metric to hit
30-day team retention above 60%, with at least 3 active users per account. Individual retention is necessary but not sufficient: a team product where one PM uses it and two don't is not a team product, it's a solo tool with a team subscription. The 3-active-user threshold is the product-market fit signal for Option C.

### Recommended if
Discovery interviews reveal that the problem is team-wide, not individual — that junior PMs and new hires struggle as much as or more than experienced PMs, that the PM lead is frustrated by having the same technical conversation repeatedly every sprint, and that the team is currently solving this with a shared Notion page of technical definitions that is out of date. If the organization is trying to build a team capability rather than help an individual feel less anxious, Option C is the right product. Also recommended if design partners are mid-market accounts (100+ engineers) where the PM team has 3–5 members, not solo PMs.

---

## Recommendation

**Run Option A first, with a committed extension launch at week 11.**

The devil's advocate review (File 06) correctly identifies that standalone adoption is the hardest test of the core hypothesis. If Bridge cannot generate 40% week-4 retention as a standalone web app — without workflow integration, without team features, without an extension — it means one of two things: the explanation quality is not good enough, or the trust-to-act barrier is higher than the product addresses. Either of those findings needs to be surfaced and resolved before the team invests in extension infrastructure, browser store approvals, or team workspace architecture.

But Option A cannot be the full answer. The strategy document's own risk analysis (Risk 1 — Behavior change required before value is delivered) identifies the core problem: Bridge only works if PMs remember to reach for it. The standalone web app tests whether the explanation is valuable. The extension tests whether the delivery mechanism is viable. Running Option A for 8 weeks and launching the extension at week 11 — while the extension is in browser store review during the web app beta — tests both hypotheses within the first public launch window.

Option C is the long-term destination, but it cannot be the starting point. The team glossary is only as useful as the explanation history that feeds it, and that history requires at least 8 weeks of individual use before it contains enough material to make team sharing feel valuable. Building team infrastructure before individual use patterns are established is building to a hypothesis, not to a validated behavior.

The specific conditions under which this recommendation changes: if discovery interviews show that PMs consistently describe the problem as a team coordination failure — not "I don't understand this term" but "my whole team uses this term differently and it causes miscommunication with engineering" — pivot to Option C. Team vocabulary misalignment is a different problem than individual translation difficulty, and it requires a different product. The decision framework below makes this explicit.

---

## Decision Framework

**If you observe this → run Option A first:**
- 8+ of 12 interviewed PMs describe a specific, recent moment where they Googled a term or asked ChatGPT and got an explanation that was either wrong or too technical to act on
- PMs describe the failure mode as "the explanation was bad" or "I couldn't tell if I could trust it" — quality and confidence are the named problems
- PMs are solo or the only PM on a small engineering team; no team-level PM vocabulary coordination problem is described
- No interviewee mentions that their teammates have the same confusion; the problem is framed as personal, not organizational

**If you observe this → run Option B first (browser extension):**
- 6+ of 12 interviewed PMs say they noticed a term they didn't understand but didn't look it up in the moment — the failure mode is inaction, not bad explanation quality
- PMs who use ChatGPT for technical explanations only do so when they're already in ChatGPT for something else, not as a deliberate "go look this up" behavior
- PMs describe the cost of switching tools mid-task as too high during sprint ceremonies (planning, standups, ticket refinement)
- At least 3 interviewees say something equivalent to "I'd use it if it was just there" without prompting from the interviewer

**If you observe this → run Option C first (team product):**
- PMs describe the problem as team-wide, not individual: "we all struggle with this," "I have to explain the same things to every new PM we hire," "our whole team uses technical terms inconsistently and it confuses engineering"
- At least one PM describes an existing team workaround (shared doc, Notion page, internal wiki) that they maintain for technical vocabulary — existence of this workaround confirms demand; its inadequacy confirms the gap Bridge fills
- Design partner accounts have 3+ PMs per product team, all of whom would be active users from day one
- PMs express more concern about onboarding new PMs to technical context than about their own in-the-moment confusion

**If findings are mixed (the most likely outcome):**
Run Option A for weeks 1–8 with the extension in browser store review simultaneously. At week 8, read the behavioral outcome data: if "used it" rate is above 40% and week-4 retention is above 35%, the explanation loop is working and the extension will amplify it. If "used it" rate is below 40% despite high satisfaction scores, pause the extension and investigate the trust-to-act barrier before adding more surfaces to a product that isn't changing behavior yet.
