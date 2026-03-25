from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any
import json


_LOG_LOCK = Lock()
_LOG_FILE = Path(__file__).resolve().parent / 'fusion_bridge.log'


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_event(event: str, **data: Any) -> None:
    payload = {
        'ts': _ts(),
        'event': event,
        **data,
    }

    line = json.dumps(payload, ensure_ascii=False)
    with _LOG_LOCK:
        with _LOG_FILE.open('a', encoding='utf-8') as handle:
            handle.write(line + '\n')


def read_recent_lines(limit: int = 50) -> list[str]:
    if not _LOG_FILE.exists():
        return []

    lines = _LOG_FILE.read_text(encoding='utf-8').splitlines()
    return lines[-limit:]
