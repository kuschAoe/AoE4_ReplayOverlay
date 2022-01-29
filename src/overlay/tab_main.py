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
from overlay.tab_override import OverrideTab
from overlay.tab_settings import SettingsTab
from overlay.worker import scheldule

logger = get_logger(__name__)


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent, version: str):
        super().__init__(parent)
        self.version = version
        self.force_stop: bool = False
        self.prevent_overlay_update: bool = False

        self.override_tab = OverrideTab(self)
        self.override_tab.data_override.connect(self.override_event)
        self.override_tab.update_override.connect(self.override_update_event)
        self.settigns_tab = SettingsTab(self)

        self.addTab(self.settigns_tab, "Settings")
        self.addTab(self.override_tab, "Override")

    def start(self):
        logger.info(
            f"Starting (v{self.version}) (c:{hf.is_compiled()}) [{platform.platform()}]"
        )
        self.check_for_new_version()
        self.settigns_tab.start()
        self.check_waking()

    def got_match_history(self, match_history: List[Any]):
        if match_history is None:
            self.settigns_tab.message(
                "Failed to get match history! Possibly an issue with AoEIV.net",
                color='red')
            logger.warning("No match history data")
            return
        self.settigns_tab.message("")
        self.stats_tab.update_other_stats(match_history)
        self.games_tab.update_widgets(match_history)

    def run_new_game_check(self, delayed_seconds: int = 0):
        """ Creates a new thread for a new api check"""
        scheldule(self.new_game, self.api_checker.check_for_new_game,
                  delayed_seconds)

    def new_game(self, game_data: Optional[Dict[str, Any]]):
        """Received new data from api check, passes data along and reruns the check"""
        if self.force_stop:
            return
        if game_data is not None and "new_rating" in game_data:
            logger.info(
                f"Game finished (rating_timestamp: {game_data['timestamp']})")
            self.graph_tab.run_update()
            self.stats_tab.run_mode_update()
            self.update_with_match_history_data(2)
        elif game_data is not None:
            processed = hf.process_game(game_data)
            start = time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime(processed['started']))
            logger.info(
                f"New live game (match_id: {processed['match_id']} | mode: {processed['mode']-16} | started: {start})"
            )
            self.override_tab.update_data(processed)
            if not self.prevent_overlay_update:
                self.settigns_tab.overlay_widget.update_data(processed)
                self.websocket_manager.send({
                    "type": "player_data",
                    "data": processed
                })

        self.run_new_game_check(delayed_seconds=30)

    def stop_checking_api(self):
        """ The app is closing, we need to start shuttings things down"""
        self.force_stop = True
        self.api_checker.force_stop = True

    def check_for_new_version(self):
        """ Checks for a new version, creates a button if there is one """
        link = hf.version_check(self.version)
        if not link:
            return
        logger.info("New version available!")
        self.settigns_tab.update_button.clicked.connect(
            partial(webbrowser.open, link))
        self.settigns_tab.update_button.show()

    def override_event(self, data: Dict[str, Any]):
        self.settigns_tab.overlay_widget.update_data(data)
        self.websocket_manager.send({"type": "player_data", "data": data})

    def override_update_event(self, prevent: bool):
        self.prevent_overlay_update = prevent


    ### Functionality dedicated to checking for PC waking, and resetting keyboard threads

    def check_waking(self):
        """ Manages all checks and keyboard resets"""
        scheldule(self.pc_waken_from_sleep, self.wait_for_wake)

    def wait_for_wake(self):
        """ Function that checks for a interruption"""
        interval = 10  # Seconds
        while True:
            start = time.time()
            # Wait 5s
            for _ in range(interval * 2):
                time.sleep(0.5)
                if self.force_stop:
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
            self.settigns_tab.init_hotkeys()
            self.buildorder_tab.init_hotkeys()
        except Exception:
            logger.exception(f"Failed to reset keyboard")
