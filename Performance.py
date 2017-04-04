
# coding: utf-8
from Money import Money, MoneyContainer, values
from typing import NamedTuple, Union
from numpy.random import poisson
from fractions import Fraction

class Performance(object):
    tip_size : Money
    tips : MoneyContainer
    tip_rate : float
    start_time : Fraction
    end_time : Fraction
    duration : Fraction
    finished : bool
    def __init__(self,
                 tip_size : int, tips : int, tip_rate : float, 
                 start_time : Union[Fraction, int], duration : Union[Fraction,int]):
        self.tip_size = Money(tip_size)
        self.tips = MoneyContainer(tips)
        self.tip_rate = tip_rate
        self.start_time = Fraction(start_time)
        self.duration = Fraction(duration)
        self.end_time = start_time + duration
        self.previous_time = self.start_time
        self.finished = False
    def advance(self, dt : Fraction):
        current_time = min(self.previous_time + dt, self.end_time)
        if current_time >= self.end_time or current_time < self.start_time:
            self.finished = True
        real_dt = current_time - self.previous_time
        self.previous_time = current_time
        tip_count = poisson(self.tip_rate * real_dt)
        tip_total = self.tip_size.value * tip_count
        self.tips.add(tip_total)
    def expectation(self):
        return float(self.tip_size.value * self.duration * self.tip_rate)
