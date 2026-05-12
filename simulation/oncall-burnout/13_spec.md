# Sentinel — API Contracts & Acceptance Specifications
**Version**: 1.0
**Date**: 2026-05-12
**Author**: PM + Tech Lead
**Status**: Ready for QA Review

---

## 1. OpenAPI 3.0.3 Specification

```yaml
openapi: 3.0.3
info:
  title: Sentinel API
  description: On-call intelligence platform — incident routing, runbook management, team health analytics
  version: 1.0.0
  contact:
    name: Sentinel Engineering
    email: engineering@sentinel.internal

servers:
  - url: https://api.sentinel.internal/v1
    description: Production
  - url: https://api.staging.sentinel.internal/v1
    description: Staging

security:
  - BearerAuth: []

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT issued by Sentinel after OAuth via PagerDuty or OpsGenie

  schemas:
    # ─────────────────────────────────────────────────────────────────
    # Incident
    # ─────────────────────────────────────────────────────────────────
    Incident:
      type: object
      required:
        - id
        - provider
        - provider_incident_id
        - service_name
        - alert_type
        - severity
        - status
        - triggered_at
        - team_id
      properties:
        id:
          type: string
          format: uuid
          description: Sentinel's internal incident UUID
          example: "550e8400-e29b-41d4-a716-446655440000"
        provider:
          type: string
          enum: [pagerduty, opsgenie]
          example: "pagerduty"
        provider_incident_id:
          type: string
          description: Native incident ID from PagerDuty or OpsGenie
          example: "P3J1K2L"
        service_name:
          type: string
          description: Normalized service name
          example: "payments-svc"
        alert_type:
          type: string
          description: Normalized alert type key
          example: "high_error_rate"
        severity:
          type: string
          enum: [critical, high, medium, low]
          example: "high"
        status:
          type: string
          enum: [triggered, acknowledged, resolved, escalated]
          example: "triggered"
        triggered_at:
          type: string
          format: date-time
          example: "2026-05-12T02:14:00Z"
        resolved_at:
          type: string
          format: date-time
          nullable: true
          example: "2026-05-12T02:37:00Z"
        duration_seconds:
          type: integer
          nullable: true
          description: Seconds from triggered_at to resolved_at. Null if unresolved.
          example: 1380
        team_id:
          type: string
          format: uuid
          example: "7f3e2100-dead-beef-cafe-000000000001"
        routing_suggestion:
          $ref: '#/components/schemas/RoutingSuggestion'
          nullable: true
        runbook_id:
          type: string
          format: uuid
          nullable: true
          description: ID of the runbook captured at incident close
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    # ─────────────────────────────────────────────────────────────────
    # RoutingSuggestion
    # ─────────────────────────────────────────────────────────────────
    RoutingSuggestion:
      type: object
      required:
        - incident_id
        - computed_at
        - routing_source
        - suggestions
      properties:
        incident_id:
          type: string
          format: uuid
        computed_at:
          type: string
          format: date-time
        routing_source:
          type: string
          enum: [heuristic_v1]
          description: Algorithm version that produced this suggestion
        suggestions:
          type: array
          minItems: 0
          maxItems: 10
          items:
            $ref: '#/components/schemas/EngineeerSuggestion'

    EngineerSuggestion:
      type: object
      required:
        - engineer_id
        - engineer_name
        - score
        - confidence_pct
        - on_call_status
        - resolution_count
      properties:
        engineer_id:
          type: string
          format: uuid
        engineer_name:
          type: string
          example: "Priya Kapoor"
        score:
          type: number
          format: float
          minimum: 0.0
          maximum: 1.0
          description: Weighted composite heuristic score
          example: 0.87
        confidence_pct:
          type: integer
          minimum: 0
          maximum: 100
          description: Top suggestion normalized to 100%. Relative confidence among candidates.
          example: 91
        on_call_status:
          type: string
          enum: [primary, secondary, not_on_call]
          example: "primary"
        resolution_count:
          type: integer
          description: Number of times this engineer has resolved this alert_type on this service
          example: 7
        last_resolved_at:
          type: string
          format: date-time
          nullable: true
          example: "2026-05-09T14:22:00Z"
        score_breakdown:
          type: object
          properties:
            alert_type_match:
              type: number
              format: float
              example: 0.70
            recency:
              type: number
              format: float
              example: 0.93
            on_call_status:
              type: number
              format: float
              example: 1.0

    # ─────────────────────────────────────────────────────────────────
    # Runbook
    # ─────────────────────────────────────────────────────────────────
    Runbook:
      type: object
      required:
        - id
        - title
        - service_name
        - alert_type
        - content
        - structured_data
        - created_by
      properties:
        id:
          type: string
          format: uuid
        title:
          type: string
          maxLength: 255
          example: "payments-svc — High Error Rate (DB Pool Exhaustion)"
        service_name:
          type: string
          example: "payments-svc"
        alert_type:
          type: string
          example: "high_error_rate"
        content:
          type: string
          description: Full runbook body in Markdown
          example: "## Root Cause\nDB connection pool exhausted...\n\n## Steps\n1. ..."
        structured_data:
          $ref: '#/components/schemas/RunbookStructuredData'
        incident_id:
          type: string
          format: uuid
          nullable: true
          description: The incident this runbook was captured from (if any)
        created_by:
          type: string
          format: uuid
          description: engineer_id of author
        updated_by:
          type: string
          format: uuid
          nullable: true
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
        usage_count:
          type: integer
          description: Number of incidents where this runbook was opened
          example: 7
        avg_mttr_with_runbook_seconds:
          type: integer
          nullable: true
          description: Average MTTR (seconds) for incidents where this runbook was used
          example: 1140
        avg_mttr_without_runbook_seconds:
          type: integer
          nullable: true
          description: Average MTTR (seconds) for similar incidents without a runbook
          example: 2460
        resolution_success_rate:
          type: number
          format: float
          nullable: true
          description: Fraction of uses that resulted in resolution without escalation (0.0–1.0)
          example: 0.86

    RunbookStructuredData:
      type: object
      properties:
        root_cause:
          type: string
          description: Brief description of what caused this incident type
          example: "DB connection pool exhausted after max_connections config drift"
        steps:
          type: array
          items:
            type: string
          description: Ordered list of resolution steps
          example:
            - "kubectl get pods -n payments"
            - "Check pg_stat_activity for connection count"
            - "Update POOL_MAX_SIZE env var"
            - "kubectl rollout restart deployment/payments-svc"
        services_affected:
          type: array
          items:
            type: string
          example: ["payments-svc", "checkout-api"]
        prevention:
          type: string
          nullable: true
          description: How to prevent recurrence
          example: "Add pool config to deploy checklist. Alert on pool utilization > 80%."

    # ─────────────────────────────────────────────────────────────────
    # HDIReport
    # ─────────────────────────────────────────────────────────────────
    HDIReport:
      type: object
      required:
        - team_id
        - period_start
        - period_end
        - hdi_pct
        - total_incidents
        - engineer_breakdown
        - trend
      properties:
        team_id:
          type: string
          format: uuid
        period_start:
          type: string
          format: date
          example: "2026-04-12"
        period_end:
          type: string
          format: date
          example: "2026-05-12"
        hdi_pct:
          type: number
          format: float
          description: Hero Dependency Index percentage. % of incidents resolved by top ceil(team_size*0.2) engineers.
          example: 64.0
        hdi_severity:
          type: string
          enum: [low, moderate, high, critical]
          description: "low: <30%, moderate: 30-50%, high: 50-70%, critical: >70%"
          example: "high"
        total_incidents:
          type: integer
          example: 112
        team_size:
          type: integer
          example: 6
        engineer_breakdown:
          type: array
          items:
            $ref: '#/components/schemas/EngineerIncidentCount'
        trend:
          type: array
          description: Weekly HDI data points over the period for trend chart
          items:
            $ref: '#/components/schemas/HDITrendPoint'
        previous_period_hdi_pct:
          type: number
          format: float
          nullable: true
          description: HDI for the equivalent prior period (same duration)
          example: 71.0
        runbook_coverage:
          type: object
          properties:
            engineers_with_runbooks:
              type: integer
              example: 3
            total_runbooks_in_period:
              type: integer
              example: 8

    EngineerIncidentCount:
      type: object
      properties:
        engineer_id:
          type: string
          format: uuid
        engineer_name:
          type: string
          example: "Priya Kapoor"
        resolution_count:
          type: integer
          example: 42
        pct_of_total:
          type: number
          format: float
          example: 37.5
        is_hero:
          type: boolean
          description: True if this engineer is in the top ceil(team_size*0.2) by resolution count

    HDITrendPoint:
      type: object
      properties:
        week_start:
          type: string
          format: date
          example: "2026-05-05"
        hdi_pct:
          type: number
          format: float
          example: 62.0
        incident_count:
          type: integer
          example: 28

    # ─────────────────────────────────────────────────────────────────
    # Error
    # ─────────────────────────────────────────────────────────────────
    Error:
      type: object
      required:
        - error
        - message
      properties:
        error:
          type: string
          description: Machine-readable error code
          example: "WEBHOOK_SIGNATURE_INVALID"
        message:
          type: string
          description: Human-readable error description
          example: "Webhook signature validation failed. Ensure the signing secret matches."
        details:
          type: object
          additionalProperties: true
          nullable: true

paths:
  # ─────────────────────────────────────────────────────────────────
  # Webhooks
  # ─────────────────────────────────────────────────────────────────
  /webhooks/pagerduty:
    post:
      summary: Receive PagerDuty incident webhook events
      description: |
        Accepts PagerDuty v3 webhook payloads for incident.triggered, incident.acknowledged,
        incident.resolved, and incident.escalated events.

        Signature validation is mandatory. Invalid signatures return 401 immediately.
        Processing is asynchronous — the endpoint returns 200 within 100ms.
        Duplicate delivery (same X-PagerDuty-Event-Message-Id) is silently acknowledged.
      operationId: receivePagerDutyWebhook
      security: []
      tags: [Webhooks]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              description: PagerDuty v3 webhook payload (passed through as-is to queue)
            example:
              event:
                id: "01ABCDEF0123456789ABCDEF01"
                event_type: "incident.triggered"
                occurred_at: "2026-05-12T02:14:00.000Z"
                agent:
                  html_url: "https://acme.pagerduty.com/incidents/P3J1K2L"
                  id: "P3J1K2L"
                  self: "https://api.pagerduty.com/incidents/P3J1K2L"
                  summary: "[HIGH] payments-service — High Error Rate"
                  type: "incident_reference"
                data:
                  incident:
                    id: "P3J1K2L"
                    status: "triggered"
                    service:
                      id: "PAY_SVC_1"
                      name: "payments-service"
                    urgency: "high"
                    created_at: "2026-05-12T02:14:00Z"
      parameters:
        - in: header
          name: X-PagerDuty-Signature
          required: true
          schema:
            type: string
          description: HMAC-SHA256 signature of the request body using the webhook signing secret
        - in: header
          name: X-PagerDuty-Event-Message-Id
          required: false
          schema:
            type: string
          description: Unique event ID for deduplication
      responses:
        '200':
          description: Event received and queued for processing
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "queued"
        '401':
          description: Webhook signature validation failed
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: "WEBHOOK_SIGNATURE_INVALID"
                message: "Webhook signature validation failed. Ensure the signing secret matches."
        '400':
          description: Malformed payload
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /webhooks/opsgenie:
    post:
      summary: Receive OpsGenie alert webhook events
      operationId: receiveOpsGenieWebhook
      security: []
      tags: [Webhooks]
      description: |
        Accepts OpsGenie action webhooks for create, acknowledge, and close events.
        Signature: HMAC-SHA256 of `timestamp + body` using the OpsGenie integration API key.
      parameters:
        - in: header
          name: X-OG-Signature
          required: true
          schema:
            type: string
        - in: header
          name: X-OG-Delivery-Time
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
      responses:
        '200':
          description: Event queued
        '401':
          description: Signature invalid

  # ─────────────────────────────────────────────────────────────────
  # Incidents
  # ─────────────────────────────────────────────────────────────────
  /incidents/{id}/routing-suggestion:
    get:
      summary: Get routing suggestion for an incident
      description: |
        Returns the pre-computed routing suggestion for the incident. The suggestion is
        computed asynchronously when the incident is first ingested from the webhook.
        If the incident is very new (< 2 seconds), suggestion may not be ready yet —
        poll with exponential backoff or use the WebSocket event channel.
      operationId: getRoutingSuggestion
      tags: [Incidents]
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: string
            format: uuid
          description: Sentinel incident UUID
      responses:
        '200':
          description: Routing suggestion retrieved
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RoutingSuggestion'
              example:
                incident_id: "550e8400-e29b-41d4-a716-446655440000"
                computed_at: "2026-05-12T02:14:02Z"
                routing_source: "heuristic_v1"
                suggestions:
                  - engineer_id: "aaa-111-bbb-222"
                    engineer_name: "Priya Kapoor"
                    score: 0.87
                    confidence_pct: 91
                    on_call_status: "primary"
                    resolution_count: 7
                    last_resolved_at: "2026-05-09T14:22:00Z"
                    score_breakdown:
                      alert_type_match: 0.70
                      recency: 0.93
                      on_call_status: 1.0
                  - engineer_id: "ccc-333-ddd-444"
                    engineer_name: "Marcus Torres"
                    score: 0.52
                    confidence_pct: 54
                    on_call_status: "secondary"
                    resolution_count: 2
                    last_resolved_at: "2026-04-28T09:11:00Z"
                    score_breakdown:
                      alert_type_match: 0.20
                      recency: 0.64
                      on_call_status: 0.6
        '202':
          description: Incident received but routing suggestion not yet computed. Retry after 1–2 seconds.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "pending"
                  message:
                    type: string
                    example: "Routing suggestion is being computed. Retry in 1-2 seconds."
        '404':
          description: Incident not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: "INCIDENT_NOT_FOUND"
                message: "No incident found with id 550e8400-e29b-41d4-a716-446655440000"
        '403':
          description: Incident belongs to a different team than the authenticated engineer

  # ─────────────────────────────────────────────────────────────────
  # Runbooks
  # ─────────────────────────────────────────────────────────────────
  /incidents/{id}/runbook:
    post:
      summary: Create and attach a runbook to an incident
      description: |
        Creates a new runbook (or updates an existing one if update_runbook_id is provided)
        and links it to the specified incident. Also marks the incident as resolved in
        Sentinel and fires the resolved event back to PagerDuty/OpsGenie.
      operationId: createRunbookForIncident
      tags: [Runbooks]
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - title
                - structured_data
              properties:
                title:
                  type: string
                  maxLength: 255
                  example: "payments-svc — High Error Rate (DB Pool Exhaustion)"
                structured_data:
                  $ref: '#/components/schemas/RunbookStructuredData'
                update_runbook_id:
                  type: string
                  format: uuid
                  nullable: true
                  description: If provided, update this existing runbook instead of creating new
                resolver_engineer_id:
                  type: string
                  format: uuid
                  description: Engineer who resolved the incident (defaults to authenticated user)
      responses:
        '201':
          description: Runbook created and attached to incident
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Runbook'
        '200':
          description: Existing runbook updated and re-attached to incident
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Runbook'
        '422':
          description: Validation error — missing required structured_data fields
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: "VALIDATION_ERROR"
                message: "structured_data.root_cause is required"
                details:
                  field: "structured_data.root_cause"
        '404':
          description: Incident not found
        '409':
          description: Incident already has a runbook attached. Use update_runbook_id to update.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: "RUNBOOK_ALREADY_ATTACHED"
                message: "This incident already has a runbook. Pass update_runbook_id to update it."
                details:
                  existing_runbook_id: "runbook-uuid-here"

  /runbooks:
    get:
      summary: Search and list runbooks
      operationId: listRunbooks
      tags: [Runbooks]
      parameters:
        - in: query
          name: q
          schema:
            type: string
          description: Full-text search query across title, content, and service name
          example: "connection pool exhausted"
        - in: query
          name: service_name
          schema:
            type: string
          description: Filter by exact service name
          example: "payments-svc"
        - in: query
          name: alert_type
          schema:
            type: string
          description: Filter by exact alert type
          example: "high_error_rate"
        - in: query
          name: author
          schema:
            type: string
            format: uuid
          description: Filter by engineer_id of author
        - in: query
          name: page
          schema:
            type: integer
            default: 1
            minimum: 1
        - in: query
          name: per_page
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
        - in: query
          name: sort
          schema:
            type: string
            enum: [updated_at_desc, usage_count_desc, mttr_impact_desc]
            default: updated_at_desc
      responses:
        '200':
          description: Paginated runbook list
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Runbook'
                  pagination:
                    type: object
                    properties:
                      page:
                        type: integer
                        example: 1
                      per_page:
                        type: integer
                        example: 20
                      total:
                        type: integer
                        example: 47
                      total_pages:
                        type: integer
                        example: 3
                  coverage_gaps:
                    type: object
                    description: Alert types with incident history but no runbook
                    properties:
                      count:
                        type: integer
                        example: 12
                      alert_types:
                        type: array
                        items:
                          type: string
                        example: ["cpu_throttling", "disk_io_saturation", "tls_cert_expiry"]

  # ─────────────────────────────────────────────────────────────────
  # Dashboard
  # ─────────────────────────────────────────────────────────────────
  /dashboard/hdi:
    get:
      summary: Get Hero Dependency Index report for a team
      operationId: getHDIReport
      tags: [Dashboard]
      parameters:
        - in: query
          name: team_id
          required: true
          schema:
            type: string
            format: uuid
        - in: query
          name: start_date
          required: true
          schema:
            type: string
            format: date
          example: "2026-04-12"
        - in: query
          name: end_date
          required: true
          schema:
            type: string
            format: date
          example: "2026-05-12"
      responses:
        '200':
          description: HDI report for the specified team and period
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HDIReport'
        '400':
          description: Invalid date range (end before start, or range > 180 days)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: "INVALID_DATE_RANGE"
                message: "end_date must be after start_date and range cannot exceed 180 days"
        '403':
          description: Authenticated user is not a manager of team_id
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: "INSUFFICIENT_PERMISSIONS"
                message: "HDI dashboard is accessible to team managers only"
        '422':
          description: Insufficient data to compute HDI
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              example:
                error: "INSUFFICIENT_DATA"
                message: "Fewer than 10 resolved incidents in this period. HDI cannot be reliably computed."
                details:
                  incident_count: 4
                  minimum_required: 10
```

---

## 2. Acceptance Specifications

All scenarios use Given/When/Then format. Test IDs are referenced in Jira tickets.

---

### 2.1 Engineer Receives Incident → System Suggests Resolver

**SENT-AC-001: Routing suggestion computed on incident trigger**

```
Given: Incident INC-5000 for service "payments-svc" with alert_type "high_error_rate"
       is triggered in PagerDuty
And:   Engineer Priya Kapoor has 7 prior resolutions of high_error_rate on payments-svc,
       most recent 3 days ago
And:   Priya is currently the primary on-call engineer for payments-svc

When:  PagerDuty delivers the webhook to POST /webhooks/pagerduty
       with a valid X-PagerDuty-Signature

Then:  The endpoint returns HTTP 200 with body {"status": "queued"} within 100ms
And:   Within 2 seconds, a routing suggestion is computed and persisted on the incident row
And:   GET /incidents/{sentinel_id}/routing-suggestion returns HTTP 200
And:   The top suggestion is Priya Kapoor with:
         - on_call_status = "primary"
         - resolution_count = 7
         - score >= 0.80
         - confidence_pct = 100 (top-ranked suggestion always normalizes to 100)
```

**SENT-AC-002: Routing suggestion with no prior resolution history**

```
Given: Incident INC-5001 for service "inventory-svc" with alert_type "disk_io_saturation"
And:   No engineer has ever resolved this alert_type on this service in Sentinel's history
And:   Engineer Sam Rivera is the primary on-call engineer for inventory-svc

When:  The webhook for INC-5001 is received and processed

Then:  GET /incidents/{id}/routing-suggestion returns HTTP 200
And:   The suggestions array contains all on-call engineers sorted by on_call_status
And:   The top suggestion is Sam Rivera with on_call_status = "primary"
And:   All score_breakdown.alert_type_match values = 0.0
And:   All score_breakdown.recency values = 0.0
And:   Confidence scores reflect only the on_call_status component
```

**SENT-AC-003: Routing suggestion when top resolver is not on-call**

```
Given: Incident INC-5002 for "payments-svc" / "high_error_rate"
And:   Priya Kapoor has the strongest historical match (score without on_call = 0.82)
And:   Priya is NOT currently on-call (on_call_status = "not_on_call")
And:   Marcus Torres is primary on-call with 2 prior resolutions (score without on_call = 0.35)

When:  Routing suggestion is computed

Then:  The suggestions array includes both engineers
And:   Marcus Torres ranks first because his on_call_status weight pushes total score above Priya's
And:   The response includes score_breakdown for both engineers showing the on_call_status penalty
And:   Both engineers appear in the UI with their on_call_status clearly labeled
```

---

### 2.2 Engineer Closes Incident → Capture Modal Appears

**SENT-AC-010: Close incident triggers runbook capture prompt**

```
Given: Engineer Alex is viewing incident INC-5000 in the Sentinel UI
And:   INC-5000 is in "acknowledged" status

When:  Alex clicks "Close Incident"

Then:  The Runbook Capture Modal appears within 200ms
And:   The modal pre-populates:
         - title field with "[service_name] — [alert_type]" as a suggested title (editable)
         - services_affected with services from the incident payload
And:   The modal does NOT close the incident until "Save & Close" or "Skip" is clicked
And:   A runbook_capture_modal_opened event is logged with incident_id and engineer_id
```

**SENT-AC-011: Similar runbook pre-selects "Update existing"**

```
Given: Engineer opens the Runbook Capture Modal for INC-5000
And:   A runbook titled "payments-svc — High Error Rate (DB Pool)" exists
And:   pg_trgm similarity score between INC-5000 alert_type/service and the runbook >= 0.85

When:  The Runbook Capture Modal renders

Then:  The "Update existing" radio option is pre-selected (not "New runbook")
And:   The matched runbook title is shown: "Updating: payments-svc — High Error Rate (DB Pool)"
And:   The existing runbook's structured_data is pre-populated in the form fields
And:   Engineer can switch to "New runbook" to override this default
```

**SENT-AC-012: Skip runbook capture**

```
Given: Engineer clicks "Skip for now" on the Runbook Capture Modal

When:  The skip action is submitted

Then:  The incident is marked resolved in Sentinel (status = "resolved", resolved_at = now())
And:   A runbook_skipped event is logged with {incident_id, engineer_id, skip_count}
And:   If this is the engineer's 3rd skip (cumulative, not consecutive), a notification is
       queued: "3 incidents without runbooks — your team is missing context"
And:   The modal closes and the incident card updates to show "Resolved (no runbook)"
```

---

### 2.3 Engineer Completes Runbook Capture → Runbook Attached

**SENT-AC-020: Successful runbook save**

```
Given: Engineer Alex fills in the Runbook Capture Modal for INC-5000 with:
         root_cause: "DB connection pool exhausted after config drift"
         steps: ["kubectl get pods -n payments", "Check pg_stat_activity", "Restart deployment"]
         services_affected: ["payments-svc", "checkout-api"]
         prevention: "Add pool config to deploy checklist"

When:  Alex clicks "Save & Close Incident"

Then:  POST /incidents/{id}/runbook returns HTTP 201
And:   The new Runbook object is returned with a valid UUID
And:   The incident's runbook_id is set to the new runbook's ID
And:   The incident status is updated to "resolved" with resolved_at = now()
And:   A toast notification appears: "Runbook saved. INC-5000 closed."
And:   An embedding generation job is enqueued (does not block the response)
And:   The Runbook Library shows the new runbook within 5 seconds (after embedding completes)
```

**SENT-AC-021: Runbook save validation — missing required field**

```
Given: Engineer submits the Runbook Capture Modal with root_cause left empty

When:  The save is attempted

Then:  POST /incidents/{id}/runbook returns HTTP 422
And:   The error body contains:
         error: "VALIDATION_ERROR"
         message: "structured_data.root_cause is required"
         details.field: "structured_data.root_cause"
And:   An inline error appears below the "What caused this?" field in the UI
And:   The "Save & Close Incident" button re-enables
And:   The incident is NOT closed and NOT marked resolved
```

**SENT-AC-022: Duplicate runbook submission (idempotency)**

```
Given: Engineer successfully saved a runbook for INC-5000 (returns 201)
And:   Due to a network retry, the same POST /incidents/{id}/runbook is sent again
       with identical payload

When:  The duplicate request is received

Then:  The endpoint returns HTTP 409 with:
         error: "RUNBOOK_ALREADY_ATTACHED"
         details.existing_runbook_id: <the original runbook ID>
And:   No duplicate runbook is created in the database
And:   The incident's runbook_id remains pointing to the original runbook
```

---

### 2.4 Engineer Searches Runbook Library → Similar Runbooks Surface

**SENT-AC-030: Full-text search returns relevant results**

```
Given: The runbook library contains 15 runbooks
And:   3 runbooks contain the phrase "connection pool" in their content

When:  Engineer searches GET /runbooks?q=connection+pool+exhausted

Then:  HTTP 200 is returned
And:   The 3 matching runbooks appear in the response data array
And:   Results are ordered by relevance (pg_trgm similarity score descending)
And:   The response includes pagination with total = 3
And:   Non-matching runbooks do not appear in results
```

**SENT-AC-031: Search by service filter**

```
Given: 47 runbooks exist, 8 of which have service_name = "payments-svc"

When:  Engineer requests GET /runbooks?service_name=payments-svc

Then:  HTTP 200 is returned
And:   Response data contains exactly 8 runbooks
And:   All returned runbooks have service_name = "payments-svc"
And:   pagination.total = 8
```

**SENT-AC-032: Search with no results**

```
Given: No runbook exists for service "legacy-billing-svc"

When:  Engineer requests GET /runbooks?service_name=legacy-billing-svc

Then:  HTTP 200 is returned (not 404)
And:   Response data is an empty array []
And:   pagination.total = 0
And:   coverage_gaps.count reflects this service has incidents but no runbook
```

**SENT-AC-033: Coverage gaps surfaced in response**

```
Given: 5 incidents have been resolved for alert_type "tls_cert_expiry" across multiple services
And:   No runbook exists with alert_type = "tls_cert_expiry"

When:  Engineer requests GET /runbooks (no filters)

Then:  Response coverage_gaps.count >= 1
And:   coverage_gaps.alert_types includes "tls_cert_expiry"
```

---

### 2.5 Manager Views HDI Dashboard → Correct Data Shown

**SENT-AC-040: HDI computed correctly for a 6-person team**

```
Given: Team "Payments" has 6 engineers
And:   Over the last 30 days:
         Priya K: 42 resolutions
         Marcus T: 30 resolutions
         Dana L: 16 resolutions
         Sam R: 12 resolutions
         Yuki M: 8 resolutions
         Amir C: 4 resolutions
         Total: 112 resolutions
And:   Top 20% of 6 engineers = ceil(6 * 0.2) = ceil(1.2) = 2 engineers (Priya + Marcus)
And:   (42 + 30) / 112 = 64.3%

When:  Manager requests GET /dashboard/hdi?team_id={id}&start_date=2026-04-12&end_date=2026-05-12

Then:  HTTP 200 is returned
And:   hdi_pct = 64.3 (rounded to 1 decimal place)
And:   hdi_severity = "high"
And:   total_incidents = 112
And:   engineer_breakdown contains 6 entries
And:   Priya K has is_hero = true, pct_of_total = 37.5
And:   Marcus T has is_hero = true, pct_of_total = 26.8
And:   All other engineers have is_hero = false
And:   trend array contains one data point per week in the 30-day range (4-5 points)
```

**SENT-AC-041: HDI insufficient data returns 422**

```
Given: Team "Infra" has only resolved 4 incidents in the last 30 days

When:  Manager requests GET /dashboard/hdi for this team and period

Then:  HTTP 422 is returned
And:   error = "INSUFFICIENT_DATA"
And:   details.incident_count = 4
And:   details.minimum_required = 10
```

**SENT-AC-042: Non-manager engineer cannot access HDI**

```
Given: Alex (engineer role, not manager) is authenticated

When:  Alex requests GET /dashboard/hdi?team_id={id}...

Then:  HTTP 403 is returned
And:   error = "INSUFFICIENT_PERMISSIONS"
```

---

### 2.6 Error Scenarios

**SENT-AC-050: Webhook with invalid signature is rejected**

```
Given: PagerDuty sends a webhook to POST /webhooks/pagerduty
And:   The X-PagerDuty-Signature header is missing or contains an incorrect HMAC

When:  The request is received

Then:  HTTP 401 is returned within 50ms
And:   error = "WEBHOOK_SIGNATURE_INVALID"
And:   No event is queued for processing
And:   The incident is NOT created in the database
And:   A security_event log entry is written with {ip_address, timestamp, provider, reason}
```

**SENT-AC-051: Webhook with valid signature but duplicate event ID**

```
Given: PagerDuty successfully delivered webhook event ID "EVT-001" for incident P3J1K2L
And:   PagerDuty retries the same event (same X-PagerDuty-Event-Message-Id = "EVT-001")

When:  The duplicate is received

Then:  HTTP 200 is returned (not an error — PagerDuty expects 200 to stop retrying)
And:   Body: {"status": "queued"} (same response as original — idempotent)
And:   The event is NOT re-queued for processing
And:   No duplicate incident is created
And:   A webhook_events row exists with processed = false (already processed from first delivery)
```

**SENT-AC-052: Routing suggestion for incident with no team routing history**

```
Given: A brand-new team just connected PagerDuty to Sentinel (zero historical incidents)
And:   Their first incident triggers for service "api-gateway" / "high_latency"
And:   Engineer Jordan Lee is the primary on-call engineer

When:  GET /incidents/{id}/routing-suggestion is called

Then:  HTTP 200 is returned (not 404 or 422)
And:   suggestions array has at least 1 entry
And:   Jordan Lee is the top suggestion with on_call_status = "primary"
And:   score_breakdown.alert_type_match = 0.0 for all engineers
And:   score_breakdown.recency = 0.0 for all engineers
And:   The UI renders the suggestion card with a notice: "No resolution history yet — suggested based on on-call schedule only"
```

**SENT-AC-053: Routing suggestion not yet ready (202 response)**

```
Given: A webhook was just received (< 500ms ago) and the routing engine is still running

When:  GET /incidents/{id}/routing-suggestion is called

Then:  HTTP 202 is returned
And:   Body: {"status": "pending", "message": "Routing suggestion is being computed. Retry in 1-2 seconds."}
And:   After 2 seconds, the same endpoint returns HTTP 200 with the computed suggestion
```

---

## 3. Test Data Requirements

For automated acceptance testing, seed data must include:

| Entity | Count | Notes |
|---|---|---|
| Engineers | 8 | Mix of roles: 6 ICs, 2 managers |
| Teams | 2 | "Payments" (6 engineers), "Infra" (2 engineers) |
| Historical incidents | 120 | 90-day history, varied alert types, all resolved |
| incident_resolutions | 120 | Linked to above, skewed: 2 engineers resolve 65% |
| Runbooks | 15 | Cover 10 of the 22 distinct alert types in the incident history |
| rotation_schedules | 2 | One per team, current primary = Priya (Payments), Jordan (Infra) |

Seed script: `scripts/seed-test-data.ts`

---

## 4. Contract Testing

All endpoints are covered by Pact contract tests (consumer-driven contract testing). React SPA is the consumer; the Express API is the provider.

Pact tests live in `test/contract/`. Run with:
```bash
npm run test:contract
```

Contract broker: internal Pact Broker at `https://pact.sentinel.internal`.
