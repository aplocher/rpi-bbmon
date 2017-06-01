from os import system as system_call

import time


class VoiceOutput:
    def __init__(self):
        self.last_said = 0

    def say(self, text_to_say):
        current = time.time()
        if self.last_said + 60 < current:
            self.last_said = current
            system_call("echo \""+ text_to_say +"\" | espeak > /dev/null 2>&1")

