import sys
import traceback
from datetime import datetime
from pathlib import Path

import adsk.core

from executor import Executor
from logging_utils import log_event
from request_queue import RequestQueue
from bridge_server import BridgeServer
from runtime_pump import RuntimePump

_BOOT_LOG_PATH = Path(__file__).resolve().parent / 'fusion_bridge_boot.log'
_ADDIN_DIR = str(Path(__file__).resolve().parent)
_APP = None
_UI = None
_QUEUE = None
_EXECUTOR = None
_SERVER = None
_PUMP = None
_RUNTIME = {
    'busy': False,
    'currentJobId': None,
    'startedAt': None,
    'pumpMode': None,
}
_RUNTIME_LOG_PREFIX = 'stage5-full'

if _ADDIN_DIR not in sys.path:
    sys.path.insert(0, _ADDIN_DIR)


def _boot_log(message):
    try:
        with _BOOT_LOG_PATH.open('a', encoding='utf-8') as handle:
            handle.write('[{}] {}\n'.format(datetime.utcnow().isoformat(), message))
    except Exception:
        pass


def _safe_message_box(text):
    if _UI:
        try:
            _UI.messageBox(text)
        except Exception:
            pass


def process_pending_jobs():
    global _QUEUE, _EXECUTOR, _RUNTIME

    if _QUEUE is None or _EXECUTOR is None:
        return

    while True:
        job = _QUEUE.get_nowait()
        if job is None:
            return

        job.started_at = datetime.utcnow().timestamp()
        _RUNTIME['busy'] = True
        _RUNTIME['currentJobId'] = job.job_id
        log_event('job_started', jobId=job.job_id)

        try:
            job.response = _EXECUTOR.execute(job.code, job_id=job.job_id)
        finally:
            job.finished_at = datetime.utcnow().timestamp()
            _RUNTIME['busy'] = False
            _RUNTIME['currentJobId'] = None
            job.done.set()
            log_event(
                'job_finished',
                jobId=job.job_id,
                durationMs=int((job.finished_at - job.started_at) * 1000) if job.started_at else None,
            )


def _start_runtime_pump():
    global _PUMP, _RUNTIME

    _PUMP = RuntimePump(_APP, process_pending_jobs, interval_ms=250)
    try:
        _PUMP.start()
    except Exception:
        log_event('runtime_pump_custom_start_failed', error=traceback.format_exc())
        _PUMP.start_timer_fallback()

    _RUNTIME['pumpMode'] = _PUMP.mode
    log_event('runtime_pump_mode', mode=_RUNTIME['pumpMode'])


def run(context):
    global _APP, _UI, _QUEUE, _EXECUTOR, _SERVER

    _boot_log('run() entered')
    _boot_log('version: {}'.format(_RUNTIME_LOG_PREFIX))
    _boot_log('context type: {}'.format(type(context).__name__))
    _boot_log('addin_dir: {}'.format(_ADDIN_DIR))
    _boot_log('sys.path has addin dir: {}'.format(_ADDIN_DIR in sys.path))

    try:
        _APP = adsk.core.Application.get()
        _boot_log('app acquired: {}'.format(_APP is not None))
        if not _APP:
            return

        _UI = _APP.userInterface
        _boot_log('ui acquired: {}'.format(_UI is not None))

        _QUEUE = RequestQueue()
        _EXECUTOR = Executor()
        _boot_log('queue+executor ready')

        _RUNTIME['startedAt'] = datetime.utcnow().isoformat()
        _SERVER = BridgeServer(_QUEUE, _RUNTIME, host='127.0.0.1', port=8765)
        _SERVER.start()
        _boot_log('bridge_server started on 127.0.0.1:8765')
        log_event('debug_stage5_server_started', host='127.0.0.1', port=8765)

        _start_runtime_pump()
        _boot_log('runtime pump mode: {}'.format(_RUNTIME.get('pumpMode')))

        if _UI:
            _safe_message_box('FusionBridge {} gestartet (Full runtime)'.format(_RUNTIME_LOG_PREFIX))
            _boot_log('popup shown')

    except Exception:
        _boot_log('run() crashed')
        _boot_log(traceback.format_exc())
        _safe_message_box('FusionBridge {} Fehler:\n{}'.format(_RUNTIME_LOG_PREFIX, traceback.format_exc()))


def stop(context):
    global _SERVER, _EXECUTOR, _QUEUE, _PUMP

    try:
        if _PUMP:
            _PUMP.stop()
            _boot_log('runtime pump stopped')
            log_event('debug_stage5_pump_stopped', mode=_RUNTIME.get('pumpMode'))
        if _SERVER:
            _SERVER.stop()
            _boot_log('server stopped')
            log_event('debug_stage5_server_stopped')

        _SERVER = None
        _EXECUTOR = None
        _QUEUE = None
        _PUMP = None
    except Exception:
        _boot_log('stop() exception:\n{}'.format(traceback.format_exc()))
    _boot_log('stop() called')
