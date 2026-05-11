# Integration: Jira

Connect Claude to Jira so skills can read tickets, create stories, update statuses, and post comments directly.

## What This Unlocks

| Skill | With Jira Integration |
|-------|----------------------|
| `agile-stories` | Creates tickets directly in your backlog instead of outputting markdown |
| `prd` | Links PRD to an epic; reads linked tickets for context |
| `agile-ceremonies` | Reads sprint tickets for retro and planning context |
| `monte-carlo` | Reads story points from the current sprint automatically |
| `stakeholder-updates` | Reads ticket status to generate accurate status updates |
| `claude-automation` | Reads ticket descriptions to generate PRD drafts |

## Setup

### 1. Get your Jira credentials

You need:
- **Jira base URL**: `https://your-org.atlassian.net`
- **Email**: your Atlassian account email
- **API token**: generate at https://id.atlassian.com/manage-profile/security/api-tokens

### 2. Add to Claude settings

```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "@anthropic-labs/mcp-server-jira"],
      "env": {
        "JIRA_BASE_URL": "https://your-org.atlassian.net",
        "JIRA_EMAIL": "you@yourcompany.com",
        "JIRA_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

### 3. Restart Claude

After saving settings, restart Claude. You should see Jira listed under connected tools.

## Example Prompts (with integration active)

**Read tickets for context:**
```
Summarize the open tickets in sprint 24 of the PULSE project.
```

**Create stories from a PRD:**
```
Create Jira tickets in the PULSE project for the user stories in this PRD.
Set story points based on our pointing scale. Assign to the current sprint.
[paste PRD]
```

**Update ticket status:**
```
Move PULSE-142 to "In Review" and add a comment: "PR is up, waiting on design sign-off."
```

**Generate a status update from live ticket data:**
```
Look at the open tickets in Sprint 24 of PULSE and write a weekly status update.
Flag anything that's blocked or hasn't moved in 3+ days.
```

## Permissions Required

The API token needs the following Jira permissions:
- `read:jira-work` — read issues, sprints, projects
- `write:jira-work` — create and update issues, add comments

## Customization

Add your project key to `CLAUDE.md` under "Data & Tools":
```
Project tracker: Jira — project key: PULSE
```

Claude will use this as the default project when creating tickets, so you don't need to specify it every time.
