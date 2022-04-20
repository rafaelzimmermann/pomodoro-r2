import time
from machine import Pin


def write_progress_bar_custom_char(output):
    chars = [
        [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10],
        [0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18],
        [0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C],
        [0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E],
        [0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F],
    ]
    location = 0
    for char_map in chars:
        output.lcd.custom_char(location, char_map)
        location += 1


def write_arrows_char(output):
    chars = [
        [0x00, 0x01, 0x03, 0x03, 0x06, 0x0C, 0x08, 0x10],  # Arrow left up
        [0x10, 0x08, 0x0C, 0x06, 0x07, 0x03, 0x01, 0x00],  # Arrow left bottom
        [0x00, 0x10, 0x18, 0x1C, 0x0C, 0x06, 0x02, 0x01],  # Arrow right up
        [0x01, 0x02, 0x06, 0x0C, 0x1C, 0x18, 0x10, 0x00],  # Arrow right bottom
    ]
    location = 0
    for char_map in chars:
        output.lcd.custom_char(location, char_map)
        location += 1


def arrows(output):
    write_arrows_char(output)
    return [[chr(0), chr(1)], [chr(2), chr(3)]]


def progress_bar(output, percentage):
    write_progress_bar_custom_char(output)
    line_size = 16
    p = line_size * float(percentage)
    p_int = int(p)
    partial_c = p - p_int
    line = []
    for i in range(0, line_size):
        if i < p_int:
            line.append(chr(4))
        elif i == p_int:
            line.append(chr(int(partial_c * 4)))
        else:
            line.append(chr(17))
    return line


class Button:

    def __init__(self, pin):
        self.pin = self.arrow_right = Pin(pin, Pin.IN, Pin.PULL_UP)

    def is_pressed(self):
        return not self.pin.value()


class Buzzer:

    def __init__(self, pin):
        self.pin = Pin(pin, Pin.OUT)

    def beep(self, duration):
        self.pin.value(1)
        time.sleep(duration)
        self.pin.value(0)




