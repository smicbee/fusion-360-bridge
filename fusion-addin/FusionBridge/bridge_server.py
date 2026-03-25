import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from fusion_context import get_state
from logging_utils import log_event, read_recent_lines
from request_queue import ExecJob


class BridgeRequestHandler(BaseHTTPRequestHandler):
    queue = None
    runtime = None

    def _send_json(self, status_code, payload):
        data = json.dumps(payload).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == '/ping':
            self._send_json(200, {
                'ok': True,
                'service': 'fusion-bridge',
                'version': '0.3.0',
            })
            return

        if self.path == '/state':
            self._send_json(200, get_state(
                queue_size=self.queue.size(),
                is_busy=self.runtime.get('busy', False),
                current_job_id=self.runtime.get('currentJobId'),
                pump_mode=self.runtime.get('pumpMode'),
            ))
            return

        if self.path == '/logs':
            self._send_json(200, {
                'ok': True,
                'lines': read_recent_lines(),
            })
            return

        self._send_json(404, {'ok': False, 'error': 'not found'})

    def do_POST(self):
        if self.path != '/exec':
            self._send_json(404, {'ok': False, 'error': 'not found'})
            return

        length = int(self.headers.get('Content-Length', '0'))
        raw = self.rfile.read(length)

        try:
            payload = json.loads(raw.decode('utf-8'))
        except Exception:
            self._send_json(400, {'ok': False, 'error': 'invalid json'})
            return

        code = payload.get('code')
        timeout_seconds = payload.get('timeoutSeconds', 120)
        if not isinstance(code, str) or not code.strip():
            self._send_json(400, {'ok': False, 'error': 'missing code'})
            return

        if not isinstance(timeout_seconds, (int, float)) or timeout_seconds <= 0:
            timeout_seconds = 120

        job = ExecJob(code=code)
        self.queue.put(job)
        log_event('job_enqueued', jobId=job.job_id, queueSize=self.queue.size())

        finished = job.done.wait(timeout=timeout_seconds)
        if not finished:
            self._send_json(504, {
                'ok': False,
                'error': 'execution timeout',
                'jobId': job.job_id,
            })
            return

        self._send_json(200, job.response or {'ok': False, 'error': 'no response', 'jobId': job.job_id})

    def log_message(self, format, *args):
        return


class BridgeServer:
    def __init__(self, queue, runtime, host='127.0.0.1', port=8765):
        self.queue = queue
        self.runtime = runtime
        self.host = host
        self.port = port
        self.httpd = None
        self.thread = None

    def start(self):
        BridgeRequestHandler.queue = self.queue
        BridgeRequestHandler.runtime = self.runtime
        self.httpd = ThreadingHTTPServer((self.host, self.port), BridgeRequestHandler)
        self.thread = Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        log_event('server_started', host=self.host, port=self.port)

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None
            log_event('server_stopped')
