import sys
import time
import RPi.GPIO as GPIO
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtQuick import *
from flowmeter import *
import locale
import urllib
import urllib2
import json

class Main(QObject):
    flowLevel = 0
    currentTime = 0

    pourLevel1 = 0
    pourLevel2 = 0

    totalAmount1 = 18.5
    totalAmount2 = 16.2

    pourLevelTime = 0
    lastPourLevel1 = 0
    lastPourLevel2 = 0

    pourTime = 0
    isPouring = False

    totalConsume = 0

    def __init__(self, parent=None):
        locale.setlocale(locale.LC_NUMERIC, 'nb_NO.UTF-8')

        QObject.__init__(self)
        self.engine = QQmlApplicationEngine(self)
        self.engine.load(QUrl.fromLocalFile('bardisplay.qml'))
        self.window = self.engine.rootObjects()[0]

        self.updatePour()

        self.pourTimer = QTimer()
        self.pourTimer.timeout.connect(self.updatePour)
        self.pourTimer.start(500)

        self.spotifyTimer = QTimer()
        self.spotifyTimer.timeout.connect(self.updateSpotifyInfo)
        self.spotifyTimer.start(5000)

        self.initKeyValues()
        self.initGpio()

        self.updateConsume()
    def show(self):
        self.window.showFullScreen()
        #self.window.show()

    def initGpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(23, GPIO.RISING, callback=self.tickFlow1, bouncetime=20)

        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(24, GPIO.RISING, callback=self.tickFlow2, bouncetime=20)

        self.fm1 = FlowMeter('metric', ["beer"])
        self.fm1.enabled = True

        self.fm2 = FlowMeter('metric', ["beer"])
        self.fm2.enabled = True

    def tickFlow1(self, channel):
        # We're resetting the pourlevel next time somebody pours
        if self.isPouring == False:
            self.pourLevel1 = 0

        self.isPouring = True
        self.pourTime = time.time()
        self.currentTime = int(self.pourTime * FlowMeter.MS_IN_A_SECOND)
        if self.fm1.enabled == True:
            self.fm1.update(self.currentTime)
            self.pourLevel1 = self.fm1.getThisPour()

    def tickFlow2(self, channel):
        if self.isPouring == False:
            self.pourLevel2 = 0

        self.isPouring = True
        self.pourTime = time.time()
        self.currentTime = int(self.pourTime * FlowMeter.MS_IN_A_SECOND)
        if self.fm2.enabled == True:
            self.fm2.update(self.currentTime)
            self.pourLevel2 = self.fm2.getThisPour()

    def updatePour(self):
        # If the flow hasn't been updated in two seconds, we're probably not pouring ..
        if self.pourTime + 2 < time.time() and self.isPouring:
            self.lastPourLevel1 = self.pourLevel1
            self.lastPourLevel2 = self.pourLevel2
            self.isPouring = False
            self.totalConsume += self.pourLevel1 + self.pourLevel2
            self.updateConsume()

            if self.pourLevel1 > 0:
                self.subtractConsume(1, self.pourLevel1)
                self.fm1.clearThisPour()
                self.pourLevel1 = 0
            if self.pourLevel2 > 0:
                self.subtractConsume(2, self.pourLevel2)
                self.fm2.clearThisPour()
                self.pourLevel2 = 0

        self.window.setFlow(1, locale.format("%.2f", self.pourLevel1, grouping=True) + " L")
        self.window.setAmount(1, locale.format("%.2f", self.totalAmount1, grouping=True) + " L")
        self.window.setFlow(2, locale.format("%.2f", self.pourLevel2, grouping=True) + " L")
        self.window.setAmount(2, locale.format("%.2f", self.totalAmount2, grouping=True) + " L")
        self.window.setTotal("Totalt konsumert: " + locale.format("%.2f", self.totalConsume) + " L")

    def initKeyValues(self):
        req = urllib2.Request('http://api.ondskap.net/value/6BA5E9B2-7051-482F-96DE-13A6FB929FF0/beertap1_amount')
        response = urllib2.urlopen(req)
        data = json.load(response)
        self.totalAmount1 = float(data[u'value'])

        req = urllib2.Request('http://api.ondskap.net/value/6BA5E9B2-7051-482F-96DE-13A6FB929FF0/beertap2_amount')
        response = urllib2.urlopen(req)
        data = json.load(response)
        self.totalAmount2 = float(data[u'value'])

        req = urllib2.Request('http://api.ondskap.net/value/6BA5E9B2-7051-482F-96DE-13A6FB929FF0/beertap_total_consume')
        response = urllib2.urlopen(req)
        data = json.load(response)
        self.totalConsume = float(data[u'value'])

    def updateConsume(self):
        url = 'http://api.ondskap.net/value/6BA5E9B2-7051-482F-96DE-13A6FB929FF0/beertap_total_consume'
        consume = {'value': self.totalConsume}
        req = urllib2.Request(url, urllib.urlencode(consume))
        response = urllib2.urlopen(req)
        response.read()

    def subtractConsume(self, tap, amount):
        if tap == 1:
            url = 'http://api.ondskap.net/value/6BA5E9B2-7051-482F-96DE-13A6FB929FF0/beertap1_amount'
        if tap == 2:
            url = 'http://api.ondskap.net/value/6BA5E9B2-7051-482F-96DE-13A6FB929FF0/beertap2_amount'

        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = json.load(response)
        oldPourLevel = float(data[u'value'])
        oldPourLevel -= amount

        newPourLevel = {'value': oldPourLevel}
        req = urllib2.Request(url, urllib.urlencode(newPourLevel))
        response = urllib2.urlopen(req)
        response.read()

        if tap == 1:
            self.totalAmount1 = oldPourLevel
        if tap == 2:
            self.totalAmount2 = oldPourLevel

        self.logTapAmount(tap, amount)

    def logTapAmount(self, tap, amount):
        url = 'http://api.ondskap.net/beerlog/6BA5E9B2-7051-482F-96DE-13A6FB929FF0'

        tapLog = {'tap': tap, 'amount': amount}
        req = urllib2.Request(url, urllib.urlencode(tapLog))
        response = urllib2.urlopen(req)
        response.read()

    def updateSpotifyInfo(self):
        # Simple service for getting the current spotify song via dbus-metadata.
        url = 'http://192.168.5.21:4545'

        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        spotify = response.read()

        image = spotify.split("\n")[0].replace("mpris:artUrl: ", "")
        album = spotify.split("\n")[3].replace("xesam:album: ", "")
        albumArtist = spotify.split("\n")[4].replace("xesam:albumArtist: ", "")
        artist = spotify.split("\n")[5].replace("xesam:artist: ", "")
        title = spotify.split("\n")[8].replace("xesam:title: ", "")

        self.window.setSpotifyText(artist + "\n" + title + "\n" + album)
        self.window.setSpotifyCover(image)

def startMain():
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    startMain()
