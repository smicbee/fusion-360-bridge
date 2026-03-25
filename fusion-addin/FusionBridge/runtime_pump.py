import threading
import time
import traceback
import uuid

import adsk.core

from logging_utils import log_event


class _CustomEventHandler(adsk.core.CustomEventHandler):
    def __init__(self, callback):
        super().__init__()
        self._callback = callback

    def notify(self, args):
        self._callback()


class _TimerHandler(adsk.core.TimerEventHandler):
    def __init__(self, callback):
        super().__init__()
        self._callback = callback

    def notify(self, args):
        self._callback()


class RuntimePump:
    def __init__(self, app, process_callback, interval_ms=250):
        self.app = app
        self.process_callback = process_callback
        self.interval_ms = interval_ms
        self.mode = None
        self.event_id = None
        self.custom_event = None
        self.custom_handler = None
        self.timer_handler = None
        self.trigger_thread = None
        self.stop_event = threading.Event()

    def start(self):
        self._start_custom_event_mode()

    def stop(self):
        self.stop_event.set()

        if self.trigger_thread and self.trigger_thread.is_alive():
            self.trigger_thread.join(timeout=2)

        if self.mode == 'custom-event':
            try:
                if self.custom_event and self.custom_handler:
                    self.custom_event.remove(self.custom_handler)
            except Exception:
                log_event('runtime_pump_custom_remove_failed', error=traceback.format_exc())

            try:
                if self.event_id:
                    self.app.unregisterCustomEvent(self.event_id)
            except Exception:
                log_event('runtime_pump_custom_unregister_failed', error=traceback.format_exc())

        elif self.mode == 'timer':
            try:
                if self.timer_handler:
                    self.app.timerEvent.remove(self.timer_handler)
            except Exception:
                log_event('runtime_pump_timer_remove_failed', error=traceback.format_exc())

            try:
                self.app.unregisterTimerEvent()
            except Exception:
                log_event('runtime_pump_timer_unregister_failed', error=traceback.format_exc())

    def _safe_process(self):
        try:
            self.process_callback()
        except Exception:
            log_event('runtime_pump_process_failed', error=traceback.format_exc())

    def _start_custom_event_mode(self):
        self.event_id = f'fusionbridge.process.{uuid.uuid4()}'
        self.custom_event = self.app.registerCustomEvent(self.event_id)
        self.custom_handler = _CustomEventHandler(self._safe_process)
        self.custom_event.add(self.custom_handler)

        self.trigger_thread = threading.Thread(target=self._custom_event_loop, daemon=True)
        self.trigger_thread.start()
        self.mode = 'custom-event'
        log_event('runtime_pump_started', mode=self.mode, intervalMs=self.interval_ms, eventId=self.event_id)

    def _custom_event_loop(self):
        while not self.stop_event.is_set():
            try:
                self.app.fireCustomEvent(self.event_id)
            except Exception:
                log_event('runtime_pump_custom_fire_failed', error=traceback.format_exc())
            self.stop_event.wait(self.interval_ms / 1000.0)

    def start_timer_fallback(self):
        self.timer_handler = _TimerHandler(self._safe_process)
        self.app.registerTimerEvent(self.interval_ms)
        self.app.timerEvent.add(self.timer_handler)
        self.mode = 'timer'
        log_event('runtime_pump_started', mode=self.mode, intervalMs=self.interval_ms)
