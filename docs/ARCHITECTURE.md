# Architecture

Mercury is a monorepo with a FastAPI backend, a React + Vite frontend, and a
synthetic-data ingestion path. It is structured to look like a small SOC platform
but runs entirely on synthetic data — see **Scope & non-goals** below.

## High-level layout

```
backend/    FastAPI app, detection engine, MITRE catalog, tests
frontend/   React 19 + Vite SOC dashboard (JSX, Tailwind, Recharts)
data/       Synthetic JSON / JSON-Lines log fixtures
scripts/    ingest_logs.py — replay CLI for /api/events/batch
docs/       Architecture, API, MITRE mapping, demo runbook, resume bullets
```

## Backend layout (`backend/app/`)

| Module | Responsibility |
|---|---|
| `main.py` | FastAPI app factory; wires routers, CORS, observability middleware, and the startup `seed_demo_data` call |
| `config.py` | Pydantic settings (`VANGUARD_*` env vars: DB URL, JWT secret, alg, expiry) |
| `db.py` | SQLAlchemy engine/session; defaults to `sqlite:///./vanguard_ai.db` |
| `models.py` | ORM models: `User`, `Event`, `Detection`, `Alert`, `Incident`, `InvestigationNote`, audit/feature-flag tables |
| `schemas.py` | Pydantic v2 request/response models |
| `security.py` | Password hashing (bcrypt), JWT issue/decode |
| `dependencies.py` | Auth dependency, current-user / role guards |
| `observability.py` | Structured logging filter + request-tracing middleware |
| `routers/` | FastAPI routers (one per resource) |
| `services/` | Detection engine, catalog, seed data, audit, feature flags, AI assistant, pagination, job runner |

### Routers (verified against `backend/app/routers/`)

| Router | Prefix | Notable routes |
|---|---|---|
| `auth` | `/api/auth` | `POST /login`, `GET /me`, `GET /analysts` |
| `events` | `/api/events` | `POST /`, `POST /batch`, `POST /stream`, `POST /replay`, `POST /scenarios/{key}/seed`, `POST /simulations/run`, `GET /scenarios`, `GET /{event_id}` |
| `alerts` | `/api/alerts` | `GET /`, `GET /{id}`, `PATCH /{id}/status`, `PATCH /{id}/assign`, notes / timeline / feedback / `ai-summary` / `ai-triage` |
| `detections` | `/api/detections` | `GET /`, `GET /catalog` |
| `incidents` | `/api/incidents` | `GET`/`POST /`, `GET /{id}`, `PATCH /{id}/status`, `POST /{id}/alerts`, `GET /{id}/timeline`, `GET /{id}/ai-wrapup` |
| `jobs` | `/api/jobs` | `GET /`, `POST /process-pending` |
| `metrics` | `/api/metrics` | `GET /summary`, `/kpis`, `/detection-comparison`, `/jobs`, `/detection-quality`, `/scenario-benchmarks`, `/correlation-hotspots` |
| `platform` | `/api/platform` | `GET /feature-flags`, `PATCH /feature-flags/{key}`, `GET /audit-logs` |
| `health` | (root) | `GET /health`, `GET /ready`, `GET /health/dependencies` |

## Detection pipeline

```
Ingested Event
   │
   ▼
┌─────────────────────────────────────────────────────────────┐
│  detection_service.py                                       │
│   ├─ Rule signals  (catalog-driven, deterministic)          │
│   └─ Anomaly signals (sklearn IsolationForest on rolling    │
│                       windows of recent events)             │
└─────────────────────────────────────────────────────────────┘
   │  emits DetectionSignal:
   │   { name, severity, confidence, mitre_techniques,
   │     recommendation, dedup_window_minutes,
   │     correlation_entity, detection_method, evidence }
   ▼
Per-rule dedup on (rule_key, correlation_entity, window)
   │
   ▼
Alert  →  attached to Incident (case) via /api/incidents
   │
   ▼
Investigation lifecycle:
   open → investigating → resolved | false_positive
   + analyst notes, timeline entries, true/false-positive feedback
```

### Catalog-driven detections (`services/detection_catalog.py`)

8 frozen `DetectionDefinition` entries, each carrying severity, default
confidence, MITRE techniques, MITRE tactics, recommendation, and a per-rule
dedup window. The same catalog drives the API's `/api/detections/catalog`
response and the MITRE coverage table in `docs/MITRE_MAPPING.md`.

### Anomaly model

`scikit-learn` `IsolationForest` is fit on rolling event windows during scoring
(not a long-lived trained artifact). This is appropriate for a portfolio demo
but is **not** a production ML lifecycle.

### Deferred / batch processing

`POST /api/events/batch` accepts a `defer_detection` flag. Deferred events queue
detection jobs that are later processed via `POST /api/jobs/process-pending`,
allowing demos of back-pressure and bulk processing.

## Frontend layout (`frontend/src/`)

| Path | Purpose |
|---|---|
| `App.jsx` | Router with protected-route wrapper |
| `pages/LoginPage.jsx` | JWT login form |
| `pages/DashboardPage.jsx` | KPIs, detection quality, correlation hotspots (Recharts) |
| `pages/AlertsPage.jsx` | Alert feed with filters |
| `pages/AlertDetailPage.jsx` | Alert detail with MITRE technique tags, evidence, notes, AI summary/triage |
| `pages/IncidentsPage.jsx` | Incident (case) queue and status management |
| `pages/DetectionsPage.jsx` | Detection catalog + deferred-job runner |
| `pages/EventsPage.jsx` | Raw event browse + scenario seeding |
| `pages/SettingsPage.jsx` | Feature flags / platform settings |
| `services/api.js` | Fetch wrapper for the FastAPI backend |
| `components/Layout.jsx`, `StatusBadge.jsx` | Shared UI |

> The UI currently shows MITRE tags **per alert** and ATT&CK-tactic counts in the
> dashboard's metrics views. A full ATT&CK technique × tactic matrix heatmap UI
> is on the roadmap (see README → Limitations & Future Work).

## Data layer

- **Default:** SQLite file (`vanguard_ai.db`), created on startup.
- **Docker Compose:** PostgreSQL 16 (`postgres:16`) on port 5432; DB `vanguard_ai`.
- **Schema:** Users, Organizations, Events, Detections, Alerts, Incidents,
  InvestigationNotes, AuditLogs, FeatureFlags, DetectionJobs.

## Auth & RBAC

- JWT (HS256), issued by `POST /api/auth/login`, decoded in `dependencies.py`.
- Roles seeded on first boot: `admin`, `analyst`, `deteng`, `viewer`
  (see `services/seed.py`).
- Role gating is enforced per-route; audit log records sensitive mutations.

## Observability

- `observability.configure_logging()` installs a structured JSON-friendly format.
- `request_tracing_middleware` injects a request ID, latency, and route into
  each log line.
- No external APM today (planned: OpenTelemetry export).

## CI

`.github/workflows/ci.yml`:

- **Backend job:** ruff, bandit, mypy (non-blocking), pytest.
- **Frontend job:** `npm ci`, `npm run lint`, `npm run build`.

## Scope & non-goals

Mercury is a **portfolio / interview demonstration** project.

- It runs on synthetic logs (`data/*.json` + seeded scenarios). It does not
  ingest real enterprise telemetry, EDR streams, or SaaS audit logs.
- It is not a deployed SIEM and should not be used to monitor a real production
  environment.
- The Isolation Forest is fit on the fly; there is no model registry or drift
  monitoring.
- Multi-tenant isolation is not hardened, even though the schema models orgs.
- Secrets in `.env.example` / `docker-compose.yml` are demo defaults.

See the README's **Limitations & Future Work** table for the planned trajectory.
