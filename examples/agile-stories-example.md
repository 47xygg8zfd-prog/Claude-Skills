# Example Output: Agile Stories Skill

**Prompt used:** "Break the Weekly Digest PRD into tickets for the first sprint"

---

## Epic: Weekly Team Digest (v1)

**Goal**: Deliver a weekly email digest to managers summarizing team activity, increasing WAU by 20%.  
**Target**: Q3 2026  

---

### Story 1: Digest opt-in setting (admin)

**As an** admin,  
**I want to** enable or disable the weekly digest for my organization,  
**So that** I can control outbound email volume and roll out the feature on my own timeline.

**Acceptance Criteria**
- [ ] Admin settings page includes a "Weekly Digest" toggle (default: OFF)
- [ ] Toggling ON shows a confirmation modal explaining what will be sent and to whom
- [ ] Toggling OFF stops all future digests within 24 hours
- [ ] Change is logged in the org audit trail

**Story Points**: 3  
**Dependencies**: Admin settings page refactor (Story 4)

---

### Story 2: Digest data aggregation job

**As a** system,  
**I want to** compute weekly summary metrics per team every Sunday night,  
**So that** digest content is ready for Monday morning delivery.

**Acceptance Criteria**
- [ ] Scheduled job runs at 11pm UTC every Sunday
- [ ] Aggregates: team velocity, response time, collaboration score, at-risk member flags
- [ ] Stores output in `digest_snapshots` table keyed by `team_id` + `week_start_date`
- [ ] Job completes within 15 minutes for orgs with up to 500 teams
- [ ] Failed runs trigger a PagerDuty alert and skip that week's send (no partial digests)

**Story Points**: 5  
**Dependencies**: None

---

### Story 3: Digest email template

**As a** manager,  
**I want to** receive a well-formatted digest email,  
**So that** I can quickly scan my team's weekly highlights without logging in.

**Acceptance Criteria**
- [ ] Email renders correctly in Gmail, Outlook, and Apple Mail (desktop + mobile)
- [ ] Sections: headline metric, top 3 highlights, 1 suggested action, CTA button
- [ ] CTA deep-links to the relevant dashboard section (not just the homepage)
- [ ] Unsubscribe link present and functional (1-click, no login required)
- [ ] Plain-text fallback included

**Story Points**: 5  
**Dependencies**: Story 2 (data), design mockup sign-off

---

### Story 4: Digest delivery service

**As a** system,  
**I want to** send digest emails to eligible managers every Monday at 9am local time,  
**So that** delivery is timely and relevant to each recipient's timezone.

**Acceptance Criteria**
- [ ] Sends only to managers in orgs where digest is enabled (Story 1)
- [ ] Respects recipient's timezone (falls back to org timezone if user timezone not set)
- [ ] Skips send if no digest snapshot exists for the team (Story 2)
- [ ] Delivery logged per recipient with status (sent / skipped / bounced)
- [ ] Send volume does not exceed email provider rate limits

**Story Points**: 3  
**Dependencies**: Stories 1, 2, 3

---

### Story 5: Digest open/click tracking

**As a** PM,  
**I want to** track open and click-through rates for the digest,  
**So that** I can measure engagement and iterate on content.

**Acceptance Criteria**
- [ ] Open events tracked via 1x1 pixel (standard)
- [ ] CTA clicks tracked with UTM parameters: `utm_source=digest`, `utm_medium=email`, `utm_campaign=weekly_digest`
- [ ] Events flow into the product analytics pipeline within 1 hour of occurrence
- [ ] Dashboard widget added to the internal PM analytics view

**Story Points**: 2  
**Dependencies**: Story 4

---

## Sprint 1 Scope

| Story | Points | Owner |
|-------|--------|-------|
| Story 2: Data aggregation job | 5 | Backend |
| Story 3: Email template | 5 | Frontend / Design |
| Story 1: Admin opt-in setting | 3 | Full-stack |
| **Total** | **13** | |

Stories 4 and 5 move to Sprint 2 once the data and template are validated.
