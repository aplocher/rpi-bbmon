from platform import system as system_name
from subprocess import call
from os import system as system_call
from subprocess import Popen, PIPE
import sys
import os
import datetime

from subprocess import call


class Utils:
    @staticmethod
    def ping(host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that some hosts may not respond to a ping request even if the host name is valid.
        """

        # Ping parameters as function of OS
        ping_param = "-n 1" if system_name().lower() == "windows" else "-c 1"

        # Pinging
        return system_call("ping " + ping_param + " " + host + " > /dev/null") == 0

    @staticmethod
    def reboot():
        call('/sbin/reboot', shell=False)

    @staticmethod
    def shutdown():
        call('/sbin/halt', shell=False)

    @staticmethod
    def reset_wifi(adapter):
        my_cmd = "sudo ifdown " + adapter + " && sudo ifup " + adapter  # might be wlan0
        proc = subprocess.Popen(my_cmd, shell=True, stdout=subprocess.PIPE)

    @staticmethod
    def restart_self():
        args = sys.argv[:]
        Utils.log('Re-spawning %s' % ' '.join(args))

        args.insert(0, sys.executable)
        if sys.platform == 'win32':
            args = ['"%s"' % arg for arg in args]

        os.chdir(_startup_cwd)
        os.execv(sys.executable, args)

    @staticmethod
    def log(text):
        with open("/home/pi/logs/log.txt", "a") as myfile:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S (%m/%d)")
            myfile.write(timestamp + ': ' + text + '\n')

    @staticmethod
    def log_screen(text):
        with open("/home/pi/logs/screen.txt", "a") as myfile:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S (%m/%d)")
            myfile.write(timestamp + ': ' + text + '\n')

    @staticmethod
    def log_temp(temp):
        with open("/home/pi/logs/temperature.txt", "a") as myfile:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S (%m/%d)")
            myfile.write(timestamp + ':::' + str(temp) + '\n');
