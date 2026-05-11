---
name: codebase-reader
description: >
  Systematically read, map, and explain a codebase. Use this skill when the user
  asks Claude to understand, explore, summarize, or navigate source code — whether
  it's a new repo they've joined, a codebase they're reviewing for a technical
  decision, or their own code they want explained or documented. Trigger phrases:
  "read the codebase", "understand this repo", "explain the code", "give me a
  map of this project", "what does this codebase do", "how is this structured",
  "I'm new to this repo", "audit the code", "summarize the architecture".
---

# Codebase Reader Skill

Read, map, and explain any codebase — from a bird's-eye architecture view down to specific file or function explanations.

## When to Use
- Onboarding to a new repository or codebase
- Technical due diligence on a product or acquisition
- Preparing for an architecture review or RFC
- Helping a PM or non-technical stakeholder understand what the code does
- Generating missing documentation (README, architecture doc, ADR)

---

## Reading Protocol

Work through the codebase in this order — stop when you have enough to answer the user's question, or continue through all layers for a full audit.

### Layer 1 — Orientation (always do this first)

Read in order:
1. `README.md` — project purpose, setup, key commands
2. `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` — tech stack, dependencies, scripts
3. `.github/`, `Makefile`, `docker-compose.yml` — how it's built and deployed
4. Top-level directory structure — what each folder is responsible for

**Output**: A 3-5 sentence orientation summary covering: what the project does, the language/framework, how to run it, and what the top-level folders mean.

### Layer 2 — Architecture Map

Identify and map:
- **Entry points**: where does execution start? (`main.py`, `index.ts`, `cmd/`, `app.py`, `server.js`)
- **Core modules**: what are the 5-10 most important files or packages?
- **Data layer**: where are models, schemas, or migrations defined?
- **API surface**: routes, controllers, GraphQL schema, gRPC definitions
- **Background jobs**: workers, cron jobs, queues, event handlers
- **External integrations**: third-party APIs, SDKs, webhooks called or received

**Output**: An architecture map showing how the pieces connect. Use a text diagram if the structure is non-obvious.

```
[Entry Point]
    ↓
[Router / Controller Layer]
    ↓
[Service / Business Logic Layer]
    ↓
[Repository / Data Access Layer]
    ↓
[Database / External Services]
```

### Layer 3 — Key File Deep-Dives

For each key file identified in Layer 2:
- **Purpose**: what this file is responsible for
- **Key functions / classes**: name, signature, what it does
- **Dependencies**: what it imports and why
- **Gotchas**: anything surprising, non-obvious, or worth flagging

### Layer 4 — Data Model

- List all entities / models / tables with their key fields
- Identify relationships (one-to-many, many-to-many)
- Note any denormalization, soft deletes, or non-obvious schema decisions
- Flag missing indexes or potential performance issues if visible in the schema

### Layer 5 — Quality Signals

Scan for:
- **Test coverage**: are there tests? What framework? Rough coverage impression?
- **Error handling**: is it consistent? Any obvious swallowed errors?
- **Logging**: structured or unstructured? Sufficient for production debugging?
- **Security**: obvious issues — hardcoded secrets, SQL string interpolation, unvalidated input
- **Technical debt hotspots**: files with TODO/FIXME comments, unusually large files, deep nesting

---

## Output Formats

### Full Codebase Report
Use when the user wants a complete understanding. Produce all 5 layers in order.

### Architecture One-Pager
Use when the user wants a shareable summary for stakeholders. Produce:
- What it does (2 sentences)
- Tech stack (bullets)
- Architecture diagram (text)
- Key components (table: name, responsibility)
- Open questions or risks

### Onboarding Guide
Use when the user is new to the repo. Produce:
- "What is this?" (1 paragraph)
- "How do I run it?" (step-by-step commands)
- "Where does [feature] live?" (map of key locations)
- "What should I read first?" (ordered reading list)
- "What are the gotchas?" (3-5 things that will trip you up)

### Specific File or Function Explanation
Use when the user points at a specific file, function, or concept. Produce:
- What it does (plain language)
- Why it exists (what problem it solves)
- How it works (step-by-step for complex logic)
- What calls it and what it calls
- Edge cases or failure modes to know about

---

## Output Guidelines

- **Plain language first** — explain what code does in terms a non-engineer can follow, then add technical detail
- **Show, don't just tell** — quote specific lines or function names when making claims about the code
- **Flag uncertainty** — if you can't determine something from the code, say so rather than guessing
- **Surface risks** — if you see something that looks like a bug, security issue, or performance problem, call it out
- **Ask before deep-diving** — for large codebases, confirm the user's focus before spending time on Layer 3+

## Integration Points

- Use **tech-translation** to explain findings to non-technical stakeholders
- Use **prd** skill if the codebase reading is in service of writing a feature spec
- Use **technical-architect** agent for deeper architecture analysis and ADR writing
- Use **architecture-designer** agent to produce a formal system design doc from the codebase reading
