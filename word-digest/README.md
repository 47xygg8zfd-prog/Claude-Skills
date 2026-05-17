# Word Digest

A daily vocabulary email digest. Claude generates N sophisticated English words — each with pronunciation, etymology, example sentences, a memory tip, and related words — formatted as an HTML email and sent via Gmail SMTP.

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

💡 Memory tip: PALM + IMPRESS + PAST — something pressed in the palm of
   the past that still leaves an impression.

Related: manuscript (family), layered (synonym), tabula rasa (antonym),
         pentimento (related concept)
```

---

## Prerequisites

- Python 3.11+
- `pip install anthropic`
- A Gmail account with 2-Step Verification enabled
- A Gmail App Password (see below — your regular password will not work)

---

## Setup

### Step 1: Copy the config template

```bash
cp word-digest/config.env.example word-digest/config.env
```

Edit `word-digest/config.env` and fill in your values. This file is gitignored — never commit it.

### Step 2: Get a Gmail App Password

Gmail blocks regular passwords for SMTP access. You need an App Password:

1. Go to **https://myaccount.google.com/security**
2. Under "How you sign in to Google", enable **2-Step Verification** (if not already on)
3. Go to **https://myaccount.google.com/apppasswords**
4. Under "App name", type `Word Digest` and click **Create**
5. Copy the 16-character password (shown once — save it)
6. Set `WORD_DIGEST_EMAIL_PASSWORD=xxxx xxxx xxxx xxxx` in your config (spaces optional)

### Step 3: Fill in the rest of config.env

```bash
ANTHROPIC_API_KEY=sk-ant-...          # your Anthropic API key
WORD_DIGEST_EMAIL_FROM=you@gmail.com  # the Gmail account you just set up
WORD_DIGEST_EMAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx
WORD_DIGEST_EMAIL_TO=you@gmail.com    # send to yourself to start
```

---

## Running

### Test first — no email sent

```bash
# Load env vars
export $(grep -v '^#' word-digest/config.env | xargs)

# Generate words, print to console (no email)
python agents/word_digest.py --dry-run

# Generate words, save HTML to file (open in browser to check formatting)
python agents/word_digest.py --output /tmp/digest-preview.html
open /tmp/digest-preview.html   # macOS
# xdg-open /tmp/digest-preview.html  # Linux
```

### Send the email

```bash
export $(grep -v '^#' word-digest/config.env | xargs)
python agents/word_digest.py
```

### Options

```bash
python agents/word_digest.py --count 5    # 5 words (default: 3, max: 10)
python agents/word_digest.py --dry-run    # plain text, no email
python agents/word_digest.py --preview    # print HTML to stdout
python agents/word_digest.py --output FILE  # save HTML to file
```

---

## Scheduling with Cron

### Basic setup

```bash
crontab -e
```

Add this line to send at 7:00 AM daily:

```
0 7 * * * cd /path/to/Claude-Skills && export $(grep -v '^#' word-digest/config.env | xargs) && python agents/word_digest.py >> ~/word-digest.log 2>&1
```

> **Important**: Cron does not load your shell's `.bashrc` or `.zshrc`, so environment
> variables set there won't be available. The `export $(...)` pattern above loads them
> from the config file directly.

### With logging

The `>> ~/word-digest.log 2>&1` at the end appends both stdout and stderr to a log
file. Check it if something goes wrong:

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
  <key>Label</key>
  <string>com.worddigest.daily</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>-c</string>
    <string>cd /path/to/Claude-Skills && export $(grep -v '^#' word-digest/config.env | xargs) && python agents/word_digest.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>7</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>/tmp/word-digest.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/word-digest.log</string>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.worddigest.daily.plist
```

---

## Multiple Recipients

Separate addresses with commas in `config.env`:

```
WORD_DIGEST_EMAIL_TO=alice@example.com,bob@example.com,carol@example.com
```

---

## Other SMTP Providers

| Provider | Host | Port | Notes |
|---------|------|------|-------|
| Gmail | smtp.gmail.com | 587 | Requires App Password |
| Outlook / Hotmail | smtp-mail.outlook.com | 587 | Use account password or app password |
| iCloud | smtp.mail.me.com | 587 | Requires app-specific password |
| Fastmail | smtp.fastmail.com | 587 | Use app password |

---

## Troubleshooting

**"Authentication failed" / 535 error**
→ You're using your regular Google password. Gmail blocks this. Use an App Password (see Setup Step 2).

**"Connection refused" on port 587**
→ Check `WORD_DIGEST_SMTP_HOST` and `WORD_DIGEST_SMTP_PORT`. Try port 465 with SSL if 587 is blocked by your network.

**No words parsed**
→ Claude's output was likely cut short. Try again — this is rare. If it persists, the `max_tokens` may need increasing for large `--count` values.

**Cron runs but no email**
→ Check `~/word-digest.log`. The most common cause is env vars not loading — verify the `export $(grep ...)` line in your cron entry.

**Words look repeated over time**
→ Claude uses non-deterministic sampling so repetition is possible but unlikely. If you want to track history, append each day's words to a log file and add them to the user prompt as "words to avoid."
