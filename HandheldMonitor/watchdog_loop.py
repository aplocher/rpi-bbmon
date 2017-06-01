import time
from multiprocessing import Process
from utils import Utils

class WatchdogLoop:
    def __init__(self):
        self.stop_loop = False
        self.process = Process(target=self.__start_internal, args=())
        self.process.daemon = True

    def stop(self):
        print("Stopping watchdog")
        self.stop_loop = True
        #self.thr.join()

    def start(self):
        print("Starting watchdog")
        self.process.start()
        #self.watch_callback_queue()

    def __start_internal(self):
        print("Starting watchdog (internal)")
    #    try:
        while not self.stop_loop:
            if not Utils.ping("bc-linpc-01"):
                # failed once, try again in 2 seconds
                print("Host down (first host, first attempt)")
                time.sleep(2)
                if not Utils.ping("bc-linpc-01"):
                    # still failed, try a different host
                    print("Host down (first host, second attempt)")
                    Utils.log('Network unavailable?')
                    if not Utils.ping("bc-dvr-01"):
                        # STILL FAILED?! ok well lets reset our wifi adapter
                        print("Host down (second host)")
                        print("Resetting network adapter")
                        Utils.log('Resetting Wifi')
                        Utils.reset_wifi("wlan0")
                        time.sleep(5)
                        if not Utils.ping("bc-linpc-01"):
                            # SERIOUSLY?? Restart whole Python script now
                            Utils.log('Restarting self')
                            Utils.restart_self()
                    else:
                        print("Up 2")
                else:
                    print("Up 1x2")
            time.sleep(1)
        time.sleep(0.2)