"""Generate synthetic events for Mercury portfolio demos.

Output format: JSON array compatible with scripts/ingest_logs.py.
"""

from __future__ import annotations

import argparse
import json
import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

USERS = ["jdoe", "asmith", "mjones", "analyst1", "service_backup"]
HOSTS = ["ws-17", "ws-22", "db-01", "vpn-gw", "eng-laptop-04"]
IPS = ["10.0.4.12", "10.0.4.42", "172.16.1.5", "198.51.100.23", "203.0.113.9"]


def build_event(ts: datetime, idx: int) -> dict:
    user = random.choice(USERS)
    host = random.choice(HOSTS)
    src_ip = random.choice(IPS)
    outcome = "failure" if random.random() < 0.3 else "success"
    event_type = random.choice(["auth", "network", "endpoint"])

    return {
        "timestamp": ts.isoformat(),
        "source": f"synthetic-generator-{event_type}",
        "event_type": event_type,
        "severity": random.choice(["low", "medium", "high"]),
        "raw_event": {
            "event_id": f"synth-{idx:05d}",
            "user": user,
            "host": host,
            "src_ip": src_ip,
            "outcome": outcome,
            "action": random.choice(["login", "dns_query", "process_start", "privilege_change"]),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic Mercury demo logs.")
    parser.add_argument("--count", type=int, default=120, help="Number of events to generate")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/generated_synthetic_logs.json"),
        help="Output JSON file path",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()

    random.seed(args.seed)
    start = datetime.now(UTC) - timedelta(minutes=max(args.count // 2, 1))
    events = [build_event(start + timedelta(seconds=i * 30), i + 1) for i in range(args.count)]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(events, indent=2), encoding="utf-8")

    print(f"Wrote {len(events)} synthetic event(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
