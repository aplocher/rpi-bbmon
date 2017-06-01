from sound_monitor import SoundMonitor
from temp_monitor import TempMonitor
from socket_listener import SocketListener

def main():
    temp = TempMonitor()

    sound = SoundMonitor()
    sound.start()

    socket = SocketListener(temp, sound)
    socket.start()

if __name__ == '__main__':
    main()