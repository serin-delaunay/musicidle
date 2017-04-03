
# coding: utf-8
from Money import Money, MoneyContainer, MoneyVerbosity, values
from typing import Optional

class Player(object):
    savings : Money
    tips : MoneyContainer
    def __init__(self) -> None:
        self.savings = Money(0)
        self.tips = MoneyContainer(values['Pig Pen'])
