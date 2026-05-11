# AI Feature Evaluation

How to define quality, run evals, and catch regressions before they reach users.

---

## The Eval Mindset

You cannot ship an AI feature without a quality bar. "It seems good" is not a quality bar. Before writing a single line of prompt engineering, define:

1. **What does a great output look like?** (write 5 examples)
2. **What does an acceptable output look like?** (write 5 examples)
3. **What does a failing output look like?** (write 5 examples)

These become your **eval set** — the ground truth you test against every time you change the prompt, model, or parameters.

---

## Building an Eval Set

### Step 1: Collect real inputs
Pull 50–200 real examples of the input your feature will receive. Use actual user data (anonymized) wherever possible — synthetic inputs miss the weird edge cases production data surfaces.

### Step 2: Write expected outputs
For each input, write the ideal output. This is tedious but non-negotiable. Options:
- **Write them yourself** if you're the domain expert
- **Use a stronger model** to draft, then review (e.g., use Claude Opus to evaluate outputs from Claude Haiku)
- **Hire domain experts** for specialized tasks (e.g., legal, medical)

### Step 3: Categorize inputs
Tag inputs by type so you can track quality by category:
- Common case (60–70% of volume)
- Edge case (unusual input structure, missing fields)
- Adversarial (inputs designed to break the system)
- High-stakes (inputs where errors are most costly)

### Step 4: Write evaluation criteria
For each output dimension, define a rubric:

| Dimension | 1 (Failing) | 3 (Acceptable) | 5 (Excellent) |
|-----------|-------------|----------------|---------------|
| Accuracy | Contains factual errors | Mostly correct, minor gaps | Fully accurate |
| Completeness | Missing key information | Covers main points | Covers all relevant points |
| Format | Wrong structure | Mostly correct structure | Exactly right structure |
| Tone | Wrong tone for audience | Acceptable tone | Perfectly calibrated |
| Conciseness | Too long or too short | Roughly right length | Exactly right length |

---

## Running Evals

### Manual evals (required before launch)
Run your prompt against the full eval set. Score each output on your rubric. Track:
- Average score per dimension
- % of outputs scoring ≥ 3 on all dimensions (your "pass rate")
- Failure mode breakdown (what types of errors appear most?)

**Minimum bar before shipping**: 85%+ pass rate on common cases, 70%+ on edge cases.

### LLM-as-judge (scalable ongoing eval)
Use a stronger or separate model to score outputs automatically. Useful for regression testing at scale.

```python
import anthropic

client = anthropic.Anthropic()

def evaluate_output(input_text: str, output_text: str, criteria: str) -> dict:
    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=512,
        system="""You are an expert evaluator. Score the output on the given criteria.
Return JSON: {"score": 1-5, "reasoning": "one sentence", "pass": true/false}""",
        messages=[{
            "role": "user",
            "content": f"""Input: {input_text}

Output to evaluate: {output_text}

Criteria: {criteria}"""
        }]
    )
    return response.content[0].text
```

**Pitfall**: LLM-as-judge has its own biases (favors longer outputs, confident-sounding text). Calibrate it against your manual eval set before trusting it.

### A/B testing AI outputs
When comparing prompt versions or models, A/B test with real users:
- Show 50% of users output from Prompt A, 50% from Prompt B
- Measure: acceptance rate, edit rate, task completion, downstream engagement
- **Don't use output quality ratings alone** — users often rate fluent-but-wrong outputs highly

---

## Regression Testing

Every time you change the prompt, model, or parameters: re-run evals before deploying.

Automate this in CI:
1. Store eval set in a versioned file (JSON or CSV)
2. Run eval script on every PR that touches prompt files
3. Fail the PR if pass rate drops more than 5 points vs. baseline
4. Track eval scores over time — they're your quality trendline

---

## Red-Teaming

Before launch, spend 30–60 minutes deliberately trying to break the feature:
- Input that's too short, too long, in the wrong language
- Input with sensitive content (PII, offensive language)
- Input that's ambiguous or contradictory
- Input that tries to manipulate the model (prompt injection)

Document every failure mode found and decide: fix before launch, or add a guardrail.
