from dataclasses import dataclass, field
from queue import Queue, Empty
from threading import Event
from typing import Any, Optional
import uuid


@dataclass
class ExecJob:
    code: str
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
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
