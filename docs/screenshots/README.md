# Screenshots — Mercury Portfolio Demo

All screenshots in this folder come from the local Mercury portfolio environment and synthetic data replay.

> **Reminder:** Synthetic log portfolio demo — not a production SIEM.

## Current screenshot set
| File | View | Data context |
|---|---|---|
| `01-alerts-feed.png` | `/alerts` | Alert list after synthetic replay |
| `02-incident-queue.png` | `/incidents` | Incident queue and workflow states |
| `03-mitre-attack-coverage.png` | `/detections` | Mapping fields for implemented rules |
| `04-metrics-dashboard.png` | `/dashboard` | Summary metrics from demo dataset |
| `05-api-swagger-docs.png` | `http://localhost:8000/docs` | Backend API docs |
| `06-alert-detail.png` | `/alerts/:id` | Alert evidence and analyst actions |
| `07-login.png` | `/login` | Seeded user login page |
| `08-deferred-jobs.png` | `/detections` jobs section | Deferred processing view |

## TODO recapture checklist
- [ ] Re-capture `/alerts` after latest rule changes
- [ ] Re-capture `/incidents` after assignment/status workflow updates
- [ ] Re-capture `/detections` if mapping metadata changes
- [ ] Re-capture `/dashboard` if metric cards change
- [ ] Re-capture API docs when endpoint contracts change

## Capture workflow
```bash
make dev

TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

make replay-bruteforce TOKEN="$TOKEN"
```

## Caption guidance
- Mention that data is synthetic/simulated.
- Use “Portfolio Preview,” “UI Preview,” or “Design Preview” (not “Live Preview”).
- Only reference ATT&CK where a rule mapping is actually implemented.
