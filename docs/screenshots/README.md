# Screenshots — Mercury

This folder contains screenshots from the local portfolio demo using synthetic data only.

## Captured screenshots
| File | View | Notes |
|---|---|---|
| `01-alerts-feed.png` | `/alerts` | Alert queue after synthetic replay |
| `02-incident-queue.png` | `/incidents` | Incident list and workflow states |
| `03-mitre-attack-coverage.png` | `/detections` | Detection catalog mappings for implemented rules |
| `04-metrics-dashboard.png` | `/dashboard` | Demo-scale summary metrics |
| `05-api-swagger-docs.png` | `http://localhost:8000/docs` | Backend API documentation |
| `06-alert-detail.png` | `/alerts/:id` | Alert evidence and action controls |
| `07-login.png` | `/login` | Seeded demo authentication page |
| `08-deferred-jobs.png` | `/detections` jobs panel | Deferred processing demo view |

## Screenshot checklist for updates
- [ ] Re-capture `/alerts` after latest synthetic replay
- [ ] Re-capture `/incidents` showing assignment and status changes
- [ ] Re-capture `/detections` mapping panel for currently implemented rules
- [ ] Re-capture `/dashboard` summary cards
- [ ] Re-capture API docs page if endpoints change

## Capture workflow
```bash
docker compose up --build

TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

python scripts/ingest_logs.py data/brute_force_scenario.json --token "$TOKEN"
```

## Caption rules
- State that data shown is synthetic or simulated.
- Avoid language implying real enterprise telemetry or live SIEM ingestion.
- Use ATT&CK terminology only for implemented mappings.
