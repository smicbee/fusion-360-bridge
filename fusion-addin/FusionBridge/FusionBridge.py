import traceback
from pathlib import Path

import adsk.core

_APP = None
_UI = None
_LOG_PATH = Path(__file__).resolve().parent / 'fusion_bridge_boot.log'


def _log(message: str) -> None:
    try:
        with _LOG_PATH.open('a', encoding='utf-8') as handle:
            handle.write(message + '\n')
    except Exception:
        pass


def run(context):
    global _APP, _UI

    _log('run() entered')

    try:
        _APP = adsk.core.Application.get()
        _log(f'app acquired: {_APP is not None}')

        _UI = _APP.userInterface if _APP else None
        _log(f'ui acquired: {_UI is not None}')

        product = _APP.activeProduct if _APP else None
        _log(f'active product type: {product.objectType if product else None}')

        document = _APP.activeDocument if _APP else None
        _log(f'active document: {document.name if document else None}')

        if _UI:
            _UI.messageBox('FusionBridge Debug-Start erfolgreich')
            _log('message box shown')
        else:
            _log('ui missing, message box skipped')
    except Exception:
        error = traceback.format_exc()
        _log('run() crashed')
        _log(error)
        try:
            if _UI:
                _UI.messageBox('FusionBridge Debug-Startfehler:\n{}'.format(error))
        except Exception:
            _log('failed to show error message box')


def stop(context):
    _log('stop() called')
