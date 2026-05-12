# Demo Runbook

A scripted walkthrough for showing Mercury end-to-end in roughly **5 minutes**.
All data is synthetic — see the README's "Limitations & Future Work" for scope.

## 0) Prerequisites

- Docker + docker compose
- Python 3.11+ on the host (for the `scripts/ingest_logs.py` CLI)
- (Optional) `jq` for nicer JSON in the terminal

## 1) Start the stack

```bash
docker compose up --build
```

This starts:

- `db` — PostgreSQL 16
- `backend` — FastAPI on <http://localhost:8000> (Swagger at `/docs`)
- `frontend` — React + Vite dev server on <http://localhost:5173>

The backend seeds demo users and baseline events on first boot
(`backend/app/services/seed.py`).

## 2) Log in to the dashboard

- URL: <http://localhost:5173>
- Demo credentials (seeded):

  | Username | Password | Role |
  |---|---|---|
  | `admin` | `admin123` | Admin (full access) |
  | `analyst` | `analyst123` | SOC Analyst |
  | `deteng` | `deteng123` | Detection Engineer |
  | `viewer` | `viewer123` | Read-only |

  Use `admin` for the full feature set.

## 3) End-to-end demo flow (UI)

1. Go to **Events** (`/events`).
2. From the scenarios panel, seed **Credential Access: Password Spray**
   (`POST /api/events/scenarios/credential_access_password_spray/seed`).
3. Open **Alerts** (`/alerts`) — a high-severity Brute Force / Password
   Spray alert should appear, tagged with MITRE technique T1110.
4. Open the alert detail and walk through:
   - status transitions (open → investigating → resolved / false_positive)
   - analyst assignment
   - investigation note
   - AI summary and AI triage endpoints
   - true / false-positive feedback
5. Go to **Incidents** (`/incidents`) → create an incident and attach the alert
   via `POST /api/incidents/{id}/alerts`.
6. Update the incident status and generate the **AI wrap-up**.
7. Go to **Dashboard** (`/dashboard`) and review KPIs, detection-quality, and
   correlation hotspots (Recharts panels driven by `/api/metrics/*`).
8. Go to **Detections** (`/detections`) and show the catalog with MITRE
   technique and tactic tags per rule.

## 4) Demo flow via the API + CLI

```bash
# Get a token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

# Replay a synthetic scenario file in 50-event batches
python scripts/ingest_logs.py data/brute_force_scenario.json --token "$TOKEN"
# Per batch: { accepted, alerts_generated }

# View open alerts
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/alerts?status=open" | python -m json.tool

# Inspect a specific alert
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/alerts/1" | python -m json.tool
```

Available replayable inputs in `data/`:

- `sample_auth_logs.json`
- `sample_network_logs.json`
- `sample_endpoint_logs.json`
- `brute_force_scenario.json`

## 5) Deferred-processing demo (back-pressure)

1. Ingest a batch with `defer_detection=true`:

   ```bash
   curl -X POST http://localhost:8000/api/events/batch \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "defer_detection": true,
       "events": [
         {
           "source":"identity_provider",
           "source_ip":"198.51.100.50",
           "username":"jdoe",
           "event_type":"login_failed",
           "message":"Failed login"
         }
       ]
     }'
   ```

2. Open **Detections** → **Process Pending Jobs**, or call
   `POST /api/jobs/process-pending`.
3. Return to **Alerts** and confirm the alert appears.

## 6) MITRE ATT&CK coverage view

- UI: detection catalog page (`/detections`) and per-alert MITRE tags on
  the alert detail page.
- API: `GET /api/detections/catalog` returns each detection's technique IDs
  and tactics.
- Reference table: [`docs/MITRE_MAPPING.md`](MITRE_MAPPING.md).

## 7) Suggested screenshots

Capture these for the portfolio:

1. Login page
2. Alert feed at `/alerts` (severity + MITRE tags visible)
3. Alert detail with AI summary and notes
4. Incident queue at `/incidents`
5. Dashboard KPIs and correlation hotspots
6. Detections catalog at `/detections`
7. Swagger UI at `http://localhost:8000/docs`

Store under `docs/screenshots/` and update
[`docs/screenshots/README.md`](screenshots/README.md).

## 8) Troubleshooting

- **Backend unreachable from frontend:** confirm `VITE_API_BASE_URL` matches the
  backend host/port and the `/health` endpoint returns 200.
- **No alerts appear after ingestion:** verify feature flags via
  `GET /api/platform/feature-flags` and check the relevant detection is
  enabled.
- **401 on every API call:** clear `localStorage` key `vanguard_token` in the
  browser and re-log in.
- **Postgres startup race:** Compose `depends_on` waits for the DB health
  check; if `backend` exits early, run `docker compose logs backend`.
- **`scripts/ingest_logs.py` errors:** confirm the input file is valid JSON or
  JSON-Lines (`--dry-run` parses without posting).
