import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp
from PyQt5.QtGui import QFont, QGuiApplication, QCursor
import sys
from widgets.View import View
from widgets.EditorWindow import Window


class Main(QMainWindow):
    def __init__(self, first_time):
        super().__init__()

        self.view = View(self)

        self.first_time = first_time

        if self.first_time:
            self.setup_everything()

        self.refresh()
        self.input_data()
        self.aruanne()
        self.init_ui()

        self.setCentralWidget(self.view)

    def setup_everything(self):
        pass

    def init_ui(self):

        menubar = self.menuBar()

        fileMenu = menubar.addMenu("Tööriistad")
        fileMenu.addAction(self.refreshAct)
        fileMenu.addAction(self.inputAct)

        createMenu = menubar.addMenu("Aruanne")
        createMenu.addAction(self.aruandeAct)

    def aruanne(self):
        self.aruandeAct = QAction("Koosta aruanne")
        self.aruandeAct.setStatusTip("Koosta aruanne")
        self.aruandeAct.setShortcut("Ctrl+C")
        self.aruandeAct.triggered.connect(lambda: print("Creating a report!"))

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

    def move_cursor(self, point):

        screen = QGuiApplication.primaryScreen()

        cursor = QCursor()

        # cursor.setPos(self.mapToGlobal(point))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    try:
        first_time_being_run = open("first_time.txt", "r")

        if first_time_being_run.read():  # First time the program has been run
            holder = True
        else:
            holder = False

    except FileNotFoundError as E:
        print(E)
        holder = None

    ex = Main(holder)
    ex.showMaximized()
    sys.exit(app.exec_())
