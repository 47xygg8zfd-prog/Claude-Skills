"""
Competitive Intel Agent
Takes competitor information (release notes, news, G2 reviews, LinkedIn posts,
or any text) and produces a structured competitive briefing with threat
assessment, positioning implications, and recommended responses.

Usage:
    python competitive_intel.py --competitor "Teamlytics" --input updates.txt
    python competitive_intel.py --competitor "Teamlytics" --input updates.txt --output briefing.md
    python competitive_intel.py --file intel_dump.txt --output briefing.md
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPT = """You are a senior product manager producing a competitive intelligence briefing.

Given raw competitive information (release notes, news articles, G2 reviews, job postings,
LinkedIn posts, or any signal about a competitor), produce a structured briefing:

## Competitive Intel Briefing: [Competitor Name]
**Date**: [today]
**Prepared by**: PM

---

### Executive Summary
[3 bullets. The most important things to know. What changed, what it means, what we should do.]

---

### What's New
For each significant update found in the input:

**[Update title]**
- **What**: [What they shipped, announced, or changed]
- **Signal strength**: High / Medium / Low
- **Threat level**: 🔴 Direct threat / 🟡 Watch / 🟢 Neutral
- **Implication**: [What this means for our product or positioning]

---

### Positioning Impact
[How does this change the competitive landscape?]
- **Where we still win**: [Areas unaffected or where we're now stronger]
- **Where we're now at risk**: [Areas where their move creates a gap for us]
- **Table stakes shift**: [Anything that's now expected in the category that wasn't before]

---

### Recommended Responses

| Action | Priority | Owner | Timeline |
|--------|----------|-------|----------|
| [Product response] | High / Med / Low | PM / Eng | [Sprint / Quarter] |
| [Sales response] | | Sales / CS | |
| [Marketing response] | | Marketing | |

---

### What to Monitor Next
[3-5 signals to watch in the next 30-60 days that would indicate escalation or de-escalation]

---

Rules:
- Attribute claims to their source ("per their release notes", "per G2 review dated X")
- Flag low-confidence inferences with [INFERRED — verify before acting]
- Distinguish between "they shipped it" and "they announced it" — announcements without
  shipping are worth less
- Don't editorialize about competitor quality — assess threat to our business, not product quality
- If input is thin, say so: [LIMITED DATA — this briefing is based on sparse input]"""


def generate_briefing(
    intel_content: str,
    competitor_name: str = "",
    output_file: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    competitor_context = (
        f"Competitor: {competitor_name}\n\n" if competitor_name else ""
    )

    print(f"Generating competitive briefing{f' for {competitor_name}' if competitor_name else ''}...\n")
    print("=" * 60)

    result = []

    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    f"{competitor_context}"
                    f"Produce a competitive briefing from this intelligence:\n\n{intel_content}"
                ),
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print("\n" + "=" * 60)

    if output_file:
        Path(output_file).write_text("".join(result))
        print(f"\nBriefing saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a competitive intelligence briefing from raw intel"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", help="Path to file containing competitive intel")
    group.add_argument("--text", help="Intel as inline text")
    parser.add_argument("--competitor", help="Competitor name (optional but recommended)")
    parser.add_argument("--output", help="Save briefing to this markdown file")
    args = parser.parse_args()

    if args.text:
        intel_content = args.text
    else:
        intel_content = Path(args.input).read_text()
        print(f"Loaded intel from: {args.input}\n")

    generate_briefing(
        intel_content,
        competitor_name=args.competitor or "",
        output_file=args.output,
    )


if __name__ == "__main__":
    main()
