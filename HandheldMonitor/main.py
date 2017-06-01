import atexit
import time

from char_lcd_output import CharLcdOutput
from gstreamer_wrapper import GStreamerWrapper
from led_light_output import LedLightOutput
from nav_button_loop import NavButtonLoop
from process_manager import ProcessManager
from remote_monitor_loop import RemoteMonitorLoop
from screen_navigator import ScreenNavigator
from voice_output import VoiceOutput
from watchdog_loop import WatchdogLoop

def main():
    print("Starting")

    proc_manager = ProcessManager()

    lcd_output = CharLcdOutput()
    light_output = LedLightOutput()
    voice_output = VoiceOutput()

    gst = GStreamerWrapper()
    gst.play_wall()

    nav = ScreenNavigator(gst, lcd_output)

    temp_loop = RemoteMonitorLoop(proc_manager, lcd_output, light_output, voice_output)
    btn_loop = NavButtonLoop(proc_manager, nav, lcd_output)
    watchdog_loop = WatchdogLoop()

    print("Initialized")
    try:
        print("Starting Char LCD Output")
        lcd_output.display_text(text_line1="Starting", priority=CharLcdOutput.TextPriorityEnum.Normal, timeout=10)

        print("Starting TempLoop")
        temp_loop.start()

        print("Starting SoundMonitorLoop")
        # soundMonitorLoop.start()

        print("Starting NavButtonLoop")
        btn_loop.start()

        print("Starting WatchdogLoop")
        watchdog_loop.start()

        # Continuously monitor child processes for any that have exited / raised an error
        # Once one is detected end app
        # Child processes are daemonized so they will exit with the parent
        # Shell script loop will restart the whole Python script at that point
        while not proc_manager.hasAnyErrors():
            time.sleep(1)
    finally:
        lcd_output.display_text(text_line1='Exiting', text_line2 = '', priority = CharLcdOutput.TextPriorityEnum.System)
        time.sleep(1)
        lcd_output.display_text(text_line1='', text_line2='', priority=CharLcdOutput.TextPriorityEnum.System)


if __name__ == '__main__':
    main()
