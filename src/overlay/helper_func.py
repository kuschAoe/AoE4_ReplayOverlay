# 29 January 2022 - Modified by KuschAoe

import json
import os
import pathlib
import sys
import time

from typing import Any, Dict, Union

import requests
from PyQt5 import QtCore

from overlay.logging_func import get_logger
from overlay.settings import settings

logger = get_logger(__name__)
ROOT = pathlib.Path(sys.argv[0]).parent.absolute()


def pyqt_wait(miliseconds: int):
    """ Pause executing for `time` in miliseconds"""
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(miliseconds, loop.quit)
    loop.exec_()


def is_compiled() -> bool:
    """ Checks whether the app is compiled by Nuitka"""
    return '__compiled__' in globals()


def file_path(file: str) -> str:
    """ Returns the path to the main directory regardless of the current working directory """
    return os.path.normpath(os.path.join(ROOT, file))


def version_to_int(version: str):
    """Convets `1.0.1` to an integer """
    return sum([
        int(i) * (1000**idx) for idx, i in enumerate(version.split('.')[::-1])
    ])


def version_check(version: str) -> str:
    """ Checks version. Returns either link for the new version or an empty string. """
    try:
        url = "https://raw.githubusercontent.com/kuschAoe/AoE4_ReplayOverlay/main/version.json"
        data = json.loads(requests.get(url).text)
        if version_to_int(version) < version_to_int(data['version']):
            return data['link']
    except Exception:
        logger.warning("Failed to check for a new version")
    return ""



def strtime(t: Union[int, float], show_seconds: bool = False) -> str:
    """ Returns formatted string 
    X days, Y hours, Z minutes
    """
    years, delta = divmod(t, 31557600)
    days, delta = divmod(delta, 86400)
    hours, delta = divmod(delta, 3600)
    minutes, seconds = divmod(delta, 60)

    s = []
    if years:
        s.append(f"{years:.0f} years")
    if days:
        s.append(f"{days:.0f} days")
    if hours:
        s.append(f"{hours:.0f} hours")
    if minutes or (not show_seconds and not s):
        s.append(f"{minutes:.0f} minutes")
    if show_seconds:
        s.append(f"{seconds:.0f} seconds")
    return " ".join(s)
