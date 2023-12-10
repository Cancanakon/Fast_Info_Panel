import requests
import json
import http.client
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QValidator
import time
import sys
import threading
import datetime
import PyQt5.QtWidgets
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
import json
from PyQt5.QtWidgets import QApplication, QWidget
import random
from functions.gettime import dataThreadTime





class dataThread(QThread):

    dataChanged = pyqtSignal(str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str,str)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):

        while True:

            collectapi1 = http.client.HTTPSConnection('api.collectapi.com')
            collectapi2 = http.client.HTTPSConnection('api.collectapi.com')
            collectapi3 = http.client.HTTPSConnection('api.collectapi.com')
            collectapi4 = http.client.HTTPSConnection('api.collectapi.com')

            headers = {
                'content-type': "application/json",
                'authorization': "_YOUR_API_KEY_"
            }

            randomNumberSurah = random.randint(3, 100)
            randomNumberVerse = random.randint(1, 3)
            verseRequest = requests.get(
                f"https://api.acikkuran.com/surah/{randomNumberSurah}/verse/{randomNumberVerse}/translations")
            textVerse = verseRequest.json()

            collectapi1.request("GET", "/weather/getWeather?data.lang=tr&data.city=karabuk", headers=headers)
            resWeather = collectapi1.getresponse()
            dataWeather = resWeather.read().decode("utf-8")
            resultWeather = json.loads(dataWeather)

            weatherDate = resultWeather['result'][0]['date']
            weatherDay = resultWeather['result'][0]['day']
            weatherIcon = resultWeather['result'][0]['icon']
            weatherDescription = resultWeather['result'][0]['description']
            weatherDegree = resultWeather['result'][0]['degree']
            weatherMinDegree = resultWeather['result'][0]['min']
            weatherMaxDegree = resultWeather['result'][0]['max']
            weatherHumidity = resultWeather['result'][0]['humidity']


            collectapi2.request("GET", "/pray/all?data.city=karabuk", headers=headers)

            resPrayTime = collectapi2.getresponse()
            dataPrayTime = resPrayTime.read().decode("utf-8")
            resultPrayTime = json.loads(dataPrayTime)


            morningTime = resultPrayTime['result'][0]['saat']
            sunTime = resultPrayTime['result'][1]['saat']
            noonTime = resultPrayTime['result'][2]['saat']
            afternoonTime = resultPrayTime['result'][3]['saat']
            eveningTime = resultPrayTime['result'][4]['saat']
            nightTime = resultPrayTime['result'][5]['saat']


            collectapi3.request("GET", "/health/dutyPharmacy?ilce=merkez&il=Karabuk", headers=headers)
            resPharmacy = collectapi3.getresponse()
            dataPharmacy = resPharmacy.read().decode("utf-8")
            resultPharmacy = json.loads(dataPharmacy)


            pharmacyName = resultPharmacy['result'][0]['name']
            distPharmacy = resultPharmacy['result'][0]['dist']
            addressPharmacy = resultPharmacy['result'][0]['address']
            phonePharmacy = resultPharmacy['result'][0]['phone']



            textVerseF =  textVerse['data'][0]['text']


            self.dataChanged.emit(weatherDate,weatherDay,weatherIcon,weatherDescription,weatherDegree,
                                  weatherMinDegree,weatherMaxDegree,weatherHumidity,morningTime,sunTime,noonTime,
                                         afternoonTime,eveningTime,nightTime,pharmacyName,distPharmacy,
                                  addressPharmacy,phonePharmacy,textVerseF)

            time.sleep(28800)
