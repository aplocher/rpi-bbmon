import threading
import time
import RPi

from subprocess import call

from utils import Utils
from char_lcd_output import CharLcdOutput
from multiprocessing import Process

class NavButtonLoop:
    def __init__(self, proc_manager, nav, lcd):
        self.proc_manager = proc_manager
        self.nav = nav
        self.lcd = lcd
        self.stop_loop = False
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(12, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)

        self.process = Process(target=self.__start_internal, args=())
        self.process.daemon = True

        proc_manager.add(self.process)

    def click(self):
        self.nav.navigate_next()

    def start(self):
        self.process.start()

    def __start_internal(self):
        last_state = -1
        last_fullpress_time = None
        press_started_time = None
        while not self.stop_loop:
            try:
                current_state = RPi.GPIO.input(12)
                if current_state != last_state:
                    print current_state
                    current_time = time.time()
                    if current_state == RPi.GPIO.LOW:
                        print("PRESSED BTN")
                        press_started_time = time.time()
                    else:
                        print("RELEASED BTN")
                        press_released_time = time.time()
                        if press_started_time is not None:
                            time_held = press_released_time - press_started_time
                            if time_held > 8:
                                self.lcd.display_text(text_line1='Shutting down ...',
                                                      priority=CharLcdOutput.TextPriorityEnum.System, timeout=20)
                                threading.Timer(2, Utils.shutdown).start()
                            elif time_held > 4:
                                self.lcd.display_text(text_line1='Rebooting ...',
                                                      priority=CharLcdOutput.TextPriorityEnum.System, timeout=20)
                                threading.Timer(2, Utils.reboot).start()
                            elif 0.12 < time_held < 2:
                                self.nav.navigate_next()

                        press_started_time = None

                    last_state = current_state

                if current_state == RPi.GPIO.LOW:
                    if press_started_time is not None:
                        t = time.time()

                        if t - press_started_time > 8:
                            self.lcd.display_text(text_line1='Let go to shutdown', text_line2='(manual poweroff)',
                                                  priority=CharLcdOutput.TextPriorityEnum.System, timeout=5)
                        elif t - press_started_time > 4:
                            self.lcd.display_text(text_line1='Let go to reboot', text_line2='Hold to shutdown',
                                                  priority=CharLcdOutput.TextPriorityEnum.System, timeout=5)
                        elif t - press_started_time > 2:
                            self.lcd.display_text(text_line1='Keep holding to', text_line2='reboot/shutdown',
                                                  priority=CharLcdOutput.TextPriorityEnum.System, timeout=2)
            finally:
                time.sleep(0.1)

    def stop(self):
        self.stop_loop = True