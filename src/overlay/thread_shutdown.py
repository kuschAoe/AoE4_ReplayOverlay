import time

_continue = True

def signal_threads_to_shutdown():
    global _continue
    _continue = False

def continue_running() -> bool:
    return _continue

class ThreadShutDownException(Exception):
    """Thread stopped because shutdown was initiated"""
    pass

def sleep(duration: float, interval: float):
    for _ in range(duration/interval):
        if not continue_running():
            raise ThreadShutDownException()
        time.sleep(interval)