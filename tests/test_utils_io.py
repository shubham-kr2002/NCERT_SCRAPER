import json
from pathlib import Path

from ncert_scraper.utils.io import append_jsonl, read_json, write_json


def test_write_and_read_json(tmp_path: Path) -> None:
    path = tmp_path / "a" / "b.json"
    payload = {"ok": True}
    write_json(path, payload)
    assert read_json(path, default={}) == payload


def test_read_json_returns_default(tmp_path: Path) -> None:
    assert read_json(tmp_path / "missing.json", default={"x": 1}) == {"x": 1}


def test_append_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "x.jsonl"
    append_jsonl(path, {"id": 1})
    append_jsonl(path, {"id": 2})
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert json.loads(lines[0]) == {"id": 1}
    assert json.loads(lines[1]) == {"id": 2}

