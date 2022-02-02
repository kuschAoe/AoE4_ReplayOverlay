# 1 February 2022 - Modified by KuschAoe

import json
import os
from typing import Dict, List, Optional

from overlay.logging_func import CONFIG_FOLDER, get_logger

logger = get_logger(__name__)
CONFIG_FILE = os.path.join(CONFIG_FOLDER, "config.json")


class _Settings:
    def __init__(self):
        self.interval: int = 15
        self.app_width: int = 900
        self.app_height: int = 600
        self.overlay_hotkey: str = ""
        self.overlay_geometry: Optional[List[int]] = None
        self.font_size: int = 12
        self.team_colors = ((74, 255, 2, 0.35), (3, 179, 255, 0.35), (255, 0,
                                                                      0, 0.35))
        self.path_aoe4_warnings_log = None

    def load(self):
        """ Loads configuration from app data"""
        if not os.path.isfile(CONFIG_FILE):
            return
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.loads(f.read())
        except Exception:
            logger.warning("Failed to parse config file")
            return

        for key in self.__dict__:
            if key in data:
                setattr(self, key, data[key])

    def save(self):
        """ Saves configuration to app data"""
        with open(CONFIG_FILE, 'w') as f:
            f.write(json.dumps(self.__dict__, indent=2))


settings = _Settings()

def get_aoe4_warnings_log_path() -> str:
    if settings.path_aoe4_warnings_log is None:
        return get_aoe4_warnings_log_path_default()
    return settings.path_aoe4_warnings_log

def get_aoe4_warnings_log_path_default() -> str:
    return os.path.expanduser("~\\Documents\\My Games\\Age of Empires IV\\warnings.log")