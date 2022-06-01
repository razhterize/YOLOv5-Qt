
import Jetson.GPIO as GPIO
from time import sleep, time
from widget_info import WidgetInfo

class Jetson():
    def __init__(self):
        super(Jetson, self).__init__()
        GPIO.setWarnings(False)
        self.jetson_info = WidgetInfo()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(11, GPIO.IN)
        GPIO.setup(13, GPIO.IN)


    def lighting(self):
        if self.state is False:
            self.state = True
            self.btn_lighting.setText('Light Off')
            GPIO.output(7, GPIO.HIGH)
        elif self.state is True:
            self.btn_lighting.setText('Light On')
            self.state = False
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
