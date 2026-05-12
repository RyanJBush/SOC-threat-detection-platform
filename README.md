# Mercury — SOC Threat Detection Platform

A portfolio SOC detection demo that simulates alerting workflows from synthetic security logs.

⚠️ **Portfolio demo.** This is not a production SIEM. It demonstrates SOC-style detection workflows and data pipelines using synthetic data.

## Recruiter-facing summary
Mercury is a full-stack cybersecurity portfolio project built to show how I think about detection engineering, triage workflow design, and documentation quality. The platform ingests synthetic log events, applies demo-scale detection logic, and presents alerts/incidents in a SOC-style UI. It is intentionally scoped for learning and interview discussion, not real enterprise monitoring.

## What this project demonstrates
- Designing a clear ingest → detect → triage workflow with synthetic data.
- Building a FastAPI + React application with role-based user flows.
- Documenting architecture and API behavior for recruiter and interviewer review.
- Implementing detection metadata, alert lifecycle states, and case management concepts.

## Tech stack
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Alembic, Python
- **Frontend:** React, TypeScript, Vite
- **Platform:** Docker Compose
- **Domain model:** SOC-style alerts/incidents with synthetic event replay

## Architecture overview
- Architecture docs: `docs/ARCHITECTURE.md`
- API reference: `docs/api.md`
- Detection mapping reference: `docs/MITRE_MAPPING.md`

## How to run locally
```bash
docker compose up --build
```

- Frontend: <http://localhost:5173>
- Backend OpenAPI docs: <http://localhost:8000/docs>

Seeded demo users:
- `admin / admin123`
- `analyst / analyst123`
- `deteng / deteng123`
- `viewer / viewer123`

## Demo workflow
1. Start the stack with Docker Compose.
2. Log in from the UI using a seeded account.
3. Replay synthetic logs using the ingest script:
   ```bash
   TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}' \
     | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

   python scripts/ingest_logs.py data/brute_force_scenario.json --token "$TOKEN"
   ```
4. Review generated alerts and incident queue behavior in the UI.

Synthetic datasets included:
- `data/brute_force_scenario.json`
- `data/sample_auth_logs.json`
- `data/sample_network_logs.json`
- `data/sample_endpoint_logs.json`

## Screenshots / demo
- Screenshot index and capture notes: `docs/screenshots/README.md`
- Portfolio preview page: `docs/preview/index.html`

## Limitations and future work
- Uses synthetic log data generated for demo purposes; no real telemetry connectors.
- Not hardened for production operations (HA, scaling, SSO, multi-tenant isolation).
- MITRE ATT&CK mappings are limited to implemented detection catalog entries.
- Future improvements: additional synthetic scenarios, better tuning workflows, and richer detection visualization inspired by MITRE ATT&CK framework patterns.

## Resume bullets
- `docs/resume-bullets.md`

## License
This project is licensed under the MIT License. See `LICENSE`.
