
# coding: utf-8
from Money import Money, MoneyContainer, MoneyVerbosity, values
from typing import Optional
from shutil import copyfile
from pickle import load, dump
import Config

class Game(object):
    savings : Money = Money(0)
    tips : MoneyContainer = MoneyContainer(values['Pig Pen'])
    frame_counter : int = 0
    def __init__(self, old_game : Optional['Game'] = None) -> None:
        if old_game is None:
            return
        self.savings = old_game.savings
        self.tips = old_game.tips
        self.frame_counter = old_game.frame_counter
    def advance(self) -> None:
        self.frame_counter += 1
        if self.frame_counter % Config.SAVE_FRAMES == 0:
            # TODO draw "Saving" somewhere unobtrusive and force-refresh
            self.save()
    def gain_tip(self) -> None:
        self.tips.add(1)
    def save_tips(self) -> None:
        self.savings.value += self.tips.value
        self.tips.value = 0
    def backup(self) -> None:
        try:
            copyfile(Config.SAVE_FILE, Config.BACKUP_FILE)
        except FileNotFoundError:
            pass
    def save(self) -> None:
        self.backup()
        with open(Config.SAVE_FILE, 'wb') as file:
            dump(self, file)
    @classmethod
    def load(cls) -> 'Game':
        with open(Config.SAVE_FILE, 'rb') as file:
            return cls(load(file))
