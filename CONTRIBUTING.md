# Contributing to PM Skills

This repo is designed to grow. If you've built a skill, prompt, or workflow that's useful for your PM workflow, here's how to add it.

---

## Adding a New Skill

### 1. Create the folder

```
pm-skills/
└── your-skill-name/
    └── SKILL.md
```

Use lowercase kebab-case for the folder name. Keep it short and descriptive — `feature-flags`, `interview-guide`, `pricing-strategy`.

### 2. Write the SKILL.md

Every skill file should follow this structure:

```markdown
# Skill: [Name]

## Trigger Phrases
- "[phrase that activates this skill]"
- "[another phrase]"

## Description
[One paragraph. What does this skill do and when should it activate?]

## Behavior
[The main content — what Claude should do, what it should ask, what it should output.
Be specific about output format. Include examples of the output structure.]

## Output Style
[Tone, format rules, what to include/exclude]

## Customization Tips
- [How to personalize this skill with company-specific context]
```

**Checklist before submitting:**
- [ ] Trigger phrases are specific enough to not fire accidentally
- [ ] Output format is clearly defined (tables, sections, bullet lists, etc.)
- [ ] Behavior covers the happy path and at least one edge case
- [ ] Customization Tips section explains how to add company context
- [ ] Tested with at least 3 real prompts

### 3. Add an example

Create a matching example file in `examples/`:

```
examples/
└── your-skill-name-example.md
```

Use the same fictional product (Pulse) if possible so examples stay cohesive. If your skill is too domain-specific for Pulse, use a clearly labeled alternative.

### 4. Update the READMEs

Add a row to the skills table in both:
- `pm-skills/README.md`
- Root `README.md`

---

## Adding a Prompt

Open `prompts/README.md` and add:

1. A row in the relevant category table:
```markdown
| [Prompt name](#anchor) | [When to use it] |
```

2. The prompt itself in the prompts section:
```markdown
### [Prompt name]
\```
[The prompt text, with [PLACEHOLDERS] for the variable parts]
\```
```

Keep prompts self-contained — they should work by copy-pasting with minimal editing.

---

## Adding a Workflow

Create a new file in `workflows/`:

```
workflows/
└── your-workflow-name.md
```

Add a row to `workflows/README.md`.

**Workflow structure:**
- Start with an Overview section showing the skill chain as a simple diagram
- One section per step: which skill, what input, what prompt, what to carry forward
- End with a Tips section covering common mistakes and shortcuts

---

## Adding a Template

Create a new file in `templates/`:

```
templates/
└── your-template-name-template.md
```

Add a row to `templates/README.md`.

**Template guidelines:**
- Use `[bracketed placeholders]` for everything the user needs to fill in
- Match the output format of the corresponding skill (if one exists)
- Include a brief comment at the top explaining when to use it
- Delete-friendly: sections the user might not need should be easy to remove

---

## Adding an Integration

Create a new file in `integrations/`:

```
integrations/
└── tool-name.md
```

Add a row to `integrations/README.md`.

**Integration file structure:**
1. What it unlocks (table: skill → what's now possible)
2. Setup steps (credentials, config snippet, restart)
3. Example prompts (3-5 real prompts that work with the integration)
4. Required permissions
5. Customization (what to add to CLAUDE.md)

---

## General Guidelines

- **Be specific.** Vague skills produce vague outputs. Define the format explicitly.
- **Test before submitting.** Run 3+ real prompts against your skill and include the best one as the example.
- **Match the existing style.** Look at adjacent skill files for tone and structure before writing.
- **One skill, one job.** If a skill is trying to do two unrelated things, split it.
- **Keep CLAUDE.md in mind.** Skills should reference context from CLAUDE.md (product name, team, OKRs) where it's useful, so filling in CLAUDE.md makes the skill smarter.

---

## Questions?

Open an issue or add a comment in your PR describing what you're trying to build. Happy to help scope it.
