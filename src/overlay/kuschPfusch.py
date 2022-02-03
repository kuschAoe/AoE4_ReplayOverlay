from typing import Any, Dict, Optional
import time
import json
import re

from overlay.thread_shutdown import sleep
from overlay.logging_func import get_logger
import overlay.settings as s

logger = get_logger(__name__)


def tail(f):
    f.seek(-1500, 2)
    return f.read()

def get_replay_data() -> Optional[Dict[str, Any]]:
    info = ""
    try:
        with open(s.get_aoe4_warnings_log_path(), "rb") as f:
            info = tail(f)
    except Exception:
        logger.exception("")

    reg = re.findall("oVeRlAy(.*?)dAtA", str(info))
    if reg:
        return json.loads(reg[-1])

def kuschPfuschWorker(delayed_seconds: int) -> Optional[Dict[str, Any]]:
    time.sleep(delayed_seconds)
    for i in range(5):
        result = get_replay_data()
        if result is not None:
            return result

        sleep(0.5, 0.5)
    
    return


    


