 # 29 Januray 2022 - Modified by KuschAoe

import sys
import keyboard
from PyQt5 import QtCore, QtGui, QtWidgets

from overlay.helper_func import file_path
from overlay.custom_widgets import CustomKeySequenceEdit
from overlay.logging_func import get_logger
from overlay.overlay_widget import AoEOverlay
from overlay.settings import settings

logger = get_logger(__name__)

command = "dofile(\"" + file_path("AoE4LuaScript/OverlayDataCollector.lua") + "\")"

class SettingsTab(QtWidgets.QWidget):
    show_hide_overlay = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.overlay_widget = AoEOverlay()
        self.init_UI()
        self.show_hide_overlay.connect(self.overlay_widget.show_hide)

    def init_UI(self):
        # Layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.main_layout.setContentsMargins(25, 25, 25, 25)
        self.main_layout.setSpacing(25)
        self.setLayout(self.main_layout)

        # Notification
        self.notification_label = QtWidgets.QLabel()

        ### Overlay box
        overlay_box = QtWidgets.QGroupBox("Overlay")
        overlay_box.setMinimumSize(400, 100)
        overlay_box.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                  QtWidgets.QSizePolicy.Fixed))
        overlay_layout = QtWidgets.QGridLayout()
        overlay_box.setLayout(overlay_layout)
        self.main_layout.addWidget(overlay_box)

        # Hotkey for overlay
        key_label = QtWidgets.QLabel("Hotkey for showing and hiding overlay:")
        overlay_layout.addWidget(key_label, 0, 0)

        self.key_showhide = CustomKeySequenceEdit(self)
        self.key_showhide.setMaximumWidth(100)
        self.key_showhide.setToolTip("Hotkey for showing and hiding overlay")
        overlay_layout.addWidget(self.key_showhide, 0, 1)
        self.key_showhide.key_changed.connect(self.hotkey_changed)

        # Overlay font
        font_label = QtWidgets.QLabel("Overlay font size:")
        overlay_layout.addWidget(font_label, 1, 0)

        self.font_size_combo = QtWidgets.QComboBox()
        for i in range(1, 50):
            self.font_size_combo.addItem(f"{i} pt")
        self.font_size_combo.setCurrentIndex(settings.font_size - 1)
        self.font_size_combo.currentIndexChanged.connect(
            self.font_size_changed)
        overlay_layout.addWidget(self.font_size_combo, 1, 1)

        # Position change button
        self.btn_change_position = QtWidgets.QPushButton(
            "Change/fix overlay position")
        self.btn_change_position.setToolTip(
            "Click to change overlay position. Click again to fix its position."
        )
        self.btn_change_position.clicked.connect(
            self.overlay_widget.change_state)
        overlay_layout.addWidget(self.btn_change_position, 2, 0, 1, 2)
        
        ### replay data extraction box
        extraction_box = QtWidgets.QGroupBox("Replay Data Extraction")
        extraction_box.setMinimumSize(400, 100)
        extraction_box.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                  QtWidgets.QSizePolicy.Fixed))
        extraction_layout = QtWidgets.QGridLayout()
        extraction_box.setLayout(extraction_layout)
        self.main_layout.addWidget(extraction_box)

        # command for ingame console
        command_label = QtWidgets.QLabel("Command for ingame console:")
        extraction_layout.addWidget(command_label, 0, 0)

        command_textfiled = QtWidgets.QLineEdit()
        command_textfiled.setReadOnly(True)
        command_textfiled.setText(command)
        extraction_layout.addWidget(command_textfiled, 1, 0, 1, 2)

        copy_command_button = QtWidgets.QPushButton("Copy to clipboard")
        copy_command_button.clicked.connect(self.copy_command_to_clipboard)
        extraction_layout.addWidget(copy_command_button, 0, 1)

        # Position change button
        self.btn_change_position = QtWidgets.QPushButton(
            "Change/fix overlay position")
        self.btn_change_position.setToolTip(
            "Click to change overlay position. Click again to fix its position.")
        self.btn_change_position.clicked.connect(
            self.overlay_widget.change_state)
        overlay_layout.addWidget(self.btn_change_position, 2, 0, 1, 2)

        ### Messages
        self.msg = QtWidgets.QLabel()
        self.main_layout.addWidget(self.msg)

        # Create update button
        self.update_button = QtWidgets.QPushButton("New update!")
        self.update_button.setMaximumWidth(400)
        self.update_button.setToolTip("Click here to download new app version")
        self.update_button.setStyleSheet(
            'background-color: #3bb825; color: black')
        self.update_button.hide()
        self.main_layout.addWidget(self.update_button)

    def start(self):
        # Initialize
        self.init_hotkeys()

    def copy_command_to_clipboard(self):
        cb = QtGui.QGuiApplication.clipboard()
        cb.setText(command, mode=cb.Clipboard)

    def init_hotkeys(self):
        if settings.overlay_hotkey:
            self.key_showhide.setKeySequence(
                QtGui.QKeySequence.fromString(settings.overlay_hotkey))
            keyboard.add_hotkey(settings.overlay_hotkey,
                                self.show_hide_overlay.emit)

    def notification(self, text: str, color: str = "black"):
        """ Shows a notification"""
        self.notification_label.setText(text)
        self.notification_label.setStyleSheet(f"color: {color}")

    def message(self, text: str, color: str = "black"):
        """ Shows a message"""
        self.msg.setText(text)
        self.msg.setStyleSheet(f"color: {color}")

    def font_size_changed(self):
        font_size = self.font_size_combo.currentIndex() + 1
        settings.font_size = font_size
        self.overlay_widget.update_style(font_size)

    def hotkey_changed(self, new_hotkey: str):
        """ Checks whether the hotkey is actually new and valid.
        Updates keyboard threads"""
        new_hotkey = new_hotkey.replace("Num+", "")

        if new_hotkey == "Del":
            self.key_showhide.setKeySequence(QtGui.QKeySequence.fromString(""))
            settings.overlay_hotkey = ""
            return
        elif not new_hotkey or new_hotkey == settings.overlay_hotkey:
            return

        if settings.overlay_hotkey:
            keyboard.remove_hotkey(settings.overlay_hotkey)
        logger.info(f"Setting new hotkey to: {new_hotkey}")
        settings.overlay_hotkey = new_hotkey
        keyboard.add_hotkey(new_hotkey, self.show_hide_overlay.emit)
