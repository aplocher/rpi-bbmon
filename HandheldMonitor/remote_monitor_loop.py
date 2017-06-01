import socket
import time
from utils import Utils
from char_lcd_output import CharLcdOutput
from multiprocessing import Process

class RemoteMonitorLoop:
    min_tempc_warning = 18.0
    max_tempc_warning = 31.0

    def __init__(self, proc_manager, lcd, front_lights, voice):
        self.stop_loop = False
        self.lcd = lcd
        self.proc_manager = proc_manager
        self.front_lights = front_lights
        self.voice = voice
        self.process = Process(target=self.__start_internal, args=())
        self.process.daemon = True
        proc_manager.add(self.process)

    def stop(self):
        print("Stopping thermo")
        self.stop_loop = True
        # self.thr.join()

    def start(self):
        self.process.start()

    def __start_internal(self):
        while not self.stop_loop:
            HOST = 'bc-bbcam-01'
            PORT = 50011

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((HOST, PORT))
                try:

                    data = s.recv(32).strip()
                    print(data)
                    segs = data.split(';')
                    print(segs[0])
                    print(segs[1])
                    sound_detected = segs[1] == "True"

                    temp_c = float(segs[0])
                    temp_f = temp_c * 9.0 / 5.0 + 32.0
                    lcd_priority = CharLcdOutput.TextPriorityEnum.Unimportant

                    if temp_c > self.max_tempc_warning or temp_c < self.min_tempc_warning:
                        self.front_lights.blinkMultiple(5)
                        lcd_priority = CharLcdOutput.TextPriorityEnum.Important

                    if temp_c < self.min_tempc_warning:
                        self.voice.say('Warning, Low temperature. ' + str(temp_f) + ' Degrees Fahrenheit')

                    if temp_c > self.max_tempc_warning:
                        self.voice.say('Warning, High temperature. ' + str(temp_f) + ' Degrees Fahrenheit')

                    Utils.log_temp(temp_c)

                    self.lcd.display_text(text_line1='Nursery temp.:', text_line2="%0.1f-f / %0.1f-c" % (temp_f, temp_c,),
                                          priority=lcd_priority, timeout=8)

                    if sound_detected:
                        self.front_lights.blinkMultiple(5)
                        self.lcd.display_text(text_line1='!! WARNING !!', text_line2='*Sound detected*', timeout=8)
                        self.voice.say('Warning, sound detected')
                finally:
                    try:
                        s.close()
                    except Exception:
                        pass

                    if not self.stop_loop:
                        time.sleep(10)
            except Exception, e:
                print("Socket connection failed: "+ str(e))
                self.lcd.display_text(text_line1='Cant connect to', text_line2='temp/snd sensor', timeout=8)
                time.sleep(5)