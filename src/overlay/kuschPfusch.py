from typing import Any, Dict, Optional
import time
import json
import re
from os import path

from overlay.thread_shutdown import sleep
from overlay.logging_func import get_logger

logger = get_logger(__name__)

aoe4WarningsFilePath = path.expanduser("~\\Documents\\My Games\\Age of Empires IV\\warnings.log")

def tail(f):
    f.seek(-1500, 2)
    return f.read()

def get_replay_data() -> Optional[Dict[str, Any]]:
    info = ""
    try:
        with open(aoe4WarningsFilePath, "rb") as f:
            info = tail(f)
    except Exception:
        logger.exception("")

    reg = re.findall("oVeRlAy(.*?)dAtA", str(info))
    if reg:
        return json.loads(reg[-1])

def kuschPfuschWorker(delayed_seconds: int) -> Optional[Dict[str, Any]]:
    time.sleep(delayed_seconds)
    while True:
        result = get_replay_data()
        if result is not None:
            return result

        sleep(0.5, 0.5)


    


