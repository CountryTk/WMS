from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea


class Alert(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.layout_main = QVBoxLayout()
        self.parent = parent
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.container_widget = QWidget()
        self.scroll_area.setWidget(self.container_widget)
        self.container_layout = QVBoxLayout(self.container_widget)

        self.layout_main.addWidget(self.scroll_area)

        self.setLayout(self.layout_main)

