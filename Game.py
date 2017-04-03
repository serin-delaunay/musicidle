
# coding: utf-8
from Money import Money, MoneyContainer, MoneyVerbosity, values

class Game(object):
    savings : Money = Money(0)
    tips : MoneyContainer = MoneyContainer(values['Pig Pen'])
    def __init__(self) -> None:
        pass
    def gain_tip(self) -> None:
        self.tips.add(1)
    def save_tips(self) -> None:
        self.savings.value += self.tips.value
        self.tips.value = 0
    def save(self) -> None:
        pass
    def load(self) -> 'Game':
        return Game()
