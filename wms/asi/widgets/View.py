from PyQt5.QtWidgets import QWidget, QHBoxLayout
from widgets.Sidebar import Sidebar
from widgets.Table import Tab
"""
This is the main view of the whole project, all the UI logic is handled here
"""


class View(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.parent = parent
        self.info_area = Tab(self)

        # self.sidebar = Sidebar()

        # self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.info_area)

        self.setLayout(self.layout)
