# Spec Suite: TechBridge — PM Technical Fluency Platform
**Stage**: Spec-Driven Development | **Date**: 2026-05-12
**Status**: Draft — requires sign-off from backend, frontend, and QA before sprint start

---

## OpenAPI Contracts

```yaml
openapi: 3.0.3
info:
  title: TechBridge API
  version: 1.0.0
  description: API for the TechBridge PM Technical Fluency Platform

servers:
  - url: https://api.techbridge.app/v1

security:
  - bearerAuth: []

paths:
  /explain:
    post:
      summary: Generate a plain-language explanation of technical content
      operationId: generateExplanation
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExplainRequest'
            example:
              content: "We need to refactor the auth layer before we can add SSO. The current implementation tightly couples session management to the monolith."
              context: "Slack message from tech lead in #product-eng"
      responses:
        '200':
          description: Streaming explanation (text/event-stream)
          content:
            text/event-stream:
              schema:
                $ref: '#/components/schemas/ExplanationChunk'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/RateLimited'
        '502':
          $ref: '#/components/responses/UpstreamError'

  /concepts:
    get:
      summary: List and search the concept library
      operationId: listConcepts
      parameters:
        - name: q
          in: query
          schema:
            type: string
          description: Full-text search query
          example: "database index"
        - name: tag
          in: query
          schema:
            type: string
            enum: [sprint-planning, architecture-review, incident-debrief, technical-debt, writing-requirements]
          description: Filter by PM workflow tag
        - name: page
          in: query
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 50
            default: 20
      responses:
        '200':
          description: Paginated list of concepts
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ConceptList'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

  /concepts/{id}:
    get:
      summary: Get a single concept by ID
      operationId: getConcept
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Full concept detail
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Concept'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'

  /surveys:
    post:
      summary: Submit a confidence survey response
      operationId: submitSurvey
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SurveyRequest'
            example:
              day: 14
              score: 4
              sub_scores:
                estimate_evaluation: 4
                architecture_questions: 3
                requirements_writing: 4
                incident_participation: 3
                technical_debt_triage: 4
      responses:
        '201':
          description: Survey recorded
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SurveyResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '409':
          description: Survey for this day already submitted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProblemDetails'

  /bookmarks:
    post:
      summary: Bookmark an explanation or concept
      operationId: createBookmark
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookmarkRequest'
      responses:
        '201':
          description: Bookmark created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookmarkResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
    Unauthorized:
      description: Missing or invalid authentication
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
    RateLimited:
      description: Rate limit exceeded (20 req/hour/user for /explain)
      headers:
        Retry-After:
          schema:
            type: integer
          description: Seconds until rate limit resets
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'
    UpstreamError:
      description: Claude API unavailable
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'

  schemas:
    ExplainRequest:
      type: object
      required: [content]
      properties:
        content:
          type: string
          minLength: 10
          maxLength: 5000
          description: The technical text to explain (Slack message, ticket, design doc excerpt)
        context:
          type: string
          maxLength: 500
          description: Optional context about where this content came from

    ExplanationChunk:
      type: object
      properties:
        chunk:
          type: string
          description: Streaming text fragment (present on all events except the final)
        done:
          type: boolean
          description: True on the final event only
        explanation_id:
          type: string
          format: uuid
          description: ID of the saved explanation (present only on the final event)

    ConceptSummary:
      type: object
      required: [id, title, plain_explanation, workflow_tags]
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        title:
          type: string
          description: The technical term or concept name
          example: "Database Index"
        plain_explanation:
          type: string
          description: One-sentence plain-language summary
          example: "A lookup table that lets the database find rows without scanning every record."
        workflow_tags:
          type: array
          items:
            type: string
          description: Which PM workflows this concept is relevant to
          example: ["technical-debt", "architecture-review"]

    Concept:
      allOf:
        - $ref: '#/components/schemas/ConceptSummary'
        - type: object
          properties:
            technical_depth:
              type: string
              description: More detailed technical explanation for PMs who want to go deeper
            pm_script:
              type: string
              description: Example of what to say to an engineer when this topic comes up
            related_concept_ids:
              type: array
              items:
                type: string
                format: uuid
            updated_at:
              type: string
              format: date-time
              readOnly: true

    ConceptList:
      type: object
      required: [concepts, total]
      properties:
        concepts:
          type: array
          items:
            $ref: '#/components/schemas/ConceptSummary'
        total:
          type: integer
          description: Total matching concepts (for pagination UI)
        next_cursor:
          type: string
          nullable: true
          description: Cursor for the next page; null if this is the last page

    SurveyRequest:
      type: object
      required: [day, score]
      properties:
        day:
          type: integer
          enum: [0, 14, 30]
          description: Which survey checkpoint this is
        score:
          type: integer
          minimum: 1
          maximum: 5
          description: Overall confidence score
        sub_scores:
          type: object
          description: Per-dimension confidence scores (optional but encouraged)
          properties:
            estimate_evaluation:
              type: integer
              minimum: 1
              maximum: 5
            architecture_questions:
              type: integer
              minimum: 1
              maximum: 5
            requirements_writing:
              type: integer
              minimum: 1
              maximum: 5
            incident_participation:
              type: integer
              minimum: 1
              maximum: 5
            technical_debt_triage:
              type: integer
              minimum: 1
              maximum: 5

    SurveyResponse:
      type: object
      properties:
        survey_id:
          type: string
          format: uuid
        recorded_at:
          type: string
          format: date-time

    BookmarkRequest:
      type: object
      properties:
        explanation_id:
          type: string
          format: uuid
          description: ID of the explanation to bookmark (one of explanation_id or concept_id required)
        concept_id:
          type: string
          format: uuid
          description: ID of the concept to bookmark

    BookmarkResponse:
      type: object
      properties:
        bookmark_id:
          type: string
          format: uuid

    ProblemDetails:
      type: object
      required: [type, title, status]
      description: RFC 7807 Problem Details
      properties:
        type:
          type: string
          format: uri
          example: "https://api.techbridge.app/errors/rate-limited"
        title:
          type: string
          example: "Rate limit exceeded"
        status:
          type: integer
          example: 429
        detail:
          type: string
          example: "You have exceeded 20 explanation requests per hour. Retry after 1847 seconds."
```

**Design Notes**:
- **Auth**: Bearer JWT via Auth0. All endpoints require auth — no anonymous usage. This is intentional: confidence tracking requires a persistent user identity.
- **Streaming**: `/explain` returns `text/event-stream`, not JSON. Frontend must use `EventSource` or `fetch` with `ReadableStream`. Final event includes `explanation_id` so the client can show the bookmark button.
- **Versioning**: URL path (`/v1`). When breaking changes are needed, `/v2` is introduced and `/v1` is sunset with 90 days notice.
- **Error shape**: RFC 7807 throughout — consistent for frontend error handling and future API consumers.
- **Rate limiting**: 20 req/hour/user on `/explain` only. Other endpoints are not rate-limited in v1.

---

## JSON Schemas (Key Objects)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://api.techbridge.app/schemas/Explanation.json",
  "title": "Explanation",
  "description": "A generated plain-language explanation of technical content",
  "type": "object",
  "required": ["id", "user_id", "input_text", "output_text", "created_at"],
  "properties": {
    "id": { "type": "string", "format": "uuid", "readOnly": true },
    "user_id": { "type": "string", "format": "uuid", "description": "Owner of this explanation" },
    "input_text": { "type": "string", "minLength": 10, "maxLength": 5000 },
    "output_text": { "type": "string", "description": "Full generated explanation text" },
    "input_type": {
      "type": "string",
      "enum": ["slack_msg", "ticket", "design_doc", "other"],
      "description": "Auto-detected or user-specified content type"
    },
    "created_at": { "type": "string", "format": "date-time", "readOnly": true }
  },
  "examples": [{
    "id": "a3f7c812-1b2d-4e5f-9a0b-3c4d5e6f7a8b",
    "user_id": "d1e2f3a4-b5c6-7d8e-9f0a-1b2c3d4e5f6a",
    "input_text": "We need to refactor the auth layer before we can add SSO.",
    "output_text": "In plain English: The code that handles logins needs to be cleaned up...",
    "input_type": "slack_msg",
    "created_at": "2026-05-12T14:32:00Z"
  }]
}
```

---

## Acceptance Specs (Given/When/Then)

```gherkin
Feature: Contextual Explanation Engine

  # User Story 1: Mid-level PM wants plain-language explanation of technical content

  @happy-path @p0
  Scenario: PM gets a plain-language explanation of a technical Slack message
    Given a PM is authenticated and on the Explain screen
    When they paste "We need to refactor the auth layer before adding SSO" and tap "Explain this"
    Then they see a streaming explanation appear within 3 seconds
    And the explanation contains a "Plain English" section
    And the explanation contains a "Why engineers care" section
    And the explanation contains a "What to ask next" section

  @happy-path @p0
  Scenario: Explanation is saved and accessible after generation
    Given a PM has just received an explanation
    When the streaming completes
    Then the explanation appears in "Recent Explanations" on the home screen
    And the explanation can be reopened by tapping it

  @edge-case @p1
  Scenario: PM pastes a very short input
    Given a PM is on the Explain screen
    When they type fewer than 10 characters and tap "Explain this"
    Then the button remains disabled
    And an inline message reads "Paste at least a sentence to explain"

  @error-path @p0
  Scenario: Claude API returns an error during streaming
    Given a PM is waiting for an explanation
    When the Claude API returns a 5xx error
    Then the streaming stops
    And a message reads "Something went wrong — try again"
    And a "Try again" button is visible
    And the original input text is preserved in the textarea

  @p0 @security
  Scenario: Unauthenticated user cannot access the explanation engine
    Given a user is not logged in
    When they attempt to call POST /api/explain
    Then the API returns HTTP 401
    And no explanation is generated

  @p1 @edge-case
  Scenario: PM hits the rate limit
    Given a PM has made 20 explanation requests in the past hour
    When they attempt to generate a 21st explanation
    Then the API returns HTTP 429
    And the UI shows "You've used your explanation quota for this hour. Come back in [X] minutes."

Feature: Concept Library

  # User Story 2: PM preparing for architecture review wants plain-language briefing

  @happy-path @p0
  Scenario: PM searches for a technical concept
    Given a PM is on the Concept Library screen
    When they type "database index" in the search bar
    Then a list of matching concepts appears within 500ms
    And each result shows the concept title and a one-line description

  @happy-path @p1
  Scenario: PM filters concepts by workflow
    Given a PM is on the Concept Library screen
    When they tap the "Architecture Review" filter chip
    Then only concepts tagged "architecture-review" are displayed
    And the search bar still works within the filtered set

  @edge-case @p1
  Scenario: PM searches for a term with no matches
    Given a PM is on the Concept Library screen
    When they search for "zythocracy"
    Then the results area shows "No concepts match 'zythocracy' — try a simpler term"
    And no error is thrown

Feature: Confidence Tracker

  # User Story 3: Senior PM wants to evaluate engineering estimate reasonableness

  @happy-path @p0
  Scenario: PM submits a day-0 confidence survey at signup
    Given a PM has just created an account
    When they complete the day-0 confidence survey with a score of 2
    Then the score is saved
    And subsequent API calls to POST /surveys with day=0 return HTTP 409

  @p1 @edge-case
  Scenario: PM submits a duplicate survey for the same checkpoint
    Given a PM has already submitted a day-14 survey
    When they attempt to submit another day-14 survey
    Then the API returns HTTP 409 with detail "Survey for day 14 already submitted"

  @p0 @happy-path
  Scenario: PM bookmarks an explanation
    Given a PM has just received an explanation
    When they tap the bookmark icon
    Then the explanation is saved to "My Saved"
    And a toast notification reads "Saved to My Saved"
    And the bookmark icon changes to a filled state
```

---

## Open Decisions (must be resolved before sprint start)

| Decision | Options | Owner | Target |
|----------|---------|-------|--------|
| Streaming transport | SSE via `fetch` + `ReadableStream` vs. `EventSource` | Frontend + Backend | Sprint kickoff |
| Rate limit enforcement | In-process counter (Redis) vs. API gateway rule | Backend + Infra | Before backend sprint starts |
| Concept content seeding | JSON seed file in repo vs. admin CMS | PM + Backend | Before launch; does not block engineering sprint |
| Prompt injection mitigation strategy | System prompt hardening vs. input sanitization layer | Backend + Security | Before QA phase |
