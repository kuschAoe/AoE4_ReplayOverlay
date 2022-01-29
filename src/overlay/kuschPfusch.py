from typing import Any, Dict, List, Optional, Tuple
import time

i = 0

def kuschPfuschWorker(delayed_seconds: int
                        ) -> Optional[Dict[str, Any]]:

    time.sleep(delayed_seconds)
    global i 
    i = i + 1
    return {"playerName": "kusch",
        "villagerCount": i,
        "militaryCount": 42}


    


