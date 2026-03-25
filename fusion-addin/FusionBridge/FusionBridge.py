import sys
import traceback
from datetime import datetime
from pathlib import Path

import adsk.core

from logging_utils import log_event
from executor import Executor
from request_queue import RequestQueue
from bridge_server import BridgeServer

_BOOT_LOG_PATH = Path(__file__).resolve().parent / 'fusion_bridge_boot.log'
_ADDIN_DIR = str(Path(__file__).resolve().parent)
_APP = None
_UI = None
_QUEUE = None
_EXECUTOR = None
_SERVER = None
_RUNTIME = {
    'busy': False,
    'currentJobId': None,
    'startedAt': None,
}
_RUNTIME_LOG_PREFIX = 'stage4-server'

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

        # Debug-only request processing path: no timer/custom event yet
        _RUNTIME['startedAt'] = datetime.utcnow().isoformat()
        _SERVER = BridgeServer(_QUEUE, _RUNTIME, host='127.0.0.1', port=8765)
        _SERVER.start()
        _boot_log('bridge_server started on 127.0.0.1:8765')
        log_event('debug_stage4_server_started', host='127.0.0.1', port=8765)

        if _UI:
            _safe_message_box('FusionBridge {} gestartet (Server aktiv)'.format(_RUNTIME_LOG_PREFIX))
            _boot_log('popup shown')

    except Exception:
        _boot_log('run() crashed')
        _boot_log(traceback.format_exc())
        _safe_message_box('FusionBridge {} Fehler:\n{}'.format(_RUNTIME_LOG_PREFIX, traceback.format_exc()))


def stop(context):
    global _SERVER, _EXECUTOR, _QUEUE

    try:
        if _SERVER:
            _SERVER.stop()
            _boot_log('server stopped')
            log_event('debug_stage4_server_stopped')
        _SERVER = None
        _EXECUTOR = None
        _QUEUE = None
    except Exception:
        _boot_log('stop() exception:\n{}'.format(traceback.format_exc()))
    _boot_log('stop() called')
