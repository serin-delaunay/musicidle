
# coding: utf-8
from typing import Callable, DefaultDict, List
from collections import defaultdict
from Version import Version
from Game import Game
from sortedcontainers import SortedDict

updates : SortedDict = SortedDict()

Updater = Callable[[Game], None]

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

@register_update(0,0,2)
def _u002(game : Game):
    from Money import Money, MoneyContainer, MoneyVerbosity, values
    game.player.savings = Money(0)
    game.player.tips = MoneyContainer(values['Pig Pen'])

@register_update(0,0,3)
def _u003(game : Game):
    from Agent import Agent
    Agent.__init__(game.player)

@register_update(0,0,4)
def _u004(game : Game):
    from fractions import Fraction
    import Config
    from Timer import Timer
    game.timer = Timer()
    game.timer.time = Fraction(game.frame_counter, Config.FRAMES_PER_SECOND)

@register_update(0,0,5)
def _u005(game : Game):
    del game.frame_counter
