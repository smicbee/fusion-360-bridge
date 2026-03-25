import traceback
import adsk.core

from bridge_server import BridgeServer
from executor import Executor
from request_queue import RequestQueue

_app = None
_ui = None
_handlers = []
_queue = None
_server = None
_executor = None
_timer = None


class TimerHandler(adsk.core.TimerEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            process_pending_jobs()
        except Exception:
            if _ui:
                _ui.messageBox('FusionBridge timer error:\n{}'.format(traceback.format_exc()))


def process_pending_jobs():
    global _queue, _executor

    if _queue is None or _executor is None:
        return

    while True:
        job = _queue.get_nowait()
        if job is None:
            break

        job.response = _executor.execute(job.code)
        job.done.set()


def run(context):
    global _app, _ui, _queue, _server, _executor, _timer

    _app = adsk.core.Application.get()
    _ui = _app.userInterface

    try:
        _queue = RequestQueue()
        _executor = Executor()
        _server = BridgeServer(_queue, host='127.0.0.1', port=8765)
        _server.start()

        _timer = TimerHandler()
        _app.registerTimerEvent(250)
        _app.timerEvent.add(_timer)
        _handlers.append(_timer)

        _ui.messageBox('FusionBridge gestartet auf http://127.0.0.1:8765')
    except Exception:
        if _ui:
            _ui.messageBox('FusionBridge Startfehler:\n{}'.format(traceback.format_exc()))


def stop(context):
    global _server, _app, _timer

    try:
        if _app and _timer:
            _app.timerEvent.remove(_timer)
            _app.unregisterTimerEvent()
            _timer = None

        if _server:
            _server.stop()
            _server = None
    except Exception:
        if _ui:
            _ui.messageBox('FusionBridge Stopfehler:\n{}'.format(traceback.format_exc()))
