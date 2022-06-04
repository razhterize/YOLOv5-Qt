import threading
from gb import YOLOGGER, thread_runner
import Jetson.GPIO as GPIO
from time import sleep, time
from widget_info import WidgetInfo
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton

class Jetson():
    def __init__(self):
        super(Jetson, self).__init__()

        GPIO.setwarnings(False)
        
        self.jetson_info = WidgetInfo()
        self.btn_lighting = QPushButton()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(11, GPIO.IN)
        GPIO.setup(13, GPIO.IN)

        self.btn_lighting.setFixedHeight(30)
        self.btn_lighting.setText('Light On')
        self.btn_lighting.clicked.connect(self.lighting)

        threading.Thread(target=self.change_timer).start()

    def lighting(self):
        self.jetson_info.img_src = 'img/bat-full.png'
        self.jetson_info.update_test('img/bat-full.png')
        # if self.state is False:
        #     self.state = True
        #     self.btn_lighting.setText('Light Off')
        #     GPIO.output(7, GPIO.HIGH)
        # elif self.state is True:
        #     self.state = False
        #     self.btn_lighting.setText('Light On')
        #     GPIO.output(7, GPIO.LOW)

    # def battery_indicator(self):
    #     while True:
    #         sleep(10 - time() % 10)
    #         if GPIO.input(11) is GPIO.HIGH:
    #             #bat low
    #             self.jetson_info.update_bat_status('img/bat-empty.png')
    #         elif GPIO.input(11) is GPIO.LOW and GPIO.input(13) is GPIO.HIGH:
    #             #bat mid
    #             self.jetson_info.update_bat_status('img/bat-half.png')
    #         elif GPIO.input(13) is GPIO.LOW:
    #             #bat high
    #             self.jetson_info.update_bat_status('img/bat-full.png')
    
    @thread_runner
    def change_timer(self):
        while True:
            sleep(5)
            self.jetson_info.update_test('img/bat-empty.png')
            sleep(5)
            self.jetson_info.update_test('img/bat-half.png')
            sleep(5)
            self.jetson_info.update_test('img/bat-full.png')
    