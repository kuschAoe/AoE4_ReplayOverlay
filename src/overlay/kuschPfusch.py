from typing import Any, Dict, List, Optional, Tuple
import time

i = 0

def kuschPfuschWorker(delayed_seconds: int
                        ) -> Optional[Dict[str, Any]]:

    time.sleep(delayed_seconds)
    global i 
    i = i + 1
    return {
        "players": [{
            "name": "kusch",
            "civ": "English",
            "worker": str(i),
            "military": "42",
            "team": 1
            }],
        }


    


