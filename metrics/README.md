# PM Metrics Playbook

Standard KPI definitions, measurement approaches, and Snowflake query patterns organized by product area. Stop re-deriving the same formulas every quarter.

## Product Areas

| File | Covers |
|------|--------|
| [acquisition.md](acquisition.md) | Signups, traffic sources, conversion funnels, CAC |
| [activation.md](activation.md) | Onboarding completion, time-to-value, aha moment |
| [engagement.md](engagement.md) | DAU/WAU/MAU, stickiness, feature adoption, session depth |
| [retention.md](retention.md) | Cohort retention, churn, resurrection, LTV |
| [revenue.md](revenue.md) | MRR, ARR, expansion, contraction, NRR |

## How to Use

Each file contains:
1. **Metric definitions** — precise, unambiguous definitions with common pitfalls
2. **Measurement approach** — how to calculate it correctly
3. **Benchmarks** — rough industry context for B2B SaaS
4. **Snowflake SQL** — copy-paste query pattern (adapt table/column names to your schema)
5. **Common mistakes** — the ways PMs most often get this metric wrong

## Schema Conventions

The SQL in this playbook assumes these table names — adjust to match yours:

| Table | Contains |
|-------|---------|
| `events` | All user actions with `user_id`, `event_type`, `event_timestamp` |
| `users` | User records with `user_id`, `account_id`, `created_at`, `is_internal` |
| `accounts` | Account records with `account_id`, `plan_tier`, `mrr`, `created_at`, `churned_at` |
| `sessions` | Session records with `session_id`, `user_id`, `started_at`, `ended_at` |

Add your actual table names to `CLAUDE.md` so the `data-queries` skill can use them automatically.
