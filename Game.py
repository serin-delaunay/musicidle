
# coding: utf-8
from Player import Player
from typing import Optional, NamedTuple
from shutil import copyfile
from Serialisation import load, dump
from Timer import Timer
import Config
from Version import Version

class Game(object):
    player : Player
    timer : Timer
    version : Version
    def __init__(self) -> None:
        self.player = Player()
        self.timer = Timer
        self.version = Version(0,0,4)
    def advance(self) -> None:
        self.timer.advance()
        if self.timer.regular_event(Config.SAVE_SECONDS):
            # TODO draw "Saving" somewhere unobtrusive and force-refresh
            self.save()
    def gain_tip(self) -> None:
        self.player.tips.add(1)
    def save_tips(self) -> None:
        self.player.savings.value += self.player.tips.value
        self.player.tips.value = 0
    def backup(self) -> None:
        try:
            copyfile(Config.SAVE_FILE, Config.BACKUP_FILE)
        except FileNotFoundError:
            pass
    def valid(self) -> bool:
        # TODO detect incorrect states caused by bugs or version changes
        return True
    def save(self) -> None:
        if self.valid():
            self.backup()
        dump(self, Config.SAVE_FILE)
    @classmethod
    def load(cls) -> 'Game':
        game : 'Game' = load(Config.SAVE_FILE)
        return game
