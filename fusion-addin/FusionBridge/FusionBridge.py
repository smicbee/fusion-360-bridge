import traceback
from pathlib import Path

import adsk.core

from executor import Executor
from logging_utils import log_event

_BOOT_LOG_PATH = Path(__file__).resolve().parent / 'fusion_bridge_boot.log'
_APP = None
_UI = None
_EXECUTOR = None


def _boot_log(message):
    try:
        with _BOOT_LOG_PATH.open('a', encoding='utf-8') as handle:
            handle.write(message + '\n')
    except Exception:
        pass


def run(context):
    global _APP, _UI, _EXECUTOR

    _boot_log('run() entered')
    _boot_log('context type: {}'.format(type(context).__name__))

    try:
        _APP = adsk.core.Application.get()
        _boot_log('app acquired: {}'.format(_APP is not None))
        if not _APP:
            return

        _UI = _APP.userInterface
        _boot_log('ui acquired: {}'.format(_UI is not None))

        log_event('debug_stage3_before_executor')
        _boot_log('logging_utils imported and log_event callable')

        _EXECUTOR = Executor()
        _boot_log('executor instantiated successfully')
        log_event('debug_stage3_executor_ready')

        if _UI:
            _UI.messageBox('FusionBridge Debug-Stufe 3: Executor initialisiert')
            _boot_log('popup shown')
        else:
            _boot_log('ui missing, popup skipped')
    except Exception:
        error = traceback.format_exc()
        _boot_log('run() crashed')
        _boot_log(error)
        try:
            log_event('debug_stage3_crashed', error=error)
        except Exception:
            _boot_log('log_event failed during crash')
        try:
            if _UI:
                _UI.messageBox('FusionBridge Debug-Stufe 3 Fehler:\n{}'.format(error))
        except Exception:
            _boot_log('failed to show error message box')


def stop(context):
    _boot_log('stop() called')
    try:
        log_event('debug_stage3_stopped')
    except Exception:
        _boot_log('stop log_event failed')
