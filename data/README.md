# Sample Security Logs

Synthetic security telemetry used for demos, tests, and reproducible detection runs.
None of these events represent real users, hosts, or IPs.

## Files

| File | Format | Purpose |
|---|---|---|
| `sample_auth_logs.json` | JSON Lines | Authentication events (logins, failures, MFA) |
| `sample_network_logs.json` | JSON Lines | Network telemetry (connections, DNS, beaconing) |
| `sample_endpoint_logs.json` | JSON Lines | Endpoint process / privilege-change events |
| `brute_force_scenario.json` | JSON array | Reproducible brute-force burst for the detection demo |

## Replaying through the API

```bash
python scripts/ingest_logs.py data/sample_auth_logs.json \
  --api http://localhost:8000 --token "$MERCURY_TOKEN"
```

See `docs/api.md` for the full ingestion contract.
