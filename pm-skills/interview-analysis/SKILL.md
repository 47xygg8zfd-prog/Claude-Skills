# Skill: Interview Analysis

## Trigger Phrases
- "analyze this interview"
- "what themes are in these transcripts"
- "extract JTBD from"
- "build an OST from these interviews"
- "what did users say about"
- "synthesize these transcripts"
- "find patterns in these interviews"
- "interview analysis"

## Description
Analyze raw user interview transcripts to extract themes, jobs-to-be-done, opportunity nodes for an OST, and persona signals. Use when the user has raw interview notes or transcripts and needs structured insights — not when they already have synthesized research.

## Behavior

### This Skill vs. customer-research-synthesis

| Signal | Use this skill | Use customer-research-synthesis |
|--------|---------------|--------------------------------|
| Input is raw quotes and observations | Yes | No |
| Input is already tagged or themed | No | Yes |
| You need to find structure | Yes | No |
| You need to draw conclusions from existing structure | No | Yes |

If you're handed a transcript with no tagging, use this skill first. If you have processed notes, go to customer-research-synthesis.

---

### The Analysis Protocol (run in order — do not skip steps)

1. **Read for behavior, not opinion.** What did the user actually do? Statements like "I usually just..." and "what I ended up doing was..." are behavioral gold. "I would love a feature that..." is not evidence.

2. **Extract pain moments.** When did the user express frustration, workaround, or delay? These are the moments that matter. Mark each with the direct quote.

3. **Map to JTBD.** For every pain moment, complete the frame: *When [situation], I want to [motivation], so I can [outcome].* Do not fill in blanks the user didn't give you — if you don't have a "so I can," say so.

4. **Identify workarounds.** What did users build, hack, or tolerate to get the job done without your product? Workarounds reveal unmet needs more reliably than stated preferences.

---

### Mode 1: Theme Extraction

| Theme | Evidence (direct quotes) | Frequency | Behavioral or Attitudinal | OST Opportunity Node |
|-------|--------------------------|-----------|--------------------------|----------------------|
| [Theme name] | "[Quote]" — P3 | N/X participants | Behavioral / Attitudinal | [Opportunity node label] |

Rules:
- Only promote a theme to the table if it appears in 2+ participants OR is backed by direct behavioral evidence from 1
- Label every row: Behavioral (what they did) or Attitudinal (what they said they think/want)
- Attitudinal themes without a behavioral anchor are flagged, not discarded

---

### Mode 2: JTBD Map

| When [Situation] | I want to [Motivation] | So I can [Outcome] | Evidence | Frequency |
|------------------|----------------------|-------------------|----------|-----------|
| [Specific trigger context] | [The job to be done] | [The real goal behind it] | "[Quote]" — P2 | N/X |

Do not invent outcomes. If the participant didn't say why they wanted something, mark the outcome as [inferred] and explain the inference.

---

### Mode 3: OST Input

Format ready to feed into the continuous-discovery OST skill.

**Opportunity Node Candidates**

| Opportunity Node | Evidence (quotes) | Frequency | Addressability (High/Med/Low) | Notes |
|-----------------|-------------------|-----------|-------------------------------|-------|
| [Node label] | "[Quote]" | N/X | [H/M/L] | [What would make this addressable] |

Addressability scoring:
- **High**: Clear solution space, within product scope, team has capability
- **Med**: Solvable but unclear how, or requires partnership / platform work
- **Low**: Real pain but outside product scope, or would require fundamental product rearchitecture

---

### Mode 4: Persona Signals

Identify behavioral patterns that suggest distinct user segments. Not demographic — behavioral.

| Segment Signal | Behavioral Pattern | Participants Showing It | Implication |
|----------------|-------------------|------------------------|-------------|
| [Label] | [What they do differently] | P1, P4, P7 | [What this means for product or messaging] |

Example of a good signal: "Power users build their own tracking spreadsheets before opening the product." Example of a bad signal: "Some users are managers." Segments that don't predict behavior don't help you build.

---

### Interview Analysis Rules

- Never report what users said they want without a behavioral data point to support it.
- "I would use that" is an opinion, not evidence. It does not belong in a JTBD or theme table without behavioral corroboration.
- Frequency matters. N=1 is a hypothesis, not a pattern. Be explicit about N in every output.
- When behavior and stated preference contradict each other, behavior wins. Always. Note the contradiction explicitly — it's often the most interesting finding.
- Quotes are evidence; paraphrases are interpretation. Keep them separate in your output.

## Output Style
- Lead with the most surprising or high-frequency behavioral finding, not the most flattering one
- Flag contradictions between what users said and what they did — these are insights, not noise
- When you lack behavioral backing for a finding, say so explicitly rather than presenting it as settled

## Customization Tips
- Add your OST structure to CLAUDE.md so opportunity nodes are formatted to match your existing tree
- Add your persona names if you have working hypotheses — Claude will map signals to existing personas or flag when a new segment is emerging
- Specify your minimum frequency threshold for a theme (default: 2+ participants)
