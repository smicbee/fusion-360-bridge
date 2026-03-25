import traceback
from pathlib import Path

import adsk.core

from executor import Executor
from logging_utils import log_event

_APP = None
_UI = None
_EXECUTOR = None
_BOOT_LOG_PATH = Path(__file__).resolve().parent / 'fusion_bridge_boot.log'


def _boot_log(message: str) -> None:
    try:
        with _BOOT_LOG_PATH.open('a', encoding='utf-8') as handle:
            handle.write(message + '\n')
    except Exception:
        pass


def run(context):
    global _APP, _UI, _EXECUTOR

    _boot_log('run() entered')

    try:
        _APP = adsk.core.Application.get()
        _boot_log(f'app acquired: {_APP is not None}')

        _UI = _APP.userInterface if _APP else None
        _boot_log(f'ui acquired: {_UI is not None}')

        product = _APP.activeProduct if _APP else None
        _boot_log(f'active product type: {product.objectType if product else None}')

        document = _APP.activeDocument if _APP else None
        _boot_log(f'active document: {document.name if document else None}')

        log_event('debug_stage2_before_executor')
        _boot_log('logging_utils imported and used successfully')

        _EXECUTOR = Executor()
        _boot_log('executor instantiated successfully')
        log_event('debug_stage2_executor_ready')

        if _UI:
            _UI.messageBox('FusionBridge Debug-Stufe 2 erfolgreich')
            _boot_log('message box shown')
        else:
            _boot_log('ui missing, message box skipped')
    except Exception:
        error = traceback.format_exc()
        _boot_log('run() crashed')
        _boot_log(error)
        try:
            log_event('debug_stage2_crashed', error=error)
        except Exception:
            _boot_log('log_event also failed during crash handling')
        try:
            if _UI:
                _UI.messageBox('FusionBridge Debug-Stufe 2 Fehler:\n{}'.format(error))
        except Exception:
            _boot_log('failed to show error message box')


def stop(context):
    _boot_log('stop() called')
    try:
        log_event('debug_stage2_stopped')
    except Exception:
        _boot_log('stop logging failed')
