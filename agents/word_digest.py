"""
Word Digest
Sends a daily vocabulary email digest using the Free Dictionary API
(dictionaryapi.dev — free, no key required) and a bundled word list.
No Claude API or paid service needed.

Usage:
    python word_digest.py                       # send today's words
    python word_digest.py --count 3             # number of words (default: 3)
    python word_digest.py --dry-run             # print words, no email
    python word_digest.py --preview             # print HTML to stdout
    python word_digest.py --output digest.html  # save HTML to file

Environment variables (see config.env.example):
    WORD_DIGEST_SMTP_HOST       SMTP hostname (default: smtp.gmail.com)
    WORD_DIGEST_SMTP_PORT       SMTP port (default: 587)
    WORD_DIGEST_EMAIL_FROM      Sender address
    WORD_DIGEST_EMAIL_PASSWORD  Gmail app password
    WORD_DIGEST_EMAIL_TO        Comma-separated recipients
"""

import argparse
import json
import os
import random
import smtplib
import urllib.request
import urllib.error
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


# Curated list of sophisticated but usable words.
# The script picks from this list using today's date as a seed,
# so each day's selection is consistent but changes daily.
WORD_LIST = [
    "abeyance", "abstemious", "acerbic", "acumen", "alacrity", "allay",
    "ameliorate", "anachronism", "anodyne", "anomalous", "antipathy",
    "apocryphal", "apposite", "arcane", "arduous", "argot", "assuage",
    "astute", "atavistic", "augur", "auspicious", "avarice", "axiomatic",
    "baroque", "beguile", "bellicose", "bespoke", "bifurcate", "blithe",
    "bombastic", "brazen", "brusque", "bucolic", "byzantine", "cacophony",
    "cadence", "calumny", "candor", "capricious", "catharsis", "caustic",
    "caveat", "censure", "chicanery", "circumspect", "coalesce", "cogent",
    "complicit", "conundrum", "copious", "culpable", "cursory", "dauntless",
    "debacle", "decorum", "deferential", "deleterious", "demagogue",
    "desultory", "diaphanous", "didactic", "diffident", "dilettante",
    "discern", "disdain", "disparate", "dissonance", "dogmatic", "draconian",
    "duplicity", "ebullient", "effusive", "egregious", "elegy", "elusive",
    "embellish", "empirical", "endemic", "enigmatic", "ephemeral",
    "equanimity", "equivocal", "erudite", "esoteric", "euphemism",
    "exacerbate", "exigent", "expedient", "extol", "facetious", "fallacious",
    "fastidious", "fatuous", "fecund", "felicitous", "fervent", "fickle",
    "flippant", "florid", "foment", "forbearance", "forthright", "fortuitous",
    "fractious", "frugal", "furtive", "garrulous", "grandiloquent",
    "gratuitous", "gregarious", "guile", "hackneyed", "hapless", "harangue",
    "hegemony", "heresy", "hubris", "hyperbole", "iconoclast", "idiosyncrasy",
    "ignominious", "immutable", "imperious", "imperturbable", "impervious",
    "implacable", "impudent", "inchoate", "incisive", "incongruous",
    "indefatigable", "indigent", "indolent", "ineffable", "inimical",
    "innate", "insidious", "insular", "intransigent", "inveterate",
    "irascible", "irreverent", "laconic", "languid", "latent", "laudable",
    "loquacious", "lucid", "lugubrious", "malaise", "malevolent", "malleable",
    "maverick", "mendacious", "mercurial", "meticulous", "misanthrope",
    "mitigate", "mordant", "morose", "myopic", "nebulous", "nonchalant",
    "nuanced", "obdurate", "obsequious", "obstinate", "onerous",
    "opprobrium", "ostracize", "palimpsest", "paradox", "pariah",
    "parsimonious", "penchant", "perfidious", "pervasive", "petulant",
    "piquant", "placid", "platitude", "plausible", "pragmatic", "precarious",
    "precipitous", "presumptuous", "prevaricate", "probity", "prodigal",
    "prolific", "propitious", "propriety", "prosaic", "provincial", "prudent",
    "pugnacious", "querulous", "quixotic", "rancor", "rapacious",
    "recalcitrant", "reclusive", "redolent", "reticent", "sagacious",
    "sanctimonious", "sardonic", "scrupulous", "serendipity", "solipsism",
    "specious", "spurious", "stoic", "strident", "subjugate", "sublime",
    "succinct", "supercilious", "sycophant", "tacit", "tangential",
    "tenacious", "terse", "timorous", "torpid", "tractable", "truculent",
    "turpitude", "ubiquitous", "umbrage", "vacuous", "vehement", "venal",
    "verbose", "vicarious", "vindictive", "visceral", "vitriolic", "volatile",
    "voracious", "wanton", "wistful", "zealous",
]

CARD_COLORS = ["#6b4c9a", "#2e7d8a", "#c0632a"]


def pick_words(count: int) -> list[str]:
    """Pick `count` words using today's date as seed — consistent within a day."""
    rng = random.Random(date.today().isoformat())
    return rng.sample(WORD_LIST, min(count, len(WORD_LIST)))


def fetch_word_data(word: str) -> dict:
    """Fetch word data from the Free Dictionary API. Returns a normalized dict."""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            entries = json.loads(resp.read())
            data = entries[0]
    except (urllib.error.HTTPError, urllib.error.URLError,
            IndexError, json.JSONDecodeError) as e:
        print(f"  Warning: could not fetch '{word}' ({e})")
        return {"word": word, "phonetic": "", "part_of_speech": "",
                "definition": "", "example": "", "synonyms": [],
                "antonyms": [], "ok": False}

    # Phonetic
    phonetic = data.get("phonetic", "")
    if not phonetic:
        for p in data.get("phonetics", []):
            if p.get("text"):
                phonetic = p["text"]
                break

    meanings = data.get("meanings", [])
    part_of_speech = meanings[0].get("partOfSpeech", "") if meanings else ""

    definition = example = ""
    synonyms: list[str] = []
    antonyms: list[str] = []

    for meaning in meanings:
        for defn in meaning.get("definitions", []):
            if not definition and defn.get("definition"):
                definition = defn["definition"]
            if not example and defn.get("example"):
                example = defn["example"]
        synonyms += [s for s in meaning.get("synonyms", []) if s not in synonyms]
        antonyms += [a for a in meaning.get("antonyms", []) if a not in antonyms]

    return {
        "word": word,
        "phonetic": phonetic,
        "part_of_speech": part_of_speech,
        "definition": definition or "Definition not available.",
        "example": example,
        "synonyms": synonyms[:4],
        "antonyms": antonyms[:3],
        "ok": True,
    }


def build_word_card(w: dict, index: int, total: int) -> str:
    """Build one HTML word card."""
    color = CARD_COLORS[index % len(CARD_COLORS)]
    n = index + 1

    phonetic_line = ""
    if w["phonetic"] or w["part_of_speech"]:
        parts = [p for p in [w["phonetic"], w["part_of_speech"]] if p]
        phonetic_line = f"""
            <p style="font-family:Georgia,serif;color:{color};
                      font-size:14px;font-style:italic;margin:0 0 16px;">
              {" &nbsp;·&nbsp; ".join(parts)}
            </p>"""

    example_block = ""
    if w["example"]:
        example_block = f"""
      <p style="font-family:Arial,sans-serif;font-size:10px;text-transform:uppercase;
                letter-spacing:1.5px;color:#9b8e7a;margin:16px 0 8px;">In use</p>
      <table width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 16px;">
        <tr>
          <td style="border-left:3px solid #e0d8ec;padding:6px 0 6px 12px;">
            <p style="font-family:Georgia,serif;font-size:14px;color:#3a3a3a;
                      margin:0;line-height:1.6;font-style:italic;">
              &ldquo;{w["example"]}&rdquo;
            </p>
          </td>
        </tr>
      </table>"""

    related_pills = ""
    related_items = (
        [(s, color) for s in w["synonyms"]] +
        [(a, "#c0632a") for a in w["antonyms"]]
    )
    if related_items:
        pills = "".join(
            f'<span style="display:inline-block;background:#f0ebf8;color:{c};'
            f'font-size:12px;padding:2px 10px;border-radius:12px;margin:2px 2px 2px 0;">'
            f'{word}</span>'
            for word, c in related_items
        )
        related_pills = f"""
      <p style="font-family:Arial,sans-serif;font-size:10px;text-transform:uppercase;
                letter-spacing:1.5px;color:#9b8e7a;margin:0 0 8px;">Related</p>
      <p style="margin:0;">{pills}</p>"""

    return f"""
<tr><td style="padding:20px 32px 0;">
  <table width="100%" cellpadding="0" cellspacing="0"
         style="background:#ffffff;border-radius:8px;
                border-left:4px solid {color};
                box-shadow:0 1px 3px rgba(0,0,0,0.08);">
    <tr><td style="padding:24px;">

      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td>
            <h2 style="font-family:Georgia,serif;color:#1a1a2e;
                       font-size:28px;margin:0 0 4px;letter-spacing:-0.5px;">
              {w["word"]}
            </h2>
            {phonetic_line}
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

      <p style="font-family:Georgia,serif;color:#2a2a2a;font-size:16px;
                line-height:1.6;margin:0 0 4px;">
        {w["definition"]}
      </p>
      {example_block}
      {related_pills}

    </td></tr>
  </table>
</td></tr>"""


def build_html(words: list[dict], today_str: str) -> str:
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
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f0;">
    <tr><td style="padding:32px 16px;">
      <table align="center" cellpadding="0" cellspacing="0"
             style="width:100%;max-width:600px;margin:0 auto;">

        <tr><td style="background:#1a1a2e;border-radius:8px 8px 0 0;
                       padding:32px;text-align:center;">
          <p style="font-family:Arial,sans-serif;font-size:22px;
                    color:#e8d5b7;margin:0 0 6px;letter-spacing:1px;">
            &#128218; Your Daily Words
          </p>
          <p style="font-family:Arial,sans-serif;font-size:14px;
                    color:#9b8e7a;margin:0;">{today_str}</p>
        </td></tr>

        {cards}

        <tr><td style="height:20px;"></td></tr>

        <tr><td style="background:#1a1a2e;border-radius:0 0 8px 8px;
                       padding:20px 32px;text-align:center;">
          <p style="font-family:Arial,sans-serif;font-size:12px;
                    color:#9b8e7a;margin:0;line-height:1.6;">
            Powered by the Free Dictionary API &nbsp;·&nbsp; Word Digest
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""


def print_words_plain(words: list[dict]) -> None:
    for i, w in enumerate(words, 1):
        print(f"\n{'─' * 60}")
        parts = [p for p in [w["phonetic"], w["part_of_speech"]] if p]
        header = f"  {i}. {w['word'].upper()}"
        if parts:
            header += f"  {' · '.join(parts)}"
        print(header)
        print(f"{'─' * 60}")
        print(f"\n  {w['definition']}")
        if w["example"]:
            print(f'\n  "{w["example"]}"')
        if w["synonyms"]:
            print(f"\n  Synonyms: {', '.join(w['synonyms'])}")
        if w["antonyms"]:
            print(f"  Antonyms: {', '.join(w['antonyms'])}")
    print(f"\n{'─' * 60}")


def send_email(html: str, subject: str) -> None:
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
            "See config.env.example for setup instructions."
        )

    recipients = [a.strip() for a in to_raw.split(",") if a.strip()]
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


def main():
    parser = argparse.ArgumentParser(
        description="Send a daily vocabulary word email digest (no API key required)",
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
    parser.add_argument("--count", type=int, default=3, metavar="N",
                        help="Number of words (default: 3, max: 10)")
    parser.add_argument("--preview", action="store_true",
                        help="Print HTML to stdout instead of sending")
    parser.add_argument("--output", metavar="FILE",
                        help="Save HTML to file (e.g. digest.html)")
    parser.add_argument("--dry-run", action="store_true", dest="dry_run",
                        help="Print words to console; skip email")
    args = parser.parse_args()

    if args.count < 1 or args.count > 10:
        parser.error("--count must be between 1 and 10")

    selected = pick_words(args.count)
    print(f"Fetching {len(selected)} word{'s' if len(selected) != 1 else ''}...")
    words = []
    for word in selected:
        print(f"  {word}...", end=" ", flush=True)
        data = fetch_word_data(word)
        words.append(data)
        print("ok" if data["ok"] else "fallback")

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
