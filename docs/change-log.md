# Mercury Change Log

## 2026-05-12 — Portfolio honesty and documentation pass

### Disclaimers and honesty fixes
- Added top-level disclaimer language in README and preview content: synthetic logs only, not a production SIEM.
- Replaced marketing-heavy phrasing with portfolio-demo wording across updated docs.
- Kept ATT&CK references scoped to implemented mapping fields and detection metadata.

### Synthetic log clarity
- Documented synthetic replay workflow with explicit ingest steps and dataset references.
- Added `scripts/generate_synthetic_logs.py` to create reproducible synthetic event files for local demos.
- Added `make replay-bruteforce` and `make generate-synth` to simplify repeatable demo runs.

### Preview and documentation improvements
- Reworked `docs/preview/index.html` with a cohesive dark SOC aesthetic and a clear ingest → parse → detect → visualize pipeline.
- Updated screenshot docs with synthetic-data reminders and a recapture checklist.
- Refined resume bullets for concrete, project-specific wording aligned with existing code behavior.
