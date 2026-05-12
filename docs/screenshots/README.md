# Screenshots

This directory holds portfolio screenshots referenced from the top-level
[`README.md`](../../README.md) and [`docs/DEMO_RUNBOOK.md`](../DEMO_RUNBOOK.md).

All captures should be from the running local stack against the **synthetic**
data shipped in `data/` — Mercury is a portfolio project, not a deployed SIEM.

## Recommended set

Capture these at 1440×900 (or larger) using the seeded `admin` user
(`admin / admin123`) after replaying `data/brute_force_scenario.json` via
`scripts/ingest_logs.py`:

| # | File | Captured | View | What it shows |
|---|---|---|---|---|
| 1 | `01-alerts-feed.png` | ✅ | `/alerts` (Alert feed) | Populated alert list with severity badges (Critical/High/Medium), Open status pills, confidence scores, and brute-force / privilege-escalation / threat-intel alerts visible |
| 2 | `02-incident-queue.png` | ✅ | `/incidents` (Case queue) | "Create Incident" panel plus Incident Queue with two cases — one **Investigating** brute-force incident and one **Closed** API-abuse incident — demonstrating status transitions |
| 3 | `03-mitre-attack-coverage.png` | ✅ | `/detections` → Detection Results | Scrolled to the **Detection Results** table on `/detections`, listing detection types whose underlying catalog entries map to MITRE techniques T1110, T1078, T1098, T1071, T1498, T1583. The catalog is also served raw at `GET /api/detections/catalog` (visible in screenshot #5). |
| 4 | `04-metrics-dashboard.png` | ✅ | `/dashboard` (Metrics) | KPI tiles (Total Events, Total Alerts, Critical Alerts, Active Incidents, Detection Coverage), MTTD/MTTR/FPR tiles, Alerts Over Time chart, Alerts by Severity pie, Alerts by Type bars, Alert Queue & Incident List |
| 5 | `05-api-swagger-docs.png` | ✅ | `http://localhost:8000/docs` | FastAPI Swagger UI listing the `health`, `auth`, `events` (and below the fold: `alerts`, `incidents`, `detections`, `jobs`, `platform`, `metrics`) route groups |

Optional / nice-to-haves:

- `06-alert-detail.png` ✅ — alert detail page for alert #11 (Abnormal Request Spike) showing MITRE technique tag (T1498), event breakdown, IP/User history, workflow actions, AI Assistant panel, an analyst note ("Triaged: source IP confirmed from threat-intel feed…"), and the alert timeline.
- `07-login.png` ✅ — login screen with username/password fields pre-populated for the demo `admin / admin123` user.
- `08-deferred-jobs.png` ✅ — Detections page top section showing the **Process Pending Jobs** action and the Detection Pipeline Jobs queue.

> Captured on 2026-05-12 against the local dev stack (FastAPI on `127.0.0.1:8801`, Vite frontend on `127.0.0.1:5184`) seeded with `data/brute_force_scenario.json`, `data/sample_auth_logs.json`, `data/sample_endpoint_logs.json`, `data/sample_network_logs.json`, plus the `brute_force_login_attack`, `suspicious_ip_access`, and `api_abuse_spike` scenarios via `/api/events/scenarios/{key}/seed`. No fabricated UI — every image is a Playwright capture of the running app.

## How to capture (macOS / Linux)

```bash
# 1. Start the stack
docker compose up --build

# 2. Open another shell and seed data
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
python scripts/ingest_logs.py data/brute_force_scenario.json --token "$TOKEN"
python scripts/ingest_logs.py data/sample_auth_logs.json --token "$TOKEN"

# 3. Log in to http://localhost:5173 as admin / admin123 and capture each view.
# 4. Save PNGs into this directory using the file names in the table above.
```

## Style guidelines

- **Format:** PNG, sRGB, ≤1 MB each where possible.
- **Naming:** lowercase, hyphen-separated, prefixed with the 2-digit order shown
  above. Keep names stable so the README links don't rot.
- **Privacy:** screenshots are from the synthetic dataset — no real customer
  data, no real IPs, no real user identities should ever appear here.
- **Annotations:** light text callouts in red (#dc2626) are fine; avoid
  blurring the actual UI.
- **Retina captures:** if exporting at 2× resolution, mention it in the
  filename suffix (e.g. `01-alerts-feed@2x.png`).

## Embedding in docs

Once captured, you can reference them from the top-level README, for example:

```markdown
![Alert feed](docs/screenshots/01-alerts-feed.png)
![Incident queue](docs/screenshots/02-incident-queue.png)
![MITRE ATT&CK coverage](docs/screenshots/03-mitre-attack-coverage.png)
![Metrics dashboard](docs/screenshots/04-metrics-dashboard.png)
![API docs](docs/screenshots/05-api-swagger-docs.png)
```

If a screenshot is intentionally absent (e.g., a view still in flux), keep its
row in the table above with a `_TODO_` marker rather than deleting it, so the
intended set stays visible.
