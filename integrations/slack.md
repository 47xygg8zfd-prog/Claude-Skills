# Integration: Slack

Connect Claude to Slack so skills can post status updates, notify channels, and summarize threads directly.

## What This Unlocks

| Skill | With Slack Integration |
|-------|----------------------|
| `stakeholder-updates` | Posts weekly status updates directly to your team channel |
| `release-notes` | Sends release announcements to product and CS channels |
| `agile-ceremonies` | Posts retro summaries and sprint goals to the team channel |
| `okrs` | Posts OKR check-in summaries on a schedule |
| `competitive-analysis` | Sends battlecard updates to the sales channel |
| Prompts | Summarizes long threads; posts action items after meetings |

## Setup

### 1. Create a Slack app

1. Go to https://api.slack.com/apps → **Create New App** → **From scratch**
2. Name it "Claude PM Skills" and select your workspace
3. Under **OAuth & Permissions**, add these Bot Token Scopes:
   - `channels:read` — list channels
   - `channels:history` — read messages (for thread summaries)
   - `chat:write` — post messages
   - `groups:read` — access private channels the bot is in
   - `groups:history` — read private channel messages
4. Click **Install to Workspace** and copy the **Bot User OAuth Token** (starts with `xoxb-`)

### 2. Invite the bot to relevant channels

In each Slack channel Claude should post to:
```
/invite @Claude PM Skills
```

### 3. Add to Claude settings

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropic-labs/mcp-server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token-here",
        "SLACK_TEAM_ID": "T0123456789"
      }
    }
  }
}
```

To find your Team ID: in Slack, go to your workspace settings URL — the ID starts with `T`.

### 4. Restart Claude

## Example Prompts (with integration active)

**Post a status update:**
```
Write a weekly status update for the digest project and post it to #product-updates.
Status: On Track. This week: digest launched, 41% open rate.
Next week: analyze week 2 data, sprint 25 planning.
```

**Send a release announcement:**
```
Write a Slack announcement for the v2.4 release and post it to #product-announcements.
Keep it to 3 bullet points. Friendly tone.
What shipped: weekly digest, SSO, small teams bug fix.
```

**Summarize a thread:**
```
Summarize the thread in #product from today about the SendGrid contract decision.
Extract: what was decided, who owns the action, and by when.
```

**Post retro action items:**
```
Post the Sprint 24 retro action items to #pulse-team.
Format as a checklist with owners.
[paste action items]
```

## Customization

Add your key Slack channels to `CLAUDE.md`:
```
Comms: Slack
- Team channel: #pulse-team
- Stakeholder updates: #product-updates
- Announcements: #product-announcements
- CS channel: #cs-team
- Sales channel: #sales-team
- On-call: #pulse-oncall
```

Claude will use these as defaults when posting, so you don't need to specify the channel every time.
