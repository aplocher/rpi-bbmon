import socket

class SocketListener:
    def __init__(self, temp_monitor, sound_monitor):
        self.temp_monitor = temp_monitor
        self.sound_monitor = sound_monitor

    def start(self):
        HOST = ''
        PORT = 50011
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            try:
                conn, addr = s.accept()
                print("Connection from %s" % str(addr))
                response = "%s;%s;\n" %(str(self.temp_monitor.read()), str(
                    self.sound_monitor.was_alerted()))
                conn.sendall(response)
                self.sound_monitor.clear_alerted()
            except Exception, e:
                print('retry - ' + str(e))
            finally:
                conn.close()

        conn.close()