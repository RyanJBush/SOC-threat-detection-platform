# Resume Bullets — Mercury (SOC Threat Detection Platform)

Use these for student/recent-grad cybersecurity resumes. Keep scope honest: **synthetic logs, portfolio SOC workflow simulator, not production SIEM**.

## Core bullets

- Built **Mercury**, a FastAPI + React SOC threat detection portfolio platform that replays synthetic security events and models alert triage plus case queue workflows.
- Implemented detection logic for synthetic auth/network/endpoint events and surfaced generated alerts with severity, confidence, and evidence context.
- Added SOC-style alert lifecycle operations (status transitions, assignment, notes, feedback) and incident grouping to demonstrate analyst workflow design.
- Mapped implemented detections to MITRE ATT&CK techniques/tactics in a catalog-backed structure exposed via API and UI.
- Authored clear architecture, API, runbook, and screenshot documentation to make the project recruiter/interviewer friendly and reproducible.

## Detection-engineering angle

- Designed a detection catalog with explicit metadata (severity, confidence, dedup window, ATT&CK mapping where implemented) to keep rule behavior explainable.
- Demonstrated replay-based validation by ingesting synthetic scenario files and reviewing downstream alert output for tuning.

## SOC analyst angle

- Built alert investigation flows that mirror analyst queue operations without implying real enterprise incident response execution.
- Used analyst feedback states (true/false positive) to support learning-focused detection quality review on demo datasets.

## One-line version

- Created a cybersecurity portfolio project that simulates SOC detection and case management workflows on synthetic logs using FastAPI, React, and ATT&CK mapping for implemented detections.
