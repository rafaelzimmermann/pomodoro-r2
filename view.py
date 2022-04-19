from lcd.gpio_lcd import GpioLcd
from machine import Pin
from pomodoro import Timer
from components import progress_bar
import time

SCREEN_WIDTH = 16
ALIGN_LEFT = 0
ALIGN_RIGHT = 1
ALIGN_CENTER = 2


def padding(size):
    return " " * int(size)


def align_text(text, align):
    if len(text) == SCREEN_WIDTH:
        return text
    if align == ALIGN_RIGHT:
        text = padding(SCREEN_WIDTH - len(text)) + text
    if align == ALIGN_CENTER:
        p = padding((SCREEN_WIDTH - len(text)) / 2)
        text = f"{p}{text}{p}"
    return text


class Output:

    def __init__(self):
        self.lcd = GpioLcd(
            rs_pin=Pin(12, Pin.OUT),
            enable_pin=Pin(11, Pin.OUT),
            d4_pin=Pin(10, Pin.OUT),
            d5_pin=Pin(9, Pin.OUT),
            d6_pin=Pin(8, Pin.OUT),
            d7_pin=Pin(7, Pin.OUT)
        )

    def write_line(self, text, line_index, align=ALIGN_LEFT):
        self.lcd.move_to(0, line_index)
        self.lcd.putstr(align_text(text, align))

    def clean(self):
        self.write_line("", 0, ALIGN_RIGHT)
        self.write_line("", 1, ALIGN_RIGHT)


class DisplayTimer:

    def __init__(self, output):
        self.output = output

    def show(self):
        t = Timer(1)
        t.start()
        while t.progress() < 1:
            x = t.progress()
            bar = progress_bar(self.output, x)
            timer_txt = t.time_left_fmt()
            self.output.write_line(bar, 0)
            self.output.write_line(timer_txt, 1, align=ALIGN_CENTER)
            time.sleep(1)


class StartScreen:

    def __init__(self, output):
        self.output = output
        self.show_splash_screen()
        self.run()

    def run(self):
        dt = DisplayTimer(self.output)
        dt.show()

    def show_splash_screen(self):
        self.output.write_line("POMODORO 0.1", 1)
        time.sleep(1)
