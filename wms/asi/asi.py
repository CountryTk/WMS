import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp
from PyQt5.QtGui import QFont, QGuiApplication, QCursor
import sys
from widgets.View import View
from widgets.Welcome import Welcome
from resources.style import blue
from widgets.EditorWindow import Window


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = View(self)

        self.refresh()
        self.input_data()
        self.init_ui()


        self.setCentralWidget(self.view)

    def init_ui(self):

        menubar = self.menuBar()

        fileMenu = menubar.addMenu("Tööriistad")
        fileMenu.addAction(self.refreshAct)
        fileMenu.addAction(self.inputAct)

    def input_data(self):

        self.inputAct = QAction("Muuda andmeid")
        self.inputAct.setStatusTip("Muuda kohaliku inventuuri andmeid")
        self.inputAct.setShortcut("Ctrl+M")
        self.inputAct.triggered.connect(self.input_window)

    def refresh(self):

        self.refreshAct = QAction("Uuenda databaasi")
        self.refreshAct.setStatusTip("Uuendab databaasi")
        self.refreshAct.setShortcut("Ctrl+U")
        self.refreshAct.triggered.connect(self.refresh_db)

    def input_window(self):

        window = Window(self)
        index = self.view.info_area.tabs.addTab(window, "Muuda andmeid")

        self.view.info_area.tabs.setCurrentIndex(index)

    def refresh_db(self):

        self.view.info_area.refresh_db()

    def restart(self):

        os.execl(sys.executable, sys.executable, *sys.argv)

    def move_cursor(self, x, y):

        screen = QGuiApplication.primaryScreen()

        cursor = QCursor()

        cursor.setPos(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.setStyleSheet(blue)
    ex.showMaximized()
    sys.exit(app.exec_())
