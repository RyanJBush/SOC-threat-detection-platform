"""Replay sample security logs into the Mercury ingestion API.

Reads JSON Lines or a JSON array of event objects matching the EventCreate schema,
posts them to /api/events/batch in chunks, and prints a per-batch summary.

Example:
    python scripts/ingest_logs.py data/sample_auth_logs.json \\
        --api http://localhost:8000 --token "$MERCURY_TOKEN"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib import error, request


def load_events(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if text.startswith("["):
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError(f"{path}: expected a JSON array of events")
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(f"{path}[{idx}]: expected a JSON object")
        return data
    events: list[dict[str, Any]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSON ({exc})") from exc
        if not isinstance(parsed, dict):
            raise ValueError(f"{path}:{line_no}: expected a JSON object per line")
        events.append(parsed)
    return events


def post_batch(api: str, token: str | None, events: list[dict[str, Any]]) -> dict[str, Any]:
    payload = json.dumps({"events": events}).encode("utf-8")
    req = request.Request(
        url=f"{api.rstrip('/')}/api/events/batch",
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} from {api}: {body}") from exc
    except error.URLError as exc:
        raise SystemExit(f"Cannot reach {api}: {exc.reason}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Replay sample logs into Mercury.")
    parser.add_argument("file", type=Path, help="JSON Lines or JSON array of events")
    parser.add_argument(
        "--api",
        default="http://localhost:8000",
        help="Base URL of the Mercury API (default: http://localhost:8000)",
    )
    parser.add_argument("--token", default=None, help="Bearer token for authenticated ingestion")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Events per POST /api/events/batch call (default: 50)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and validate the file without posting to the API",
    )
    args = parser.parse_args(argv)

    if not args.file.exists():
        print(f"error: file not found: {args.file}", file=sys.stderr)
        return 2

    events = load_events(args.file)
    print(f"Loaded {len(events)} event(s) from {args.file}")
    if args.dry_run or not events:
        return 0

    sent = 0
    for start in range(0, len(events), args.batch_size):
        chunk = events[start : start + args.batch_size]
        result = post_batch(args.api, args.token, chunk)
        sent += len(chunk)
        accepted = result.get("accepted", len(chunk))
        alerts = result.get("alerts_generated", "?")
        print(f"  batch {start // args.batch_size + 1}: accepted={accepted} alerts={alerts}")
    print(f"Done. Posted {sent} event(s) to {args.api}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
