# Resume Bullets — Mercury (SOC Threat Detection Platform)

ATS-friendly, one-line bullets grounded in the actual repo
(`backend/app/`, `frontend/src/`, `data/`, `scripts/`). Pick 2–4 based on the
role (SOC Analyst, Security Engineer, Detection Engineer, Threat Intel, full
stack, etc.).

> **Scope honesty:** numbers reflect the synthetic demo dataset and seeded
> scenarios in `data/` + `backend/app/services/seed_scenarios.py`, not
> production traffic. Mercury is a portfolio project, not a deployed SIEM.
> Keep "portfolio project" or "demo dataset" in your phrasing if asked.

## Top picks (5–8, recruiter-friendly)

- Built **Mercury**, a Python / FastAPI **SOC threat-detection portfolio platform** with a hybrid rule + ML detection engine, **MITRE ATT&CK** mapping, and a React 19 + Vite analyst dashboard.
- Designed an **8-detection catalog** (signature rules + Isolation-Forest anomaly scorers) covering brute force (T1110), privilege escalation (T1098), impossible-travel logins, C2 indicators (T1071), and request-volume spikes (T1498) on synthetic auth / network / endpoint logs.
- Modelled the full SOC workflow — event → detection (with per-rule **dedup window** + **correlation entity**) → alert → incident (case) → analyst note → true/false-positive feedback — and exposed it across **9 FastAPI routers**.
- Shipped a **React 19 + Vite** SOC dashboard (Tailwind, Recharts) with login, alert feed, alert investigation, incident queue, detections catalog, raw events, and KPI / metrics views over JWT-authenticated REST APIs.
- Implemented **RBAC** across four roles (admin, analyst, detection engineer, viewer), JWT auth, audit logging, and runtime feature-flag toggles via a dedicated platform router.
- Authored **63 pytest tests** across 8 modules (ingestion, detection engine, RBAC, services, ingest CLI) gated on **ruff + bandit + mypy + pytest** in GitHub Actions CI; added a frontend lint + build CI job.
- Packaged the stack with **Docker Compose** (PostgreSQL 16 + FastAPI + Vite) and a `scripts/ingest_logs.py` CLI that replays synthetic log batches through `/api/events/batch` for reproducible detection demos.
- Documented architecture, API contract, MITRE coverage, demo runbook, and limitations under `docs/` to support recruiter / interviewer review (`docs/ARCHITECTURE.md`, `docs/api.md`, `docs/DEMO_RUNBOOK.md`, `docs/MITRE_MAPPING.md`).

## SOC analyst focus

- Modelled **alert severity scoring** combining detection confidence, MITRE technique weight, and per-rule dedup windows to reduce analyst alert fatigue on a synthetic 1k-event corpus.
- Built **alert investigation views** (status workflow, analyst assignment, notes, timeline, evidence events) so analysts can pivot from an alert into source IPs, usernames, and MITRE technique context in one click.
- Implemented **true / false-positive feedback** endpoints feeding a `detection-quality` metrics view, demonstrating a loop from analyst decision back into detection-quality reporting.

## Detection / SIEM engineering focus

- Engineered a SIEM-style **log ingestion API** (`POST /api/events`, `/batch`, `/stream`, `/replay`) plus scenario seeding (`/api/events/scenarios/{key}/seed`) for fully reproducible detection runs.
- Implemented an **Isolation-Forest anomaly scorer** in scikit-learn alongside deterministic signature rules; both methods emit a unified `DetectionSignal` schema with dedup window and correlation entity.
- Mapped every detection to MITRE ATT&CK techniques (T1110, T1078, T1098, T1071, T1498, T1583) and tactics; exposed the catalog via `/api/detections/catalog` to drive the frontend and `docs/MITRE_MAPPING.md`.

## Software / platform engineering focus

- Built a Dockerized monorepo (FastAPI + React + PostgreSQL) with **JWT** auth, **RBAC**, **audit logging**, **feature flags**, and structured request-tracing middleware.
- Designed deferred / batch ingestion: `POST /api/events/batch` queues jobs (`defer_detection=true`) processed via `POST /api/jobs/process-pending`, demonstrating back-pressure handling.
- Achieved **63 passing pytest tests** with shared fixtures and an SQLite test DB; CI gated on ruff, bandit, mypy, pytest, and a frontend lint + build job.

## One-liner (single-bullet version)

- Built **Mercury**, a Python / FastAPI SOC threat-detection portfolio platform with hybrid rule + Isolation-Forest detection, MITRE ATT&CK mapping, incident workflow, a React 19 dashboard, and 63 pytest tests in GitHub Actions CI.

## How to talk about it in an interview

- **Problem framing:** SOC analysts are overwhelmed by raw alerts. Mercury explores **noise reduction** (per-rule dedup, correlation entities, confidence scoring) and **context enrichment** (MITRE technique + recommendation per alert) end-to-end.
- **Scope honesty:** It's a portfolio project running on synthetic data, not a deployed SIEM. The Isolation Forest is fit on rolling event windows at scoring time — there's no model registry or drift monitoring.
- **What I'd do next:** streaming ingestion (Kafka / Redis Streams), real threat-intel feeds (MISP / AlienVault OTX), proper ML lifecycle, multi-tenant isolation, and a true ATT&CK technique × tactic matrix heatmap UI.
- **Trade-offs I'd defend:** catalog-driven rules (frozen dataclasses) for simplicity vs. a DSL; SQLite default for fast local demos with Postgres in Compose for prod-shape behaviour; deferring detection vs. inline scoring (back-pressure vs. latency).
