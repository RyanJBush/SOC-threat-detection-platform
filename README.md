# Mercury — SOC Threat Detection Platform

Mercury is a **cybersecurity student portfolio project** that simulates SOC analyst workflows on **synthetic logs only**. It is designed to demonstrate detection engineering, alert triage, and case handling fundamentals in a clean full-stack implementation.

> Mercury is **not** a production SIEM, does **not** ingest real enterprise telemetry, and does **not** represent real incident response operations.

## What this project is

- A FastAPI + React platform for replaying sample security events.
- A sandbox for SOC-style detection-to-alert-to-case workflows.
- A portfolio artifact focused on architecture clarity and security domain fluency.

## What this project is not

- Not a production SOC tool.
- Not connected to real EDR/SIEM pipelines.
- Not validating detections against live enterprise environments.

## Quick start (demo)

```bash
docker compose up --build
```

- Frontend: <http://localhost:5173>
- Backend API docs: <http://localhost:8000/docs>

Demo users (seeded):

- `admin / admin123`
- `analyst / analyst123`
- `deteng / deteng123`
- `viewer / viewer123`

## Replay sample logs

Use the included CLI to replay synthetic scenarios:

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

python scripts/ingest_logs.py data/brute_force_scenario.json --token "$TOKEN"
```

Other synthetic datasets:

- `data/sample_auth_logs.json`
- `data/sample_network_logs.json`
- `data/sample_endpoint_logs.json`

## View generated alerts

- UI: open `/alerts` after replay.
- API:

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/alerts?status=open" | python -m json.tool
```

Alerts are generated from implemented detection logic in the backend service and surfaced with severity, confidence, evidence links, and workflow status.

## Case queue / alert workflow

Mercury models a **SOC-style analyst workflow**:

1. ingest synthetic events
2. create detections and alerts
3. triage alert status (`open`, `investigating`, `resolved`, `false_positive`)
4. add analyst notes and assignments
5. group related alerts into incidents (case queue)

This is workflow simulation for learning/portfolio use, not real incident response execution.

## MITRE ATT&CK mapping

Mercury uses ATT&CK mapping language **only where implemented in the detection catalog**.

- Mapping source: `backend/app/services/detection_catalog.py`
- Reference table: `docs/MITRE_MAPPING.md`
- API surface: `GET /api/detections/catalog`

No ATT&CK coverage is implied beyond those implemented detections.

## Documentation map

- Architecture: `docs/ARCHITECTURE.md`
- API docs: `docs/api.md`
- Demo runbook: `docs/DEMO_RUNBOOK.md`
- Resume bullets: `docs/resume-bullets.md`
- Screenshots guide: `docs/screenshots/README.md`

## Limitations

- Synthetic logs only; no real telemetry connectors.
- No production hardening expectations (HA, scaling, SSO, tenancy isolation).
- Detection quality reflects seeded/demo data, not enterprise baselines.
- AI helper endpoints are demo scaffolding, not analyst-grade copilots.

## Future work

- Add additional synthetic attack scenarios and detection tuning exercises.
- Improve ATT&CK visualization (technique/tactic matrix from implemented rules).
- Add stream-processing simulation path (queue-backed demo mode).
- Expand analyst workflow metrics from feedback loops.

## Portfolio framing

Mercury is intentionally positioned as a **strong student cybersecurity portfolio project**: honest scope, reproducible demos, and clearly implemented SOC fundamentals.
