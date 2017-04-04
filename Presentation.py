
# coding: utf-8
from Game import Game
from Mouse import MouseEventType
from DisplayElement import DisplayElement, DisplayDict, PrintArgs, Clickable
from vec import vec
import Config

class Presentation(object):
    game : Game
    stop : bool = False
    root : DisplayElement
    def __init__(self, game : Game):
        self.game = game
        self.root = DisplayDict(vec(0,0))
    def update(self):
        self.game.advance()
        tips_text = 'Tips: {0}.'.format(self.game.player.tips)
        self.root.elements['tips'] = Clickable(
            PrintArgs(tips_text, vec(0,0),bbox=Config.WINDOW_SIZE))
        savings_text = 'Savings: {0}.'.format(self.game.player.savings)
        self.root.elements['savings'] = Clickable(
            PrintArgs(savings_text, vec(0,1),bbox=Config.WINDOW_SIZE))
        self.root.elements['extended'] = Clickable(
            PrintArgs(self.game.player.name, vec(0,2), bbox=Config.WINDOW_SIZE))
    def handle(self, signal):
        if signal.event_type == MouseEventType.close:
            self.game.save()
            self.stop = True
        else:
            # find target display element, pass the signal to that
            if signal.event_type == MouseEventType.left:
                self.game.gain_tip()
            elif signal.event_type == MouseEventType.right:
                self.game.save_tips()
