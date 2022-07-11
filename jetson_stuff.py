import Jetson.GPIO as GPIO
from time import sleep
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

class Jetson():
    def __init__(self):
        super(Jetson, self).__init__()

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        self.state = True

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(11, GPIO.IN)
        GPIO.setup(13, GPIO.IN)  

    def lighting(self):
        if self.state is False:
            self.state = True
            GPIO.output(7, GPIO.HIGH)
        elif self.state is True:
            self.state = False
            GPIO.output(7, GPIO.LOW)

    def bat_status(self):
        x = ''
        if GPIO.input(11) is GPIO.LOW and GPIO.input(13) is GPIO.HIGH:
            x = 'half'
        elif GPIO.input(11) is GPIO.HIGH:
            x = 'empty'
        elif GPIO.input(13) is GPIO.LOW:
            x = 'full'
        return x
        
    def clean(self):
        GPIO.cleanup()