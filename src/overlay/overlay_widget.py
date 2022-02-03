 # 29 January 2022 - Modified by KuschAoe

from typing import Any, Dict

from PyQt5 import QtCore, QtGui, QtWidgets

from overlay.custom_widgets import OverlayWidget
from overlay.helper_func import file_path
from overlay.settings import settings

def set_pixmap(civ: str, widget: QtWidgets.QWidget):
    """ Sets civ pixmap to a widget. Handles caching."""
    path = file_path(f"img/{civ}")
    pixmap = QtGui.QPixmap(path)
    pixmap = pixmap.scaled(widget.width(), widget.height(), 
        QtCore.Qt.AspectRatioMode.KeepAspectRatio, 
        QtCore.Qt.TransformationMode.SmoothTransformation)
    widget.setPixmap(pixmap)


class PlayerWidget:
    """ Player widget shown on the overlay"""
    def __init__(self, row: int, toplayout: QtWidgets.QGridLayout):
        self.visible = True
        self.civ = "english"
        self.create_widgets()

        self.widgets = [self.flag, self.name, self.worker_icon, 
            self.worker, self.military_icon, self.military]

        for column, widget in enumerate(self.widgets):
            toplayout.addWidget(widget, row, column)

    def create_widgets(self):
        # Separated so this can be changed in a child inner overlay for editing
        self.flag = QtWidgets.QLabel()
        self.flag.setObjectName("flag")
        self.name = QtWidgets.QLabel()
        self.worker_icon = QtWidgets.QLabel()
        self.worker_icon.setObjectName("icon")
        set_pixmap("overlay_icons/worker.png", self.worker_icon)
        self.worker = QtWidgets.QLabel()
        self.worker.setAlignment(QtCore.Qt.Alignment(0x82))
        self.military_icon = QtWidgets.QLabel()
        self.military_icon.setObjectName("icon")
        set_pixmap("overlay_icons/military.png", self.military_icon)
        self.military = QtWidgets.QLabel()
        self.military.setAlignment(QtCore.Qt.Alignment(0x82))

    def show(self, show: bool = True):
        self.visible = show
        """ Shows or hides all widgets in this class """
        for widget in self.widgets:
            widget.show() if show else widget.hide()

    def set_color(self, color):
        color = tuple([int(channel) for channel in color])
        self.name.setStyleSheet("font-weight: bold; "
                                f"color: rgba{color}")

    def redraw_icons(self, font_size):
        self.flag.setFixedSize(QtCore.QSize(font_size*4, font_size * 3))
        set_pixmap("flags/" + self.civ + ".webp", self.flag)
        self.worker_icon.setFixedSize(QtCore.QSize(font_size*9/4, font_size * 3))
        set_pixmap("overlay_icons/worker.png", self.worker_icon)
        self.military_icon.setFixedSize(QtCore.QSize(font_size*9/4, font_size * 3))
        set_pixmap("overlay_icons/military.png", self.military_icon)

    def update_player(self, player_data: Dict[str, Any]):
        self.civ = player_data['civ']
        set_pixmap("flags/" + player_data['civ'] + ".webp", self.flag)
        self.set_color(player_data['color'])

        self.name.setText(player_data['name'])
        self.worker.setText(str(int(float(player_data['worker']))))
        self.military.setText(str(int(float(player_data['military']))))

        self.show() if player_data['name'] else self.show(False)


class AoEOverlay(OverlayWidget):
    """Overlay widget showing AOE4 information """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.players = []
        self.setup_as_overlay()
        self.initUI()

    def setup_as_overlay(self):
        if settings.overlay_geometry is None:
            sg = QtWidgets.QDesktopWidget().screenGeometry(0)
            self.move(sg.width() - self.width() + 15, sg.top() - 20)
        else:
            self.move(settings.overlay_geometry[0], settings.overlay_geometry[1])

        self.setWindowTitle('AoE IV: Overlay')

    def initUI(self):
        self.playerlayout = QtWidgets.QGridLayout()
        self.playerlayout.setSpacing(0)
        self.playerlayout.setAlignment(QtCore.Qt.AlignRight
                                       | QtCore.Qt.AlignTop)
        self.setLayout(self.playerlayout)
        # Add players
        self.init_players()
        self.update_style(settings.font_size)

    def init_players(self):
        for i in range(8):
            self.players.append(PlayerWidget(i, self.playerlayout))
        [p.show(False) for p in self.players]

    def update_style(self, font_size: int):
        [p.redraw_icons(font_size) for p in self.players]

        self.setStyleSheet(
            #"QWidget{background: red}"
            "OverlayWidget{background: black}"
            f"QLabel {{font-size: {font_size}pt; color: white; font-weight: bold; margin-top: {font_size*2/3}px; margin-right: {font_size*2/3}px; min-width: {font_size*4}px}}"
            "QLabel#icon {margin-top: 0px; min-width: 0px; margin-right: 0px}"
            "QLabel#flag {min-width: 0px; margin-right: 0px}"
            )
        
        if self.isVisible():
            self.show()
            self.setFixedSize(self.playerlayout.totalSizeHint())

    def update_data(self, game_data: Dict[str, Any]):
        if not self.fixed:
            return

        [p.show(False) for p in self.players]
        for i, player in enumerate(game_data['players']):
            self.players[i].update_player(player)
        self.setFixedSize(self.playerlayout.totalSizeHint())

    def save_geometry(self):
        """ Saves overlay geometry into settings"""
        pos = self.pos()
        settings.overlay_geometry = [
            pos.x() + 8, pos.y() + 31
        ]
