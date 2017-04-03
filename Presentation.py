
# coding: utf-8
from Game import Game
from Mouse import MouseEventType
from DisplayElement import DisplayElement, DisplayDict, PrintArgs
from vec import vec

class Presentation(object):
    game : Game
    stop : bool = False
    root : DisplayElement
    size : vec = vec(0,0)
    def __init__(self, game : Game):
        self.game = game
    def update(self):
        text = 'Tips: {0}. Savings: {1}.'.format(self.game.tips, self.game.savings)
        self.root = PrintArgs(text, vec(0,0),bbox=self.size)
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
