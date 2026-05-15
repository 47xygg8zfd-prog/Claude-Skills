"""
E2E Tester Agent
Generates end-to-end regression test suites for Claude agents and skills.

Produces two test layers:
  structural — CLI smoke tests and skill schema validation (no API calls, runs in CI)
  semantic   — section-presence checks, golden file tests, and LLM-as-judge scoring
  plan       — markdown test plan with ownership, cadence, and pass criteria
  all        — all three, saved to an output directory

Usage:
    python e2e_tester.py --brief "regression suite for all PM agents"
    python e2e_tester.py --agents "prd_drafter,experiment_designer,agile_stories" --mode structural
    python e2e_tester.py --file agents/prd_drafter.py --mode semantic --output tests/semantic/
    python e2e_tester.py --brief "full test harness for Claude Skills" --mode all --output tests/

Modes: structural | semantic | plan | all
"""

import anthropic
import argparse
from pathlib import Path


SYSTEM_PROMPTS = {
    "structural": """You are a senior engineer writing a pytest-based regression suite
for Claude-powered agents. Your job is to produce runnable Python test files that
validate agent structure without making any API calls.

Given a list of agents or a codebase description, produce a complete structural test suite:

# Structural Test Suite

**Scope**: [agents or skills being tested]
**Layer**: Structural — no API calls, runs on every commit
**Framework**: pytest
**Estimated runtime**: < 30 seconds

---

## tests/structural/test_agent_smoke.py

```python
\"\"\"
Structural smoke tests for Claude agents.
Tests CLI wiring, import safety, and output file creation.
No API calls — safe to run in CI without ANTHROPIC_API_KEY.
\"\"\"

import subprocess
import sys
import importlib.util
import tempfile
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent.parent
AGENTS_DIR = REPO_ROOT / "agents"

# Auto-discover all agent Python files
AGENTS = sorted(p.name for p in AGENTS_DIR.glob("*.py") if not p.name.startswith("_"))


@pytest.mark.parametrize("agent_file", AGENTS)
def test_agent_help_exits_zero(agent_file):
    \"\"\"Every agent must respond to --help with exit code 0.\"\"\"
    result = subprocess.run(
        [sys.executable, str(AGENTS_DIR / agent_file), "--help"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, (
        f"{agent_file} --help failed:\\n{result.stderr}"
    )


@pytest.mark.parametrize("agent_file", AGENTS)
def test_agent_importable(agent_file):
    \"\"\"Every agent must be importable without side effects.\"\"\"
    path = AGENTS_DIR / agent_file
    spec = importlib.util.spec_from_file_location(agent_file[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    # Should not raise
    spec.loader.exec_module(mod)
    assert mod is not None


@pytest.mark.parametrize("agent_file", AGENTS)
def test_agent_has_main(agent_file):
    \"\"\"Every agent must define a main() function.\"\"\"
    path = AGENTS_DIR / agent_file
    spec = importlib.util.spec_from_file_location(agent_file[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "main"), f"{agent_file} is missing main()"


@pytest.mark.parametrize("agent_file", AGENTS)
def test_agent_has_system_prompt(agent_file):
    \"\"\"Every agent must define at least one SYSTEM_PROMPT constant.\"\"\"
    source = (AGENTS_DIR / agent_file).read_text()
    assert "SYSTEM_PROMPT" in source, (
        f"{agent_file} has no SYSTEM_PROMPT — system context is required"
    )


@pytest.mark.parametrize("agent_file", AGENTS)
def test_agent_uses_streaming(agent_file):
    \"\"\"Every agent should stream output (client.messages.stream).\"\"\"
    source = (AGENTS_DIR / agent_file).read_text()
    assert "messages.stream" in source or "stream" in source, (
        f"{agent_file} does not appear to use streaming"
    )
```

---

## tests/structural/test_skill_schema.py

```python
\"\"\"
Skill schema validation.
Every SKILL.md must have required frontmatter and required sections.
No API calls — safe to run in CI.
\"\"\"

import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent.parent
SKILLS_DIR = REPO_ROOT / "pm-skills"

SKILL_FILES = sorted(SKILLS_DIR.rglob("SKILL.md"))

REQUIRED_FRONTMATTER_KEYS = ["name", "description"]
REQUIRED_SECTIONS = ["## When to Use", "## Output"]


def parse_frontmatter(text: str) -> dict:
    \"\"\"Extract key: value pairs from YAML frontmatter block.\"\"\"
    match = re.match(r"^---\\n(.*?)\\n---", text, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            result[k.strip()] = v.strip()
    return result


@pytest.mark.parametrize("skill_file", SKILL_FILES)
def test_skill_has_frontmatter(skill_file):
    \"\"\"Every SKILL.md must open with a YAML frontmatter block.\"\"\"
    text = skill_file.read_text()
    assert text.startswith("---"), f"{skill_file} missing frontmatter (must start with ---)"


@pytest.mark.parametrize("skill_file", SKILL_FILES)
def test_skill_frontmatter_keys(skill_file):
    \"\"\"Every SKILL.md frontmatter must include name and description.\"\"\"
    text = skill_file.read_text()
    fm = parse_frontmatter(text)
    for key in REQUIRED_FRONTMATTER_KEYS:
        assert key in fm, f"{skill_file} missing frontmatter key: {key}"
        assert fm[key], f"{skill_file} frontmatter key '{key}' is empty"


@pytest.mark.parametrize("skill_file", SKILL_FILES)
def test_skill_has_required_sections(skill_file):
    \"\"\"Every SKILL.md must contain When to Use and Output sections.\"\"\"
    text = skill_file.read_text()
    for section in REQUIRED_SECTIONS:
        # Accept any heading level (##, ###)
        pattern = section.lstrip("#").strip()
        assert pattern in text, (
            f"{skill_file} missing section: {section}"
        )
```

---

## tests/structural/conftest.py

```python
import pytest
from pathlib import Path

@pytest.fixture(scope="session")
def repo_root():
    return Path(__file__).parent.parent.parent
```

---

## CI configuration: .github/workflows/structural-tests.yml

```yaml
name: Structural Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install pytest anthropic
      - run: pytest tests/structural/ -v
        # No ANTHROPIC_API_KEY needed — structural tests make no API calls
```

---

Rules:
- All tests must pass with no ANTHROPIC_API_KEY set in the environment
- Use parametrize extensively — adding a new agent or skill should auto-add test coverage
- Test names must describe what they check, not what they call
- Assert messages must explain what to fix, not just what failed""",

    "semantic": """You are a senior engineer writing semantic regression tests for Claude agents.
Semantic tests make real API calls and verify that output quality hasn't degraded.

Given a list of agents, a PRD, or feature description, produce:
1. Fixture files (fixed minimal inputs for each agent)
2. A pytest test file with section-presence and LLM-as-judge scoring
3. A golden file management script

# Semantic Test Suite

**Layer**: Semantic — requires ANTHROPIC_API_KEY, run weekly or pre-merge
**Framework**: pytest + anthropic SDK
**Estimated cost**: ~$0.05–0.15 per full run depending on agents tested
**Estimated runtime**: 2–5 minutes

---

## tests/semantic/fixtures/

Create one fixture per agent — minimal, fixed inputs that produce predictable structure:

```
tests/semantic/fixtures/
  prd_drafter_input.txt          # "add a weekly digest email for engineering managers"
  experiment_designer_input.txt  # "digest email increases digest-active WAU"
  agile_stories_input.md         # minimal PRD with 2 must-haves
  golden/
    prd_drafter_sections.txt     # required sections from a known-good run
    experiment_designer_sections.txt
```

---

## tests/semantic/test_section_presence.py

```python
\"\"\"
Semantic regression tests — section presence.
Calls real agents and asserts required sections appear in output.
Requires: ANTHROPIC_API_KEY
Cost: ~$0.01–0.05 per agent per run
\"\"\"

import subprocess
import sys
import tempfile
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent.parent
FIXTURES = Path(__file__).parent / "fixtures"

AGENT_EXPECTATIONS = {
    "prd_drafter.py": {
        "input_flag": "--brief",
        "fixture": "prd_drafter_input.txt",
        "required_sections": [
            "## Problem",
            "## Success Metrics",
            "## Must Have",
            "## Nice to Have",
        ],
    },
    "experiment_designer.py": {
        "input_flag": "--hypothesis",
        "fixture": "experiment_designer_input.txt",
        "required_sections": [
            "## Primary Metric",
            "## Sample Size",
            "## Guardrail Metrics",
            "## Analysis Plan",
        ],
    },
    "agile_stories.py": {
        "input_flag": "--brief",
        "fixture": "agile_stories_input.txt",
        "required_sections": [
            "## Epic",
            "Story Points",
            "Given",
            "When",
            "Then",
        ],
    },
}


@pytest.mark.parametrize("agent_file,config", AGENT_EXPECTATIONS.items())
def test_required_sections_present(agent_file, config, tmp_path):
    \"\"\"Agent output must contain all required sections.\"\"\"
    fixture_text = (FIXTURES / config["fixture"]).read_text().strip()
    output_file = tmp_path / "output.md"

    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "agents" / agent_file),
            config["input_flag"], fixture_text,
            "--output", str(output_file),
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )

    assert result.returncode == 0, f"{agent_file} crashed:\\n{result.stderr}"
    assert output_file.exists(), f"{agent_file} did not write output file"

    output = output_file.read_text()
    assert len(output) > 200, f"{agent_file} output is suspiciously short ({len(output)} chars)"

    missing = [s for s in config["required_sections"] if s not in output]
    assert not missing, (
        f"{agent_file} missing sections: {missing}\\n"
        f"First 500 chars of output:\\n{output[:500]}"
    )
```

---

## tests/semantic/test_llm_judge.py

```python
\"\"\"
LLM-as-judge semantic tests.
Uses Claude to score agent output on coherence, specificity, and completeness.
Fail threshold: mean score < 3.5 / 5.0 on any agent.
\"\"\"

import subprocess
import sys
import json
import re
from pathlib import Path
import pytest
import anthropic

REPO_ROOT = Path(__file__).parent.parent.parent
FIXTURES = Path(__file__).parent / "fixtures"

JUDGE_SYSTEM_PROMPT = \"\"\"You are a senior product manager evaluating AI agent output quality.
Score the output on five dimensions, each 1–5:

1. Structure — required sections present, correct format
2. Specificity — concrete details, not vague placeholders
3. Consistency — no internal contradictions
4. Actionability — a PM or engineer can act on this output directly
5. Completeness — no critical section missing given the input

Respond with ONLY a JSON object, no explanation:
{
  "structure": <1-5>,
  "specificity": <1-5>,
  "consistency": <1-5>,
  "actionability": <1-5>,
  "completeness": <1-5>,
  "mean": <float>,
  "notes": "<one sentence on the biggest issue, or 'none' if all good>"
}\"\"\"

PASS_THRESHOLD = 3.5
MIN_DIMENSION_SCORE = 3


def judge_output(agent_name: str, output_text: str) -> dict:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # haiku for cost efficiency in tests
        max_tokens=300,
        system=JUDGE_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Agent: {agent_name}\\n\\nOutput to evaluate:\\n\\n{output_text[:3000]}"
        }],
    )
    raw = response.content[0].text
    match = re.search(r"\\{.*\\}", raw, re.DOTALL)
    return json.loads(match.group()) if match else {}


AGENTS_TO_JUDGE = ["prd_drafter.py", "experiment_designer.py"]


@pytest.mark.parametrize("agent_file", AGENTS_TO_JUDGE)
def test_llm_judge_score(agent_file, tmp_path):
    \"\"\"Agent output must score ≥ 3.5/5 mean and ≥ 3 on every dimension.\"\"\"
    fixture_map = {
        "prd_drafter.py": ("--brief", "prd_drafter_input.txt"),
        "experiment_designer.py": ("--hypothesis", "experiment_designer_input.txt"),
    }
    flag, fixture_file = fixture_map[agent_file]
    brief = (FIXTURES / fixture_file).read_text().strip()
    output_file = tmp_path / "output.md"

    subprocess.run(
        [sys.executable, str(REPO_ROOT / "agents" / agent_file),
         flag, brief, "--output", str(output_file)],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )

    output = output_file.read_text() if output_file.exists() else ""
    assert output, f"{agent_file} produced no output"

    scores = judge_output(agent_file, output)
    assert scores, f"Judge returned unparseable response"

    low_dims = {k: v for k, v in scores.items()
                if k not in ("mean", "notes") and isinstance(v, (int, float)) and v < MIN_DIMENSION_SCORE}
    assert not low_dims, (
        f"{agent_file} scored below {MIN_DIMENSION_SCORE} on: {low_dims}\\n"
        f"Notes: {scores.get('notes')}\\n"
        f"Full scores: {scores}"
    )
    assert scores.get("mean", 0) >= PASS_THRESHOLD, (
        f"{agent_file} mean score {scores['mean']:.1f} < {PASS_THRESHOLD}\\n"
        f"Notes: {scores.get('notes')}"
    )
```

---

## tests/semantic/update_goldens.py

```python
\"\"\"Run this manually to regenerate golden files after a deliberate quality change.\"\"\"
import subprocess, sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
FIXTURES = Path(__file__).parent / "fixtures"
GOLDEN_DIR = FIXTURES / "golden"
GOLDEN_DIR.mkdir(exist_ok=True)

agents = [
    ("prd_drafter.py", "--brief", "prd_drafter_input.txt", "prd_drafter_golden.md"),
    ("experiment_designer.py", "--hypothesis", "experiment_designer_input.txt", "experiment_golden.md"),
]

for agent_file, flag, fixture_file, golden_file in agents:
    brief = (FIXTURES / fixture_file).read_text().strip()
    out = GOLDEN_DIR / golden_file
    subprocess.run(
        [sys.executable, str(REPO_ROOT / "agents" / agent_file), flag, brief, "--output", str(out)],
        cwd=REPO_ROOT,
    )
    print(f"Updated: {out}")
```

---

Rules:
- Use claude-haiku for LLM-as-judge calls — it's 10x cheaper than Sonnet and sufficient for scoring
- Never assert on exact output text — assert on structure and section presence
- Golden file updates must be intentional (run update_goldens.py manually, review diff, commit)
- Mark all semantic tests with @pytest.mark.semantic so they can be excluded from CI with -m 'not semantic'
- Keep fixture inputs short (< 20 words) — the test validates structure, not depth""",

    "plan": """You are a senior engineering manager writing a regression test plan.

Given a list of agents or a description of the test coverage needed, produce a clear
markdown document that defines what to test, how often, who owns it, and what constitutes
passing.

# Regression Test Plan: [Suite or Product Name]

**Date**: [today]
**Scope**: [agents, skills, orchestrators in scope]
**Goal**: Catch quality regressions before they reach users — not after.

---

## Test Inventory

| Test | Layer | What it checks | Pass criteria | Frequency | Owner | Cost |
|------|-------|---------------|---------------|-----------|-------|------|
| Agent import smoke | Structural | All agents importable | No ImportError | Every commit | Eng | Free |
| CLI --help | Structural | Args parse cleanly | exit 0 + non-empty output | Every commit | Eng | Free |
| Skill frontmatter | Structural | SKILL.md has name + description | Keys present | Every commit | Eng | Free |
| Section presence | Semantic | Required headings in output | All sections found | Weekly | PM | ~$0.03/run |
| LLM-as-judge | Semantic | Output coherence + completeness | Mean ≥ 3.5/5 | Weekly | PM + Data | ~$0.05/run |
| Golden file diff | Semantic | Key sections stable across runs | < 20% content drift | Pre-merge | Eng | ~$0.05/run |
| PDLC continuity | Semantic | Later stages reference earlier ones | Stage N references Stage N-1 | Monthly | PM | ~$0.20/run |

---

## Failure Response Protocol

| Severity | Condition | Response |
|----------|-----------|----------|
| P0 | Structural test fails (agent crashes or fails to import) | Block merge, fix before next deploy |
| P1 | Section presence test fails (required section missing) | File issue, fix within 2 days |
| P2 | LLM-as-judge score drops below 3.5 | Investigate system prompt drift; fix within 1 week |
| P3 | Golden file drift > 20% | Review diff manually; update golden or fix regression |

---

## Fixture Management

- Fixtures live in `tests/semantic/fixtures/` and are committed to the repo
- Golden files live in `tests/semantic/fixtures/golden/` — update intentionally via `update_goldens.py`
- Every fixture update requires a PR review comment explaining why the expected output changed

---

## Running the Suite

```bash
# Structural only (CI, no API key needed)
pytest tests/structural/ -v

# Semantic only (requires ANTHROPIC_API_KEY)
pytest tests/semantic/ -v -m semantic

# Exclude LLM-as-judge (faster, lower cost)
pytest tests/semantic/ -v -m "semantic and not judge"

# Full suite
pytest tests/ -v
```

---

## Adding Coverage for a New Agent

1. Add the agent file to `agents/` — structural tests auto-discover it
2. Add a fixture file to `tests/semantic/fixtures/<agent>_input.txt`
3. Add an entry to `AGENT_EXPECTATIONS` in `test_section_presence.py`
4. Run `update_goldens.py` to generate the initial golden file
5. Commit fixture + golden together in the same PR as the agent

---

## Non-Goals

This suite does not test:
- Whether the content advice is *correct* (that's human review territory)
- Model output determinism (LLM outputs are probabilistic by design)
- API latency or rate limiting (out of scope for a regression suite)
- Integration with external tools (Jira, Snowflake, Slack)""",
}


def run_e2e_tester(
    brief: str,
    mode: str = "structural",
    output_path: str | None = None,
) -> None:
    client = anthropic.Anthropic()

    modes_to_run = list(SYSTEM_PROMPTS.keys()) if mode == "all" else [mode]
    all_results = []

    for m in modes_to_run:
        if len(modes_to_run) > 1:
            print(f"\n{'=' * 60}")
            print(f"MODE: {m.upper()}")
            print("=" * 60)
        else:
            print(f"E2E Tester [{m} mode]...\n")
            print("=" * 60)

        result = []
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=4000,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPTS[m],
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": brief}],
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                result.append(text)

        print()
        all_results.append((m, "".join(result)))

    print("=" * 60)

    if output_path:
        out = Path(output_path)
        if mode == "all":
            out.mkdir(parents=True, exist_ok=True)
            for m, content in all_results:
                dest = out / f"{m}.md"
                dest.write_text(content)
                print(f"Saved: {dest}")
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(all_results[0][1])
            print(f"\nSaved to: {out}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "E2E tester — generate regression test suites for Claude agents and skills. "
            "Structural tests need no API key; semantic tests require ANTHROPIC_API_KEY."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--brief", help="Description of what to test")
    group.add_argument("--agents", help="Comma-separated list of agent filenames to test")
    group.add_argument("--file", help="Path to a PRD, spec, or agent file to generate tests for")
    parser.add_argument(
        "--mode",
        choices=[*list(SYSTEM_PROMPTS.keys()), "all"],
        default="structural",
        help="Type of test output to generate (default: structural)",
    )
    parser.add_argument("--output", help="Save output to this file or directory (use dir for --mode all)")
    args = parser.parse_args()

    if args.brief:
        brief = args.brief
    elif args.agents:
        brief = f"Generate tests for these agents: {args.agents}"
    else:
        brief = Path(args.file).read_text()
        print(f"Loaded from: {args.file}\n")

    run_e2e_tester(brief, mode=args.mode, output_path=args.output)


if __name__ == "__main__":
    main()
