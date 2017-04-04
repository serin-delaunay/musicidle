
# coding: utf-8
from Money import Money, MoneyContainer, MoneyVerbosity, values
from typing import Optional
from Agent import Agent

class Player(Agent):
    savings : Money
    tips : MoneyContainer
    def __init__(self) -> None:
        super().__init__()
        self.savings = Money(0)
        self.tips = MoneyContainer(values['Pig Pen'])
