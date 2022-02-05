# 29 January 2022 - Modified by KuschAoe

import subprocess
import sys
import webbrowser
from functools import partial
from types import TracebackType
from typing import Type

from PyQt5 import QtCore, QtGui, QtWidgets

from overlay.helper_func import file_path, pyqt_wait
from overlay.logging_func import get_logger
from overlay.settings import CONFIG_FOLDER, settings
from overlay.tab_main import TabWidget
from overlay.thread_shutdown import signal_threads_to_shutdown

logger = get_logger(__name__)

VERSION = "0.0.2"


def excepthook(exc_type: Type[BaseException], exc_value: Exception,
               exc_tback: TracebackType):
    """ Provides the top-most exception handling. Logs unhandled exceptions and cleanly shuts down the app."""
    # Log the exception
    logger.exception("Unhandled exception!",
                     exc_info=(exc_type, exc_value, exc_tback))
    # Try to save settings
    try:
        settings.save()
    except Exception:
        logger.exception("Failed to save settings")
    # Shut down other threads
    try:
        signal_threads_to_shutdown()
        pyqt_wait(1000)
    except Exception:
        pass
    sys.exit()


sys.excepthook = excepthook


class MainApp(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
        self.centralWidget().start()

    def initUI(self):
        self.setWindowTitle(f"AoE IV: Replay Overlay Control Panel({VERSION})")
        self.setWindowIcon(QtGui.QIcon(file_path('img/icon.ico')))
        self.setGeometry(0, 0, settings.app_width, settings.app_height)
        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() -
                  QtCore.QPoint(int(self.width() / 2), int(self.height() / 2)))

        # Create central widget
        self.setCentralWidget(TabWidget(self, VERSION))

        ### Create menu bar items
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        link_menu = menubar.addMenu('Links')

        # Config
        icon = self.style().standardIcon(
            getattr(QtWidgets.QStyle, 'SP_DirLinkIcon'))
        htmlAction = QtWidgets.QAction(icon, 'Config/logs', self)
        htmlAction.setStatusTip('Open the folder with config files')
        htmlAction.triggered.connect(
            lambda: subprocess.run(['explorer', CONFIG_FOLDER]))
        file_menu.addAction(htmlAction)

        # Exit
        icon = self.style().standardIcon(
            getattr(QtWidgets.QStyle, 'SP_DialogCloseButton'))
        exitAction = QtWidgets.QAction(icon, 'Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        file_menu.addAction(exitAction)

        # Github
        icon = QtGui.QIcon(file_path("img/github.png"))
        githubAction = QtWidgets.QAction(icon, 'App on Github', self)
        githubAction.triggered.connect(
            partial(webbrowser.open,
                    "https://github.com/kuschAoe/AoE4_ReplayOverlay"))
        link_menu.addAction(githubAction)

        self.show()

    def closeEvent(self, event):
        Main.centralWidget().settigns_tab.overlay_widget.hide()

    def finish(self):
        """ Give it some time to stop everything correctly"""
        settings.app_width = self.width()
        settings.app_height = self.height()
        settings.save()
        signal_threads_to_shutdown()
        pyqt_wait(1000)


if __name__ == '__main__':
    settings.load()
    app = QtWidgets.QApplication(sys.argv)
    Main = MainApp()
    exit_event = app.exec_()
    Main.finish()
    sys.exit(exit_event)
