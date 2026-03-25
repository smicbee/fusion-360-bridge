from dataclasses import dataclass, field
from queue import Queue, Empty
from threading import Event
from typing import Any, Optional
import time
import uuid


@dataclass
class ExecJob:
    code: str
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    done: Event = field(default_factory=Event)
    response: Optional[dict[str, Any]] = None


class RequestQueue:
    def __init__(self):
        self._queue: Queue[ExecJob] = Queue()

    def put(self, job: ExecJob) -> None:
        self._queue.put(job)

    def get_nowait(self) -> Optional[ExecJob]:
        try:
            return self._queue.get_nowait()
        except Empty:
            return None

    def size(self) -> int:
        return self._queue.qsize()
