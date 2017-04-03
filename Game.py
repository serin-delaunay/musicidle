
# coding: utf-8
from Player import Player
from typing import Optional, NamedTuple
from shutil import copyfile
from Serialisation import load, dump
import Config
from Version import Version

class Game(object):
    player : Player
    frame_counter : int = 0
    version : Version = Version(0,0,1)
    def __init__(self) -> None:
        self.player = Player()
    def advance(self) -> None:
        self.frame_counter += 1
        if self.frame_counter % Config.SAVE_FRAMES == 0:
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
