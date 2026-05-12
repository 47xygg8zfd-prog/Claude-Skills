# Sentinel — Backend Implementation Plan
**Version**: 1.0
**Date**: 2026-05-12
**Author**: Backend Lead
**Status**: Sprint 1 Ready

---

## 1. Implementation Order

The implementation sequence is dependency-driven. Do not begin step N until step N-1 is merged and deployed to staging.

1. **DB migrations** — all tables, indexes, extensions
2. **PagerDuty webhook receiver** — signature validation, normalization, idempotency, queue publish
3. **OpsGenie webhook receiver** — same pattern, different signature scheme
4. **Routing engine** — scoring function, on-call API call, routing_events logging
5. **Runbook CRUD** — create, update, list with pg_trgm search, similarity matching
6. **Dashboard aggregation** — HDI query, trend calculation, HDI endpoint
7. **Tests** — unit (routing engine scoring), integration (webhook → routing suggestion → runbook save), contract (Pact provider)

Each step has its own PR. PRs do not merge to main without passing CI.

---

## 2. Database Migrations

### 2.1 Extensions

```sql
-- Migration: 001_extensions.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "vector";  -- pgvector; confirm available on RDS instance
```

### 2.2 Core Tables

```sql
-- Migration: 002_core_tables.sql

-- Engineers
CREATE TABLE engineers (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email           TEXT NOT NULL,
  name            TEXT NOT NULL,
  provider        TEXT NOT NULL CHECK (provider IN ('pagerduty', 'opsgenie')),
  provider_user_id TEXT NOT NULL,
  team_id         UUID,               -- FK added after teams table
  role            TEXT NOT NULL DEFAULT 'engineer' CHECK (role IN ('engineer', 'manager', 'admin')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (provider, provider_user_id)
);

-- Teams
CREATE TABLE teams (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name            TEXT NOT NULL,
  provider        TEXT NOT NULL CHECK (provider IN ('pagerduty', 'opsgenie')),
  provider_team_id TEXT NOT NULL,
  org_id          UUID NOT NULL,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (provider, provider_team_id)
);

ALTER TABLE engineers ADD CONSTRAINT fk_engineers_team
  FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE SET NULL;

-- Incidents
CREATE TABLE incidents (
  id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  provider              TEXT NOT NULL CHECK (provider IN ('pagerduty', 'opsgenie')),
  provider_incident_id  TEXT NOT NULL,
  service_name          TEXT NOT NULL,
  alert_type            TEXT NOT NULL,   -- normalized
  alert_type_raw        TEXT NOT NULL,   -- original from provider, for audit
  severity              TEXT NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low')),
  status                TEXT NOT NULL DEFAULT 'triggered'
                          CHECK (status IN ('triggered', 'acknowledged', 'resolved', 'escalated')),
  triggered_at          TIMESTAMPTZ NOT NULL,
  acknowledged_at       TIMESTAMPTZ,
  resolved_at           TIMESTAMPTZ,
  team_id               UUID NOT NULL REFERENCES teams(id),
  routing_suggestion    JSONB,           -- cached RoutingSuggestion object
  runbook_id            UUID,            -- FK added after runbooks table
  raw_payload           JSONB NOT NULL,  -- original webhook payload, for debugging
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (provider, provider_incident_id)
);

CREATE INDEX idx_incidents_service_alert ON incidents (service_name, alert_type);
CREATE INDEX idx_incidents_team_resolved ON incidents (team_id, resolved_at)
  WHERE resolved_at IS NOT NULL;
CREATE INDEX idx_incidents_triggered_at ON incidents (triggered_at DESC);
CREATE INDEX idx_incidents_status ON incidents (status) WHERE status != 'resolved';

-- Runbooks
CREATE TABLE runbooks (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title           TEXT NOT NULL,
  service_name    TEXT NOT NULL,
  alert_type      TEXT NOT NULL,
  content         TEXT NOT NULL,         -- full markdown
  structured_data JSONB NOT NULL,        -- {root_cause, steps[], services_affected[], prevention}
  embedding       vector(1536),          -- nullable at launch; populated async after pg_trgm validation
  incident_id     UUID REFERENCES incidents(id) ON DELETE SET NULL,
  team_id         UUID NOT NULL REFERENCES teams(id),
  created_by      UUID NOT NULL REFERENCES engineers(id),
  updated_by      UUID REFERENCES engineers(id),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Full-text search index (pg_trgm) on title + content
CREATE INDEX idx_runbooks_trgm_title ON runbooks USING GIN (title gin_trgm_ops);
CREATE INDEX idx_runbooks_trgm_content ON runbooks USING GIN (content gin_trgm_ops);
-- Standard B-tree for filter queries
CREATE INDEX idx_runbooks_service_alert ON runbooks (service_name, alert_type);
CREATE INDEX idx_runbooks_team ON runbooks (team_id);
-- pgvector HNSW index (added in migration 006 when embeddings are enabled)
-- CREATE INDEX idx_runbooks_embedding ON runbooks USING hnsw (embedding vector_cosine_ops);

ALTER TABLE incidents ADD CONSTRAINT fk_incidents_runbook
  FOREIGN KEY (runbook_id) REFERENCES runbooks(id) ON DELETE SET NULL;

-- Incident Resolutions (join table)
CREATE TABLE incident_resolutions (
  id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  incident_id                 UUID NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
  engineer_id                 UUID NOT NULL REFERENCES engineers(id),
  resolver_source             TEXT NOT NULL
                                CHECK (resolver_source IN ('manual', 'suggested', 'escalation')),
  routing_suggestion_accepted BOOLEAN,   -- null if resolver_source = 'manual'
  duration_seconds            INT NOT NULL CHECK (duration_seconds >= 0),
  runbook_id                  UUID REFERENCES runbooks(id) ON DELETE SET NULL,
  created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (incident_id)  -- one resolution per incident
);

CREATE INDEX idx_resolutions_engineer ON incident_resolutions (engineer_id);
CREATE INDEX idx_resolutions_incident ON incident_resolutions (incident_id);

-- Routing Events (suggestion + outcome log)
CREATE TABLE routing_events (
  id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  incident_id           UUID NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
  suggested_engineer_id UUID NOT NULL REFERENCES engineers(id),
  suggestion_rank       INT NOT NULL,
  was_accepted          BOOLEAN,        -- null until incident resolved
  override_engineer_id  UUID REFERENCES engineers(id),
  final_mttr_seconds    INT,            -- null until incident resolved
  weights_snapshot      JSONB NOT NULL, -- {alert_type_match: 0.4, recency: 0.3, on_call_status: 0.3}
  score_breakdown       JSONB NOT NULL, -- {alert_type_match: 0.70, recency: 0.93, on_call_status: 1.0}
  routing_source        TEXT NOT NULL DEFAULT 'heuristic_v1',
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_routing_events_incident ON routing_events (incident_id);
CREATE INDEX idx_routing_events_engineer ON routing_events (suggested_engineer_id);
CREATE INDEX idx_routing_events_accepted ON routing_events (was_accepted) WHERE was_accepted IS NOT NULL;

-- Rotation Schedules (audit/history; not used in hot path)
CREATE TABLE rotation_schedules (
  id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  provider              TEXT NOT NULL,
  provider_schedule_id  TEXT NOT NULL,
  schedule_name         TEXT NOT NULL,
  team_id               UUID NOT NULL REFERENCES teams(id),
  schedule_data         JSONB NOT NULL,  -- raw schedule response from provider
  synced_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (provider, provider_schedule_id)
);

-- GitHub Commits
CREATE TABLE github_commits (
  id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  repo_slug     TEXT NOT NULL,
  sha           TEXT NOT NULL,
  message       TEXT NOT NULL,
  author_name   TEXT NOT NULL,
  committed_at  TIMESTAMPTZ NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (repo_slug, sha)
);

CREATE INDEX idx_github_commits_repo_time ON github_commits (repo_slug, committed_at DESC);

-- Services (catalog for autocomplete + GitHub mapping)
CREATE TABLE services (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name            TEXT NOT NULL UNIQUE,
  team_id         UUID REFERENCES teams(id),
  github_repo     TEXT,  -- e.g. "acme-corp/payments-service"
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Webhook Events (idempotency log)
CREATE TABLE webhook_events (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  provider          TEXT NOT NULL,
  provider_event_id TEXT NOT NULL,
  incident_id       TEXT,             -- provider's native incident ID (before Sentinel creates its own)
  event_type        TEXT NOT NULL,
  received_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  processed         BOOLEAN NOT NULL DEFAULT FALSE,
  UNIQUE (provider, provider_event_id)
);

CREATE INDEX idx_webhook_events_received ON webhook_events (received_at DESC);
```

---

## 3. API Endpoint Implementations

### 3.1 `POST /webhooks/pagerduty`

**File**: `src/routes/webhooks/pagerduty.ts`

```typescript
import { Router, Request, Response } from 'express';
import crypto from 'crypto';
import { webhookQueue } from '../../queues/webhookQueue';
import { db } from '../../db';

const router = Router();

function validatePagerDutySignature(
  rawBody: Buffer,
  signatureHeader: string,
  signingSecret: string
): boolean {
  // PagerDuty sends multiple signatures: "v1=<hash>,v1=<hash2>"
  const signatures = signatureHeader.split(',');
  const expectedHash = crypto
    .createHmac('sha256', signingSecret)
    .update(rawBody)
    .digest('hex');
  return signatures.some(sig => {
    const [, hash] = sig.trim().split('=');
    return crypto.timingSafeEqual(Buffer.from(hash, 'hex'), Buffer.from(expectedHash, 'hex'));
  });
}

router.post('/', async (req: Request, res: Response) => {
  const signature = req.headers['x-pagerduty-signature'] as string;
  const eventMessageId = req.headers['x-pagerduty-event-message-id'] as string;
  const rawBody: Buffer = (req as any).rawBody;

  // 1. Validate signature
  if (!signature || !validatePagerDutySignature(rawBody, signature, process.env.PD_WEBHOOK_SECRET!)) {
    return res.status(401).json({
      error: 'WEBHOOK_SIGNATURE_INVALID',
      message: 'Webhook signature validation failed.',
    });
  }

  // 2. Idempotency check — insert into webhook_events
  //    ON CONFLICT DO NOTHING lets us detect duplicates
  const result = await db.raw(`
    INSERT INTO webhook_events (provider, provider_event_id, event_type, received_at)
    VALUES ('pagerduty', ?, ?, NOW())
    ON CONFLICT (provider, provider_event_id) DO NOTHING
    RETURNING id
  `, [eventMessageId ?? crypto.randomUUID(), req.body?.event?.event_type ?? 'unknown']);

  // No rows returned = duplicate; acknowledge and stop
  if (result.rows.length === 0) {
    return res.status(200).json({ status: 'queued' });
  }

  // 3. Enqueue for async processing
  await webhookQueue.add('pagerduty-event', {
    provider: 'pagerduty',
    raw: req.body,
    webhookEventId: result.rows[0].id,
  }, {
    attempts: 3,
    backoff: { type: 'exponential', delay: 1000 },
  });

  return res.status(200).json({ status: 'queued' });
});

export { router as pagerdutyWebhookRouter };
```

**Normalization function** (`src/services/incident/normalize.ts`):

```typescript
import { ALERT_TYPE_MAP } from '../../config/alertTypeMap';

interface NormalizedIncidentEvent {
  provider: 'pagerduty' | 'opsgenie';
  event_type: 'triggered' | 'acknowledged' | 'resolved' | 'escalated';
  provider_incident_id: string;
  service_name: string;
  alert_type: string;
  alert_type_raw: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  triggered_at: string;
  raw_payload: Record<string, unknown>;
}

export function normalizePagerDutyEvent(raw: Record<string, unknown>): NormalizedIncidentEvent {
  const event = raw.event as Record<string, unknown>;
  const data = event.data as Record<string, unknown>;
  const incident = data.incident as Record<string, unknown>;

  const alertTypeRaw: string = (incident.alert_key as string)
    ?? (incident.description as string)
    ?? 'unknown';

  return {
    provider: 'pagerduty',
    event_type: mapPdEventType(event.event_type as string),
    provider_incident_id: incident.id as string,
    service_name: normalizeServiceName((incident.service as Record<string, unknown>).name as string),
    alert_type: normalizeAlertType(alertTypeRaw),
    alert_type_raw: alertTypeRaw,
    severity: mapPdUrgency(incident.urgency as string),
    triggered_at: incident.created_at as string,
    raw_payload: raw,
  };
}

function normalizeAlertType(raw: string): string {
  const lower = raw.toLowerCase().replace(/[^a-z0-9_]/g, '_');
  return ALERT_TYPE_MAP[lower] ?? lower;  // fall through to raw normalized if not in map
}

function normalizeServiceName(raw: string): string {
  // "payments-service" → "payments-svc", "Payments Service" → "payments-svc"
  return raw.toLowerCase()
    .replace(/\s+/g, '-')
    .replace(/-service$/, '-svc')
    .replace(/-api$/, '-api');
}

function mapPdEventType(pd: string): NormalizedIncidentEvent['event_type'] {
  const map: Record<string, NormalizedIncidentEvent['event_type']> = {
    'incident.triggered': 'triggered',
    'incident.acknowledged': 'acknowledged',
    'incident.resolved': 'resolved',
    'incident.escalated': 'escalated',
  };
  return map[pd] ?? 'triggered';
}

function mapPdUrgency(urgency: string): NormalizedIncidentEvent['severity'] {
  if (urgency === 'high') return 'high';
  if (urgency === 'low') return 'low';
  return 'medium';
}
```

---

### 3.2 `GET /incidents/:id/routing-suggestion`

**File**: `src/routes/incidents/routingSuggestion.ts`

The routing suggestion is computed asynchronously when the incident is first ingested. This endpoint serves the cached result from the `routing_suggestion` JSONB column on the incidents table. Sub-10ms response time for the cached path.

```typescript
router.get('/:id/routing-suggestion', requireAuth, async (req, res) => {
  const { id } = req.params;

  const incident = await db('incidents')
    .where({ id, team_id: req.user.team_id })
    .first();

  if (!incident) {
    return res.status(404).json({ error: 'INCIDENT_NOT_FOUND', message: `No incident found with id ${id}` });
  }

  if (!incident.routing_suggestion) {
    // Still computing (race condition on very fresh incidents)
    return res.status(202).json({
      status: 'pending',
      message: 'Routing suggestion is being computed. Retry in 1-2 seconds.',
    });
  }

  return res.status(200).json(incident.routing_suggestion);
});
```

---

### 3.3 `POST /incidents/:id/runbook`

**File**: `src/routes/incidents/runbook.ts`

```typescript
router.post('/:id/runbook', requireAuth, async (req, res) => {
  const { id } = req.params;
  const { title, structured_data, update_runbook_id, resolver_engineer_id } = req.body;

  // Validate required fields
  if (!structured_data?.root_cause) {
    return res.status(422).json({
      error: 'VALIDATION_ERROR',
      message: 'structured_data.root_cause is required',
      details: { field: 'structured_data.root_cause' },
    });
  }
  if (!structured_data?.steps || structured_data.steps.length === 0) {
    return res.status(422).json({
      error: 'VALIDATION_ERROR',
      message: 'structured_data.steps must contain at least one step',
      details: { field: 'structured_data.steps' },
    });
  }

  const incident = await db('incidents').where({ id, team_id: req.user.team_id }).first();
  if (!incident) return res.status(404).json({ error: 'INCIDENT_NOT_FOUND' });

  if (incident.runbook_id && !update_runbook_id) {
    return res.status(409).json({
      error: 'RUNBOOK_ALREADY_ATTACHED',
      message: 'This incident already has a runbook. Pass update_runbook_id to update it.',
      details: { existing_runbook_id: incident.runbook_id },
    });
  }

  // Build markdown content from structured data
  const content = buildRunbookMarkdown(title, structured_data);

  await db.transaction(async (trx) => {
    let runbook;
    if (update_runbook_id) {
      [runbook] = await trx('runbooks')
        .where({ id: update_runbook_id, team_id: req.user.team_id })
        .update({
          title,
          content,
          structured_data,
          updated_by: req.user.id,
          updated_at: new Date(),
        })
        .returning('*');
    } else {
      [runbook] = await trx('runbooks').insert({
        title,
        service_name: incident.service_name,
        alert_type: incident.alert_type,
        content,
        structured_data,
        incident_id: id,
        team_id: req.user.team_id,
        created_by: req.user.id,
      }).returning('*');
    }

    // Link runbook to incident and mark resolved
    await trx('incidents').where({ id }).update({
      runbook_id: runbook.id,
      status: 'resolved',
      resolved_at: new Date(),
      updated_at: new Date(),
    });

    // Create resolution record
    const resolverId = resolver_engineer_id ?? req.user.id;
    const suggestion = incident.routing_suggestion?.suggestions?.[0];
    await trx('incident_resolutions').insert({
      incident_id: id,
      engineer_id: resolverId,
      resolver_source: suggestion ? 'suggested' : 'manual',
      routing_suggestion_accepted: suggestion
        ? suggestion.engineer_id === resolverId
        : null,
      duration_seconds: Math.floor(
        (Date.now() - new Date(incident.triggered_at).getTime()) / 1000
      ),
      runbook_id: runbook.id,
    });

    // Update routing_events with outcome
    if (incident.routing_suggestion) {
      await trx('routing_events')
        .where({ incident_id: id })
        .update({
          was_accepted: suggestion?.engineer_id === resolverId,
          override_engineer_id: suggestion?.engineer_id !== resolverId ? resolverId : null,
          final_mttr_seconds: Math.floor(
            (Date.now() - new Date(incident.triggered_at).getTime()) / 1000
          ),
        });
    }

    // Enqueue async embedding generation
    await embeddingQueue.add('generate-embedding', { runbook_id: runbook.id });

    return update_runbook_id
      ? res.status(200).json(runbook)
      : res.status(201).json(runbook);
  });
});
```

---

### 3.4 `GET /runbooks`

**File**: `src/routes/runbooks/list.ts`

```typescript
router.get('/', requireAuth, async (req, res) => {
  const { q, service_name, alert_type, author, page = 1, per_page = 20, sort = 'updated_at_desc' } = req.query;

  let query = db('runbooks')
    .where({ team_id: req.user.team_id });

  // Full-text search via pg_trgm similarity
  if (q) {
    query = query.whereRaw(
      `(title % ? OR content % ? OR similarity(title || ' ' || content, ?) > 0.1)`,
      [q, q, q]
    ).orderByRaw(`similarity(title || ' ' || content, ?) DESC`, [q]);
  }

  if (service_name) query = query.where({ service_name });
  if (alert_type) query = query.where({ alert_type });
  if (author) query = query.where({ created_by: author });

  // Sort (overridden by relevance if q is set)
  if (!q) {
    const sortMap: Record<string, [string, 'asc' | 'desc']> = {
      updated_at_desc: ['updated_at', 'desc'],
      usage_count_desc: ['usage_count', 'desc'],
      mttr_impact_desc: ['avg_mttr_without_runbook_seconds', 'desc'],
    };
    const [col, dir] = sortMap[sort as string] ?? ['updated_at', 'desc'];
    query = query.orderBy(col, dir);
  }

  const countQuery = query.clone().clearOrder().count<{count: string}>('* as count').first();
  const [{ count }, rows] = await Promise.all([
    countQuery,
    query.limit(Number(per_page)).offset((Number(page) - 1) * Number(per_page)),
  ]);

  // Coverage gaps: alert types with incidents but no runbook (team-scoped)
  const gaps = await db.raw(`
    SELECT DISTINCT i.alert_type
    FROM incidents i
    WHERE i.team_id = ?
      AND i.resolved_at IS NOT NULL
      AND NOT EXISTS (
        SELECT 1 FROM runbooks r
        WHERE r.team_id = i.team_id
          AND r.alert_type = i.alert_type
      )
    ORDER BY i.alert_type
    LIMIT 20
  `, [req.user.team_id]);

  return res.json({
    data: rows,
    pagination: {
      page: Number(page),
      per_page: Number(per_page),
      total: Number(count),
      total_pages: Math.ceil(Number(count) / Number(per_page)),
    },
    coverage_gaps: {
      count: gaps.rows.length,
      alert_types: gaps.rows.map((r: { alert_type: string }) => r.alert_type),
    },
  });
});
```

---

### 3.5 `GET /dashboard/hdi`

**File**: `src/routes/dashboard/hdi.ts`

```typescript
router.get('/hdi', requireAuth, requireRole('manager'), async (req, res) => {
  const { team_id, start_date, end_date } = req.query as Record<string, string>;

  // Validate date range
  const start = new Date(start_date);
  const end = new Date(end_date);
  const diffDays = (end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24);

  if (end <= start || diffDays > 180) {
    return res.status(400).json({
      error: 'INVALID_DATE_RANGE',
      message: 'end_date must be after start_date and range cannot exceed 180 days',
    });
  }

  // Verify manager has access to this team
  if (req.user.team_id !== team_id && req.user.role !== 'admin') {
    return res.status(403).json({
      error: 'INSUFFICIENT_PERMISSIONS',
      message: 'HDI dashboard is accessible to team managers only',
    });
  }

  // Main HDI aggregation
  const breakdownResult = await db.raw(`
    WITH resolutions_in_period AS (
      SELECT
        ir.engineer_id,
        e.name AS engineer_name,
        COUNT(*) AS resolution_count
      FROM incident_resolutions ir
      JOIN incidents i ON i.id = ir.incident_id
      JOIN engineers e ON e.id = ir.engineer_id
      WHERE i.team_id = :team_id
        AND i.resolved_at BETWEEN :start AND :end
      GROUP BY ir.engineer_id, e.name
    ),
    team_total AS (
      SELECT SUM(resolution_count)::INT AS total,
             COUNT(*)::INT AS team_size
      FROM resolutions_in_period
    ),
    ranked AS (
      SELECT
        r.engineer_id,
        r.engineer_name,
        r.resolution_count::INT,
        t.total,
        t.team_size,
        ROUND(r.resolution_count::NUMERIC / t.total * 100, 1) AS pct_of_total,
        RANK() OVER (ORDER BY r.resolution_count DESC) AS rnk
      FROM resolutions_in_period r, team_total t
    )
    SELECT
      engineer_id,
      engineer_name,
      resolution_count,
      pct_of_total,
      total,
      team_size,
      rnk <= CEIL(team_size * 0.2) AS is_hero
    FROM ranked
    ORDER BY resolution_count DESC
  `, { team_id, start: start.toISOString(), end: end.toISOString() });

  const rows = breakdownResult.rows;

  if (rows.length === 0 || rows[0].total < 10) {
    return res.status(422).json({
      error: 'INSUFFICIENT_DATA',
      message: 'Fewer than 10 resolved incidents in this period. HDI cannot be reliably computed.',
      details: {
        incident_count: rows[0]?.total ?? 0,
        minimum_required: 10,
      },
    });
  }

  // HDI calculation
  const heroResolutions = rows
    .filter((r: { is_hero: boolean }) => r.is_hero)
    .reduce((sum: number, r: { resolution_count: number }) => sum + r.resolution_count, 0);
  const hdiPct = Math.round((heroResolutions / rows[0].total) * 1000) / 10;

  // Trend: weekly HDI
  const trendResult = await db.raw(`
    SELECT
      DATE_TRUNC('week', i.resolved_at) AS week_start,
      COUNT(*) AS incident_count,
      -- Inline HDI calc per week (top 20% of engineers in that week)
      ROUND(
        SUM(CASE WHEN engineer_rank.rnk <= CEIL(engineer_rank.team_size * 0.2) THEN ir.resolution_count ELSE 0 END)::NUMERIC
        / SUM(ir.resolution_count) * 100,
        1
      ) AS hdi_pct
    FROM (
      SELECT
        ir2.incident_id,
        ir2.engineer_id,
        COUNT(*) OVER (PARTITION BY DATE_TRUNC('week', i2.resolved_at), ir2.engineer_id) AS resolution_count,
        COUNT(DISTINCT ir2.engineer_id) OVER (PARTITION BY DATE_TRUNC('week', i2.resolved_at)) AS team_size,
        RANK() OVER (PARTITION BY DATE_TRUNC('week', i2.resolved_at) ORDER BY COUNT(*) OVER (PARTITION BY DATE_TRUNC('week', i2.resolved_at), ir2.engineer_id) DESC) AS rnk
      FROM incident_resolutions ir2
      JOIN incidents i2 ON i2.id = ir2.incident_id
      WHERE i2.team_id = :team_id AND i2.resolved_at BETWEEN :start AND :end
    ) engineer_rank
    JOIN incident_resolutions ir ON ir.incident_id = engineer_rank.incident_id
    JOIN incidents i ON i.id = ir.incident_id
    GROUP BY DATE_TRUNC('week', i.resolved_at)
    ORDER BY week_start ASC
  `, { team_id, start: start.toISOString(), end: end.toISOString() });

  const hdiSeverity = hdiPct < 30 ? 'low' : hdiPct < 50 ? 'moderate' : hdiPct < 70 ? 'high' : 'critical';

  return res.json({
    team_id,
    period_start: start_date,
    period_end: end_date,
    hdi_pct: hdiPct,
    hdi_severity: hdiSeverity,
    total_incidents: rows[0].total,
    team_size: rows[0].team_size,
    engineer_breakdown: rows.map((r: Record<string, unknown>) => ({
      engineer_id: r.engineer_id,
      engineer_name: r.engineer_name,
      resolution_count: r.resolution_count,
      pct_of_total: r.pct_of_total,
      is_hero: r.is_hero,
    })),
    trend: trendResult.rows,
  });
});
```

---

## 4. Routing Engine — Business Logic

**File**: `src/services/routing/routingEngine.ts`

```typescript
import axios from 'axios';
import NodeCache from 'node-cache';
import { db } from '../../db';

const WEIGHTS = {
  alert_type_match: 0.4,
  recency: 0.3,
  on_call_status: 0.3,
} as const;

const RECENCY_LAMBDA = 0.05; // half-life ~14 days

// Cache on-call status per service for 5 minutes to reduce PD API calls
const onCallCache = new NodeCache({ stdTTL: 300 });

export interface EngineerScore {
  engineer_id: string;
  engineer_name: string;
  score: number;
  confidence_pct: number;
  on_call_status: 'primary' | 'secondary' | 'not_on_call';
  resolution_count: number;
  last_resolved_at: string | null;
  score_breakdown: {
    alert_type_match: number;
    recency: number;
    on_call_status: number;
  };
}

export async function computeRoutingSuggestion(
  incidentId: string,
  serviceName: string,
  alertType: string,
  teamId: string,
  provider: 'pagerduty' | 'opsgenie',
  providerServiceId: string
): Promise<EngineerScore[]> {

  // 1. Fetch team engineers
  const engineers = await db('engineers').where({ team_id: teamId });

  // 2. Fetch historical resolution data for this service + alert type
  const resolutionHistory = await db.raw(`
    SELECT
      ir.engineer_id,
      COUNT(*) AS total_resolutions,
      COUNT(*) FILTER (
        WHERE i.service_name = :service AND i.alert_type = :alert_type
      ) AS matching_resolutions,
      MAX(i.resolved_at) FILTER (
        WHERE i.service_name = :service AND i.alert_type = :alert_type
      ) AS last_matching_resolved_at
    FROM incident_resolutions ir
    JOIN incidents i ON i.id = ir.incident_id
    WHERE ir.engineer_id = ANY(:engineer_ids)
      AND i.team_id = :team_id
    GROUP BY ir.engineer_id
  `, {
    service: serviceName,
    alert_type: alertType,
    engineer_ids: engineers.map((e: { id: string }) => e.id),
    team_id: teamId,
  });

  const historyMap = new Map(
    resolutionHistory.rows.map((r: Record<string, unknown>) => [r.engineer_id, r])
  );

  // 3. Fetch live on-call status
  const onCallStatus = await getOnCallStatus(provider, providerServiceId);

  // 4. Score each engineer
  const scored: EngineerScore[] = engineers.map((engineer: Record<string, string>) => {
    const history = historyMap.get(engineer.id);
    const matchingResolutions = Number(history?.matching_resolutions ?? 0);
    const totalResolutions = Number(history?.total_resolutions ?? 0);
    const lastResolvedAt = history?.last_matching_resolved_at as string | null;

    // Component 1: alert_type_match
    const alertTypeMatchScore = totalResolutions > 0
      ? matchingResolutions / totalResolutions
      : 0.0;

    // Component 2: recency — exponential decay
    let recencyScore = 0.0;
    if (lastResolvedAt) {
      const daysSince = (Date.now() - new Date(lastResolvedAt).getTime()) / (1000 * 60 * 60 * 24);
      recencyScore = Math.exp(-RECENCY_LAMBDA * daysSince);
    }

    // Component 3: on_call_status
    const status = onCallStatus.get(engineer.id) ?? 'not_on_call';
    const onCallScore = status === 'primary' ? 1.0 : status === 'secondary' ? 0.6 : 0.0;

    const totalScore =
      (WEIGHTS.alert_type_match * alertTypeMatchScore) +
      (WEIGHTS.recency * recencyScore) +
      (WEIGHTS.on_call_status * onCallScore);

    return {
      engineer_id: engineer.id,
      engineer_name: engineer.name,
      score: Math.round(totalScore * 1000) / 1000,
      confidence_pct: 0, // computed after sorting
      on_call_status: status,
      resolution_count: matchingResolutions,
      last_resolved_at: lastResolvedAt,
      score_breakdown: {
        alert_type_match: Math.round(alertTypeMatchScore * 1000) / 1000,
        recency: Math.round(recencyScore * 1000) / 1000,
        on_call_status: onCallScore,
      },
    };
  });

  // 5. Sort by score descending
  scored.sort((a, b) => b.score - a.score);

  // 6. Normalize confidence_pct: top score = 100%, others relative
  const topScore = scored[0]?.score ?? 1;
  scored.forEach(s => {
    s.confidence_pct = topScore > 0
      ? Math.round((s.score / topScore) * 100)
      : 0;
  });

  // 7. Persist routing suggestion to incident and log routing_events
  const suggestion = {
    incident_id: incidentId,
    computed_at: new Date().toISOString(),
    routing_source: 'heuristic_v1',
    suggestions: scored.slice(0, 10),
  };

  await db.transaction(async (trx) => {
    await trx('incidents').where({ id: incidentId }).update({
      routing_suggestion: JSON.stringify(suggestion),
      updated_at: new Date(),
    });

    // Log each suggestion for empirical weight tuning
    await trx('routing_events').insert(
      scored.slice(0, 10).map((s, idx) => ({
        incident_id: incidentId,
        suggested_engineer_id: s.engineer_id,
        suggestion_rank: idx + 1,
        weights_snapshot: WEIGHTS,
        score_breakdown: s.score_breakdown,
        routing_source: 'heuristic_v1',
      }))
    );
  });

  return scored;
}

async function getOnCallStatus(
  provider: 'pagerduty' | 'opsgenie',
  providerServiceId: string
): Promise<Map<string, 'primary' | 'secondary' | 'not_on_call'>> {
  const cacheKey = `oncall:${provider}:${providerServiceId}`;
  const cached = onCallCache.get<Map<string, 'primary' | 'secondary' | 'not_on_call'>>(cacheKey);
  if (cached) return cached;

  let onCallMap: Map<string, 'primary' | 'secondary' | 'not_on_call'>;

  if (provider === 'pagerduty') {
    // GET https://api.pagerduty.com/oncalls?service_ids[]=<id>&include[]=users
    const response = await axios.get('https://api.pagerduty.com/oncalls', {
      params: { 'service_ids[]': providerServiceId, 'include[]': 'users' },
      headers: { Authorization: `Token token=${process.env.PD_API_KEY}` },
    });
    onCallMap = parsePagerDutyOnCalls(response.data.oncalls);
  } else {
    // OpsGenie: GET https://api.opsgenie.com/v2/schedules/on-calls?scheduleIdentifier=...
    const response = await axios.get('https://api.opsgenie.com/v2/schedules/on-calls', {
      params: { scheduleIdentifier: providerServiceId },
      headers: { Authorization: `GenieKey ${process.env.OG_API_KEY}` },
    });
    onCallMap = parseOpsGenieOnCalls(response.data.data);
  }

  onCallCache.set(cacheKey, onCallMap);
  return onCallMap;
}

function parsePagerDutyOnCalls(
  oncalls: Array<Record<string, unknown>>
): Map<string, 'primary' | 'secondary' | 'not_on_call'> {
  const map = new Map<string, 'primary' | 'secondary' | 'not_on_call'>();
  for (const entry of oncalls) {
    const userId = (entry.user as Record<string, string>).id;
    const escalationLevel = entry.escalation_level as number;
    // PagerDuty: escalation_level 1 = primary, 2 = secondary
    const status = escalationLevel === 1 ? 'primary' : 'secondary';
    // Don't downgrade if already marked primary
    if (!map.has(userId) || map.get(userId) !== 'primary') {
      map.set(userId, status);
    }
  }
  return map;
}
```

---

## 5. Runbook Service — Similarity Matching for Capture Modal

**File**: `src/services/runbook/runbookService.ts`

```typescript
export async function findSimilarRunbook(
  serviceName: string,
  alertType: string,
  teamId: string
): Promise<{ runbook: Runbook; similarity: number } | null> {

  // Phase 1 (MVP): exact match on service_name + alert_type
  const exactMatch = await db('runbooks')
    .where({ service_name: serviceName, alert_type: alertType, team_id: teamId })
    .orderBy('updated_at', 'desc')
    .first();

  if (exactMatch) {
    return { runbook: exactMatch, similarity: 1.0 };
  }

  // Phase 2: pg_trgm similarity on (service_name || ' ' || alert_type)
  const query = `${serviceName} ${alertType}`;
  const result = await db.raw(`
    SELECT *,
      similarity(service_name || ' ' || alert_type, ?) AS sim_score
    FROM runbooks
    WHERE team_id = ?
      AND similarity(service_name || ' ' || alert_type, ?) > 0.4
    ORDER BY sim_score DESC
    LIMIT 1
  `, [query, teamId, query]);

  if (result.rows.length > 0 && result.rows[0].sim_score >= 0.85) {
    return { runbook: result.rows[0], similarity: result.rows[0].sim_score };
  }

  return null;
}

function buildRunbookMarkdown(
  title: string,
  data: RunbookStructuredData
): string {
  return [
    `# ${title}`,
    '',
    '## Root Cause',
    data.root_cause,
    '',
    '## Steps to Resolve',
    data.steps.map((step, i) => `${i + 1}. ${step}`).join('\n'),
    '',
    '## Services Affected',
    data.services_affected.map(s => `- ${s}`).join('\n'),
    '',
    data.prevention ? `## Prevention\n${data.prevention}` : '',
  ].filter(line => line !== undefined).join('\n');
}
```

---

## 6. Idempotency Design

All state-mutating operations are idempotent:

| Operation | Idempotency Key | Mechanism |
|---|---|---|
| Webhook ingestion | `(provider, provider_event_id)` | `UNIQUE` constraint on `webhook_events`; ON CONFLICT DO NOTHING |
| Incident creation | `(provider, provider_incident_id)` | `UNIQUE` constraint on `incidents`; ON CONFLICT DO UPDATE (upsert status) |
| Runbook creation for incident | `incident_id` | Check for existing `runbook_id` on incident; return 409 with existing ID |
| Incident resolution record | `incident_id` | `UNIQUE (incident_id)` on `incident_resolutions` |
| Embedding job | `runbook_id` | Bull job deduplication by `jobId = runbook.id`; `updateData` if already queued |

---

## 7. Environment Variables

```bash
# Database
DATABASE_URL=postgresql://sentinel:password@localhost:5432/sentinel_production
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=20

# Redis (Bull queue)
REDIS_URL=redis://localhost:6379

# PagerDuty
PD_WEBHOOK_SECRET=pd_webhook_signing_secret_here
PD_API_KEY=pd_api_key_here

# OpsGenie
OG_WEBHOOK_SECRET=og_webhook_secret_here
OG_API_KEY=og_api_key_here

# GitHub
GITHUB_WEBHOOK_SECRET=github_webhook_secret_here
GITHUB_APP_ID=12345
GITHUB_APP_PRIVATE_KEY_BASE64=base64_encoded_pem_here

# OpenAI (for embeddings — used in v1.1, can be omitted at launch)
OPENAI_API_KEY=sk-...

# JWT
JWT_SECRET=32_byte_random_secret_here
JWT_EXPIRY_SECONDS=86400

# App
NODE_ENV=production
PORT=3000
LOG_LEVEL=info
```

All secrets sourced from AWS Secrets Manager at runtime. Environment variables are populated by ECS task definition referencing Secrets Manager ARNs. Never committed to source control.

---

## 8. Testing Plan

### Unit Tests (Jest)

| Module | Tests |
|---|---|
| `routingEngine.ts` | Score computation with known inputs: assert scores match expected weights × components. Test recency decay at 0, 7, 14, 30 days. Test on_call_status=primary gives highest possible on_call component. Test empty history produces score from on_call only. |
| `normalize.ts` | Each provider's known payload formats normalize to correct alert_type, service_name, severity. Unknown alert type falls through to raw normalized form. |
| `hdi.ts` | HDI calculation with known resolution counts: 6-person team, verify top-2 are flagged as heroes, HDI % matches manual calculation. |
| `runbookService.ts` | Exact match returns similarity=1.0. No match returns null. |

### Integration Tests (Supertest + test DB)

| Scenario | Covers |
|---|---|
| PagerDuty webhook → routing suggestion computed | Webhook validation, normalization, queue processing, routing engine, DB write |
| Duplicate webhook → single incident created | Idempotency for webhook_events UNIQUE constraint |
| Close incident with runbook → incident resolved, runbook saved, resolution record created | Full runbook capture flow |
| Invalid signature → 401, no DB write | Security boundary |
| GET /runbooks?q=connection+pool → matching runbooks returned | pg_trgm search |
| GET /dashboard/hdi → correct HDI% for seeded data | Dashboard aggregation |

### Contract Tests (Pact)

Frontend consumer tests for all 5 API endpoints. Backend verifies against Pact broker on every CI run. New response fields are additive; breaking changes fail verification.

### Load Test (k6)

Run in staging before sprint 3 production deploy:
- 50 concurrent users hitting `GET /incidents/:id/routing-suggestion`
- Assert p99 < 500ms
- Assert error rate < 0.1%

`tests/load/routing-suggestion.k6.js` — seeded with 1000 incidents and routing suggestions.
