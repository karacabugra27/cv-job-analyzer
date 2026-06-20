import json
import os
from pathlib import Path

HISTORY_FILE = Path(
    os.getenv(
        "HISTORY_FILE",
        str(Path(__file__).parent.parent / "analysis_history.json"),
    )
)


def _load_all() -> list[dict]:
    if not HISTORY_FILE.exists():
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_all(records: list[dict]) -> None:
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def list_records() -> list[dict]:
    return list(reversed(_load_all()))


def get_record(record_id: str) -> dict | None:
    for r in _load_all():
        if r["id"] == record_id:
            return r
    return None


def save_record(record: dict) -> None:
    records = _load_all()
    records.append(record)
    _write_all(records)


def delete_record(record_id: str) -> bool:
    records = _load_all()
    new_records = [r for r in records if r["id"] != record_id]
    if len(new_records) == len(records):
        return False
    _write_all(new_records)
    return True
