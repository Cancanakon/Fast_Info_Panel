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

class dataThreadTime(QThread):

    dataChangedTime = pyqtSignal(str)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        while True:
            now = datetime.datetime.now()
            second = now.second
            minute = now.minute
            hour = now.hour
            value_time = (f'SAAT : {hour}:{minute}:{second}')
            self.dataChangedTime.emit(value_time)
            time.sleep(1)
