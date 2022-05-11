import Jetson.GPIO
from gb import YOLOGGER

class JetsonGPIO(Jetson.GPIO):
    def __init__(self):
        super(Jetson.GPIO, self).__init__()
        
        self.led_pin = 7
        self.setWarnings(False)
        self.setmode(self.BOARD)
        self.setup(self.led_pin, self.OUT)
        self.state = self.LOW
    
    def on_off(self):
        if self.state is self.LOW:
            self.OUTPUT(self.led_pin, self.HIGH)
            YOLOGGER.info('Lighting On!')
        if self.state is self.HIGH:
            self.OUTPUT(self.led_pin, self.LOW)
            YOLOGGER.info('Lighting Off!')
            