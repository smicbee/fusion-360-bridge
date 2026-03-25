import traceback
from pathlib import Path

import adsk.core

_BOOT_LOG_PATH = Path(__file__).resolve().parent / 'fusion_bridge_boot.log'


def _boot_log(message):
    try:
        with _BOOT_LOG_PATH.open('a', encoding='utf-8') as handle:
            handle.write(message + '\n')
    except Exception:
        pass


def run(context):
    _boot_log('run() entered')
    _boot_log('context type: {}'.format(type(context).__name__))

    try:
        app = adsk.core.Application.get()
        _boot_log('app acquired: {}'.format(app is not None))
        if not app:
            return

        ui = app.userInterface
        _boot_log('ui acquired: {}'.format(ui is not None))
        if ui:
            ui.messageBox('FusionBridge Popup-Check erfolgreich')
            _boot_log('popup shown')
        else:
            _boot_log('ui missing, popup skipped')
    except Exception:
        _boot_log('run() crashed')
        _boot_log(traceback.format_exc())


def stop(context):
    _boot_log('stop() called')
