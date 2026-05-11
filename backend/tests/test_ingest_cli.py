"""Smoke tests for scripts/ingest_logs.py."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "ingest_logs.py"
DATA_DIR = REPO_ROOT / "data"


def _load_module():
    spec = importlib.util.spec_from_file_location("ingest_logs", SCRIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["ingest_logs"] = module
    spec.loader.exec_module(module)
    return module


def test_load_events_jsonl_array_and_empty(tmp_path):
    mod = _load_module()

    jsonl = tmp_path / "a.jsonl"
    jsonl.write_text('{"event_type":"x","source":"s","message":"m"}\n', encoding="utf-8")
    assert mod.load_events(jsonl) == [{"event_type": "x", "source": "s", "message": "m"}]

    arr = tmp_path / "b.json"
    payload = [{"event_type": "y", "source": "s", "message": "m"}]
    arr.write_text(json.dumps(payload), encoding="utf-8")
    assert mod.load_events(arr) == payload

    empty = tmp_path / "c.json"
    empty.write_text("", encoding="utf-8")
    assert mod.load_events(empty) == []


def test_load_events_rejects_non_array_json(tmp_path):
    mod = _load_module()
    bad = tmp_path / "bad.json"
    bad.write_text('["not", "a", "dict"]', encoding="utf-8")
    with pytest.raises(ValueError):
        mod.load_events(bad)

    bad_line = tmp_path / "bad.jsonl"
    bad_line.write_text('"just a string"\n', encoding="utf-8")
    with pytest.raises(ValueError):
        mod.load_events(bad_line)


def test_sample_data_files_parse():
    mod = _load_module()
    for path in [
        DATA_DIR / "sample_auth_logs.json",
        DATA_DIR / "sample_network_logs.json",
        DATA_DIR / "sample_endpoint_logs.json",
        DATA_DIR / "brute_force_scenario.json",
    ]:
        events = mod.load_events(path)
        assert len(events) > 0, f"{path.name} should contain events"
        for evt in events:
            assert "event_type" in evt and "source" in evt and "message" in evt


def test_dry_run_does_not_call_api(tmp_path, capsys):
    mod = _load_module()
    sample = tmp_path / "s.jsonl"
    sample.write_text('{"event_type":"x","source":"s","message":"m"}\n', encoding="utf-8")
    rc = mod.main([str(sample), "--dry-run"])
    assert rc == 0
    captured = capsys.readouterr().out
    assert "Loaded 1 event" in captured
