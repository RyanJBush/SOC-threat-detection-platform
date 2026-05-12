# Architecture — Mercury (Portfolio SOC Simulator)

Mercury is a monorepo built to demonstrate SOC detection-and-triage concepts with **synthetic logs only**.

## Scope boundary

- Portfolio simulator, not production SIEM.
- SOC-style workflow modeling, not real enterprise incident response.
- MITRE ATT&CK labels appear only on detections that are explicitly implemented.

## System overview

```text
Synthetic log files / seeded scenarios
        ↓
Ingestion API (/api/events, /api/events/batch)
        ↓
Detection service (rules + anomaly scoring)
        ↓
Alerts (status, notes, assignee, evidence)
        ↓
Incidents / case queue (grouped workflow)
        ↓
React dashboard for analyst-style triage
```

## Backend architecture (`backend/app`)

- **Routers**: auth, events, alerts, detections, incidents, metrics, jobs, platform, health.
- **Core services**:
  - `detection_service.py`: transforms events into detections/alerts.
  - `detection_catalog.py`: implemented detection definitions + ATT&CK tags.
  - `seed_scenarios.py`: synthetic scenario fixtures for repeatable demos.
- **Data model**: events, detections, alerts, incidents, investigation notes, audit logs, feature flags.

## Frontend architecture (`frontend/src`)

SOC-style pages:

- Alerts feed and alert detail
- Incident/case queue
- Detections catalog
- Events explorer
- Dashboard metrics

UI reflects generated demo data and allows workflow transitions (assignment, status, notes) for portfolio demonstration.

## Data model and flow

1. Synthetic events enter via API or replay CLI.
2. Detection engine evaluates rule/anomaly logic.
3. Alerts are created and mapped to implemented ATT&CK techniques.
4. Analyst-style triage updates alert state.
5. Related alerts can be grouped into incidents (case queue).

## MITRE ATT&CK mapping design

ATT&CK context is attached only where a detection definition includes mapping metadata.

- Source of truth: `backend/app/services/detection_catalog.py`
- Human-readable table: `docs/MITRE_MAPPING.md`

No generalized ATT&CK coverage claim should be made beyond that catalog.

## Non-goals

- Real-time enterprise ingestion pipelines (SIEM connectors, EDR, cloud control-plane feeds)
- Real SOC escalation/on-call automation
- Production-grade multi-tenant security guarantees
- Claims of operational incident response outcomes

## Why this architecture works for a portfolio

- End-to-end cybersecurity narrative (ingest → detect → triage → case).
- Clear separation of API, detection logic, and UI workflow.
- Reproducible demos with local synthetic datasets.
- Honest scope suitable for student/recruiter/interview discussion.
