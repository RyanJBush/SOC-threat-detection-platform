# API Docs — Mercury SOC Threat Detection Platform

Mercury exposes a FastAPI API for a **synthetic SOC workflow simulation**.

- Swagger: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## Accuracy / scope notes

- API data is synthetic and demo-oriented.
- Endpoints model SOC processes for portfolio demonstration.
- Do not interpret outputs as real enterprise telemetry or real IR operations.

## Auth

### `POST /api/auth/login`
Returns JWT bearer token for seeded demo users.

## Event ingestion

### `POST /api/events`
Ingest one synthetic event and run detection.

### `POST /api/events/batch`
Ingest event batches. Supports deferred processing workflows.

### `GET /api/events`
List ingested synthetic events.

## Alerts workflow

### `GET /api/alerts`
View generated alerts.

### `GET /api/alerts/{alert_id}`
Alert detail (evidence + mapped metadata).

### `PATCH /api/alerts/{alert_id}/status`
Update SOC-style triage status.

### `PATCH /api/alerts/{alert_id}/assign`
Assign alert to analyst user.

### `POST /api/alerts/{alert_id}/notes`
Add investigation notes.

### `POST /api/alerts/{alert_id}/feedback`
Record true/false positive feedback.

## Case queue (incidents)

### `GET /api/incidents`
List incident cases.

### `POST /api/incidents`
Create case.

### `POST /api/incidents/{id}/alerts`
Attach alerts to a case.

### `PATCH /api/incidents/{id}/status`
Update case state.

## Detections and MITRE mapping

### `GET /api/detections/catalog`
Returns implemented detection definitions and associated ATT&CK mappings.

### `GET /api/detections`
Returns detection records that fired from synthetic inputs.

> ATT&CK mapping language should only be used for entries present in this catalog.

## Metrics and platform controls

- `GET /api/metrics/*` for dashboard analytics on synthetic runs.
- `GET /api/platform/feature-flags` and related routes for demo feature toggles and audit views.

## Minimal replay-to-alert example

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

python scripts/ingest_logs.py data/brute_force_scenario.json --token "$TOKEN"

curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/alerts?status=open" | python -m json.tool
```
