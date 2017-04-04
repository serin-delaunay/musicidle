
# coding: utf-8
from typing import Callable, DefaultDict, List
from collections import defaultdict
from Version import Version
from Game import Game
from sortedcontainers import SortedDict

updates : SortedDict = SortedDict()

Updater = Callable[[Game], None]

hotfixes : List[Updater] = []

def register_update(major : int = 0,
                    minor : int = 0,
                    revision : int = 0):
    def register_update_aux(f : Updater):
        version = Version(major,minor,revision)
        try:
            updates[version].append(f)
        except KeyError:
            updates[version] = [f]
        return f
    return register_update_aux

def update(game : Game) -> None:
    original_version : Version = game.version
    version : Version
    for version in updates.islice(updates.bisect_right(original_version)):
        u : Updater
        for u in updates[version]:
            u(game)
            game.version = version
    h : Updater
    for h in hotfixes:
        h(game)

def hotfix(f : Updater):
    hotfixes.append(f)

@register_update(0,0,2)
def _update(game : Game):
    from Money import Money, MoneyContainer, MoneyVerbosity, values
    game.player.savings = Money(0)
    game.player.tips = MoneyContainer(values['Pig Pen'])

@register_update(0,0,3)
def _update(game : Game):
    from Agent import Agent
    Agent.__init__(game.player)

@register_update(0,0,4)
def _update(game : Game):
    from fractions import Fraction
    import Config
    from Timer import Timer
    game.timer = Timer()
    game.timer.time = Fraction(game.frame_counter, Config.FRAMES_PER_SECOND)

@register_update(0,0,5)
def _update(game : Game):
    del game.frame_counter

@register_update(0,0,6)
def _update(game : Game):
    game.performances = []

@register_update(0,0,7)
def _update(game : Game):
    del game.player.tips

@register_update(0,0,8)
def _update(game : Game):
    game.performers = [game.player]
    for p in game.performances:
        p.performer = game.player
    game.player.performing = False

@hotfix
def _update(game : Game):
    pass
