from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
import json


_LOG_LOCK = Lock()
_LOG_FILE = Path(__file__).resolve().parent / 'fusion_bridge.log'


def _ts():
    return datetime.now(timezone.utc).isoformat()


def log_event(event, **data):
    payload = {
        'ts': _ts(),
        'event': event,
    }
    payload.update(data)

    line = json.dumps(payload, ensure_ascii=False)
    with _LOG_LOCK:
        with _LOG_FILE.open('a', encoding='utf-8') as handle:
            handle.write(line + '\n')


def read_recent_lines(limit=50):
    if not _LOG_FILE.exists():
        return []

    lines = _LOG_FILE.read_text(encoding='utf-8').splitlines()
    return lines[-limit:]
