import threading
import Jetson.GPIO as GPIO
from time import sleep, time
from widget_info import WidgetInfo
from main import MainWindow

class Jetson():
    def __init__(self):
        super(Jetson, self).__init__()

        main = MainWindow()

        GPIO.setwarnings(False)
        self.jetson_info = WidgetInfo()
        self.state = False
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(11, GPIO.IN)
        GPIO.setup(13, GPIO.IN)
        threading.Thread(target=self.battery_indicator).start()

    def lighting(self):
        if self.state is False:
            self.state = True
            self.main.btn_lighting.setText('Light Off')
            GPIO.output(7, GPIO.HIGH)
        elif self.state is True:
            self.state = False
            self.btn_lighting.setText('Light On')
            GPIO.output(7, GPIO.LOW)

    def battery_indicator(self):
        while True:
            sleep(10 - time() % 10)
            if GPIO.input(11) is GPIO.HIGH:
                #bat low
                self.jetson_info.update_bat_status('img/bat-empty.png')
            elif GPIO.input(11) is GPIO.LOW and GPIO.input(13) is GPIO.HIGH:
                #bat mid
                self.jetson_info.update_bat_status('img/bat-half.png')
            elif GPIO.input(13) is GPIO.LOW:
                #bat high
                self.jetson_info.update_bat_status('img/bat-full.png')
