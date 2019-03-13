from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTextEdit, QTabWidget, QSplitter, QPushButton, QLineEdit
import json
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtTest import QTest
from widgets.Scroll import ScrollArea
from widgets.Item import Item
from widgets.Alert_widget import Alert
import sqlite3
import shutil
from widgets.DataTemplate import Andmed
from urllib.request import urlopen, Request, urlretrieve
import bs4
import random
import os


class Tab(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.tabs = QTabWidget()
        self.horizontal = QSplitter(Qt.Vertical)

        self.seosed = QTabWidget()
        self.kahjumid = Alert(self)
        self.kasumid = Alert(self)
        self.alerts = Alert(self)
        self.read_only_text = QTextEdit()
        self.read_only_text.setReadOnly(True)
        self.read_only_text.setFixedHeight(50)

        self.bottom_button = QPushButton("Hüppa aruande lõppu")
        self.start_button = QPushButton("Hüppa aruande algusesse")

        self.bottom_button.clicked.connect(self.goto_bottom)
        self.start_button.clicked.connect(self.goto_start)

        self.update_thread = UpdateThread(self.parent)

        self.kogu_kahjum = []
        self.names = []
        self.kogu_kasum = []
        self.profit_or_not = None
        self.seosed.setMinimumHeight(150)

        self.tab_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        self.buttons_layout.addWidget(QLabel())  # Ignore these - box layout margins don't seem to do the job
        self.buttons_layout.addWidget(QLabel())
        self.buttons_layout.addWidget(self.start_button)
        self.buttons_layout.addWidget(self.bottom_button)
        self.buttons_layout.addWidget(QLabel())
        self.buttons_layout.addWidget(QLabel())

        self.horizontal.addWidget(self.tabs)
        self.horizontal.addWidget(self.seosed)

        self.kohalik = ScrollArea(self)
        self.tarnijad = ScrollArea(self)

        self.tab_layout.addWidget(self.horizontal)
        self.tab_layout.addLayout(self.buttons_layout)

        self.fill()

        self.alerts.container_layout.addWidget(self.read_only_text, Qt.AlignTop)

        self.tabs.addTab(self.kohalik, "Kohalik")
        self.tabs.addTab(self.tarnijad, "Tarnijad")
        self.seosed.addTab(self.kahjumid, "Kahjumid")
        self.seosed.addTab(self.kasumid, "Kasumid")
        self.index = self.seosed.addTab(self.alerts, "Märkused")

        self.setLayout(self.tab_layout)

        self.update_thread.done_signal.connect(lambda: self.read_only_text.append("Database updated, restarting application"))

        self.show_not_enough()
        self.diff()

    def fill(self):

        self.kohalik.container_layout.addWidget(Item("   Tootja", "Toode", "Jalanumber", "Kogus", "Hind", True, self))
        self.tarnijad.container_layout.addWidget(Item("   Tootja", "Toode", "Jalanumber", "Kogus", "Hind", True, self))
        self.temp = 0
        self.interesting_dict = {}
        self.another_interesting_dict = {}
        for data in self.get_kohalik_data():
            for info in self.get_data():

                if data[1] == info[1]:
                    self.names.append(data[1])

                    if data[4] < info[4]:
                        seis = "Kahjum"

                    elif data[4] > info[4]:
                        seis = "Kasum"

                    else:
                        seis = "Kasum/Kahjum"

                    tooltip_str = "<h3>Toote nimi: {}</h3><h3>Hind meil: {}€</h3><h3>Kogus meil: {} </h3>" \
                                  "<h3>Hind tarnijal: {}€</h3><h3>Kogus tarnijal: {}</h3><h3>{}: {}€</h3>".format(
                        data[1], data[4], data[3], info[4], info[3], seis, abs(info[4] - data[4]))
                    item = Item("{}. {}".format(self.temp, str(data[0])), str(data[1]),
                                str(data[2]), str(data[3]), str(data[4]), False, self, info[4], seis, abs(info[4]-data[4]), info[3])
                    item.setToolTip(tooltip_str)
                    self.kohalik.container_layout.addWidget(item)
                    self.interesting_dict[data[1]] = self.temp
                    self.temp += 1
                    break
        self.temp = 0
        for data in self.get_data():
            self.names.append(data[1])
            self.tarnijad.container_layout.addWidget(
                Item("{}. {}".format(self.temp, str(data[0])), str(data[1]), str(data[2]), str(data[3]), str(data[4]),
                     False))
            self.temp += 1
            self.another_interesting_dict[data[1]] = self.temp

        self.diff()

    def refresh(self):

        # First we delete all data inside
        for i in reversed(range(self.kohalik.container_layout.count())):
            # Since self.kohalik and self.tarnijad both have the same amount of items, we can use this for loop
            widgetToRemove = self.kohalik.container_layout.itemAt(i).widget()
            anotherWidgetToRemove = self.tarnijad.container_layout.itemAt(i).widget()
            self.kohalik.container_layout.removeWidget(widgetToRemove)
            self.tarnijad.container_layout.removeWidget(anotherWidgetToRemove)
            widgetToRemove.setParent(None)
            anotherWidgetToRemove.setParent(None)

        self.fill()

    def goto_start(self):

        self.kahjumid.scroll_area.verticalScrollBar().setValue(0)
        self.kasumid.scroll_area.verticalScrollBar().setValue(0)

    def goto_bottom(self):

        self.kahjumid.scroll_area.verticalScrollBar().setValue(self.kahjumid.scroll_area.verticalScrollBar().maximum())
        self.kasumid.scroll_area.verticalScrollBar().setValue(self.kasumid.scroll_area.verticalScrollBar().maximum())

    def refresh_db(self):

        self.seosed.setCurrentIndex(self.index)
        self.read_only_text.append("Databaasi uuendamine...")
        self.update_thread.start()
        # QTest.qWait(1500)
        # from database import Create
        # a = Create()
        # a.refresh_database()
        # self.read_only_text.append("Databaas uuendatud... tarkvara nüüd taaskäivitab ennast")
        # QTest.qWait(1000)
        # self.parent.parent.restart()

    def get_kohalik_data(self):

        connection = sqlite3.connect("inventuur.db")
        connection.commit()  # This assures that we have the latest data
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM kohalikud_andmed")
            return cursor.fetchall()
        except Exception as E:
            print("Something happened with the database... updating and restarting")
            from database import Create

            a = Create()

            a.init_db()
            a.refresh_database()

            self.parent.parent.restart()

    def get_data(self):

        connection = sqlite3.connect("inventuur.db")
        connection.commit()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM andmed")

        return cursor.fetchall()

    def not_enough(self):

        connection = sqlite3.connect("inventuur.db")
        connection.commit()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM kohalikud_andmed WHERE kogus < 20")

        return cursor.fetchall()

    def show_not_enough(self):

        data = self.not_enough()

        for data_tuple in data:
            if data_tuple[3] != 1:
                self.alerts.container_layout.addWidget(
                    QLabel("Toodet <b>{}</b> on liiga vähe (<b>{}</b> tükki)".format(data_tuple[1], data_tuple[3])))
            else:
                self.alerts.container_layout.addWidget(
                    QLabel("Toodet <b>{}</b> on liiga vähe (<b>{}</b> tükk)".format(data_tuple[1], data_tuple[3])))

    def diff(self):

        kohalik = self.get_kohalik_data()
        tarnijad = self.get_data()
        for hind_millega_meie_muume in kohalik:
            for hind_millega_me_ostame in tarnijad:
                try:
                    if hind_millega_meie_muume[4] < hind_millega_me_ostame[4] and hind_millega_me_ostame[1] == hind_millega_meie_muume[1]:
                        kahjum = hind_millega_me_ostame[4]-hind_millega_meie_muume[4]
                        kogu_kahjum = kahjum*hind_millega_me_ostame[3]
                        self.kahjumid.container_layout.addWidget(
                            QLabel("Tootja: {}".format(hind_millega_meie_muume[0])))
                        self.kahjumid.container_layout.addWidget(
                            QLabel("Toode: {} ".format(hind_millega_meie_muume[1])))
                        self.kahjumid.container_layout.addWidget(
                            QLabel("Hind millega me ostsime: {} eurot".format(hind_millega_me_ostame[4])))
                        self.kahjumid.container_layout.addWidget(
                            QLabel("Hind millega me müüme: {} eurot".format(hind_millega_meie_muume[4])))
                        self.kahjumid.container_layout.addWidget(
                            QLabel("Kogus: {}".format(hind_millega_meie_muume[3])))
                        self.kahjumid.container_layout.addWidget(
                            QLabel("{} toote hind: {} eurot".format(
                                hind_millega_meie_muume[3], hind_millega_meie_muume[4] * hind_millega_meie_muume[3])))
                        self.kahjumid.container_layout.addWidget(
                            QLabel("<p style=\"color: #FF0000;\">Iga müüdud toote pealt on kahjum:"
                                   " {} eurot, mis teeb kokku {} eurot</p>".format(kahjum, kogu_kahjum)))
                        self.kahjumid.container_layout.addWidget(QLabel("\n"))
                        self.kogu_kahjum.append(kogu_kahjum)
                        break
                    elif hind_millega_meie_muume[4] > hind_millega_me_ostame[4] and hind_millega_meie_muume[1] == hind_millega_me_ostame[1]:
                        kasum = hind_millega_meie_muume[4] - hind_millega_me_ostame[4]
                        kogu_kasum = kasum*hind_millega_meie_muume[3]
                        self.kasumid.container_layout.addWidget(
                            QLabel("Tootja: {}".format(hind_millega_meie_muume[0])))
                        self.kasumid.container_layout.addWidget(
                            QLabel("Toode: {} ".format(hind_millega_meie_muume[1])))
                        self.kasumid.container_layout.addWidget(
                            QLabel("Hind millega me ostsime: {} eurot".format(hind_millega_me_ostame[4])))
                        self.kasumid.container_layout.addWidget(
                            QLabel("Hind millega me müüme: {} eurot".format(hind_millega_meie_muume[4])))
                        self.kasumid.container_layout.addWidget(
                            QLabel("Kogus: {}".format(hind_millega_meie_muume[3])))
                        self.kasumid.container_layout.addWidget(
                            QLabel("{} toote hind: {} eurot".format(
                                hind_millega_meie_muume[3], hind_millega_meie_muume[3] * hind_millega_meie_muume[4])))
                        self.kasumid.container_layout.addWidget(
                            QLabel("<p style=\"color: #007F00;\">Iga müüdud toote pealt on kasum:"
                                   " {} eurot, mis teeb kokku {} eurot</p>".format(kasum, kogu_kasum)))
                        self.kasumid.container_layout.addWidget(QLabel("\n"))
                        self.kogu_kasum.append(kogu_kasum)
                        break
                except TypeError as E:
                    print(E)
        self.kahjumid.container_layout.addWidget(
            QLabel("<p style=\"color: #FF0000;\">Kogu kahjum on: {} eurot</p>".format(sum(self.kogu_kahjum))))

        self.kasumid.container_layout.addWidget(
            QLabel("<p style=\"color: #007F00;\">Kogu kasum on: {} eurot</p>".format(sum(self.kogu_kasum))))

        if sum(self.kogu_kasum) - sum(self.kogu_kahjum) > 0:
            self.profit_or_not = "kasumiks"

        else:
            self.profit_or_not = "kahjumiks"

        self.kahjumid.container_layout.addWidget(
            QLabel("<b>Arvestades kogu kasumist maha kogu kahjumi, jääb {} {} eurot".format(
                self.profit_or_not, sum(self.kogu_kasum) - sum(self.kogu_kahjum))))
        self.kasumid.container_layout.addWidget(
            QLabel("<b>Arvestades kogu kasumist maha kogu kahjumi, jääb {} {} eurot".format(
                self.profit_or_not, sum(self.kogu_kasum) - sum(self.kogu_kahjum))))


class UpdateThread(QThread):

    done_signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.nike_tooted = []
        self.gucci_tooted = []

    def start(self):

        self.refresh_database()

        self.done_signal.emit(True)
        print(self.parent.parent.restart())

    def collect_data(self):

        os.mkdir("images/")

        try:

            nike_url = Request("https://store.nike.com/us/en_us/pw/shoes/oi3?ipp=120")

            opened_nike_url = urlopen(nike_url).read()
            nike_object = bs4.BeautifulSoup(opened_nike_url, 'lxml')
            for sneaker_div in nike_object.find_all("div", class_="grid-item fullSize"):
                image = sneaker_div.find('img')['src']
                data = sneaker_div.find("p", class_="product-display-name").text
                image_path = os.path.join("images/", data)
                urlretrieve(image, image_path)
                print("Collecting Nike product data {}".format(image_path))
                needed_url = sneaker_div.find("a")['href']

                if len(data) > 45:
                    data = data[:45]

                self.nike_tooted.append(data)

            gucci_url = Request("https://www.gucci.com/us/en/ca/men/mens-shoes/mens-sneakers-c-men-shoes-sneakers", headers={'User-Agent': "Mozilla/5.0"})
            opened_a_url = urlopen(gucci_url).read()
            gucci_object = bs4.BeautifulSoup(opened_a_url, 'lxml')

            for gucci_div in gucci_object.find_all("div", class_="product-tiles-grid-item-image"):
                for image_tag in gucci_div.find_all("img"):
                    data = image_tag['alt']
                    image = image_tag['src']
                    image_path = os.path.join("images/", data)
                    urlretrieve("https:" + image, image_path)
                    print("Collecting Gucci product data {}".format(image_path))
                    if len(data) > 45:
                        data = data[:45]

                    self.gucci_tooted.append(data)

        except Exception as E:
            print(E)

    def add_data(self):

        try:
            shutil.rmtree("images/")
        except FileNotFoundError as E:
            print(E)

        self.collect_data()
        try:
            connection = sqlite3.connect("inventuur.db")
            cursor = connection.cursor()
            """
            We make sure to sort the products so it'd be easier to read
            """
            new_nike = list(set(self.nike_tooted))
            # new_nike.sort()
            new_gucci = list(set(self.gucci_tooted))
            # new_gucci.sort()
            for item in new_nike:  # This is to prevent any duplicates
                ok = Andmed("Nike", item, random.randint(30, 49), random.randint(0, 603), random.randint(100,190))
                cursor.execute("INSERT INTO andmed VALUES (?, ?, ?, ?, ?)", (ok.tootja, ok.toode, ok.jalanumber, ok.kogus, ok.hind))

            for item in new_gucci:
                ok = Andmed("Gucci", item, random.randint(30, 49), random.randint(0, 30), random.randint(400, 2500))
                cursor.execute("INSERT INTO andmed VALUES (?, ?, ?, ?, ?)", (ok.tootja, ok.toode, ok.jalanumber, ok.kogus, ok.hind))

            for item in new_nike:  # This is to prevent any duplicates
                ok = Andmed("Nike", item, random.randint(30, 49), random.randint(0, 603), random.randint(100,190))
                cursor.execute("INSERT INTO kohalikud_andmed VALUES (?, ?, ?, ?, ?)", (ok.tootja, ok.toode, ok.jalanumber, ok.kogus, ok.hind))

            for item in new_gucci:
                ok = Andmed("Gucci", item, random.randint(30, 49), random.randint(0, 30), random.randint(400, 2500))
                cursor.execute("INSERT INTO kohalikud_andmed VALUES (?, ?, ?, ?, ?)", (ok.tootja, ok.toode, ok.jalanumber, ok.kogus, ok.hind))

            connection.commit()
            connection.close()
        except Exception as E:
            with open("log.txt", "a") as log:
                log.write(str(E))

        print("Finished adding content into the database!")

        for filename in os.listdir("images/"):
            os.rename("images/" + filename, "images/" + filename + ".jpeg")

    def refresh_database(self):
        print("Refreshing database")
        try:
            with open("debug.txt", "a") as debug:
                connection = sqlite3.connect("inventuur.db")
                debug.write("Refresh database, connection initated")
                cursor = connection.cursor()

                cursor.execute("delete from andmed")
                cursor.execute("delete from kohalikud_andmed")
                debug.write("Refresh database, tables deleted.")
                connection.commit()
                connection.close()
                debug.close()
        except Exception as E:
            with open("log.txt", "a") as log:
                log.write(str(E))

        self.add_data()
