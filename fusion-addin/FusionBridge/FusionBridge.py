import sys
import traceback
from datetime import datetime
from pathlib import Path

import adsk.core

_BOOT_LOG_PATH = Path(__file__).resolve().parent / 'fusion_bridge_boot.log'
_ADDIN_DIR = str(Path(__file__).resolve().parent)
_BIND_HOST = '0.0.0.0'
_BIND_PORT = 8765
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
    'bindHost': _BIND_HOST,
    'bindPort': _BIND_PORT,
}
_RUNTIME_LOG_PREFIX = 'stage6-lan-bind'

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


def run(context):
    global _APP, _UI, _QUEUE, _EXECUTOR, _SERVER, _PUMP

    _boot_log('run() entered')
    _boot_log('version: {}'.format(_RUNTIME_LOG_PREFIX))
    _boot_log('context type: {}'.format(type(context).__name__))
    _boot_log('addin_dir: {}'.format(_ADDIN_DIR))
    _boot_log('sys.path has addin dir: {}'.format(_ADDIN_DIR in sys.path))
    _boot_log('bind target: {}:{}'.format(_BIND_HOST, _BIND_PORT))

    try:
        _APP = adsk.core.Application.get()
        _boot_log('app acquired: {}'.format(_APP is not None))
        if not _APP:
            return

        _UI = _APP.userInterface
        _boot_log('ui acquired: {}'.format(_UI is not None))

        if _UI:
            _safe_message_box('Bootstrap phase 1: app/ui ready')
            _boot_log('phase1 popup shown')
    except Exception:
        _boot_log('phase1 crashed')
        _boot_log(traceback.format_exc())
        _safe_message_box('FusionBridge {} phase1 crash:\n{}'.format(_RUNTIME_LOG_PREFIX, traceback.format_exc()))
        return

    try:
        from logging_utils import log_event
        from executor import Executor
        from request_queue import RequestQueue
        from bridge_server import BridgeServer
        _boot_log('core modules imported')
        log_event('debug_stage6_core_modules_imported')

        _QUEUE = RequestQueue()
        _EXECUTOR = Executor()
        _boot_log('queue+executor ready')

        _RUNTIME['startedAt'] = datetime.utcnow().isoformat()
        _SERVER = BridgeServer(_QUEUE, _RUNTIME, host=_BIND_HOST, port=_BIND_PORT)
        _SERVER.start()
        _boot_log('bridge_server started on {}:{}'.format(_BIND_HOST, _BIND_PORT))
        log_event('debug_stage6_server_started', host=_BIND_HOST, port=_BIND_PORT)
    except Exception:
        _boot_log('core init crashed')
        _boot_log(traceback.format_exc())
        _safe_message_box('FusionBridge {} core init error:\n{}'.format(_RUNTIME_LOG_PREFIX, traceback.format_exc()))
        return

    try:
        from runtime_pump import RuntimePump

        def process_pending_jobs():
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
                    log_event('job_finished', jobId=job.job_id, durationMs=int((job.finished_at - job.started_at) * 1000) if job.started_at else None)

        _PUMP = RuntimePump(_APP, process_pending_jobs, interval_ms=250)
        try:
            _PUMP.start()
            _boot_log('runtime pump start() ok')
        except Exception:
            log_event('runtime_pump_custom_start_failed', error=traceback.format_exc())
            _boot_log('runtime_pump.start() failed, trying fallback')
            try:
                _PUMP.start_timer_fallback()
            except Exception:
                log_event('runtime_pump_fallback_failed', error=traceback.format_exc())
                _boot_log('runtime pump fallback failed')
        _RUNTIME['pumpMode'] = _PUMP.mode if _PUMP else None
        log_event('runtime_pump_mode', mode=_RUNTIME['pumpMode'])
        _boot_log('runtime pump mode: {}'.format(_RUNTIME.get('pumpMode')))
    except Exception:
        _boot_log('runtime pump import/init crashed')
        _boot_log(traceback.format_exc())

    if _UI:
        _safe_message_box('FusionBridge {} gestartet auf {}:{}'.format(_RUNTIME_LOG_PREFIX, _BIND_HOST, _BIND_PORT))
        _boot_log('popup shown (phase final)')


def stop(context):
    global _SERVER, _EXECUTOR, _QUEUE, _PUMP

    try:
        from logging_utils import log_event

        if _PUMP:
            _PUMP.stop()
            _boot_log('runtime pump stopped')
            try:
                log_event('debug_stage6_pump_stopped', mode=_RUNTIME.get('pumpMode'))
            except Exception:
                pass

        if _SERVER:
            _SERVER.stop()
            _boot_log('server stopped')
            log_event('debug_stage6_server_stopped')

        _SERVER = None
        _EXECUTOR = None
        _QUEUE = None
        _PUMP = None
    except Exception:
        _boot_log('stop() exception:\n{}'.format(traceback.format_exc()))
    _boot_log('stop() called')
