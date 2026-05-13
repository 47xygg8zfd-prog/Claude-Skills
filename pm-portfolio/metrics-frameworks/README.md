# Metrics Framework — Pulse

## Why This Exists

Most product teams have metrics. Few have a metrics *framework*. The difference matters: a list of metrics is just a dashboard. A framework is a testable theory about how your product creates value and what inputs drive that value up or down.

The problem with metrics-as-dashboards is that everything looks important when nothing is prioritized. An eng manager opens seven charts and closes the tab. A metrics framework forces you to make a bet: *this* is the one number that tells you if the product is working, and *these* are the input levers most likely to move it.

This framework is built around a single principle: every input metric must have a documented hypothesis linking it to the north star. If you can't write the sentence "If [input metric] increases by X, we expect [north star] to increase because [mechanism]," the metric doesn't belong in the tree.

## How This Framework Is Structured

**`north-star-metric.md`** — Defines digest-active WAU: what it measures, why it was chosen over alternatives, the equation decomposing it into controllable inputs, and how to interpret movement in the number.

**`metric-tree.md`** — The full input metric hierarchy. Four layers: north star → growth levers (acquisition, activation, engagement, retention) → driver metrics → sub-drivers. Every metric includes a definition, baseline, target, owner, and whether it leads or lags the north star.

**`saas-retention-framework.md`** — Retention-specific analysis: cohort tables, reading retention curves, diagnosing failure modes, and the SQL to run this in Snowflake against Pulse's actual tables.

## The Core Principle

A metric tree is only useful if it changes what you work on. The goal is not comprehensiveness — it's focus. At any point in time, two or three input metrics will have disproportionate leverage on the north star. This framework is designed to surface those levers and tell you which ones to pull right now, given where Pulse actually is in Q2 2026.
