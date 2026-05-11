# Example Output: Claude Automation Skill

**Prompt used:** "I want to automate the process of turning Jira ticket descriptions into draft PRDs. Help me scope and build this."

---

## Automation Scope: Jira Ticket → Draft PRD

---

### What We're Building

A Claude-powered workflow that takes a Jira ticket (title + description + linked tickets) as input and outputs a structured PRD draft, saved to Confluence and linked back to the Jira ticket.

---

### Inputs

| Input | Source | Notes |
|-------|--------|-------|
| Ticket title | Jira API | `issue.fields.summary` |
| Ticket description | Jira API | `issue.fields.description` (Atlassian Document Format — needs parsing) |
| Linked tickets | Jira API | `issue.fields.issuelinks` — pull parent epic and blockers |
| Reporter | Jira API | Used to set PRD author |
| Labels / components | Jira API | Used to infer product area |

---

### Outputs

| Output | Destination | Format |
|--------|-------------|--------|
| PRD draft | Confluence page | Markdown → Confluence storage format |
| Jira comment | Jira ticket | "PRD draft created: [link]" |
| Slack notification | `#product` channel | "New PRD drafted for [ticket]: [link]" |

---

### Claude Prompt Design

```
You are a senior product manager at Pulse, a B2B team analytics platform.

Given the following Jira ticket, write a structured PRD draft.

TICKET TITLE: {title}
TICKET DESCRIPTION: {description}
LINKED TICKETS: {linked_tickets}
PRODUCT AREA: {component}

Write a PRD with the following sections:
1. Problem Statement (2-3 sentences — what pain does this solve?)
2. Goals (3 measurable outcomes)
3. Non-Goals (what is explicitly out of scope)
4. User Stories (3-5 stories in "As a... I want... So that..." format)
5. Open Questions (3-5 questions that need answers before engineering starts)
6. Dependencies (systems, teams, or decisions this depends on)

Use direct, concise language. Do not pad. Flag any sections where the
ticket description doesn't provide enough information to write confidently —
mark those with [NEEDS INPUT].
```

---

### Implementation Plan

**Step 1: Trigger**
- Jira automation rule: when a ticket is moved to "Needs PRD" status → call webhook
- Webhook endpoint: AWS Lambda function (or n8n / Zapier if no-code preferred)

**Step 2: Data fetch**
- Lambda calls Jira REST API to fetch full ticket data
- Parse Atlassian Document Format description into plain text

**Step 3: Claude API call**
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=2048,
    system="You are a senior PM at Pulse...",
    messages=[{
        "role": "user",
        "content": prompt  # filled with ticket data
    }]
)

prd_draft = response.content[0].text
```

**Step 4: Write to Confluence**
- POST to Confluence REST API: create page under "PRDs" space
- Page title: `[DRAFT] {ticket_title}`
- Tag with `auto-generated` label for tracking

**Step 5: Close the loop**
- POST Jira comment with Confluence page link
- POST Slack message to `#product` via webhook

---

### Estimated Build Time

| Component | Effort |
|-----------|--------|
| Jira webhook + Lambda setup | 1 day |
| Confluence API integration | 0.5 day |
| Claude prompt tuning (3-5 iterations) | 1 day |
| Slack notification | 0.5 day |
| Testing + edge cases | 1 day |
| **Total** | **~4 days** |

---

### Edge Cases to Handle

- Ticket description is empty or < 50 words → skip automation, add Jira comment: "Description too sparse to generate PRD. Please add more detail."
- Confluence API rate limit → queue with exponential backoff
- Claude returns `[NEEDS INPUT]` flags → highlight in Confluence page with a yellow callout box so the PM knows what to fill in

---

### What This Is Not

- This does not replace PM judgment — it creates a starting draft, not a final PRD
- It does not read design files, analytics data, or customer research — those still need to be added manually
- It does not auto-approve or move tickets forward
