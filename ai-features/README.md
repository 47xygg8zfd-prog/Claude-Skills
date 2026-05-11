# AI Feature Evaluation Framework

A PM's guide to scoping, testing, measuring, and shipping AI-powered features responsibly.

## Contents

| File | Covers |
|------|--------|
| [scoping.md](scoping.md) | When to use AI, how to scope the problem, build vs. buy decisions |
| [evaluation.md](evaluation.md) | Quality rubrics, human eval setup, regression testing |
| [metrics.md](metrics.md) | How to measure AI feature success in production |
| [tradeoffs.md](tradeoffs.md) | Latency, cost, accuracy tradeoffs and how to reason about them |
| [launch-checklist.md](launch-checklist.md) | Pre-launch checklist for AI features |

## When to Use This

- Before scoping an AI feature: start with [scoping.md](scoping.md)
- When running evals: start with [evaluation.md](evaluation.md)
- When defining success metrics: start with [metrics.md](metrics.md)
- When making build vs. quality vs. cost tradeoffs: start with [tradeoffs.md](tradeoffs.md)
- Before shipping: run through [launch-checklist.md](launch-checklist.md)

## The Core PM Mindset for AI Features

AI features fail for three reasons, in order of frequency:

1. **Wrong problem** — The task wasn't a good fit for AI to begin with
2. **No quality bar** — "Good enough" was never defined, so the team shipped something users don't trust
3. **No feedback loop** — The feature shipped but there's no signal on whether it's working

This framework addresses all three.
