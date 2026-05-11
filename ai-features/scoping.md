# AI Feature Scoping

How to decide whether to use AI, what to build, and how to scope it.

---

## Should This Be an AI Feature?

AI is a good fit when the task has **most** of these properties:

| Property | Example |
|----------|---------|
| Input is unstructured text, code, or images | Interview notes, support tickets, PRDs |
| Output is also language or structured data derived from language | Summaries, classifications, drafts |
| The task is hard to rule-base but easy for a human to judge | "Is this a good PRD?" |
| Volume is high enough that human throughput is the bottleneck | 500 support tickets/day |
| Errors are recoverable — wrong output doesn't break something critical | Draft suggestions, summaries |

AI is a **bad** fit when:
- Precision matters more than recall (e.g., financial calculations, regulatory decisions)
- The task requires real-time data the model doesn't have
- The task is well-defined enough that deterministic code is simpler
- Errors are costly and hard to detect (e.g., quietly incorrect numbers in a dashboard)

---

## The PM's AI Scoping Questions

Before writing a PRD for an AI feature, answer these:

### 1. What exact task is the model doing?
Be specific. "Summarize feedback" is vague. "Given a list of NPS verbatim responses, output the top 3 themes with representative quotes and a sentiment breakdown" is scoped.

### 2. What does a good output look like?
Write 3 examples of a great output and 3 examples of a bad output before touching a prompt or API. If you can't do this, the feature isn't scoped yet.

### 3. What does a failure look like, and what's the impact?
- **Silent failure**: Wrong output that looks right (worst — hardest to catch)
- **Obvious failure**: Nonsense output the user ignores
- **Graceful failure**: "I couldn't generate this — here's why"

Design for graceful failures. Silent failures destroy trust.

### 4. Who reviews the output?
AI features work best as **human-in-the-loop** — AI drafts, human reviews. Define explicitly whether the output is:
- **Auto-applied** (user sees result, no review step)
- **Suggested** (user accepts/rejects)
- **Draft only** (user edits before using)

Start with Draft or Suggested. Move to Auto-applied only after quality is validated.

### 5. Build vs. buy vs. wrap?
| Approach | When to use | Tradeoff |
|----------|-------------|----------|
| **Wrap an LLM API** (Claude, GPT, Gemini) | Most cases — general language tasks | Fast to ship, pay-per-token cost, prompt engineering required |
| **Fine-tune a model** | High-volume, narrow task with lots of training data | Better quality on specific task, high upfront cost, harder to maintain |
| **Buy a vertical AI tool** | When a specialist tool already does the job (e.g. Notion AI, Intercom Fin) | Fastest, least control, vendor dependency |
| **Build a custom model** | Rarely — only when your data is truly proprietary and scale justifies it | Most expensive, most control |

For most PM use cases: **wrap an LLM API**. Build the prompt layer, evaluate quality, and ship.

---

## Scoping Output Format

Use this structure in your PRD's "Proposed Solution" section for AI features:

```
Task: [Precise description of what the model does]
Input: [Exactly what goes into the prompt]
Output: [Exactly what comes out — format, length, structure]
Quality bar: [What "good" looks like — link to eval rubric]
Failure mode: [What happens when the model is wrong or uncertain]
Human-in-the-loop: [Auto-applied / Suggested / Draft only]
Model: [Which model and why — latency, cost, quality tradeoffs]
```
