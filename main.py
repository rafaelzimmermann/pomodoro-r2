from lcd.gpio_lcd import GpioLcd
from machine import Pin
import utime


def print_hi(name):
    lcd = GpioLcd(
        rs_pin=Pin(12, Pin.OUT),
        enable_pin=Pin(11, Pin.OUT),
        d4_pin=Pin(10, Pin.OUT),
        d5_pin=Pin(9, Pin.OUT),
        d6_pin=Pin(8, Pin.OUT),
        d7_pin=Pin(7, Pin.OUT)
    )
    lcd.putstr("1")


if __name__ == '__main__':
    led = Pin(25, Pin.OUT)
    led.low()
    for i in range(0, 3):
        print("Running!")
        led.toggle()
        utime.sleep(0.2)
    led.low()
    print_hi('PyCharm')
