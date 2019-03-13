from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFrame, QPushButton
from widgets.Popup import Window
from PyQt5.QtCore import QThread
from urllib.request import urlopen
import bs4
import random


class Item(QFrame):

    def __init__(self, tootja, toode, jalanumber, kogus, hind, bold, parent=None, tarnija_hind=None, kasum_kahjum=None, kasum=None, tarnija_kogus=None):
        super().__init__()

        if bold:
            self.setStyleSheet("QLabel { font-weight: bold; font-size: 15;}")

        self.layout_main = QHBoxLayout()

        self.tootja = tootja
        self.parent = parent
        self.popup_window = Window(str(toode), toode, jalanumber, kogus, hind, self, tarnija_hind, kasum_kahjum, kasum, tarnija_kogus)

        self.toode = toode
        self.jalanumber = jalanumber
        self.kogus = kogus
        self.hind = hind
        self.tootja_label = QLabel(self.tootja)
        self.toote_label = QLabel(self.toode)
        self.jala_label = QLabel(self.jalanumber)
        self.kogus_label = QLabel(self.kogus)
        self.hind_label = QLabel(self.hind)

        self.layout_main.addWidget(self.tootja_label)
        self.layout_main.addWidget(self.toote_label)
        self.layout_main.addWidget(self.jala_label)
        self.layout_main.addWidget(self.kogus_label)
        self.layout_main.addWidget(self.hind_label)

        self.setLayout(self.layout_main)

    def mousePressEvent(self, event):

        self.popup_window.show_()
