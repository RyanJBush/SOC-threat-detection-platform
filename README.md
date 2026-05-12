# Mercury — SOC-Style Threat Detection Portfolio Demo

> **Portfolio demo using synthetic logs — not a production SIEM.**

Mercury is a SOC-style security portfolio project built by a **University of Maryland student studying Information Science and Electrical Engineering with a Business minor**. It demonstrates how synthetic security events can move through an ingest → parse → detect → visualize workflow in a full-stack app.

## Summary
Mercury is designed for interviews, project walkthroughs, and detection-engineering discussion. The backend accepts synthetic events, applies implemented detection rules, and stores alert/incidence data. The frontend provides SOC-inspired alert and incident views for triage practice.

## What it demonstrates
- Structured event ingestion through API batch endpoints.
- Parsing and normalization of security-event fields used by detection logic.
- Rule-based alert generation on synthetic auth, network, and endpoint datasets.
- Alert lifecycle and incident queue workflows (status changes, assignment, notes).
- Detection metadata views, including ATT&CK mapping fields for implemented rules.

## Tech stack
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Python
- **Frontend:** React, Vite, TypeScript/JavaScript
- **Containerization:** Docker Compose
- **Data model:** Synthetic event replay with SOC-style alerts and incidents

## Architecture
- Architecture overview: `docs/ARCHITECTURE.md`
- API reference: `docs/api.md`
- ATT&CK mapping notes for implemented detections: `docs/MITRE_MAPPING.md`

## How to run
### Option 1: Docker (recommended)
```bash
make dev
```

### Option 2: Local split services
```bash
make install
make backend-dev
make frontend-dev
```

### Demo credentials
- `admin / admin123`
- `analyst / analyst123`
- `deteng / deteng123`
- `viewer / viewer123`

## Demo workflow
1. Start the stack.
2. Log in through the app UI.
3. Create an API token:
   ```bash
   TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}' \
     | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
   ```
4. Replay an included scenario:
   ```bash
   make replay-bruteforce TOKEN="$TOKEN"
   ```
5. Optional: generate a fresh synthetic file and replay it:
   ```bash
   make generate-synth
   python scripts/ingest_logs.py data/generated_synthetic_logs.json --token "$TOKEN"
   ```
6. Review `/alerts`, `/incidents`, `/detections`, and `/dashboard`.

## Screenshots
- Screenshot inventory and recapture checklist: `docs/screenshots/README.md`
- Portfolio Preview page: `docs/preview/index.html`

## Limitations and future work
- Synthetic logs only; no live SIEM connector or production telemetry feed.
- Intended for portfolio review, not production incident response.
- ATT&CK coverage reflects only rules currently implemented in this repository.
- Future improvements: additional synthetic scenarios, better rule tuning UX, and richer detection analytics.

## Resume bullets
- See `docs/resume-bullets.md` for concise, project-specific bullet options.

## License
MIT (`LICENSE`).
