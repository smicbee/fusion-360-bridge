from pathlib import Path

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


def stop(context):
    _boot_log('stop() called')
