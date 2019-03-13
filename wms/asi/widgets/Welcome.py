from PyQt5.QtWidgets import QVBoxLayout, \
    QLabel, QWidget, QProgressBar, QDesktopWidget
from PyQt5 import QtTest
from PyQt5.QtCore import QProcess
from PyQt5.QtCore import Qt
import os
import random


class Welcome(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.setWindowFlags(
            Qt.Widget |
            Qt.WindowCloseButtonHint |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )

        self.setStyleSheet("""
        
        QWidget {
        
            background-color: #434343;
        }
        
        QLabel {
        
            background-color: transparent;
            color: white;
        }
        
        """)

        self.progress_bar = QProgressBar()
        self.label = QLabel("""
        <h3> ASI E-poe laoülevaate tarkvara </h3>
        """)

        self.layout.addWidget(self.label)

        self.update_label = QLabel()
        self.layout.addWidget(self.update_label)
        self.layout.addWidget(self.progress_bar)

        self.setLayout(self.layout)

        self.desktop = QDesktopWidget()

        self.label_width = 150
        self.label_height = 150

        self.screenWidth = self.desktop.screen().width()

        self.screenHeight = self.desktop.screen().height()

        self.x = (self.screenWidth - self.label_width) // 2
        self.y = (self.screenHeight - self.label_height) // 2

        self.resize(self.label_width, self.label_height)
        self.move(self.x - 150, self.y - 100)

        self.show()

        self.show_loading()

    def show_loading(self):

        if os.path.isfile("inventuur.db"):  # File exists, setting up is unnecessary
            return "no"

        self.update_label.setText("Setting up the database...")
        from database import Create
        a = Create()
        for i in range(101):
            self.progress_bar.setValue(i)
            x = random.randint(1, 100) 
            QtTest.QTest.qWait(x)

            if i == 25:
                a.init_db()
                self.update_label.setText("Database initialized...")

            if i == 60:
                self.update_label.setText("Collecting data...")
                QtTest.QTest.qWait(1000)
                a.add_data()
                self.update_label.setText("Database filled...")

        self.hide()
        self.start()

    def start(self):

        self.process = QProcess()

        self.process.startDetached("python3 asi.py")

    def closeEvent(self, a0):

        os._exit(1)

