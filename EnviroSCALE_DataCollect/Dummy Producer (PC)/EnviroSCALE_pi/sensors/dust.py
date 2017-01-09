# source: http://www.waveshare.com/wiki/Dust_Sensor
import time
from adc import readadc
from Sensor import Sensor
from my_libs import *

# delay = 0.2 second

class Dust(Sensor):
    def __init__(self, analog, digital):
        self.analog = analog
        self.digital = digital
        self.device_name = "DUST"
        self.interval = 2
        self.verbose = False

        self.COV_RATIO = 0.2  # ug/mmm / mv
        self.NO_DUST_VOLTAGE = 400  # mv
        self.SYS_VOLTAGE = 5000  # mv

        self.samplingTime = .280 / 1000
        self.deltaTime = 40 / 1000000
        self.sleepTime = 9680 / 1000000

        # /*
        # I/O define
        # */
        self.PIN_ILED = digital  # //drive the led of sensor
        # adc_channel = 0  #//analog input

        # /*
        # variable
        # */
        # float density, voltage;
        # int   adcvalue;

        # /*    
        # private function
        # */

        self.flag_first = 0
        self.summ = 0
        self.buff = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def Filter(self, m):  # flag_first is 0 for first call, then 1 always
        if self.flag_first == 0:
            self.flag_first = 1
            for i in range(0, 10):
                self.buff[i] = m
                self.summ += self.buff[i]
            return m
        else:
            self.summ -= self.buff[0]
            for i in range(0, 9):
                self.buff[i] = self.buff[i + 1]

            self.buff[9] = m
            self.summ += self.buff[9]

            i = self.summ / 10.0
            return i

    def setup(self):
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
        GPIO.setup(self.PIN_ILED, GPIO.OUT)  # set GPIO24 as an output $pinMode(iled, OUTPUT);
        GPIO.output(self.PIN_ILED,
                    0)  # to set port/pin to High, use => 1/GPIO.HIGH/True  #digitalWrite(iled, LOW); //iled default closed

    def read(self):
        return 20, 20
