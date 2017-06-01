import time
from process_manager import ProcessManager
from remote_monitor_loop import RemoteMonitorLoop
from file_writer import FileWriter

def main():
    proc_manager = ProcessManager()
    file_writer = FileWriter('WebFiles/temp.html')
    temp_loop = RemoteMonitorLoop(proc_manager, file_writer)
    temp_loop.start()

    while not proc_manager.hasAnyErrors():
        time.sleep(1)
if __name__ == '__main__':
    main()