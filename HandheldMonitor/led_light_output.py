import RPi
import time

class LedLightOutput:
    def __init__(self):
        self.pin=5
        self.blinking=False
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(self.pin, RPi.GPIO.OUT)

    def blinkMultiple(self, count):
        for i in range(0,count):
            self.blinkOnce()

    def blinkOnce(self):
        RPi.GPIO.output(self.pin,RPi.GPIO.HIGH)
        time.sleep(0.1)
        RPi.GPIO.output(self.pin,RPi.GPIO.LOW)
        time.sleep(0.3)

    def startBlink(self):
        self.blinking=True
        while(self.blinking):
            self.blinkOnce()

    def startSolid(self):
        RPi.GPIO.output(self.pin, RPi.GPIO.HIGH)

    def stop(self):
        self.blinking=False
        RPi.GPIO.output(self.pin, RPi.GPIO.LOW)
