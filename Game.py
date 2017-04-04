
# coding: utf-8
from Player import Player
from Performance import Performance
from typing import Optional, NamedTuple, List
from shutil import copyfile
from Serialisation import load, dump
from Timer import Timer
import Config
import Data
from Version import Version
from Performer import Performer

class Game(object):
    player : Player
    timer : Timer
    version : Version
    performances : List[Performance]
    performers : List[Performer]
    def __init__(self) -> None:
        self.player = Player()
        self.timer = Timer
        self.performances = []
        self.performers = [self.player]
        self.version = Version(0,0,8)
    def advance(self) -> None:
        self.timer.advance()
        for p in self.performances:
            p.advance(self.timer.dt)
            if p.finished:
                self.save_tips(p)
        self.performances = [p for p in self.performances if not p.finished]
        if self.timer.regular_event(Config.SAVE_SECONDS):
            # TODO draw "Saving" somewhere unobtrusive and force-refresh
            self.save()
    def add_performer(self):
        self.performers.append(Performer())
    def hire_performer(self):
        if self.player.savings.value >= Data.PERFORMER_COST:
            self.player.savings.value -= Data.PERFORMER_COST
            self.add_performer()
    def start_performance(self):
        for p in self.performers:
            if not p.performing:
                self.performances.append(Performance(1,24,0.5,self.timer.time,5, p))
                break
    def save_tips(self, performance) -> None:
        self.player.savings.value += performance.tips.value
        performance.tips.value = 0
    def save_all_tips(self) -> None:
        for p in self.performances:
            self.save_tips(p)
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
