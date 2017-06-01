import spidev
import os
import time
from threading import Thread

class SoundMonitor:
    def __init__(self):
        # These values need to be tweaked to detect the sound properly
        self.minimum_sound_level = 730
        self.min_time_between_samples = 0.4
        self.max_time_between_samples = 3.0

        self.adc_channel = 0
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.__was_alerted = False
        self.__last_alerted = 0

        self.thread = Thread(target = self.__startInternal)

    def start(self):
        self.thread.start()

    def __startInternal(self):
        last_triggered_time = 0
        while True:
            if (self.adc_channel > 7) or (self.adc_channel < 0):
                raise ValueError('Invalid channel {}'.format(self.adc_channel))

            spi_result = self.spi.xfer([1, (8 + self.adc_channel) << 4, 0])
            adc_out = ((spi_result[1] & 3) << 8) + spi_result[2]

            if adc_out > self.minimum_sound_level:
                triggered_time = time.time()
                last_triggered = triggered_time - last_triggered_time

                if last_triggered > self.max_time_between_samples:
                    # Too much time passed - count as the FIRST
                    sample_count = 1
                elif self.min_time_between_samples < last_triggered < self.max_time_between_samples:
                    if sample_count == 0:
                        # First sound event
                        sample_count = 1
                    elif sample_count > 0:
                        print("I HEARD SOMETHING " + str(adc_out))
                        self.__was_alerted = True
                        self.__last_alerted = time.time()
                        sample_count = 0
                last_triggered_time = triggered_time

    def clear_alerted(self):
        self.__was_alerted = False

    def was_alerted(self):
        current = time.time()
        if self.__last_alerted + 60 > current:
            return self.__was_alerted
        else:
            return False