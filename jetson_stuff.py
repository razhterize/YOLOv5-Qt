import threading
# import Jetson.GPIO as GPIO
from gb import thread_runner
from time import time, sleep
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

class Jetson():
    def __init__(self):
        super(Jetson, self).__init__()

        # GPIO.setwarnings(False)
        # threading.Thread(target=self.change_timer).start()

        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(7, GPIO.OUT)
        # GPIO.setup(11, GPIO.IN)
        # GPIO.setup(13, GPIO.IN)
        self.state = False

    # Function to turn on/off lighting (only for jetson)
    def lighting(self):
        if self.state is False:
            self.state = True
        #     GPIO.output(7, GPIO.HIGH)
        elif self.state is True:
            self.state = False
        #     GPIO.output(7, GPIO.LOW)

    # Battery status (only for jetson)
    # def bat_status():
    #     x = ''
    #     if GPIO.input(11) is GPIO.LOW and GPIO.input(13) is GPIO.HIGH:
    #         x = 'half'
    #     elif GPIO.input(11) is GPIO.HIGH:
    #         x = 'empty'
    #     elif GPIO.input(13) is GPIO.LOW:
    #         x = 'full'
    #     return x
    # Testing battery function
    def bat_status(self, a):
        x = ''
        vals = ['empty', 'half', 'full']
        x = vals[a]
        return x
        