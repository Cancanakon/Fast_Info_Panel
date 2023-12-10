from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import time
import sys
import datetime
import threading
import PyQt5.QtWidgets
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from app.package.tdv_ui import Ui_main_TDV
from functions.getdata import dataThread
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from functions.gettime import dataThreadTime
import requests
from PyQt5.QtCore import QUrl, Qt
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

class Window(QMainWindow,QThread):

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        super().__init__(parent)
        self.ui = Ui_main_TDV()
        self.ui.setupUi(self)

        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)

        self.datathread = dataThread(self)
        self.datathread.dataChanged.connect(self.set1)
        self.datathread.start()

        self.datathread2 = dataThreadTime(self)
        self.datathread2.dataChangedTime.connect(self.set2)
        self.datathread2.start()

        self.ui.btn_ext.clicked.connect(self.closeEvent)

        self.webEngineView2 = QtWebEngineWidgets.QWebEngineView()
        self.webEngineView2.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.webEngineView2.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.webEngineView2.settings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        self.webEngineView2.page().fullScreenRequested.connect(lambda request: request.accept())
        baseUrl = "local"
        htmlString = """
<iframe width="1309" height="649" src="https://www.youtube.com/embed/uQV8yc4ZchM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>                                """

        self.webEngineView2.setHtml(htmlString, QUrl(baseUrl))
        self.ui.layout_Video.addWidget(self.webEngineView2)


    def set1(self, weatherDate, weatherDay, weatherIcon, weatherDescription, weatherDegree,
            weatherMinDegree, weatherMaxDegree, weatherHumidity,morningTime,sunTime,noonTime,
             afternoonTime,eveningTime,nightTime,pharmacyName,distPharmacy,
                              addressPharmacy,phonePharmacy,textVerseF):
        self.ui.lbl_date.setText(weatherDate)
        self.ui.lbl_day.setText(weatherDay)
        self.ui.lbl_weatherDescription.setText(weatherDescription)
        self.ui.lbl_degree.setText(f"{weatherMaxDegree} °")
        self.ui.lbl_minDegree.setText(f"{weatherMinDegree} °" )
        self.ui.lbl_maxDegree.setText(f"{weatherMaxDegree} °" )
        self.ui.lbl_humidity.setText(f"% {weatherHumidity} ")

        self.ui.lbl_imsak.setText(morningTime)
        self.ui.lbl_sun.setText(sunTime)
        self.ui.lbl_noon.setText(noonTime)
        self.ui.lbl_afternoon.setText(afternoonTime)
        self.ui.lbl_evening.setText(eveningTime)
        self.ui.lbl_night.setText(nightTime)

        self.ui.lbl_pharmacyName.setText(pharmacyName)
        self.ui.lbl_pharmacyDist.setText(distPharmacy)
        self.ui.lbl_pharmacyAddress.setText(addressPharmacy)
        self.ui.lbl_pharmacyPhone.setText(f"+90 {phonePharmacy}")

        self.ui.lbl_verse.setText(f"GÜNÜN AYETİ \n \n {textVerseF}")


        image = QImage()
        image.loadFromData(requests.get(f"{weatherIcon}").content)
        self.ui.lbl_WeatherIcon.setPixmap(QPixmap(image))

        image2 = QImage()
        image2.loadFromData(requests.get("https://www.tccb.gov.tr/assets/resim/icon/turk-bayragi.gif").content)
        self.ui.lbl_FlagIcon.setPixmap(QPixmap(image2))

        image3 = QImage()
        image3.loadFromData(requests.get("https://seeklogo.com/images/D/Diyanet-logo-A6F1F5C259-seeklogo.com.png").content)
        self.ui.lbl_TdvIcon.setPixmap(QPixmap(image3))

        image4 = QImage()
        image4.loadFromData(
            requests.get("https://firebasestorage.googleapis.com/v0/b/safewayapp.appspot.com/o/qrphone.png?alt=media&token=1ea0d529-9a6d-4c04-a636-0387ac2abdf4").content)
        self.ui.lbl_QRIcon2.setPixmap(QPixmap(image4))

        image5 = QImage()
        image5.loadFromData(
            requests.get(
                "https://firebasestorage.googleapis.com/v0/b/safewayapp.appspot.com/o/qrcode.png?alt=media&token=e2cf15d1-22b2-4e91-be20-a138cc9a8b42").content)
        self.ui.lbl_QRIcon1.setPixmap(QPixmap(image5))

        image6 = QImage()
        image6.loadFromData(
            requests.get(
                "https://firebasestorage.googleapis.com/v0/b/safewayapp.appspot.com/o/qrwebsite.png?alt=media&token=13d80f8c-c591-41d6-a1e1-2af14277e2ef").content)
        self.ui.lbl_QRIcon3.setPixmap(QPixmap(image6))

        image7 = QImage()
        image7.loadFromData(
            requests.get(
                "https://firebasestorage.googleapis.com/v0/b/safewayapp.appspot.com/o/militek_png.png?alt=media&token=8cead527-ebd1-45e9-88fb-6e4fcbbe4895").content)
        self.ui.lbl_EcgIcon.setPixmap(QPixmap(image7))



    def set2(self,value_time):
        self.ui.lbl_time.setText(value_time)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Uygulama Kapatma', 'Kapatmak İstediğinize Emin Misiniz?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            threadCount = QThreadPool.globalInstance().maxThreadCount()
            pool = QThreadPool.globalInstance()
            for i in range(threadCount):
                runnable = Runnable(i)
                pool.start(runnable)
            event.accept()
            print('Window closed')
        else:
            event.ignore()

app = QApplication(sys.argv)
win= Window()
win.show()
app.exec()

