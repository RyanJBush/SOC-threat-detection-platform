![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![CI](https://github.com/RyanJBush/SOC-threat-detection-platform/actions/workflows/ci.yml/badge.svg)

# Mercury

**SOC Threat Detection & Security Operations Platform**

[**🔗 View Live Preview →**](https://www.perplexity.ai/computer/a/mercury-preview-project-5-of-9-lCA5DWRgQoa4AN6VYPXAUQ)

> A production-style Security Operations Center (SOC) threat detection platform that ingests security logs, scores events with a multi-stage ML pipeline, maps findings to MITRE ATT&CK, and surfaces threats in a live analyst dashboard.

---

## 🎯 What I Built & Why

SOC analysts are drowning in alerts. I built Mercury to practice the full threat detection lifecycle — from raw log ingestion to enriched, prioritized threat cases — with a focus on the two biggest pain points: noise reduction and context enrichment.

- **Multi-stage detection** — rule-based fast-path for known signatures combined with ML anomaly scoring for novel threats, minimizing both false positives and missed detections
- **MITRE ATT&CK mapping** — every detected threat is tagged with technique and tactic IDs, giving analysts immediate context for prioritization and escalation
- **Case management workflow** — alerts are grouped into cases with status lifecycle (new → investigating → resolved), analyst notes, and escalation tracking
- **Synthetic log generation** — realistic event streams (lateral movement, privilege escalation, C2 beaconing, data exfil) for fully reproducible demos

---

## 🏗️ Architecture

```mermaid
flowchart TD
    subgraph Ingestion["Log Ingestion"]
        SYSLOG["Syslog / CEF / JSON"]
        SYNTH["Synthetic Log\nGenerator"]
    end

    subgraph API["FastAPI Backend"]
        R_INGEST["ingest router\n/api/events"]
        R_ALERTS["alerts router\n/api/alerts"]
        R_CASES["cases router\n/api/cases"]
        R_MITRE["mitre router\n/api/mitre"]
        R_RULES["rules router\n/api/rules"]
        R_METRICS["metrics router\n/api/metrics"]
        R_AUTH["auth router"]
    end

    subgraph Detection["Detection Engine"]
        RULES_ENGINE["Signature\nRule Engine"]
        ML_SCORE["ML Anomaly\nScorer (Isolation Forest)"]
        MITRE_MAP["MITRE ATT&CK\nTagger"]
        ENRICHER["Event\nEnricher"]
    end

    subgraph Data["Data Layer"]
        PG[("PostgreSQL\nEvents · Alerts · Cases · Audit")]
    end

    subgraph UI["SOC Dashboard"]
        DASH["React + TypeScript\nAlert Feed · Case Queue · ATT&CK Matrix"]
    end

    SYSLOG & SYNTH --> R_INGEST
    R_INGEST --> RULES_ENGINE & ML_SCORE
    RULES_ENGINE & ML_SCORE --> ENRICHER
    ENRICHER --> MITRE_MAP
    MITRE_MAP --> R_ALERTS
    R_ALERTS --> R_CASES
    R_INGEST & R_ALERTS & R_CASES --> PG
    DASH -->|"JWT"| R_AUTH
    DASH --> R_ALERTS & R_CASES & R_MITRE & R_METRICS
```

---

## 📷 Features

- **Multi-stage detection** — signature rules + Isolation Forest ML anomaly scoring
- **MITRE ATT&CK mapping** — technique and tactic tagging on every detected threat
- **Case management** — alert grouping, status workflow, analyst notes, escalation tracking
- **Synthetic log generation** — lateral movement, privilege escalation, C2 beaconing, data exfil scenarios
- **Live SOC dashboard** — alert feed, case queue, and ATT&CK matrix heatmap
- **RBAC** — SOC Analyst, Tier 2 Investigator, and Admin roles
- **Docker Compose** — one-command local stack

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + SQLAlchemy + PostgreSQL |
| ML / Detection | scikit-learn (Isolation Forest) + rule engine |
| Threat Intel | MITRE ATT&CK framework mapping |
| Frontend | React + Vite + TypeScript |
| Infra | Docker Compose + GitHub Actions CI |

---

## 🚀 Quick Start

```bash
docker compose up --build
# Backend API docs: http://localhost:8000/docs
# Frontend:         http://localhost:5173
```

### Local Development
```bash
cd backend && pip install -e .[dev]
uvicorn app.main:app --reload

cd frontend && npm ci && npm run dev
```

### Quality Checks
```bash
make lint && make test
```

---

## 🗂️ Repository Structure

```
backend/    FastAPI API, detection engine, MITRE mapping, case management, tests
frontend/   React SOC dashboard
docs/       Architecture, demo runbook, API reference
```

---

## 📝 Key Learnings

- Combining rule-based signatures with ML anomaly detection reduces alert fatigue while maintaining coverage for novel threats
- MITRE ATT&CK mapping transforms raw detections into analyst-readable context — the difference between "anomaly detected" and "lateral movement via T1021"
- Case management is the bridge between detection and resolution; without it, alerts just pile up

---

## 📄 License

MIT
