
# coding: utf-8
from time import perf_counter, sleep

class FPSLimiter:
    _previous_time: float
    _start_of_second: float
    _frame_count: int = 0
    _fps: int = 0
    def __init__(self, max_fps : int = 60) -> None:
        self.set_max_fps(max_fps)
        self._previous_time = perf_counter()
        self._start_of_second = self._previous_time
    def set_max_fps(self, max_fps : int = 60) -> None:
        self._max_fps = max_fps
        self._interval = 1./max_fps
    def wait(self) -> None:
        t : float = perf_counter()
        self._frame_count += 1
        if t - self._start_of_second >= 1.:
            self._fps = self._frame_count
            self._frame_count = 0
            self._start_of_second = t
        dt : float = t - self._previous_time
        if(dt < self._interval):
            sleep_interval : float = self._interval - dt
            correct_sleep_interval : float = min(self._interval, sleep_interval)
            sleep(correct_sleep_interval)
        self._previous_time = perf_counter()
    def get_fps(self) -> int:
        return self._fps
