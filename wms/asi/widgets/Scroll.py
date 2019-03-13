from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QLineEdit, QPushButton, QLabel, QBoxLayout
from widgets.Item import Item
from PyQt5.QtCore import Qt


class ScrollArea(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.layout_main = QVBoxLayout()
        self.search_layout = QHBoxLayout()
        self.search_layout.addStretch()
        self.search_layout.setDirection(QBoxLayout.RightToLeft)
        self.search_layout.setSpacing(0)
        self.search_layout.setContentsMargins(0, 0, 0, 0)

        self.search_bar = QLineEdit()
        self.search_bar.setMaximumWidth(250)
        self.search_bar.setPlaceholderText("Kirjuta otsingusona siia")

        self.search_button = QPushButton("Otsi")
        self.search_button.setMaximumWidth(100)
        self.edasi = QPushButton("Järgmine")
        self.edasi.setMaximumWidth(100)
        self.edasi.clicked.connect(self.jargmine)
        self.search_button.clicked.connect(self.search)
        self.index = 0
        self.search_layout.addWidget(self.edasi)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.search_bar)
        # self.layout_main.addLayout(self.search_layout)

        self.value_tuple = ()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.container_widget = QWidget()

        self.scroll_area.setWidget(self.container_widget)
        self.container_layout = QVBoxLayout(self.container_widget)
        self.container_layout.setContentsMargins(0, 30, 0, 30)

        self.layout_main.addWidget(self.scroll_area)
        self.setLayout(self.layout_main)

    def find_all(self, a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1:
                return
            yield start
            start += len(sub)  # use start += 1 to find overlapping matches

    def search(self):

        text = self.search_bar.text()
        self.lmao_list = []
        a = 0
        # print(self.container_layout.itemAt(0).widget.geometry())
        self.margin = self.scroll_area.verticalScrollBar().maximum() // 33
        self.indexes = []
        li = list(set(self.parent.names))
        # li.sort()
        for l in li:

            result = list(self.find_all(l, text))

            self.lmao_list.append(result)

        for index, a in enumerate(self.lmao_list):
            if a != []:
                self.indexes.append(index)

    def jargmine(self):
        try:
            # self.scroll_area.verticalScrollBar().setValue(self.margin * self.indexes[self.index])
            x = self.parent.kohalik.container_layout.itemAt(self.indexes[self.index + 1]).widget()
            print(x.toode)
            x.toode = "<b>{}</b>".format(x.toode)
            from widgets.Item import Item
            oh = Item(x.tootja, x.toode, x.jalanumber, x.kogus, x.hind, False)
            print(oh.toode)
            self.parent.kohalik.container_layout.removeWidget(self.parent.kohalik.container_layout.itemAt(self.indexes[self.index + 1]).widget())
            self.parent.kohalik.container_layout.insertWidget(self.indexes[self.index + 1], oh)
        except IndexError:
            self.index = 0
        self.index += 1
