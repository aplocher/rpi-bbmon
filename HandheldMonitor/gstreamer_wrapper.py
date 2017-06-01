from multiprocessing import Process, Queue
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst, GstBase, Gtk, GObject

class GStreamerWrapper:
    def __init__(self):
        self.queue = Queue()
        Gst.init(None)
        self.pipeline = Gst.Pipeline.new("Player")

        self.process = Process(target=self.__gst_internal, args=(self.queue,))
        self.process.daemon = True
        self.process.start()

        self.queue.put(("INIT", "",))

    def play_wall(self):
        self.queue.put(("PLAYWALL", "",))

    def play_rtsp(self, rtsp_url):
        self.queue.put(("PLAYRTSP", rtsp_url,))

    def __gst_internal(self, queue):
        while True:
            command, rtsp_url = queue.get()

            if not command:
                return
            else:
                if command == "INIT":
                    Gst.init(None)
                elif command == "PLAYWALL":
                    self.pipeline.set_state(Gst.State.READY)
                    self.pipeline = Gst.parse_launch(
                        "tcpclientsrc host=bc-linpc-01 port=9001 ! decodebin ! glimagesink sync=false")
                    self.pipeline.set_state(Gst.State.PLAYING)
                elif command == "PLAYRTSP":
                    self.pipeline.set_state(Gst.State.READY)
                    self.pipeline = Gst.parse_launch(
                        "rtspsrc location=""%s"" ! rtph264depay ! avdec_h264 ! videoconvert ! glimagesink sync=false" % rtsp_url)
                    self.pipeline.set_state(Gst.State.PLAYING)
                elif command == "STOP":
                    self.pipeline.set_state(Gst.State.NULL)

    def stop(self):
        self.queue.put(("STOP", "",))
