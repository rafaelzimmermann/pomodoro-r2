import time


def min_to_ms(value):
    return value * 60 * 1000


def ms_to_min(value):
    return value / 1000 / 60


class Timer:

    def __init__(self, timer_size_minutes):
        self.timer_size_ms = min_to_ms(timer_size_minutes)
        self.start_time = None

    def start(self):
        self.start_time = time.ticks_ms()

    def progress(self):
        return (self.timer_size_ms - self.time_left_ms()) / self.timer_size_ms

    def time_left_ms(self):
        diff = time.ticks_ms() - self.start_time
        return max(0, self.timer_size_ms - diff)

    def time_left(self):
        return int(self.time_left_ms() / 1000)

    def time_left_fmt(self):
        tl = self.time_left()
        minutes = str(int(tl / 60))
        seconds = str(tl % 60)
        minutes = f"0{minutes}" if len(minutes) < 2 else minutes
        seconds = f"0{seconds}" if len(seconds) < 2 else seconds
        return f"{minutes}:{seconds}"

    def __repr__(self):
        return str(self.start_time) + " " \
               + str(time.ticks_ms()) + " " \
               + str(self.time_left()) + " " \
               + self.time_left_fmt() + " " \
               + str(self.progress())


class Pomodoro:

    def __init__(self):
        pass

