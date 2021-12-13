from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, \
    QHBoxLayout
from PyQt5 import QtWebEngineWidgets
from api_access import getWeatherInfos
import sys
import folium
import io


class WeatherWidget(QWidget):

    init = 1

    def __init__(self, parent):
        super().__init__(parent=parent)

        # Main layout
        self.layout = QVBoxLayout()

        if self.init:
            lat = QLineEdit("43.5571085")
            lon = QLineEdit("1.4684552")
            lat = float(lat.text())
            lon = float(lon.text())
            self.m = folium.Map(location=[lat, lon], zoom_start=13)
            self.data = io.BytesIO()
            self.m.save(self.data, close_file=False)
            self.carte = QtWebEngineWidgets.QWebEngineView()
            self.carte.setHtml(self.data.getvalue().decode())
            self.layout.addWidget(self.carte)
            self.init = 0

        # Text Zone
        self.lineEditLat = QLineEdit("43.5571085")
        self.lineEditLon = QLineEdit("1.4684552")
        self.layout.addWidget(QLabel("Latitude"))
        self.layout.addWidget(self.lineEditLat)
        self.layout.addWidget(QLabel("Longitude"))
        self.layout.addWidget(self.lineEditLon)

        # Ville
        self.labelIconCity = QLabel(self)
        pixmap = QPixmap('Icons/paysage-urbain.png')
        pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio)
        self.labelIconCity.setPixmap(pixmap)
        self.labelIconCity.setAlignment(Qt.AlignCenter)
        self.labelCity = QLabel("Ville")
        # Layout ville
        hLayoutVille = QHBoxLayout()
        hLayoutVille.addWidget(self.labelIconCity)
        hLayoutVille.addWidget(self.labelCity)

        # Temperature
        self.labelIconTemp = QLabel(self)
        pixmap = QPixmap('Icons/capteur-de-temperature.png')
        pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio)
        self.labelIconTemp.setPixmap(pixmap)
        self.labelIconTemp.setAlignment(Qt.AlignCenter)
        self.labelTemp = QLabel("Température")
        # Layout temperature
        hLayoutTemp = QHBoxLayout()
        hLayoutTemp.addWidget(self.labelIconTemp)
        hLayoutTemp.addWidget(self.labelTemp)

        # Validation button
        self.validateButton = QPushButton("Valider")
        self.validateButton.clicked.connect(self.getWeatherInfos)
        self.layout.addWidget(self.validateButton)

        # Display infos
        self.layout.addLayout(hLayoutTemp)
        self.layout.addLayout(hLayoutVille)
        self.setLayout(self.layout)

    def getWeatherInfos(self):
        # Update labelled infos
        weatherDict = getWeatherInfos(float(self.lineEditLat.text()), float(self.lineEditLon.text()))
        self.labelCity.setText(weatherDict['name'])
        self.labelTemp.setText(str(round(weatherDict['main']['temp'] - 273.15, 2)) + " °C")

        # Update map
        lat = float(self.lineEditLat.text())
        lon = float(self.lineEditLon.text())
        self.m = folium.Map(location=[lat, lon], zoom_start=13)
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)
        self.carte = QtWebEngineWidgets.QWebEngineView()
        self.carte.setHtml(self.data.getvalue().decode())
        self.layout.replaceWidget(self.layout.itemAt(0).widget(), self.carte)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        weatherWidget = WeatherWidget(self)
        self.setWindowTitle("Quel temps fait-il donc ?")
        self.resize(600, 450)
        self.setCentralWidget(weatherWidget)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
