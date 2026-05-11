---
name: monte-carlo
description: >
  Run Monte Carlo simulations for PM use cases: project timeline forecasting, sprint throughput
  modeling, confidence intervals for delivery dates, and risk-adjusted roadmap planning. Use this
  skill whenever the user asks about delivery forecasts, "when will we finish", probability of
  hitting a date, throughput-based estimates, or uncertainty modeling for roadmaps. Also trigger
  for "Monte Carlo", "confidence interval", "forecast", "delivery date estimate", "how likely are
  we to hit X by Y", or "simulate our sprint velocity". Produces probability distributions and
  actionable confidence-level estimates.
---

# Monte Carlo Simulation Skill

Model uncertainty in delivery timelines, sprint throughput, and roadmap forecasts.

---

## What Monte Carlo Simulations Do (PM-Friendly Explanation)

Instead of giving a single "best guess" date, Monte Carlo runs thousands of simulations using
your historical data to give you a probability distribution:

> "There's an 85% chance we finish by June 15, and a 50% chance we finish by May 30."

This is more honest and more useful than a single date — it shows stakeholders the range of outcomes.

---

## Use Cases

1. **Sprint Throughput Forecast** — Given past velocity, when will we finish the backlog?
2. **Delivery Date Confidence** — What's the probability of hitting a hard deadline?
3. **Story Count Forecast** — How many stories will we complete in N sprints?
4. **Risk-Adjusted Roadmap** — Model best/likely/worst case for a roadmap milestone

---

## Running a Simulation

### What You Need
- **Throughput data**: Stories completed per sprint (last 10–20 sprints ideal)
- **Backlog size**: Number of stories remaining
- **Target date** (optional): Deadline to evaluate probability against
- **Number of simulations**: 10,000 is standard

### Python Simulation Script

```python
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def monte_carlo_forecast(
    throughput_history: list[int],  # stories completed per sprint
    backlog_size: int,               # remaining stories
    sprint_length_days: int = 14,    # sprint duration
    n_simulations: int = 10_000,
    target_date: datetime = None,    # optional hard deadline
    start_date: datetime = None
) -> dict:
    """
    Run Monte Carlo simulation for delivery forecasting.
    Returns percentile estimates and optional deadline probability.
    """
    start_date = start_date or datetime.today()
    sprints_to_complete = []

    for _ in range(n_simulations):
        remaining = backlog_size
        sprints = 0
        while remaining > 0:
            # Sample from historical throughput
            throughput = np.random.choice(throughput_history)
            remaining -= throughput
            sprints += 1
        sprints_to_complete.append(sprints)

    sprints_array = np.array(sprints_to_complete)

    # Convert sprints to dates
    def sprints_to_date(n):
        return start_date + timedelta(days=n * sprint_length_days)

    results = {
        "p50_sprints": int(np.percentile(sprints_array, 50)),
        "p85_sprints": int(np.percentile(sprints_array, 85)),
        "p95_sprints": int(np.percentile(sprints_array, 95)),
        "p50_date": sprints_to_date(np.percentile(sprints_array, 50)),
        "p85_date": sprints_to_date(np.percentile(sprints_array, 85)),
        "p95_date": sprints_to_date(np.percentile(sprints_array, 95)),
        "mean_sprints": round(np.mean(sprints_array), 1),
        "std_sprints": round(np.std(sprints_array), 1),
    }

    if target_date:
        target_sprints = (target_date - start_date).days / sprint_length_days
        prob = np.mean(sprints_array <= target_sprints)
        results["probability_by_target"] = round(prob * 100, 1)
        results["target_date"] = target_date

    return results


def print_forecast(results: dict):
    """Print human-readable forecast summary."""
    print("=" * 50)
    print("📊 MONTE CARLO DELIVERY FORECAST")
    print("=" * 50)
    print(f"  50% confidence (likely):      {results['p50_date'].strftime('%b %d, %Y')} ({results['p50_sprints']} sprints)")
    print(f"  85% confidence (safe):        {results['p85_date'].strftime('%b %d, %Y')} ({results['p85_sprints']} sprints)")
    print(f"  95% confidence (very safe):   {results['p95_date'].strftime('%b %d, %Y')} ({results['p95_sprints']} sprints)")
    print(f"  Average: {results['mean_sprints']} sprints ± {results['std_sprints']}")

    if "probability_by_target" in results:
        prob = results["probability_by_target"]
        target = results["target_date"].strftime('%b %d, %Y')
        emoji = "✅" if prob >= 80 else "⚠️" if prob >= 50 else "🚨"
        print(f"\n  {emoji} Probability of hitting {target}: {prob}%")
    print("=" * 50)


# ── Example Usage ──────────────────────────────────────
if __name__ == "__main__":
    # Historical sprint throughput (stories completed)
    past_throughput = [8, 12, 7, 10, 9, 11, 8, 13, 9, 10, 8, 11]

    results = monte_carlo_forecast(
        throughput_history=past_throughput,
        backlog_size=45,
        sprint_length_days=14,
        target_date=datetime(2025, 9, 1),
        start_date=datetime.today()
    )

    print_forecast(results)
```

---

## How to Run

1. Gather your last 10–20 sprints of completed story counts
2. Count remaining stories in the backlog
3. Plug into the script above
4. Read the output

**To run quickly:**
```bash
pip install numpy pandas
python monte_carlo.py
```

---

## Interpreting Results for Stakeholders

| Confidence Level | When to Use |
|-----------------|-------------|
| **50% (p50)** | Internal "likely" date — don't share externally |
| **85% (p85)** | Recommended for stakeholder commitments |
| **95% (p95)** | High-stakes launches, regulatory, contractual deadlines |

**Script for stakeholders:**
> "Based on our last 12 sprints of throughput, we have an 85% probability of completing this by [date]. There's a 50% chance we finish earlier, by [earlier date]. The main variables that could shift this are [risk factors]."

---

## Scope Change Impact Calculator

When scope is added mid-sprint, use this to show impact:

```python
def scope_change_impact(
    current_results: dict,
    added_stories: int,
    throughput_history: list[int],
    backlog_size: int,
    sprint_length_days: int = 14
) -> None:
    """Show before/after impact of adding scope."""
    new_results = monte_carlo_forecast(
        throughput_history=throughput_history,
        backlog_size=backlog_size + added_stories,
        sprint_length_days=sprint_length_days
    )
    original_p85 = current_results["p85_date"]
    new_p85 = new_results["p85_date"]
    delta_days = (new_p85 - original_p85).days

    print(f"\n⚠️  Scope Change Impact: +{added_stories} stories")
    print(f"   Original 85% date: {original_p85.strftime('%b %d, %Y')}")
    print(f"   New 85% date:      {new_p85.strftime('%b %d, %Y')}")
    print(f"   Slippage:          +{delta_days} days")
```

---

## Common PM Questions & Answers

**"Can we hit the Q3 deadline?"**
→ Run simulation with target date. If probability < 70%, escalate and discuss scope/resource tradeoffs.

**"The CEO wants a date."**
→ Give p85 date. Frame as "We're highly confident we'll deliver by X."

**"Engineering keeps missing estimates."**
→ Monte Carlo doesn't use estimates — it uses actual historical throughput. This sidesteps estimation debates.

**"We just added 10 stories. How does that affect the date?"**
→ Use the scope change impact calculator above.

---

## Integration Points
- Use **data-queries** skill to pull throughput history from Snowflake/Jira data
- Use **prd** skill to define scope before sizing the backlog
- Paste simulation output into **pptx** skill for exec roadmap presentations
