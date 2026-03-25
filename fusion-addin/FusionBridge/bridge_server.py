import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from request_queue import ExecJob
from fusion_context import get_state


class BridgeRequestHandler(BaseHTTPRequestHandler):
    queue = None

    def _send_json(self, status_code: int, payload: dict):
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
                'version': '0.1.0',
            })
            return

        if self.path == '/state':
            self._send_json(200, get_state())
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
        if not isinstance(code, str) or not code.strip():
            self._send_json(400, {'ok': False, 'error': 'missing code'})
            return

        job = ExecJob(code=code)
        self.queue.put(job)
        job.done.wait()
        self._send_json(200, job.response or {'ok': False, 'error': 'no response'})

    def log_message(self, format, *args):
        return


class BridgeServer:
    def __init__(self, queue, host='127.0.0.1', port=8765):
        self.queue = queue
        self.host = host
        self.port = port
        self.httpd = None
        self.thread = None

    def start(self):
        BridgeRequestHandler.queue = self.queue
        self.httpd = ThreadingHTTPServer((self.host, self.port), BridgeRequestHandler)
        self.thread = Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd = None
