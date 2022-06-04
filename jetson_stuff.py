import threading
# import Jetson.GPIO as GPIO
from gb import thread_runner
from time import sleep
from widget_info import WidgetInfo
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton

class Jetson():
    def __init__(self):
        super(Jetson, self).__init__()

        # GPIO.setwarnings(False)
        # threading.Thread(target=self.change_timer).start()
        
        self.jetson_info = WidgetInfo()
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

    # def battery_indicator(self):self.bat_label.setPixmap(self.bat_pixmap.scaled(40, 20))us('img/bat-empty.png')
    #         elif GPIO.input(11) is GPIO.LOW and GPIO.input(13) is GPIO.HIGH:
    #             #bat mid
    #             self.jetson_info.update_bat_status('img/bat-half.png')
    #         elif GPIO.input(13) is GPIO.LOW:
    #             #bat high
    #             self.jetson_info.update_bat_status('img/bat-full.png')

    def change_timer(self):
        while True:
            self.jetson_info.img_src = 'img/bat-empty.png'
            self.jetson_info.bat_label.setText("AAAAAAA")
            print('change1')
            sleep(2)
            self.jetson_info.img_src = 'img/bat-half.png'
            self.jetson_info.bat_label.setText("BBBBBBBB")
            print('change2')
            sleep(2)
            self.jetson_info.img_src = 'img/bat-full.png'
            self.jetson_info.bat_label.setText("CCCCCCCC")
            print('change3')
            sleep(2)
