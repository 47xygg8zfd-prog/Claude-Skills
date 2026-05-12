---
name: spec-driven-dev
description: >
  Generate formal specifications before code is written. Use this skill when
  the user asks for an OpenAPI spec, a JSON schema, an interface contract, a
  service boundary definition, Given/When/Then acceptance specs, or mock API
  payloads. Also trigger when the user says things like "write the API contract",
  "define the schema for", "spec this out before we build it", "write acceptance
  criteria as Given/When/Then", "generate a mock response for", or "what are the
  interfaces between services". Works from a PRD, architecture doc, or plain
  feature description.
---

# Spec-Driven Development Skill

Write formal, machine-readable specifications before implementation begins.
Contracts are agreed. Schemas are locked. Mocks unblock parallel work.
Engineers stop asking "what does the API return?" and start building.

## When to Use

- After architecture is drafted — to lock API contracts before backend starts
- Before frontend work begins — so UI engineers can code against mocks
- When two services need to talk — to define the boundary before either team builds
- When writing a PRD — to express acceptance criteria as executable Given/When/Then
- When a backend and frontend team work in parallel — mocks let them move independently
- When onboarding a new engineer — the spec is the source of truth, not Slack history

---

## Output Formats

### 1. OpenAPI Spec (`openapi`)
Full OpenAPI 3.0 YAML. Paths, methods, request/response schemas, error codes,
authentication, and example payloads. Paste directly into Swagger Editor or Postman.

### 2. JSON Schema (`schema`)
Draft-07 JSON Schema for a data object, event payload, or configuration structure.
Includes `required`, `type`, `format`, `enum`, `pattern`, and `description` per field.
Ready to drop into a validator (Ajv, Pydantic, Zod).

### 3. Interface Contract (`contract`)
Prose + structured definition of a service boundary. Covers:
- Request shape, response shape, error codes
- SLA commitments (latency, availability)
- Versioning strategy
- Breaking vs. non-breaking change rules

### 4. Acceptance Spec (`acceptance`)
PRD user stories converted to Given/When/Then scenarios. Each scenario is:
- Independently executable (Cucumber/Gherkin-compatible)
- Mapped to the user story it satisfies
- Tagged as happy path, edge case, or error path

### 5. Mock Payloads (`mock`)
Realistic example JSON responses for every API endpoint or event schema.
Uses plausible values — not `"string"` and `0`. Ready to import into Postman
collections or MSW (Mock Service Worker) handlers.

### 6. Test Matrix (`test-matrix`)
A coverage table mapping: User Story → Acceptance Criterion → Test Case ID →
Test Type (unit/integration/e2e) → Priority (P0/P1/P2) → Automation status.
The single source of truth for QA coverage.

---

## Spec-First Protocol

Follow this sequence when generating specs from a brief:

1. **Identify boundaries** — what are the external-facing surfaces? (API endpoints, events, config schemas)
2. **Name every object** — every resource gets a schema with a name; no anonymous inline types
3. **Enumerate errors** — every endpoint must list all non-200 responses with meaning
4. **Add examples** — every schema gets at least one complete example with real-looking values
5. **Flag decisions** — mark anything that requires a team decision with `# TODO: decision needed`

---

## OpenAPI Quality Rules

- Version: always `openapi: 3.0.3`
- Every path has a `summary` and `operationId`
- Every schema property has a `description`
- All `$ref`s point to named schemas in `components/schemas`
- No inline schemas for objects — promote to components
- Auth defined in `components/securitySchemes` and referenced per-operation
- 4xx errors use RFC 7807 Problem Details shape: `{ type, title, status, detail }`

---

## Acceptance Spec Rules

- One scenario = one behavior. Never bundle two behaviors in one scenario.
- `Given` = precondition (state of the world)
- `When` = the single action being tested
- `Then` = observable outcome (what the user or system can verify)
- No UI implementation detail in `Then` — test behavior, not layout
- Tag each scenario: `@happy-path`, `@edge-case`, `@error-path`, `@p0`, `@p1`

---

## Integration Points

| Point in Workflow | What Spec-Driven Dev Adds |
|-------------------|--------------------------|
| After architecture doc | Formalizes API contracts so backend + frontend can work in parallel |
| Before sprint start | Acceptance specs give engineers done criteria before they write a line |
| During QA planning | Test matrix derived directly from acceptance specs — no gaps |
| At API review | OpenAPI spec is the review artifact — not a whiteboard photo |
| For new engineers | Specs are documentation that can't drift from reality |

---

## Example Usage

```bash
# Generate OpenAPI spec from PRD + architecture
python spec_driven_dev.py --brief "explanation engine: POST /explain takes {content, context} returns {explanation, concepts}" --mode openapi

# Convert PRD user stories to Given/When/Then
python spec_driven_dev.py --file prd.md --mode acceptance

# Generate JSON Schema for a data model
python spec_driven_dev.py --brief "concept library entry: id, title, plain_explanation, technical_definition, related_concepts[], pm_workflow_tags[]" --mode schema

# Build full spec suite (all modes)
python spec_driven_dev.py --file architecture.md --mode all --output spec-suite.md
```
