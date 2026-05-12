# API Reference

Mercury exposes a FastAPI service. Interactive Swagger / OpenAPI docs are served
at <http://localhost:8000/docs> (and ReDoc at `/redoc`) when the backend is
running. This file summarises the endpoints most relevant to the
threat-detection workflow, grounded in the actual routers in
`backend/app/routers/`.

> All examples below assume the backend is running on `http://localhost:8000`.
> Authenticated routes require a `Bearer` JWT obtained from
> `POST /api/auth/login`.

## Conventions

- Base URL: `http://localhost:8000`
- Auth header: `Authorization: Bearer <jwt>`
- Content type: `application/json`
- Time fields: ISO-8601, UTC
- Pagination: list endpoints accept `limit`, `offset`, and optional filters
  documented per endpoint.

## Demo users (seeded on startup)

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | Admin |
| `analyst` | `analyst123` | SOC Analyst |
| `deteng` | `deteng123` | Detection Engineer |
| `viewer` | `viewer123` | Read-only |

## Authentication — `/api/auth`

### `POST /api/auth/login`

```bash
curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Response:

```json
{ "access_token": "<jwt>", "token_type": "bearer" }
```

### `GET /api/auth/me`

Returns the authenticated user (id, username, role, org).

### `GET /api/auth/analysts`

Lists users assignable as analysts (used by the alert-assign UI).

## Events ingestion — `/api/events`

### `POST /api/events`

Ingest a single event. The event is scored synchronously and may emit
detections / alerts.

```bash
curl -s -X POST http://localhost:8000/api/events \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "identity_provider",
    "source_ip": "198.51.100.50",
    "username": "jdoe",
    "event_type": "auth.login.failure",
    "severity": "medium",
    "message": "Failed login attempt",
    "metadata": {"user_agent": "curl/8.0"}
  }'
```

Common fields (see `EventCreate` in `backend/app/schemas.py` for the source of truth):

| Field | Type | Notes |
|---|---|---|
| `source` | string | Log source identifier (e.g. `identity_provider`, `zeek`) |
| `source_ip` | string? | Optional IPv4/IPv6 |
| `username` | string? | Optional actor |
| `event_type` | string | e.g. `auth.login.failure`, `process.exec` |
| `severity` | string | `low` \| `medium` \| `high` \| `critical` |
| `status` | string | Default `new` |
| `message` | string | Human-readable summary |
| `metadata` | object | Arbitrary structured fields |
| `occurred_at` | datetime? | ISO-8601; defaults to ingestion time |

### `POST /api/events/batch`

Bulk-ingest events. Body: `{ "events": [ EventCreate, ... ], "defer_detection": false }`.

When `defer_detection` is `true`, events are stored and detection jobs are
queued; they can be processed later via `POST /api/jobs/process-pending`.

Used by `scripts/ingest_logs.py`.

### `POST /api/events/stream`

Streaming variant of batch ingest (same schema; intended for chunked clients).

### `POST /api/events/replay`

Replay a saved scenario or batch back through the detection pipeline.

### `GET /api/events`

List events with optional filters (`source`, `username`, `severity`, time range,
pagination).

### `GET /api/events/{event_id}`

Single-event detail with linked detections and alerts.

### Scenarios

- `GET /api/events/scenarios` — list seedable demo scenarios.
- `POST /api/events/scenarios/{scenario_key}/seed` — seed a scenario's events
  through the ingestion pipeline. Keys are defined in
  `backend/app/services/seed_scenarios.py` (e.g. `credential_access_password_spray`).
- `POST /api/events/simulations/run` — run a parametrised simulation.

## Alerts — `/api/alerts`

### `GET /api/alerts`

List alerts. Filters (verified): `severity`, `status`, `technique`, plus
pagination. Returns alerts with MITRE techniques, severity, status, owner.

### `GET /api/alerts/{alert_id}`

Detail with underlying detections, MITRE techniques, evidence events.

### `PATCH /api/alerts/{alert_id}/status`

Body: `{ "status": "investigating" }` (or `resolved`, `false_positive`).

### `PATCH /api/alerts/{alert_id}/assign`

Body: `{ "assignee_id": <user-id> }`.

### Notes & timeline

- `GET /api/alerts/{alert_id}/notes`
- `POST /api/alerts/{alert_id}/notes`
- `GET /api/alerts/{alert_id}/timeline`

### Analyst feedback (true/false positive)

`POST /api/alerts/{alert_id}/feedback` — body includes verdict (`true_positive`
or `false_positive`) and a note.

### AI assist

- `GET /api/alerts/{alert_id}/ai-summary` — narrative summary of the alert.
- `GET /api/alerts/{alert_id}/ai-triage` — suggested triage steps.

> The AI endpoints are scaffolded in `backend/app/services/ai_assistant.py`;
> exact behaviour depends on feature-flag and model configuration.

## Incidents (cases) — `/api/incidents`

### `GET /api/incidents`, `POST /api/incidents`, `GET /api/incidents/{id}`

Group related alerts into a managed case (status, owner, timeline).

### `PATCH /api/incidents/{id}/status`

Update incident status.

### `POST /api/incidents/{id}/alerts`

Attach one or more alerts to the incident.

### `GET /api/incidents/{id}/timeline`

Chronological timeline of incident events.

### `GET /api/incidents/{id}/ai-wrapup`

AI-generated wrap-up summary for the incident.

## Detections catalog — `/api/detections`

### `GET /api/detections/catalog`

Static catalog of detection definitions, mirroring
`backend/app/services/detection_catalog.py`. Each entry: key, title, severity,
default confidence, MITRE techniques, MITRE tactics, recommendation, dedup
window. See [`docs/MITRE_MAPPING.md`](MITRE_MAPPING.md) for the table.

### `GET /api/detections`

List of runtime detection records (what actually fired against ingested events).

## Detection jobs — `/api/jobs`

### `GET /api/jobs`

List pending / completed detection jobs (used with deferred batch ingestion).

### `POST /api/jobs/process-pending`

Drain the pending-jobs queue. Returns the jobs processed.

## Metrics — `/api/metrics`

| Endpoint | Purpose |
|---|---|
| `GET /summary` | Open alerts by severity, totals, MTTR-style basics |
| `GET /kpis` | Dashboard KPI tiles |
| `GET /detection-comparison` | Rule vs. anomaly coverage breakdown |
| `GET /jobs` | Detection-job throughput metrics |
| `GET /detection-quality` | Precision / recall proxies from analyst feedback |
| `GET /scenario-benchmarks` | Per-scenario benchmark results |
| `GET /correlation-hotspots` | Top correlated entities (IPs, users) |

## Platform — `/api/platform`

| Endpoint | Purpose |
|---|---|
| `GET /feature-flags` | List feature flags |
| `PATCH /feature-flags/{flag_key}` | Toggle a feature flag |
| `GET /audit-logs` | Audit-log entries (sensitive mutations) |

## Health — `/health`, `/ready`, `/health/dependencies`

Unauthenticated liveness / readiness / dependency-check endpoints used by
Docker Compose health checks and CI smoke tests.

## End-to-end sample workflow

```bash
# 1. Log in
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

# 2. Replay synthetic logs
python scripts/ingest_logs.py data/sample_auth_logs.json --token "$TOKEN"

# 3. See alerts
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/alerts?status=open" \
  | python -m json.tool

# 4. Create an incident and attach an alert
curl -s -X POST http://localhost:8000/api/incidents \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Brute force on jdoe","summary":"From single IP"}'
```

## Out of scope

The API surface is designed for a portfolio demo. It does not implement
streaming protocols (Kafka, syslog UDP), enterprise-grade authn (OIDC/SAML),
multi-tenant isolation guarantees, or real threat-intel feed connectors. See
the README's **Limitations & Future Work** for the planned roadmap.
