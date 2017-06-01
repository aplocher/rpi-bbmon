import time
import Adafruit_CharLCD as LCD

class CharLcdOutput:
    lcd_rs = 26
    lcd_en = 20
    lcd_d4 = 21
    lcd_d5 = 13
    lcd_d6 = 16
    lcd_d7 = 6
    lcd_backlight = 4
    lcd_columns = 16
    lcd_rows = 2

    class TextPriorityEnum:
        Unimportant = 0
        Normal = 1
        Important = 2
        System = 3

    def __init__(self):
        # RPi.GPIO.setup
        self.current_priority = CharLcdOutput.TextPriorityEnum.Normal
        self.text_line_1 = ""
        self.text_line_2 = ""
        self.text = ""
        self.timeout_at = time.time()
        self.timeout_at = 0
        self.lcd = LCD.Adafruit_CharLCD(self.lcd_rs, self.lcd_en, self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7,
                                        self.lcd_columns, self.lcd_rows, self.lcd_backlight)

    def display_text(self, text_line1=None, text_line2=None, priority=TextPriorityEnum.Normal, timeout=0):
        tmp_line1 = self.text_line_1
        tmp_line2 = self.text_line_2

        # Any text with a priority higher than unimportant that has a timeout that has elapsed will
        # have priority downgraded (thus overwriteable) to Unimportant.
        if self.current_priority > CharLcdOutput.TextPriorityEnum.Unimportant and self.timeout_at > time.time():
            self.current_priority = CharLcdOutput.TextPriorityEnum.Unimportant

        if self.current_priority > priority:
            return

        if timeout > 0:
            self.timeout_at = time.time() + timeout
        else:
            self.timeout_at = time.time() + 9999

        if text_line1 is not None:
            tmp_line1 = text_line1

        if text_line2 is not None:
            tmp_line2 = text_line2

        tmp_all_lines = tmp_line1 + "\n" + tmp_line2 + "\n"

        if tmp_all_lines != self.text:
            self.text_line_1 = tmp_line1
            self.text_line_2 = tmp_line2
            self.text = tmp_all_lines
            self.lcd.clear()
            self.lcd.message(tmp_all_lines)

    def clear(self):
        self.lcd.clear()