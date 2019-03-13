from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.testlabel = QLabel("Data")

        self.layout.addWidget(self.testlabel)

        self.setLayout(self.layout)


