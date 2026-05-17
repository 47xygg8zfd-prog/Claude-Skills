"""
Word Digest Agent
Generates a daily vocabulary email digest using Claude, formats it as HTML,
and sends via SMTP. Each word includes pronunciation, part of speech, definition,
etymology, example sentences, a memory tip, and related words.

Usage:
    python word_digest.py                        # generate 3 words and send email
    python word_digest.py --count 5              # 5 words instead of 3
    python word_digest.py --preview              # print HTML to stdout, don't send
    python word_digest.py --output digest.html   # save HTML to file
    python word_digest.py --dry-run              # generate + print plain text, no email

Environment variables (see config.env.example):
    WORD_DIGEST_SMTP_HOST       SMTP server hostname (default: smtp.gmail.com)
    WORD_DIGEST_SMTP_PORT       SMTP port (default: 587)
    WORD_DIGEST_EMAIL_FROM      Sender address
    WORD_DIGEST_EMAIL_PASSWORD  SMTP password or Gmail app password
    WORD_DIGEST_EMAIL_TO        Comma-separated recipient addresses
"""

import anthropic
import argparse
import os
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


SYSTEM_PROMPT = """You are a vocabulary educator crafting a daily word digest for curious, well-read professionals.

Choose sophisticated but usable English vocabulary words. Avoid words that appear in the 10,000 most common English words. Prefer words a well-read professional would encounter but not use daily — words from literary criticism, philosophy, law, medicine, architecture, music theory, or the natural sciences that have moved into educated general usage.

Vary register, origin language, and part of speech across the set.

For each word, produce output in EXACTLY this format (including the delimiter lines):

===WORD_START===
WORD: [the word]
PRONUNCIATION: [IPA or respelling, e.g., /ˈpæl.ɪmp.sest/ or pal-IMP-sest]
PART_OF_SPEECH: [noun | verb | adjective | adverb | etc.]
DEFINITION: [Clear, jargon-free definition in 1–2 sentences. Write as if explaining to a smart friend, not a dictionary.]
ETYMOLOGY: [Origin: language → root → meaning. E.g., "Latin palimpsestus, from Greek palímpsēstos — 'scraped again' (pálin = again + psēn = to scrape)."]
EXAMPLE_FORMAL: [A formal sentence using the word in a professional or literary context.]
EXAMPLE_CONVERSATIONAL: [A natural, everyday sentence using the word in spoken English.]
MEMORY_TIP: [A mnemonic, visual association, or word-within-a-word trick to make this word stick. Be creative and concrete.]
RELATED_WORDS: [2–4 related words with their relationship. Format: word (relationship), word (relationship)]
===WORD_END===

Rules:
- Output exactly one ===WORD_START=== / ===WORD_END=== block per word, no more no less
- Never skip a field — all 9 fields are required
- Definitions must be clear enough that a non-specialist understands without looking anything up
- Example sentences must actually USE the word correctly, not just mention it
- The memory tip should be specific and vivid, not generic
- Do not add any text outside the WORD_START/WORD_END blocks"""

# Accent colors cycling across word cards
CARD_COLORS = ["#6b4c9a", "#2e7d8a", "#c0632a"]


def parse_words(raw: str) -> list[dict]:
    """Parse Claude's delimited output into a list of word dicts."""
    words = []
    for block in raw.split("===WORD_START==="):
        if "===WORD_END===" not in block:
            continue
        content = block.split("===WORD_END===")[0].strip()
        word = {}
        field_map = {
            "WORD": "word",
            "PRONUNCIATION": "pronunciation",
            "PART_OF_SPEECH": "part_of_speech",
            "DEFINITION": "definition",
            "ETYMOLOGY": "etymology",
            "EXAMPLE_FORMAL": "example_formal",
            "EXAMPLE_CONVERSATIONAL": "example_conversational",
            "MEMORY_TIP": "memory_tip",
            "RELATED_WORDS": "related_words",
        }
        for line in content.splitlines():
            for key, attr in field_map.items():
                if line.startswith(f"{key}:"):
                    word[attr] = line[len(key) + 1:].strip()
        if len(word) == 9:
            words.append(word)
    return words


def build_word_card(word: dict, index: int, total: int) -> str:
    """Build a single HTML word card (table-based for email client compatibility)."""
    color = CARD_COLORS[index % len(CARD_COLORS)]
    n = index + 1

    related_pills = "".join(
        f'<span style="display:inline-block;background:#f0ebf8;color:{color};'
        f'font-size:12px;padding:2px 10px;border-radius:12px;margin:2px 2px 2px 0;">'
        f'{r.strip()}</span>'
        for r in word["related_words"].split(",")
        if r.strip()
    )

    return f"""
<tr><td style="padding:20px 32px 0;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background:#ffffff;border-radius:8px;
                border-left:4px solid {color};
                box-shadow:0 1px 3px rgba(0,0,0,0.08);">
    <tr><td style="padding:24px;">

      <!-- badge + word -->
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td>
            <h2 style="font-family:Georgia,serif;color:#1a1a2e;
                       font-size:28px;margin:0 0 4px;letter-spacing:-0.5px;">
              {word["word"]}
            </h2>
            <p style="font-family:Georgia,serif;color:{color};
                      font-size:14px;font-style:italic;margin:0 0 16px;">
              {word["pronunciation"]} &nbsp;·&nbsp; {word["part_of_speech"]}
            </p>
          </td>
          <td style="vertical-align:top;text-align:right;">
            <span style="background:#e8d5b7;color:#1a1a2e;font-size:11px;
                         font-family:Arial,sans-serif;padding:3px 10px;
                         border-radius:12px;white-space:nowrap;">
              {n} of {total}
            </span>
          </td>
        </tr>
      </table>

      <!-- definition -->
      <p style="font-family:Georgia,serif;color:#2a2a2a;font-size:16px;
                line-height:1.6;margin:0 0 16px;">
        {word["definition"]}
      </p>

      <!-- etymology -->
      <div style="background:#f8f6f2;border-radius:4px;padding:12px 16px;margin:0 0 16px;">
        <p style="font-family:Arial,sans-serif;font-size:10px;text-transform:uppercase;
                  letter-spacing:1.5px;color:#9b8e7a;margin:0 0 4px;">Origin</p>
        <p style="font-family:Georgia,serif;font-size:14px;color:#4a4a4a;
                  font-style:italic;margin:0;line-height:1.5;">
          {word["etymology"]}
        </p>
      </div>

      <!-- example sentences -->
      <p style="font-family:Arial,sans-serif;font-size:10px;text-transform:uppercase;
                letter-spacing:1.5px;color:#9b8e7a;margin:0 0 8px;">In use</p>
      <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 16px;">
        <tr>
          <td style="border-left:3px solid #e0d8ec;padding:6px 0 6px 12px;">
            <p style="font-family:Georgia,serif;font-size:14px;color:#3a3a3a;
                      margin:0 0 8px;line-height:1.6;font-style:italic;">
              &ldquo;{word["example_formal"]}&rdquo;
            </p>
            <p style="font-family:Georgia,serif;font-size:14px;color:#3a3a3a;
                      margin:0;line-height:1.6;font-style:italic;">
              &ldquo;{word["example_conversational"]}&rdquo;
            </p>
          </td>
        </tr>
      </table>

      <!-- memory tip -->
      <div style="background:#fffbf0;border:1px solid #f0d080;
                  border-radius:4px;padding:12px 16px;margin:0 0 16px;">
        <p style="font-family:Arial,sans-serif;font-size:10px;text-transform:uppercase;
                  letter-spacing:1.5px;color:#9b8e7a;margin:0 0 4px;">&#128161; Memory tip</p>
        <p style="font-family:Georgia,serif;font-size:14px;color:#4a3800;
                  margin:0;line-height:1.5;">
          {word["memory_tip"]}
        </p>
      </div>

      <!-- related words -->
      <p style="font-family:Arial,sans-serif;font-size:10px;text-transform:uppercase;
                letter-spacing:1.5px;color:#9b8e7a;margin:0 0 8px;">Related</p>
      <p style="margin:0;">{related_pills}</p>

    </td></tr>
  </table>
</td></tr>"""


def build_html(words: list[dict], today_str: str) -> str:
    """Build the complete HTML email from parsed words."""
    cards = "".join(build_word_card(w, i, len(words)) for i, w in enumerate(words))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Your Daily Words &mdash; {today_str}</title>
</head>
<body style="margin:0;padding:0;background:#f5f5f0;
             font-family:Georgia,serif;-webkit-text-size-adjust:100%;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background:#f5f5f0;">
    <tr><td style="padding:32px 16px;">

      <!-- content column -->
      <table align="center" cellpadding="0" cellspacing="0"
             style="width:100%;max-width:600px;margin:0 auto;">

        <!-- header -->
        <tr><td style="background:#1a1a2e;border-radius:8px 8px 0 0;
                       padding:32px;text-align:center;">
          <p style="font-family:Arial,sans-serif;font-size:22px;
                    color:#e8d5b7;margin:0 0 6px;letter-spacing:1px;">
            &#128218; Your Daily Words
          </p>
          <p style="font-family:Arial,sans-serif;font-size:14px;
                    color:#9b8e7a;margin:0;">
            {today_str}
          </p>
        </td></tr>

        {cards}

        <!-- spacer -->
        <tr><td style="height:20px;"></td></tr>

        <!-- footer -->
        <tr><td style="background:#1a1a2e;border-radius:0 0 8px 8px;
                       padding:20px 32px;text-align:center;">
          <p style="font-family:Arial,sans-serif;font-size:12px;
                    color:#9b8e7a;margin:0;line-height:1.6;">
            Generated by Claude &nbsp;·&nbsp; Claude Skills Word Digest<br>
            Words chosen for a well-read professional who values precision in language.
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def print_words_plain(words: list[dict]) -> None:
    """Print words in a readable plain-text format for --dry-run."""
    for i, w in enumerate(words, 1):
        print(f"\n{'─' * 60}")
        print(f"  {i}. {w['word'].upper()}  {w['pronunciation']}  [{w['part_of_speech']}]")
        print(f"{'─' * 60}")
        print(f"\nDefinition:\n  {w['definition']}")
        print(f"\nEtymology:\n  {w['etymology']}")
        print(f"\nExamples:")
        print(f"  • {w['example_formal']}")
        print(f"  • {w['example_conversational']}")
        print(f"\nMemory tip:\n  {w['memory_tip']}")
        print(f"\nRelated: {w['related_words']}")
    print(f"\n{'─' * 60}")


def send_email(html: str, subject: str) -> None:
    """Send the HTML digest via SMTP using environment variables for config."""
    smtp_host = os.environ.get("WORD_DIGEST_SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("WORD_DIGEST_SMTP_PORT", "587"))
    from_addr = os.environ.get("WORD_DIGEST_EMAIL_FROM", "")
    password = os.environ.get("WORD_DIGEST_EMAIL_PASSWORD", "")
    to_raw = os.environ.get("WORD_DIGEST_EMAIL_TO", "")

    if not all([from_addr, password, to_raw]):
        raise ValueError(
            "Missing required environment variables.\n"
            "Set WORD_DIGEST_EMAIL_FROM, WORD_DIGEST_EMAIL_PASSWORD, "
            "and WORD_DIGEST_EMAIL_TO.\n"
            "See word-digest/config.env.example for setup instructions."
        )

    recipients = [addr.strip() for addr in to_raw.split(",") if addr.strip()]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(html, "html", "utf-8"))

    print(f"\nConnecting to {smtp_host}:{smtp_port}...")
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, recipients, msg.as_string())

    print(f"Sent to: {', '.join(recipients)}")


def generate_words(count: int) -> str:
    """Stream word generation from Claude and return the full accumulated text."""
    client = anthropic.Anthropic()

    today_fmt = date.today().strftime("%A, %B %-d, %Y")
    user_content = (
        f"Generate {count} vocabulary word{'s' if count != 1 else ''} "
        f"for today's digest. Today is {today_fmt}."
    )

    print(f"Generating {count} word{'s' if count != 1 else ''}...\n")
    print("=" * 60)

    result = []
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_content}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print("\n" + "=" * 60)
    return "".join(result)


def main():
    parser = argparse.ArgumentParser(
        description="Generate and send a daily vocabulary word email digest",
        epilog="""
cron — run daily at 7:00 AM:
  0 7 * * * cd /path/to/word-digest && export $(grep -v '^#' config.env | xargs) && python word_digest.py >> ~/word-digest.log 2>&1

Gmail app passwords (required — your regular password will not work):
  1. Enable 2-Step Verification: https://myaccount.google.com/security
  2. Generate app password: https://myaccount.google.com/apppasswords
  3. Set WORD_DIGEST_EMAIL_PASSWORD to the 16-character app password

See README.md for full setup instructions.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--count",
        type=int,
        default=3,
        metavar="N",
        help="Number of words to generate (default: 3, max: 10)",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Print the HTML email to stdout instead of sending",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="Save the HTML email to this file (e.g., digest.html)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Generate words and print plain-text to console; skip email",
    )
    args = parser.parse_args()

    if args.count < 1 or args.count > 10:
        parser.error("--count must be between 1 and 10")

    raw = generate_words(args.count)
    words = parse_words(raw)

    if not words:
        print("\nError: no words were parsed from Claude's output.")
        print("Try running again — this can happen if the model's response was truncated.")
        return

    today_str = date.today().strftime("%A, %B %-d, %Y")
    subject = f"\U0001f4da Your Daily Words — {today_str}"

    if args.dry_run:
        print_words_plain(words)
        return

    html = build_html(words, today_str)

    if args.preview:
        print(html)
        return

    if args.output:
        Path(args.output).write_text(html, encoding="utf-8")
        print(f"\nHTML saved to: {args.output}")
        return

    send_email(html, subject)


if __name__ == "__main__":
    main()
