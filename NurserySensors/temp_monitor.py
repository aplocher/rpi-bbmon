import glob
import os
import subprocess
import time

class TempMonitor:
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'

    def read(self):
        lines = self.__read_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.__read_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            print "RAW: " + str(float("{0:.2f}".format(temp_c)))
            print "Cel/Far: {0:.1f}".format(temp_f) + "-f {0:.1f}".format(temp_c) + "-c"
            return str(float("{0:.2f}".format(temp_c)))

    def __read_raw(self):
        cat_data = subprocess.Popen(['cat',self.device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = cat_data.communicate()
        out_decode = out.decode('utf-8')
        lines = out_decode.split('\n')
        return lines