import time
import traceback

import adsk.core

from bridge_server import BridgeServer
from executor import Executor
from logging_utils import log_event
from request_queue import RequestQueue
from runtime_pump import RuntimePump

_app = None
_ui = None
_queue = None
_server = None
_executor = None
_pump = None
_runtime = {
    'busy': False,
    'currentJobId': None,
    'startedAt': None,
    'pumpMode': None,
}


def process_pending_jobs():
    global _queue, _executor, _runtime

    if _queue is None or _executor is None:
        return

    job = _queue.get_nowait()
    if job is None:
        return

    job.started_at = time.time()
    _runtime['busy'] = True
    _runtime['currentJobId'] = job.job_id
    log_event('job_started', jobId=job.job_id)

    try:
        job.response = _executor.execute(job.code, job_id=job.job_id)
    finally:
        job.finished_at = time.time()
        _runtime['busy'] = False
        _runtime['currentJobId'] = None
        job.done.set()
        log_event(
            'job_finished',
            jobId=job.job_id,
            durationMs=int((job.finished_at - job.started_at) * 1000) if job.started_at else None,
        )


def _start_runtime_pump():
    global _app, _pump, _runtime

    try:
        _pump = RuntimePump(_app, process_pending_jobs, interval_ms=250)
        _pump.start()
        _runtime['pumpMode'] = _pump.mode
        return
    except Exception:
        log_event('runtime_pump_custom_start_failed', error=traceback.format_exc())

    _pump = RuntimePump(_app, process_pending_jobs, interval_ms=250)
    _pump.start_timer_fallback()
    _runtime['pumpMode'] = _pump.mode


def run(context):
    global _app, _ui, _queue, _server, _executor, _runtime

    _app = adsk.core.Application.get()
    _ui = _app.userInterface

    try:
        _queue = RequestQueue()
        _executor = Executor()
        _runtime['startedAt'] = time.time()
        _server = BridgeServer(_queue, _runtime, host='127.0.0.1', port=8765)
        _server.start()
        _start_runtime_pump()

        log_event('addin_started', pumpMode=_runtime['pumpMode'])
        _ui.messageBox('FusionBridge gestartet auf http://127.0.0.1:8765')
    except Exception:
        log_event('addin_start_failed', error=traceback.format_exc())
        if _ui:
            _ui.messageBox('FusionBridge Startfehler:\n{}'.format(traceback.format_exc()))


def stop(context):
    global _server, _pump

    try:
        if _pump:
            _pump.stop()
            _pump = None

        if _server:
            _server.stop()
            _server = None

        log_event('addin_stopped')
    except Exception:
        log_event('addin_stop_failed', error=traceback.format_exc())
        if _ui:
            _ui.messageBox('FusionBridge Stopfehler:\n{}'.format(traceback.format_exc()))
