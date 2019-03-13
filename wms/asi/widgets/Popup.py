from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QMainWindow
from PyQt5.QtGui import QPixmap, QCursor, QScreen, QGuiApplication
from PyQt5.QtCore import Qt
import random
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView
except ModuleNotFoundError as E:
    print(E)


class Window(QWidget):

    def __init__(self, image, toode, jalanumber, kogus, hind, parent=None, tarnija_hind=None, kasum_kahjum=None, kasum=None, tarnija_kogus=None):
        super().__init__()

        self.setWindowFlags(
            Qt.Widget |
            Qt.WindowCloseButtonHint |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )

        self.parent = parent

        self.image = image
        picture = "images/" + self.image + ".jpeg"

        self.label = QLabel(self)
        self.name_label = QLabel("<h3 style=\"color: #{}\">{}</h3>".format(self.gen_hex_colour_code(), toode))

        self.pixmap = QPixmap(picture)

        self.label.setPixmap(self.pixmap)

        self.hind_label = QLabel("<h3 style=\"color: #{}\">Meie hind: {} eurot</h3>".format("5B86E5", hind))
        self.kogus_label = QLabel(
            "<h3 style=\"color: #{}\">Kogus poes: {}</h3>".format("5B86E5", kogus))
        self.tarnija_hind_label = QLabel(
            "<h3 style=\"color: #{}\">Tarnija hind: {} eurot</h3>".format("5B86E5", tarnija_hind))
        self.tarnija_kogus_label = QLabel(
            "<h3 style=\"color: #{}\">Tarnija kogus: {}</h3>".format("5B86E5", tarnija_kogus))
        self.kasum_label = QLabel(
            "<h3 style=\"color: #{}\">{}: {} eurot</h3>".format("5B86E5", kasum_kahjum, kasum))


        self.layout_main = QVBoxLayout()
        self.image_layout = QHBoxLayout()
        self.profit_layout = QVBoxLayout()

        self.image_layout.addWidget(self.name_label)

        self.image_layout.addWidget(self.label)

        self.profit_layout.addWidget(self.hind_label)
        self.profit_layout.addWidget(self.kogus_label)
        self.profit_layout.addWidget(self.tarnija_hind_label)
        self.profit_layout.addWidget(self.tarnija_kogus_label)
        self.profit_layout.addWidget(self.kasum_label)

        self.layout_main.addLayout(self.image_layout)
        self.layout_main.addLayout(self.profit_layout)

        self.setFocusPolicy(Qt.StrongFocus)

        self.setLayout(self.layout_main)

    def gen_hex_colour_code(self):
        return ''.join([random.choice('0123456789ABCDEF') for x in range(6)])

    def leaveEvent(self, QEvent):
        self.hide()

    def show_(self):
        try:
            main_class = self.parent.parent.parent.parent

            window_pos = self.pos()

            main_class.move_cursor(window_pos.x(), window_pos.y())

            self.show()
        except AttributeError:
            pass
