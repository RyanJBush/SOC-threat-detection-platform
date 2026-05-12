# Demo Runbook — Mercury (Student Portfolio)

This runbook demonstrates Mercury as a **SOC-style workflow simulator** using **synthetic logs only**.

## 1) Start platform

```bash
docker compose up --build
```

- Frontend: <http://localhost:5173>
- Backend docs: <http://localhost:8000/docs>

## 2) Log in

Use seeded demo credentials:

- `admin / admin123` (full demo flow)
- `analyst / analyst123`

## 3) Replay synthetic logs

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

python scripts/ingest_logs.py data/brute_force_scenario.json --token "$TOKEN"
```

Optional additional replays:

- `data/sample_auth_logs.json`
- `data/sample_network_logs.json`
- `data/sample_endpoint_logs.json`

## 4) View generated alerts

- UI: `/alerts`
- API:

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/alerts?status=open" | python -m json.tool
```

## 5) Walk through SOC-style triage

In UI:

1. Open an alert.
2. Change status (`open` → `investigating` → `resolved` or `false_positive`).
3. Assign analyst.
4. Add note.
5. Submit analyst feedback.

## 6) Demonstrate case queue

1. Go to `/incidents`.
2. Create an incident case.
3. Attach related alert(s).
4. Update case status.

This demonstrates workflow orchestration, not live incident response.

## 7) Show MITRE mapping (implemented only)

- Open `/detections` and review catalog mappings.
- Confirm via API: `GET /api/detections/catalog`.
- Reference static doc: `docs/MITRE_MAPPING.md`.

Use ATT&CK language only for detections that exist in the catalog.

## 8) Demo talking points

- Mercury is a student portfolio system, not a vendor SIEM.
- Data is synthetic and replayed for reproducibility.
- Value shown: detection logic, workflow modeling, and documentation rigor.
