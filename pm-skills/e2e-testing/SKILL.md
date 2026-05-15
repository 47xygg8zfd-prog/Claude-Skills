---
name: e2e-testing
description: >
  Design and generate end-to-end regression test suites for Claude agents and skills.
  Use this skill when the user wants to validate that agents produce quality output,
  catch regressions before they ship, or build a test harness for a Claude-powered
  product. Trigger on phrases like "create a regression suite", "test the agents",
  "e2e tests for", "validate agent output", "golden file tests", "does this agent
  still work", or "test coverage for skills". Works from a brief, a list of agents,
  a PRD, or an existing codebase.
---

# E2E Testing Skill

Regression suites for Claude agents are different from unit tests. The output is
probabilistic, not deterministic — so tests must check *structure and substance*,
not exact strings.

## Two-Layer Testing Model

### Layer 1: Structural (fast, free, run on every commit)

Validates that agents are wired up correctly without spending API tokens:

- **Import smoke tests** — every agent module loads without error
- **CLI argument tests** — `--help` works, required args are enforced, `--output` writes a file
- **Skill schema tests** — every `SKILL.md` has required frontmatter (`name`, `description`) and required sections
- **Output file tests** — agent with `--output result.md` produces a non-empty file
- **Mode enumeration** — every mode listed in `--help` is reachable without crash

### Layer 2: Semantic (costs tokens, run weekly or pre-merge)

Validates that output *quality* hasn't degraded:

- **Section presence** — output contains expected headings (e.g., `## Must Have`, `## Success Metrics`)
- **Metric extraction** — output contains expected patterns (percentages, SQL, RICE scores)
- **Golden file diff** — key sections compared against a saved baseline; flag if missing
- **LLM-as-judge** — Claude scores output coherence and completeness (1–5); fail if < 3
- **Stage continuity** — in orchestrated runs, later stages reference earlier stage content

---

## Output Formats

### 1. Structural Test Suite (`structural`)

A complete `pytest` file covering CLI smoke tests and schema validation:

```python
# tests/structural/test_agents.py
import subprocess, sys, importlib
import pytest
from pathlib import Path

AGENTS = [...]  # auto-discovered from agents/*.py

@pytest.mark.parametrize("agent", AGENTS)
def test_agent_help(agent):
    result = subprocess.run(
        [sys.executable, f"agents/{agent}.py", "--help"],
        capture_output=True, text=True
    )
    assert result.returncode == 0

@pytest.mark.parametrize("agent", AGENTS)
def test_agent_importable(agent):
    name = agent.replace(".py", "")
    spec = importlib.util.spec_from_file_location(name, f"agents/{agent}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod is not None
```

### 2. Semantic Test Suite (`semantic`)

Golden file tests and section-presence assertions:

```python
# tests/semantic/test_golden.py
# Requires: ANTHROPIC_API_KEY and a saved fixtures/golden_prd.md

REQUIRED_SECTIONS = {
    "prd_drafter": ["## Problem", "## Must Have", "## Success Metrics"],
    "experiment_designer": ["## Primary Metric", "## Sample Size"],
    "agile_stories": ["## Epic", "Story Points"],
}
```

### 3. Test Plan Document (`plan`)

A markdown document describing what to test, how often, and who owns each suite:

```
## Regression Test Plan: [Agent or Suite Name]

| Test | Layer | Frequency | Owner | Pass criteria |
|------|-------|-----------|-------|---------------|
| CLI smoke | Structural | Every commit (CI) | Eng | exit 0 + non-empty help |
| Section presence | Semantic | Weekly | PM + Data | All required headings present |
| Golden file diff | Semantic | Pre-merge | Eng | < 20% content change |
| LLM-as-judge | Semantic | Weekly | PM | Score ≥ 3/5 on coherence |
```

### 4. Full Suite (`all`)

Structural tests + semantic tests + test plan document, output to a directory.

---

## Fixture Design Rules

- Use fixed, minimal inputs — the briefer the fixture, the faster and cheaper the test
- Save golden files after a known-good run; review diffs manually before updating
- One fixture per agent — don't reuse the same input across agents (masks agent-specific regressions)
- Mark golden files with a date and model version — model upgrades can shift output style

## LLM-as-Judge Scoring Rubric

When using Claude to evaluate agent output, score on these five dimensions:

| Dimension | What it checks |
|-----------|---------------|
| Structure | Required sections present, correct format |
| Specificity | Concrete details vs. vague placeholders |
| Consistency | Internal coherence (no contradictions) |
| Actionability | Output enables a next step (PM, engineer, or exec can act on it) |
| Completeness | No critical section missing given the input |

Score each 1–5. Fail the test if any dimension scores < 3 or mean < 3.5.

---

## Integration Points

- Use **analytics** skill after writing tests to validate that test results are measurable
- Use **spec-driven-dev** to define the interface contract before writing test assertions
- Run structural tests in CI via **GitHub Actions** (no API key needed)
- Run semantic tests via cron or pre-merge gate (requires `ANTHROPIC_API_KEY`)
- Use **codebase-reader** to auto-discover all agents and skills before writing parametrized tests
