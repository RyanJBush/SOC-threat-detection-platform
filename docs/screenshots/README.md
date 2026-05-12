# Screenshot Guide — Mercury

Screenshots in this folder should represent the **running local demo** and **synthetic data only**.

## Purpose

These images support portfolio storytelling for a student SOC simulator:

- replay synthetic logs
- inspect generated alerts
- walk case queue workflow
- view implemented MITRE mapping

## Recommended captures

| File | View | Why it matters |
|---|---|---|
| `01-alerts-feed.png` | `/alerts` | Shows generated alert queue after replay |
| `02-incident-queue.png` | `/incidents` | Shows case queue and state management |
| `03-mitre-attack-coverage.png` | `/detections` | Shows ATT&CK mapping for implemented detections |
| `04-metrics-dashboard.png` | `/dashboard` | Shows summary metrics on synthetic runs |
| `05-api-swagger-docs.png` | `http://localhost:8000/docs` | Shows documented API surface |
| `06-alert-detail.png` | `/alerts/:id` | Shows evidence + workflow actions |
| `07-login.png` | `/login` | Shows seeded demo auth entrypoint |
| `08-deferred-jobs.png` | `/detections` jobs panel | Shows deferred processing demo capability |

## Capture workflow

```bash
docker compose up --build

TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

python scripts/ingest_logs.py data/brute_force_scenario.json --token "$TOKEN"
```

Then capture each view from the browser using the local frontend.

## Accuracy rules for screenshots

- Do not include real customer/enterprise data.
- Do not claim real SOC monitoring or live incident response.
- Use ATT&CK wording only where shown by implemented detections.
- Keep captions explicit that the system runs synthetic replay scenarios.
