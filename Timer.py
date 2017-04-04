
# coding: utf-8
from fractions import Fraction
from typing import Union
import Config

class Timer(object):
    time : Fraction
    dt : int
    def __init__(self) -> None:
        self.time = Fraction(0)
        self.change_fps(Config.FRAMES_PER_SECOND)
    def frame(self) -> int:
        return int(self.time * self.dt.denominator)
    def regular_event(self, interval : Union[Fraction, int]) -> bool:
        return self.time % interval < self.dt
    def advance(self) -> None:
        self.time += self.dt
    def normalise(self) -> None:
        self.time = Fraction(int(self.frame()), self.dt.denominator)
    def change_fps(self, new_fps):
        self.dt = Fraction(1, new_fps)
        self.normalise()
