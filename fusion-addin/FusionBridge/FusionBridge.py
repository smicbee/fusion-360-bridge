import traceback
from datetime import datetime
from pathlib import Path

import adsk.core

_BOOT_LOG_PATH = Path(__file__).resolve().parent / 'fusion_bridge_boot.log'
_APP = None
_UI = None
_EXECUTOR = None
_VERSION = 'stage3b-instrumented'


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
    global _APP, _UI, _EXECUTOR

    _boot_log('run() entered')
    _boot_log('version: {}'.format(_VERSION))
    _boot_log('context type: {}'.format(type(context).__name__))

    try:
        _APP = adsk.core.Application.get()
        _boot_log('app acquired: {}'.format(_APP is not None))
        if not _APP:
            return

        _UI = _APP.userInterface
        _boot_log('ui acquired: {}'.format(_UI is not None))

        if _UI:
            _safe_message_box('FusionBridge {} gestartet'.format(_VERSION))
            _boot_log('popup shown')

        _boot_log('attempt import logging_utils')
        try:
            from logging_utils import log_event
            _boot_log('logging_utils imported')
            log_event('stage3b_logging_utils_imported')
        except Exception as e:
            _boot_log('logging_utils failed: {}'.format(e))
            _safe_message_box('Logging import failed: {}'.format(e))

        _boot_log('attempt import Executor')
        try:
            from executor import Executor
            _boot_log('executor module imported')
            _EXECUTOR = Executor()
            _boot_log('executor instantiated successfully')
            try:
                from logging_utils import log_event
                log_event('stage3b_executor_ready')
            except Exception:
                _boot_log('log_event unavailable after executor')
            _safe_message_box('Executor ready in {}'.format(_VERSION))
        except Exception as e:
            _boot_log('executor failed: {}'.format(e))
            _safe_message_box('Executor init failed: {}'.format(e))

    except Exception:
        _boot_log('run() crashed')
        _boot_log(traceback.format_exc())
        _safe_message_box('FusionBridge {} Fehler:\n{}'.format(_VERSION, traceback.format_exc()))


def stop(context):
    _boot_log('stop() called')
