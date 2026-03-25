import io
import traceback
from contextlib import redirect_stdout

from fusion_context import get_context


class Executor:
    def execute(self, code: str) -> dict:
        stdout_buffer = io.StringIO()
        context = get_context()

        try:
            with redirect_stdout(stdout_buffer):
                exec(code, context, context)

            return {
                'ok': True,
                'stdout': stdout_buffer.getvalue(),
                'result': context.get('result'),
                'error': None,
            }
        except Exception:
            return {
                'ok': False,
                'stdout': stdout_buffer.getvalue(),
                'result': context.get('result'),
                'error': traceback.format_exc(),
            }
