
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
