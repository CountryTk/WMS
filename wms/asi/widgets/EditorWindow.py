from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QPlainTextEdit, QFrame, QPushButton, \
    QTableView
from PyQt5.QtGui import QFont
import sqlite3
import os
import sys
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtCore import Qt


class Window(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        self.submit_button = QPushButton("Kanna muudatused sisse")
        self.submit_button.setFixedWidth(200)

        self.submit_button.clicked.connect(lambda: os.execl(sys.executable, sys.executable, *sys.argv))

        self.table_view = QTableView()

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("inventuur.db")

        if not self.db.open():
            print("Something went horribly wrong, you probably deleted your database...")
            os._exit(1)

        self.button_layout.addWidget(self.submit_button, Qt.AlignLeft)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        self.fill()

    def get_data(self):  # Leiame andmed, mida saaksime muuta, sama funktsioon mis Table.py's

        connection = sqlite3.connect("inventuur.db")
        query = QSqlQuery(self.db)
        query.exec("select * from kohalikud_andmed")

        while query.next():
            print(query.value(0))
            print(query.value(1))
            print(query.value(2))
            print(query.value(3))
            print(query.value(4))

    def fill(self):

        self.db_model = QSqlTableModel(self, self.db)
        self.db_model.setTable("kohalikud_andmed")
        self.db_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.db_model.select()
        self.db_model.setHeaderData(0, Qt.Horizontal, "Tootja")
        self.db_model.setHeaderData(1, Qt.Horizontal, "Toode")
        self.db_model.setHeaderData(2, Qt.Horizontal, "Jalanumber")
        self.db_model.setHeaderData(3, Qt.Horizontal, "Kogus")
        self.db_model.setHeaderData(4, Qt.Horizontal, "Hind")

        self.table_view.setModel(self.db_model)
        self.table_view.resizeColumnsToContents()
        self.layout.addWidget(self.table_view)

    def refresh(self):
        # First we delete all data inside

        self.fill()

    def run_sql(self):

        command = self.sql_area.toPlainText()

        connection = sqlite3.connect("inventuur.db")
        cursor = connection.cursor()

        cursor.execute(command)

        self.refresh()
