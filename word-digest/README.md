# Word Digest

A daily vocabulary email digest powered by Claude. Generates N sophisticated English words — each with pronunciation, etymology, example sentences, a memory tip, and related words — formats them as an HTML email, and sends via Gmail SMTP.

One Python file. No external dependencies beyond the Anthropic SDK. Runs from cron or manually.

---

## What You Get

Each email contains word cards like this:

```
PALIMPSEST  /ˈpæl.ɪmp.sest/  · noun

A manuscript or document from which earlier writing has been erased to
make room for new text, but traces of the original remain visible.
Also used figuratively for anything that shows evidence of its history.

Origin: Latin palimpsestus, from Greek palímpsēstos — "scraped again"
        (pálin = again + psēn = to scrape)

In use:
  "The city's street plan is a palimpsest of Roman roads, medieval
   lanes, and Victorian boulevards."
  "Her face was a palimpsest — you could see decades of joy and
   grief written there if you looked closely."

💡 Memory tip: PALM + IMPRESS + PAST — something pressed in the palm
   of the past that still leaves an impression.

Related: manuscript (family), layered (synonym), tabula rasa (antonym),
         pentimento (related concept)
```

---

## Prerequisites

- Python 3.11+
- `pip install anthropic`
- A Gmail account with 2-Step Verification enabled
- A Gmail App Password (your regular password will not work — see Setup)

---

## Setup

### Step 1: Copy the config template

```bash
cp config.env.example config.env
```

Edit `config.env` and fill in your values. This file is gitignored — never commit it.

### Step 2: Get a Gmail App Password

Gmail blocks regular passwords for SMTP access. You need an App Password:

1. Go to **https://myaccount.google.com/security**
2. Enable **2-Step Verification** if not already on
3. Go to **https://myaccount.google.com/apppasswords**
4. Type `Word Digest` as the app name and click **Create**
5. Copy the 16-character password (shown once — save it)
6. Set `WORD_DIGEST_EMAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx` in `config.env`

### Step 3: Fill in config.env

```bash
ANTHROPIC_API_KEY=sk-ant-...
WORD_DIGEST_EMAIL_FROM=you@gmail.com
WORD_DIGEST_EMAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx
WORD_DIGEST_EMAIL_TO=you@gmail.com
```

---

## Running

### Test first — no email sent

```bash
export $(grep -v '^#' config.env | xargs)

# Print words to console
python word_digest.py --dry-run

# Save HTML to file and open in browser
python word_digest.py --output preview.html
open preview.html          # macOS
xdg-open preview.html     # Linux
```

### Send the email

```bash
export $(grep -v '^#' config.env | xargs)
python word_digest.py
```

### Options

```bash
python word_digest.py --count 5       # 5 words (default: 3, max: 10)
python word_digest.py --dry-run       # plain text to console, no email
python word_digest.py --preview       # print HTML to stdout
python word_digest.py --output FILE   # save HTML to file
```

---

## Scheduling with Cron

```bash
crontab -e
```

Add this line to send at 7:00 AM daily:

```
0 7 * * * cd /path/to/word-digest && export $(grep -v '^#' config.env | xargs) && python word_digest.py >> ~/word-digest.log 2>&1
```

> **Important**: Cron does not load your shell's `.bashrc` or `.zshrc`. The
> `export $(grep ...)` pattern loads env vars from `config.env` directly.

Check the log if something goes wrong:

```bash
tail -20 ~/word-digest.log
```

### macOS launchd (alternative to cron)

Create `~/Library/LaunchAgents/com.worddigest.daily.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.worddigest.daily</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-c</string>
    <string>cd /path/to/word-digest && export $(grep -v '^#' config.env | xargs) && python word_digest.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key><integer>7</integer>
    <key>Minute</key><integer>0</integer>
  </dict>
  <key>StandardOutPath</key><string>/tmp/word-digest.log</string>
  <key>StandardErrorPath</key><string>/tmp/word-digest.log</string>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.worddigest.daily.plist
```

---

## Multiple Recipients

```bash
WORD_DIGEST_EMAIL_TO=alice@example.com,bob@example.com,carol@example.com
```

---

## Other SMTP Providers

| Provider | Host | Port | Notes |
|---------|------|------|-------|
| Gmail | smtp.gmail.com | 587 | Requires App Password |
| Outlook / Hotmail | smtp-mail.outlook.com | 587 | Account or app password |
| iCloud | smtp.mail.me.com | 587 | Requires app-specific password |
| Fastmail | smtp.fastmail.com | 587 | Use app password |

---

## Extending This to Other Digest Types

This project is a template for any Claude-powered daily email digest. The pattern is:

```
Claude generates structured content → Python parses it → HTML email → SMTP send → cron
```

The only things that change between digest types are the **system prompt** and the **HTML card layout**. Everything else — SMTP sending, HTML scaffolding, CLI flags, cron setup — is reusable as-is.

### Examples you could build from this

**Daily news briefing**
Replace the word prompt with one that summarizes a topic area (AI, markets, policy). Feed in RSS content or let Claude generate from its training knowledge. One card per story instead of per word.

**Quote of the day**
Prompt Claude for a quote, its author, historical context, and why it's relevant today. Simpler card layout — no etymology section needed.

**Learning digest (language, history, science)**
Same structure as this project. Change `WORD:` fields to `CONCEPT:`, `PERIOD:`, `FORMULA:` etc. The delimiter-based parsing works for any labeled-field format.

**Team standup summary**
Feed in Jira/Linear tickets as input, prompt Claude to summarize what the team shipped and what's blocked, send to a Slack channel instead of email (swap `smtplib` for a Slack webhook call).

**Personal reading digest**
Paste in articles or book excerpts, prompt Claude for a 3-point summary + one question to reflect on. Send to yourself each morning.

**Habit tracker nudge**
Claude generates a daily micro-habit suggestion tied to a goal you define in the prompt. One card, minimal layout. Pairs well with a `--goal` CLI flag.

### How to adapt the code

1. **Change the system prompt** (`SYSTEM_PROMPT` constant) — define new field names and content rules
2. **Update `parse_words()`** — rename `field_map` keys to match your new fields
3. **Update `build_word_card()`** — replace the HTML sections with your content structure
4. **Rename the env var prefix** — swap `WORD_DIGEST_` for something like `NEWS_DIGEST_` or `QUOTE_DIGEST_`

The `generate_words()`, `build_html()`, `send_email()`, and `main()` functions need no changes for most adaptations.

---

## Troubleshooting

**"Authentication failed" / 535 error**
→ You're using your regular Google password. Use a Gmail App Password instead (see Setup).

**"Connection refused" on port 587**
→ Check `WORD_DIGEST_SMTP_HOST` and `WORD_DIGEST_SMTP_PORT`. Some networks block 587 — try port 465 with SSL.

**No words parsed**
→ Claude's output was cut short. Run again. If persistent, reduce `--count` or the model may need a higher `max_tokens`.

**Cron runs but no email arrives**
→ Check `~/word-digest.log`. Most common cause: env vars not loading. Verify the `export $(grep ...)` line in your crontab.

**Words repeat over time**
→ Claude uses non-deterministic sampling so repetition is possible but rare. To track history, append each day's words to a log file and inject "avoid these words: ..." into the user prompt.
