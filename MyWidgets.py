from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# CLICKABLE LABEL WIDGET
class clickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, mouseEvent):
        self.clicked.emit()

# BLINKING LABEL WIDGET
class coloredLabel(QLabel):

    def setColor(self, colorString):     # set text color of a label
        labelColor = self.palette()
        labelColor.setColor(QPalette.WindowText, QColor(colorString))
        self.setPalette(labelColor)

    def blink(self, color1, color2):   # call onBlink function every 0.5s
        self.blinkColor1 = color1
        self.blinkColor2 = color2
        self.currentColor = color1
        self.blinkTimer = QTimer()
        self.blinkTimer.timeout.connect(self.onBlink)
        self.blinkTimer.start(500)

    def onBlink(self):       # function to detect label color and switch to other color using setColor
        if self.currentColor == self.blinkColor1:
            self.currentColor = self.blinkColor2
        else:
            self.currentColor = self.blinkColor1
        self.setColor(self.currentColor)

