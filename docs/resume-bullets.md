# Resume Bullets — Mercury (SOC Threat Detection Platform)

ATS-friendly, one-line bullets. Pick 2–4 based on the role (SOC Analyst, Security
Engineer, Detection Engineer, Threat Intel, etc.). Numbers reflect the seeded demo
dataset, not production traffic — keep "demo dataset" in your phrasing if asked.

## Top picks (most recruiter-friendly)

- Built **Mercury**, a Python/FastAPI SOC platform that ingests security logs, runs rule + ML anomaly detection, and maps alerts to **MITRE ATT&CK** techniques.
- Designed a multi-stage detection engine (8 rules + Isolation Forest anomaly scorer) that triages brute force, privilege escalation, impossible travel, and C2 beaconing on a synthetic log stream.
- Implemented a **case management** workflow (alert → investigation → resolved/false-positive) with analyst notes, severity scoring, and a SOC dashboard backed by React + FastAPI.
- Authored 130+ pytest cases covering ingestion, detection, RBAC, and metrics; wired ruff lint, bandit security scan, and mypy into a GitHub Actions CI pipeline.

## SOC analyst focus

- Modeled **alert severity scoring** combining detection confidence, MITRE technique weight, and asset context to reduce analyst alert fatigue on a synthetic 1k-event corpus.
- Built incident timeline and evidence views so analysts can pivot from an alert to the underlying events, source IPs, and MITRE technique context in one click.
- Implemented **false-positive handling**: analysts can tag alerts, suppress on a configurable window, and the dedup engine respects per-rule cooldowns.

## Detection / SIEM engineering focus

- Engineered a SIEM-style **log ingestion pipeline** (`POST /api/events`, batch, replay) accepting JSON Lines from authentication, network, and endpoint sources.
- Implemented an **Isolation Forest** anomaly scorer in scikit-learn that flags unusual login hours and high-volume failed-access bursts that signature rules miss.
- Mapped every detection to MITRE ATT&CK techniques (T1110, T1078, T1098, T1071, T1498, T1583) and tactics for coverage reporting in the dashboard's ATT&CK matrix.

## Software engineering focus

- Built a Dockerized monorepo (FastAPI + React + PostgreSQL) with RBAC (analyst / investigator / admin), JWT auth, audit logging, and feature flags.
- Achieved ~130 passing pytest tests with shared fixtures, an SQLite test database, and CI gated on lint + tests + security scan.
- Added a CLI replay tool (`scripts/ingest_logs.py`) that streams sample log batches through the API for reproducible detection demos.

## One-liner (single-bullet version)

- Built Mercury, a Python/FastAPI SOC platform with rule + ML threat detection, MITRE ATT&CK mapping, case management, and 130 passing tests in GitHub Actions CI.

## How to talk about it in an interview

- **Problem framing**: SOC analysts are overwhelmed by raw alerts. The project explores noise reduction (dedup + confidence + MITRE context) end-to-end.
- **Scope honesty**: It's a portfolio project, not a deployed SIEM. Data is synthetic and the ML model is trained on seeded events — say so.
- **What you'd do next**: streaming ingestion (Kafka), real threat-intel feeds (MISP/AlienVault OTX), and tuning detections against a public dataset (e.g., MITRE CALDERA or HELK).
