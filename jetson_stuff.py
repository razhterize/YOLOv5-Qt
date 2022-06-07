import Jetson.GPIO as GPIO
from time import sleep
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

class Jetson():
    def __init__(self):
        super(Jetson, self).__init__()

        GPIO.setwarnings(False)
        
        self.btn_lighting = QPushButton()
        self.state = True

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(11, GPIO.IN)
        GPIO.setup(13, GPIO.IN)

        self.btn_lighting.setFixedHeight(40)
        self.btn_lighting.setText('Light On')
        self.btn_lighting.clicked.connect(self.lighting)
        self.btn_lighting.setIconSize(QSize(55, 20))
        self.btn_lighting.setIcon(QIcon('img/light-off.png'))        

    def lighting(self):
        if self.state is False:
            self.state = True
            self.btn_lighting.setText('Light Off')
            self.btn_lighting.setIcon(QIcon('img/light-on.png'))
            GPIO.output(7, GPIO.HIGH)
        elif self.state is True:
            self.state = False
            self.btn_lighting.setText('Light On')
            self.btn_lighting.setIcon(QIcon('img/light-off.png'))
            GPIO.output(7, GPIO.LOW)
        print(self.state)

    def bat_status(self):
        x = ''
        if GPIO.input(11) is GPIO.LOW and GPIO.input(13) is GPIO.HIGH:
            x = 'half'
        elif GPIO.input(11) is GPIO.HIGH:
            x = 'empty'
        elif GPIO.input(13) is GPIO.LOW:
            x = 'full'
        return x
        
