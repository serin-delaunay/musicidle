
# coding: utf-8
from Money import Money, MoneyContainer, MoneyVerbosity, values
from typing import Optional
from Agent import Agent
from Performer import Performer

class Player(Performer):
    savings : Money
    def __init__(self) -> None:
        super().__init__()
        self.savings = Money(0)
