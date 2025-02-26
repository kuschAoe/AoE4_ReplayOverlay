# 29 January 2022 - Modified by KuschAoe

import importlib
import platform
import time
import webbrowser
from functools import partial
from typing import Any, Dict, List, Optional

import keyboard
from PyQt5 import QtWidgets

import overlay.helper_func as hf
from overlay.logging_func import get_logger
from overlay.settings import settings
from overlay.tab_settings import SettingsTab
from overlay.worker import schedule
from overlay.thread_shutdown import continue_running
from overlay.kuschPfusch import kuschPfuschWorker

logger = get_logger(__name__)


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent, version: str):
        super().__init__(parent)
        self.version = version
        self.prevent_overlay_update: bool = False

        self.settings_tab = SettingsTab(self)

        self.addTab(self.settings_tab, "Settings")

    def start(self):
        logger.info(
            f"Starting (v{self.version}) (c:{hf.is_compiled()}) [{platform.platform()}]"
        )
        self.check_for_new_version()
        self.settings_tab.start()
        self.check_waking()
        self.kuschPfuschScheduler()

    def kuschPfuschScheduler(self, delayed_seconds: int = 0):
        schedule(self.newReplayData, kuschPfuschWorker,
                  delayed_seconds)

    def newReplayData(self, game_data: Optional[Dict[str, Any]]):
        try:
            self.settings_tab.overlay_widget.update_data(game_data)
        except Exception:
            raw = ""
            if game_data and "raw" in game_data:
                raw = str(game_data["raw"])
            logger.exception(f"There was something wrong with the data extracted from he replay: " + raw)

        if continue_running():
            self.kuschPfuschScheduler(delayed_seconds=1)

    def check_for_new_version(self):
        """ Checks for a new version, creates a button if there is one """
        link = hf.version_check(self.version)
        if not link:
            return
        logger.info("New version available!")
        self.settings_tab.update_button.clicked.connect(
            partial(webbrowser.open, link))
        self.settings_tab.update_button.show()

    ### Functionality dedicated to checking for PC waking, and resetting keyboard threads

    def check_waking(self):
        """ Manages all checks and keyboard resets"""
        schedule(self.pc_waken_from_sleep, self.wait_for_wake)

    def wait_for_wake(self):
        """ Function that checks for a interruption"""
        interval = 10  # Seconds
        while True:
            start = time.time()
            # Wait 5s
            for _ in range(interval * 2):
                time.sleep(0.5)
                if not continue_running():
                    return None
            # Check the difference
            diff = time.time() - start
            if diff > interval + 5:
                time.sleep(4)
                return diff - interval

    def pc_waken_from_sleep(self, diff: Optional[float]):
        """ This function is run when the PC is awoken """
        if diff is None:
            return

        logger.info(f'PC awoke! ({hf.strtime(diff, show_seconds=True)})')
        self.check_waking()

        # Check for new updates & reset keyboard threads
        self.check_for_new_version()
        self.reset_keyboard_threads()

    def reset_keyboard_threads(self):
        """ Resets keyboard thread"""
        global keyboard
        try:
            logger.info(f'Resetting keyboard thread')
            keyboard.unhook_all()
            keyboard = importlib.reload(keyboard)
            self.settings_tab.init_hotkeys()
        except Exception:
            logger.exception(f"Failed to reset keyboard")
