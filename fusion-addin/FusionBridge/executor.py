import io
import time
import traceback
from contextlib import redirect_stdout

from fusion_context import get_context
from logging_utils import log_event


class Executor:
    def execute(self, code, job_id=None):
        stdout_buffer = io.StringIO()
        context = get_context()
        started_at = time.time()

        log_event('exec_started', jobId=job_id, codeLength=len(code))

        try:
            with redirect_stdout(stdout_buffer):
                exec(code, context, context)

            response = {
                'ok': True,
                'stdout': stdout_buffer.getvalue(),
                'result': context.get('result'),
                'error': None,
                'durationMs': int((time.time() - started_at) * 1000),
                'jobId': job_id,
            }
            log_event('exec_finished', jobId=job_id, ok=True, durationMs=response['durationMs'])
            return response
        except Exception:
            response = {
                'ok': False,
                'stdout': stdout_buffer.getvalue(),
                'result': context.get('result'),
                'error': traceback.format_exc(),
                'durationMs': int((time.time() - started_at) * 1000),
                'jobId': job_id,
            }
            log_event('exec_finished', jobId=job_id, ok=False, durationMs=response['durationMs'])
            return response
