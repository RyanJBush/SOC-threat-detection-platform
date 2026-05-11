# API Reference

Mercury exposes a FastAPI service. Interactive Swagger docs are served at `/docs` when
the backend is running. This file summarizes the endpoints most relevant to the
threat-detection workflow.

> All requests below assume the backend is running on `http://localhost:8000`.
> Authenticated routes require a `Bearer` token obtained from `POST /api/auth/login`.

## Authentication

### `POST /api/auth/login`

```bash
curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "analyst", "password": "analyst"}'
```

Response:

```json
{ "access_token": "<jwt>", "token_type": "bearer" }
```

Roles: `analyst` (read alerts/events), `investigator` (own cases), `admin` (full).

## Event ingestion

### `POST /api/events`

Ingest a single event. Each event is scored synchronously and may emit detections/alerts.

```bash
curl -s -X POST http://localhost:8000/api/events \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @data/brute_force_scenario.json
```

Request body fields (`EventCreate`):

| Field | Type | Notes |
|---|---|---|
| `source` | string | Log source identifier, e.g. `okta`, `zeek` |
| `source_ip` | string? | Optional IP address |
| `username` | string? | Optional actor username |
| `event_type` | string | e.g. `auth.login.failure` |
| `severity` | string | `low` \| `medium` \| `high` \| `critical` |
| `status` | string | Default `new` |
| `message` | string | Human-readable summary |
| `metadata` | object | Arbitrary structured fields |
| `occurred_at` | datetime? | ISO-8601; defaults to ingestion time |

### `POST /api/events/batch`

Same schema wrapped as `{"events": [...]}`. Recommended for bulk replay; used by
`scripts/ingest_logs.py`.

## Alerts

### `GET /api/alerts`

List alerts with optional filters: `?severity=high&status=open&technique=T1110`.

### `GET /api/alerts/{id}`

Returns the alert with its underlying detections, MITRE techniques, and evidence events.

### `PATCH /api/alerts/{id}`

Update alert status (`open` → `investigating` → `resolved` / `false_positive`) and
attach an analyst note.

## Incidents (case management)

### `GET /api/incidents`, `POST /api/incidents`, `PATCH /api/incidents/{id}`

Group related alerts into a case, track owner and status, and append analyst notes.
See `backend/app/routers/incidents.py` for full schema.

## Detections catalog

### `GET /api/detections`

Returns the static catalog of detection definitions
(`backend/app/services/detection_catalog.py`) — useful for the dashboard's coverage
view and for tuning rules.

## Metrics

### `GET /api/metrics/summary`

High-level counts: open alerts by severity, alerts per MITRE tactic, mean time to
acknowledge. Used by the SOC dashboard.

## Sample ingestion workflow

```bash
# 1. Log in
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"analyst","password":"analyst"}' | jq -r .access_token)

# 2. Replay sample logs
python scripts/ingest_logs.py data/sample_auth_logs.json --token "$TOKEN"

# 3. See what fired
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/alerts?status=open" | jq '.[] | {id, name, severity, techniques}'
```
