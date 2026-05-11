# MITRE ATT&CK Coverage

Every detection in `backend/app/services/detection_catalog.py` is tagged with one or
more ATT&CK technique IDs and tactics. This table is the canonical mapping —
the dashboard's ATT&CK matrix view is generated from the same catalog.

| Detection key | Severity | Techniques | Tactics |
|---|---|---|---|
| `brute_force_login_rule` | high | T1110 | Credential Access |
| `unusual_login_hour_anomaly` | medium | T1078 | Initial Access, Persistence |
| `privilege_escalation_indicator` | critical | T1078, T1098 | Privilege Escalation, Persistence |
| `high_volume_failed_access_anomaly` | high | T1110, T1078 | Credential Access, Initial Access |
| `threat_intel_match_indicator` | critical | T1583, T1071 | Resource Development, Command and Control |
| `impossible_travel_login_anomaly` | high | T1078 | Initial Access, Defense Evasion |
| `abnormal_request_spike_rule` | medium | T1498 | Impact |
| `suspicious_ip_behavior_rule` | critical | T1078, T1110 | Initial Access, Credential Access |

## Severity scoring

Alert severity is computed from three inputs:

1. **Base severity** from the rule definition (low / medium / high / critical).
2. **Confidence** returned by the rule or anomaly scorer (0.0–1.0).
3. **Technique weight** — critical-impact techniques (T1098 privilege change,
   T1071 C2) bias the score upward.

Ties are broken by the most recent evidence event's `occurred_at`, so analysts always
see the freshest signal first.

## False-positive handling

- Per-rule **dedup window** (`dedup_window_minutes` in the catalog) suppresses repeat
  alerts on the same `correlation_entity` (e.g. source IP, username).
- Analysts can mark an alert `false_positive`; the audit trail records who, when, and
  the note.
- A simple **suppression rule** is planned (future work) to silence a `(rule, entity)`
  pair for a configurable window.

## Planned / future coverage

- T1059 (Command and Scripting Interpreter) — needs endpoint process telemetry beyond
  the current synthetic Sysmon events.
- T1486 (Data Encrypted for Impact / ransomware) — would require file-rename burst
  detection on file-server logs.
- T1567 (Exfiltration Over Web Service) — partial coverage today via volume anomaly;
  a dedicated rule is planned.
