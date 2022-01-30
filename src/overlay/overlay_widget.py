 # 29 Januray 2022 - Modified by KuschAoe

from typing import Any, Dict

from PyQt5 import QtCore, QtGui, QtWidgets

from overlay.custom_widgets import OverlayWidget, VerticalLabel
from overlay.helper_func import file_path
from overlay.settings import settings

PIXMAP_CACHE = {}


def set_pixmap(civ: str, widget: QtWidgets.QWidget):
    """ Sets civ pixmap to a widget. Handles caching."""
    if civ in PIXMAP_CACHE:
        widget.setPixmap(PIXMAP_CACHE[civ])
        return
    path = file_path(f"img/flags/{civ}.webp")
    pixmap = QtGui.QPixmap(path)
    pixmap = pixmap.scaled(widget.width(), widget.height())
    PIXMAP_CACHE[civ] = pixmap
    widget.setPixmap(pixmap)


class PlayerWidget:
    """ Player widget shown on the overlay"""
    def __init__(self, row: int, toplayout: QtWidgets.QGridLayout):
        self.team: int = 0
        self.civ: str = ""
        self.visible = True
        self.create_widgets()
        self.name.setStyleSheet("font-weight: bold")
        self.name.setContentsMargins(5, 0, 10, 0)
        self.worker.setStyleSheet("color: yellow")
        self.military.setStyleSheet("color: red")

        for column, widget in enumerate((self.flag, self.name, self.worker, self.military)):
            toplayout.addWidget(widget, row, column)

    def create_widgets(self):
        # Separated so this can be changed in a child inner overlay for editing
        self.flag = QtWidgets.QLabel()
        self.flag.setFixedSize(QtCore.QSize(60, 30))
        self.name = QtWidgets.QLabel()
        self.worker = QtWidgets.QLabel()
        self.military = QtWidgets.QLabel()

    def show(self, show: bool = True):
        self.visible = show
        """ Shows or hides all widgets in this class """
        for widget in (self.flag, self.name, self.worker, self.military):
            widget.show() if show else widget.hide()

    def update_name_color(self):
        color = settings.team_colors[(self.team - 1) %
                                     len(settings.team_colors)]
        color = tuple(color)
        self.name.setStyleSheet("font-weight: bold; "
                                "background: QLinearGradient("
                                "x1: 0, y1: 0,"
                                "x2: 1, y2: 0,"
                                f"stop: 0 rgba{color},"
                                f"stop: 0.8 rgba{color},"
                                "stop: 1 rgba(0,0,0,0))")

    def update_flag(self):
        set_pixmap(self.civ, self.flag)

    def update_player(self, player_data: Dict[str, Any]):
        # Flag
        self.civ = player_data['civ']
        self.update_flag()

        # Indicate team with background color
        self.team = player_data['team']
        self.update_name_color()

        # Fill the rest
        self.name.setText(player_data['name'])
        self.worker.setText(player_data['worker'])
        self.military.setText(player_data['military'])

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
            self.setGeometry(0, 0, 700, 400)
            sg = QtWidgets.QDesktopWidget().screenGeometry(0)
            self.move(sg.width() - self.width() + 15, sg.top() - 20)
        else:
            self.setGeometry(*settings.overlay_geometry)

        self.setWindowTitle('AoE IV: Overlay')

    def initUI(self):
        # Layouts & inner frame
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        self.setLayout(layout)

        self.inner_frame = QtWidgets.QFrame()
        self.inner_frame.setObjectName("inner_frame")
        layout.addWidget(self.inner_frame)
        self.playerlayout = QtWidgets.QGridLayout()
        self.playerlayout.setContentsMargins(10, 20, 20, 10)
        self.playerlayout.setHorizontalSpacing(10)
        self.playerlayout.setAlignment(QtCore.Qt.AlignRight
                                       | QtCore.Qt.AlignTop)
        self.inner_frame.setLayout(self.playerlayout)
        self.update_style(settings.font_size)

        # Header
        worker = QtWidgets.QLabel("Worker")
        worker.setStyleSheet("color: yellow; font-weight: bold")
        military = QtWidgets.QLabel("Military")
        military.setStyleSheet("color: red; font-weight: bold")
        
        for column, widget in enumerate(
            (worker, military)):
            self.playerlayout.addWidget(widget, 0, column + 2)

        # Add players
        self.init_players()

    def init_players(self):
        for i in range(8):
            self.players.append(PlayerWidget(i + 1, self.playerlayout))

    def update_style(self, font_size: int):
        self.setStyleSheet(
            "QWidget{background: #000000}"
            f"QLabel {{font-size: {font_size}pt; color: white }}"
            "QFrame#inner_frame"
            "{"
            "background: QLinearGradient("
            "x1: 0, y1: 0,"
            "x2: 1, y2: 0,"
            "stop: 0 rgba(0,0,0,0),"
            "stop: 0.1 rgba(0,0,0,0.5),"
            "stop: 1 rgba(0,0,0,1))"
            "}")

        if self.isVisible():
            self.show()

    def update_data(self, game_data: Dict[str, Any]):
        [p.show(False) for p in self.players]

        for i, player in enumerate(game_data['players']):
            self.players[i].update_player(player)

    def save_geometry(self):
        """ Saves overlay geometry into settings"""
        pos = self.pos()
        settings.overlay_geometry = [
            pos.x(), pos.y(), self.width(),
            self.height()
        ]
