from lcd.gpio_lcd import GpioLcd
from machine import Pin
from pomodoro import Timer
from components import progress_bar, arrows, Button, Buzzer
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

    def __init__(self, output, timer, buttons, buzzer):
        self.buttons = buttons
        self.output = output
        self.timer = timer
        self.buzzer = buzzer

    def show(self):
        self.timer.start()
        while self.timer.progress() < 1:
            x = self.timer.progress()
            bar = progress_bar(self.output, x)
            timer_txt = self.timer.time_left_fmt()
            self.output.write_line(bar, 0)
            self.output.write_line(timer_txt, 1, align=ALIGN_CENTER)
            if self.buttons.cancel.is_pressed():
                self.timer = None
                break
            time.sleep(1)
        self.buzzer.beep(3)


class Buttons:

    def __init__(self):
        self.right = Button(3)
        self.left = Button(2)
        self.select = Button(4)
        self.cancel = Button(5)


class Options:

    RIGHT = 0
    LEFT = 1
    SELECT = 3

    def __init__(self, output, buttons):
        self.buttons = buttons
        self.output = output
        self.current_option = 0
        self.options = [self.option_0, self.option_1, self.option_2]
        self.left, self.right = arrows(self.output)

    def show(self) -> Timer:
        t = self.option_0()
        user_input = None
        while user_input != Options.SELECT:
            user_input = self.user_input()
            if user_input == Options.RIGHT:
                self.current_option += 1
                self.current_option = min(self.current_option, len(self.options) - 1)
            if user_input == Options.LEFT:
                self.current_option -= 1
                self.current_option = max(self.current_option, 0)
            t = self.options[self.current_option]()
        return t

    def user_input(self):
        user_input = -1
        while user_input < 0:
            time.sleep(0.1)
            if self.buttons.right.is_pressed():
                user_input = Options.RIGHT
                time.sleep(0.5)
            if self.buttons.left.is_pressed():
                user_input = Options.LEFT
                time.sleep(0.5)
            if self.buttons.select.is_pressed():
                user_input = Options.SELECT
                time.sleep(0.5)
        return user_input

    def option_0(self):
        lines_0 = [self.left[0], " ", " ", " ", "P", "o", "m", "o", "d", "o", "r", "o", " ", " ", " ", self.right[0]]
        lines_1 = [self.left[1], " ", " ", " ", " ", "2", "5", ":", "0", "0", " ", " ", " ", " ", " ", self.right[1]]
        self.output.write_line(lines_0, 0)
        self.output.write_line(lines_1, 1)
        return Timer(25)

    def option_1(self):
        lines_0 = [self.left[0], " ", " ", "S", "h", "o", "r", "t", " ", "B", "r", "e", "a", "k", " ", self.right[0]]
        lines_1 = [self.left[1], " ", " ", " ", " ", "0", "5", ":", "0", "0", " ", " ", " ", " ", " ", self.right[1]]
        self.output.write_line(lines_0, 0)
        self.output.write_line(lines_1, 1)
        return Timer(5)

    def option_2(self):
        lines_0 = [self.left[0], " ", " ", "L", "o", "n", "g", " ", "B", "r", "e", "a", "k", " ", " ", self.right[0]]
        lines_1 = [self.left[1], " ", " ", " ", " ", "1", "5", ":", "0", "0", " ", " ", " ", " ", " ", self.right[1]]
        self.output.write_line(lines_0, 0)
        self.output.write_line(lines_1, 1)
        return Timer(15)


class StartScreen:

    def __init__(self, output):
        self.output = output
        self.buttons = Buttons()
        self.buzz = Buzzer(0)
        self.show_splash_screen()
        self.buzz.beep(0.5)
        while True:
            self.timer = self.show_options()
            self.display_timer()
            time.sleep(1)

    def show_options(self):
        return Options(self.output, self.buttons).show()

    def display_timer(self):
        dt = DisplayTimer(self.output, self.timer, self.buttons, self.buzz)
        dt.show()

    def show_splash_screen(self):
        self.output.write_line("POMODORO 0.1", 1)
        time.sleep(1)
