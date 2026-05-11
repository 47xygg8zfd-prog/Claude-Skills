"""
Research Synthesis Agent
Ingests customer interview transcripts or feedback and produces structured
themes, JTBD statements, opportunity statements, and recommended next steps.

Usage:
    python research_synthesis.py --file transcripts.txt
    python research_synthesis.py --input "paste transcript here"
    python research_synthesis.py --file transcripts.txt --output synthesis.md
"""

import anthropic
import argparse
import sys
from pathlib import Path


SYSTEM_PROMPT = """You are a senior product researcher specializing in synthesizing
qualitative customer research into actionable product insights.

When given raw interview transcripts, survey responses, or feedback, produce a
structured synthesis with the following sections:

## Key Themes
Group findings into 3-7 named themes. For each:
- Theme name (short label)
- Frequency: how many participants mentioned it (e.g. "5/8 participants")
- Representative quote (verbatim if available)
- Underlying need or pain

## Jobs To Be Done
For the top 2-3 themes, write a JTBD statement:
"When [situation], I want to [motivation], so I can [expected outcome]."

## Opportunity Statements
Convert each major pain into an opportunity:
"How might we help [user type] [achieve goal] without [current frustration]?"

## Sentiment Summary
A brief breakdown: what percentage of the input is positive / neutral / negative,
and what topics drive each sentiment.

## Recommended Next Steps
- What is strong enough signal to act on now
- What needs further validation before acting
- Any segments that appear underrepresented and need dedicated research

Rules:
- Be evidence-based. Quote the data, don't editorialize.
- Flag low-confidence themes (only 1-2 participants mentioned it).
- Mark any section where input was insufficient with [NEEDS MORE DATA].
- Keep the output scannable — this goes into planning meetings."""


def synthesize(content: str, output_file: str | None = None) -> None:
    client = anthropic.Anthropic()

    print("Synthesizing research...\n")
    print("=" * 60)

    result = []

    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                # Cache the system prompt — saves cost on repeated runs
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Synthesize the following customer research:\n\n{content}",
            }
        ],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result.append(text)

    print("\n" + "=" * 60)

    if output_file:
        output = "".join(result)
        Path(output_file).write_text(output)
        print(f"\nOutput saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Synthesize customer research transcripts")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="Path to transcript file or directory of .txt files")
    group.add_argument("--input", help="Raw transcript text (for short inputs)")
    parser.add_argument("--output", help="Save output to this markdown file")
    args = parser.parse_args()

    if args.input:
        content = args.input
    else:
        path = Path(args.file)
        if path.is_dir():
            # Concatenate all .txt files in the directory
            files = sorted(path.glob("*.txt"))
            if not files:
                print(f"No .txt files found in {path}")
                sys.exit(1)
            parts = []
            for f in files:
                parts.append(f"--- {f.name} ---\n{f.read_text()}")
            content = "\n\n".join(parts)
            print(f"Loaded {len(files)} transcript files from {path}\n")
        else:
            content = path.read_text()
            print(f"Loaded: {path}\n")

    synthesize(content, args.output)


if __name__ == "__main__":
    main()
