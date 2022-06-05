import threading
# import Jetson.GPIO as GPIO
from gb import thread_runner
from time import time, sleep
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton

class Jetson():
    def __init__(self):
        super(Jetson, self).__init__()

        # GPIO.setwarnings(False)
        # threading.Thread(target=self.change_timer).start()
        
        self.btn_lighting = QPushButton()

        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(7, GPIO.OUT)
        # GPIO.setup(11, GPIO.IN)
        # GPIO.setup(13, GPIO.IN)

        self.btn_lighting.setFixedHeight(30)
        self.btn_lighting.setText('Light On')
        self.btn_lighting.clicked.connect(self.lighting)

        

    def lighting(self):
        self.change_timer()
        # if self.state is False:
        #     self.state = True
        #     self.btn_lighting.setText('Light Off')
        #     GPIO.output(7, GPIO.HIGH)
        # elif self.state is True:
        #     self.state = False
        #     self.btn_lighting.setText('Light On')
        #     GPIO.output(7, GPIO.LOW)

    # def bat_status():
    #     x = ''
    #     if GPIO.input(11) is GPIO.LOW and GPIO.input(13) is GPIO.HIGH:
    #         x = 'half'
    #     elif GPIO.input(11) is GPIO.HIGH:
    #         x = 'empty'
    #     elif GPIO.input(13) is GPIO.LOW:
    #         x = 'full'
    #     return x
    def bat_status(self, a):
        x = ''
        vals = ['empty', 'half', 'full']
        x = vals[a]
        return x
        