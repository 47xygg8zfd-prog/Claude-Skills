# Integration: Linear

Connect Claude to Linear so skills can read and create issues, manage cycles, and update project status directly.

## What This Unlocks

| Skill | With Linear Integration |
|-------|------------------------|
| `agile-stories` | Creates issues directly in your Linear team |
| `agile-ceremonies` | Reads cycle issues for retro and planning context |
| `monte-carlo` | Reads estimate data from the current cycle automatically |
| `stakeholder-updates` | Reads issue status to generate accurate updates |
| `feature-prioritization` | Reads existing issues and their priority scores |

## Setup

### 1. Get your Linear API key

1. Go to Linear → Settings → API
2. Create a personal API key (or workspace API key for team use)
3. Copy the key — it starts with `lin_api_`

### 2. Add to Claude settings

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@anthropic-labs/mcp-server-linear"],
      "env": {
        "LINEAR_API_KEY": "lin_api_your-key-here"
      }
    }
  }
}
```

### 3. Restart Claude

After saving settings, restart Claude. You should see Linear listed under connected tools.

## Example Prompts (with integration active)

**Read current cycle:**
```
What's in the current cycle for the Pulse team in Linear?
Summarize status by assignee and flag anything blocked.
```

**Create issues from stories:**
```
Create Linear issues in the Pulse team for these user stories.
Set priority based on the RICE scores below.
[paste stories + RICE output]
```

**Generate cycle summary for standup:**
```
Pull the Pulse team's current cycle from Linear and write a 5-bullet standup summary.
```

**Update issue after a decision:**
```
Find the Linear issue for "Weekly Digest - Admin opt-in setting" and add a comment:
"Descoped from Sprint 24. Moving to Sprint 25 as first priority."
```

## Permissions Required

The API key needs:
- Read access to issues, cycles, projects, and teams
- Write access to create and update issues, add comments

## Customization

Add your Linear team name to `CLAUDE.md`:
```
Project tracker: Linear — team: Pulse
```
