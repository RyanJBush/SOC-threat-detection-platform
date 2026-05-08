![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-06B6D4?style=flat&logo=tailwindcss&logoColor=white)
![CI](https://github.com/RyanJBush/SOC-threat-detection-platform/actions/workflows/ci.yml/badge.svg)

# 🛡️ SOC Threat Detection Platform

> An AI-powered Security Operations Center platform that ingests security telemetry, applies rule-based and ML anomaly detections, and provides a full analyst triage workflow with incident management, AI-assisted summaries, and audit logging.

---

## 🎯 What I Built & Why

SOC analysts deal with enormous alert volumes and tight response SLAs. I built this platform to simulate the core workflow of a real SOC: telemetry ingestion → automated detection → analyst triage → incident management → post-incident review. Key design decisions:

- **Rule + anomaly detection pipeline** — combining signature-based detections with ML anomaly scoring mirrors how real SOC tools (Splunk, Elastic SIEM) operate
- **AI-assisted triage and summaries** — `GET /api/alerts/{id}/ai-summary` and `/ai-triage` endpoints simulate LLM-augmented analyst assistance, reducing mean time to respond (MTTR)
- **Full RBAC with 4 roles** — Admin, Analyst, Detection Engineer, and Viewer — reflecting realistic SOC team structures
- **Scenario seeding** — pre-built attack scenarios make the platform immediately demonstrable without needing real security data

---

## 📷 Features

- **Event ingestion & querying** — stream, replay, and scenario-based security telemetry
- **Automated alert generation** — detection pipeline triggers alerts on ingest with severity classification
- **Alert triage workflow** — status updates, analyst assignment, notes, timeline, and feedback
- **Incident management** — group alerts into incidents, track status, view AI wrap-up summaries
- **Detection catalog** — browsable registry of all active detection rules
- **Platform metrics** — KPIs, detection comparison, scenario benchmarks, and detection quality scoring
- **Feature flags & audit logs** — admin controls and full audit trail
- **CI/CD** — GitHub Actions pipeline for lint, tests, and build

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + SQLAlchemy + PostgreSQL |
| ML / Detection | pandas + scikit-learn |
| Auth | JWT with RBAC (4 roles) |
| Frontend | React + Vite + Tailwind CSS + Recharts |
| Infra | Docker Compose + GitHub Actions CI |

---

## 🚀 Quick Start

### Prerequisites
- Docker + Docker Compose
- Python 3.12+
- Node.js 20+

### Docker (Recommended)
```bash
docker compose up --build
# Frontend:         http://localhost:5173
# Backend API docs: http://localhost:8000/docs
```

### Local Development
```bash
make install
cp .env.example .env

# Terminal 1 — backend
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 — frontend
cd frontend && npm run dev
```

### Quality Checks
```bash
make lint && make test && make build
```

---

## 🗂️ Repository Structure

```
backend/    FastAPI API, detection pipeline, ML scoring, incident management, tests
frontend/   SOC analyst dashboard
docs/       Architecture, ports, style guide, deployment guide, demo runbook
```

---

## 👤 Demo Credentials

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | Admin |
| `analyst` | `analyst123` | Analyst |
| `deteng` | `deteng123` | Detection Engineer |
| `viewer` | `viewer123` | Viewer |

---

## 📷 Screenshot

![SOC Dashboard](https://github.com/user-attachments/assets/7695e968-457f-43a1-a8f3-56a7216791dd)

---

## 📝 Key Learnings

- Real SOC workflows are as much about process (triage, escalation, incident grouping) as they are about detection algorithms
- AI-assisted triage summaries significantly reduce cognitive load on analysts dealing with high alert volumes
- RBAC design requires thinking about information sensitivity as well as action permissions — a Viewer shouldn’t see the same alert detail as an Analyst

---

## 📄 License

MIT
