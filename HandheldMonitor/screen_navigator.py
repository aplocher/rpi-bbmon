import threading

class ScreenNavigator:
    class ScreenEnum:
        Main = 0
        Cam1 = 1
        Cam2 = 2
        Cam3 = 3
        Cam4 = 4

    timer = None

    def __init__(self, gst, lcd):
        # TODO warning the code below is fragile. It's relying on ordinal placement with no regard for the
        # fake "enum"s defined above.  Replace with Dictionary?
        self.screenText = []
        self.screenText.append("Video wall")
        self.screenText.append("Camera 1")
        self.screenText.append("Camera 2")
        self.screenText.append("Camera 3")
        self.screenText.append("Camera 4")

        self.screenUrl = []
        self.screenUrl.append("")
        self.screenUrl.append("rtsp://bc-dvr-01:554/?user=admin&password=&channel=1&stream=0.sdp")
        self.screenUrl.append("rtsp://bc-dvr-01:554/?user=admin&password=&channel=2&stream=0.sdp")
        self.screenUrl.append("rtsp://bc-dvr-01:554/?user=admin&password=&channel=3&stream=0.sdp")
        self.screenUrl.append("rtsp://bc-dvr-01:554/?user=admin&password=&channel=4&stream=0.sdp")

        self.gst = gst
        self.lcd = lcd
        self.navigate_to(self.ScreenEnum.Main)

        self.current_screen = 0

    def navigate_to(self, dest):
        self.current_screen = dest
        self.lcd.display_text(text_line1=self.screenText[dest], timeout=6)
        self.gst.stop()

        if self.timer is not None:
            self.timer.cancel()

        self.timer = threading.Timer(0.7, self.navigate_internal, [dest])
        self.timer.start()

    def navigate_next(self):
        if self.current_screen < len(self.screenText) - 1:
            self.navigate_to(self.current_screen + 1)
        else:
            self.navigate_to(self.ScreenEnum.Main)

    def navigate_internal(self, dest):
        self.gst.stop()
        if dest == self.ScreenEnum.Main:
            self.gst.play_wall()
        else:
            url = self.screenUrl[dest]
            self.gst.play_rtsp(url)
