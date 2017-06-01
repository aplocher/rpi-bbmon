import socket
import time
from multiprocessing import Process

import sys

from file_writer import FileWriter

class RemoteMonitorLoop:
    min_tempc_warning = 18.0
    max_tempc_warning = 31.0

    def __init__(self, proc_manager, file_writer):
        self.file_writer = file_writer
        self.process = Process(target=self.__start_internal, args=())
        self.process.daemon = True
        self.stop_loop = False
        self.proc_manager = proc_manager
        proc_manager.add(self.process)

    def stop(self):
        print("Stopping thermo")
        self.stop_loop = True

    def start(self):
        print ("Starting loop (not internal)")
        self.process.start()

    def __start_internal(self):
        print "Start Loop"
        while not self.stop_loop:
            HOST = 'bc-bbcam-01'
            PORT = 50011
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((HOST, PORT))
                try:
                    data = s.recv(32).strip()
                    segs = data.split(';')
                    sound_detected = segs[1] == "True"

                    temp_c = float(segs[0])
                    temp_f = temp_c * 9.0 / 5.0 + 32.0

                    if temp_c > self.max_tempc_warning or temp_c < self.min_tempc_warning:
                        pass

                    if temp_c < self.min_tempc_warning:
                        pass

                    if temp_c > self.max_tempc_warning:
                        pass

                    self.file_writer.write('{} &deg;F / {} &deg;C'.format(temp_f, temp_c))
                finally:
                    try:
                        s.close()
                    except Exception:
                        pass

                    if not self.stop_loop:
                        time.sleep(30)
            except Exception, e:
                print("Socket connection failed: "+ str(e))
                print e
                sys.stdout.flush()
                time.sleep(5)