# Skill: Customer Research Synthesis

## Trigger Phrases
- "synthesize these interview notes"
- "find themes in this research"
- "what did customers say about"
- "turn these notes into insights"
- "summarize user feedback"
- "analyze these survey responses"
- "what are users struggling with"

## Description
Transform raw customer interview notes, survey responses, or support tickets into structured insights: themes, opportunity statements, Jobs To Be Done, and recommended actions.

## Behavior

When triggered, ask the user to paste or describe:
1. Raw research input (interview transcripts, survey data, NPS comments, support tickets)
2. Research goal or question being investigated
3. Audience segment (if known)

Then produce the following sections:

### 1. Key Themes
Group findings into 3-7 named themes. For each theme:
- **Theme name** (short label)
- **Frequency**: how many participants mentioned it
- **Representative quote(s)**
- **Underlying need or pain**

### 2. Jobs To Be Done
For the top 2-3 themes, write a JTBD statement:
> When [situation], I want to [motivation], so I can [expected outcome].

### 3. Opportunity Statements
Convert each major pain into an opportunity using the format:
> How might we help [user type] [achieve goal] without [current frustration]?

### 4. Sentiment Summary
| Sentiment | % of Responses | Top Topics |
|-----------|---------------|------------|
| Positive  | ...           | ...        |
| Neutral   | ...           | ...        |
| Negative  | ...           | ...        |

### 5. Recommended Next Steps
- What to validate further
- What is strong enough signal to act on now
- Suggested features or experiments to explore

## Output Style
- Neutral, evidence-based tone — quote the data, don't editorialize
- Flag low-confidence themes (mentioned by only 1-2 participants)
- Keep opportunity statements actionable enough to feed directly into PRD or backlog grooming

## Customization Tips
- Add your user personas so themes can be attributed to specific segments
- Add your current OKRs so Claude can flag which insights are most strategically relevant
- Add your product area taxonomy to auto-tag themes to roadmap categories
