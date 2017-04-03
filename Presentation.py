
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
        chars_text = """\u263A\u263B\u2665\u2666\u2663\u2660\u25CF\u25D8\u25CB\u25D9\u2642\u2640\u266A\u266B\u263C\u25BA\u25C4\u2195\u203C\u00B6\u00A7\u2017\u21A8\u2191\u2193\u2192\u2190\u221F\u2194\u25B2\u25BC
\u00C7\u00FC\u00E9\u00E2\u00E4\u00E0\u00E5\u00E7\u00EA\u00EB\u00E8\u00EF\u00EE\u00EC\u00C4\u00C5\u00C9\u00E6\u00C6\u00F4\u00F6\u00F2\u00FB\u00F9\u00FF\u00D6\u00DC\u00F8\u00A3\u00D8\u00D7\u0192
\u00E1\u00ED\u00F3\u00FA\u00F1\u00D1\u00AA\u00BA\u00BF\u00AE\u00AC\u00BD\u00BC\u00A1\u00AB\u00BB\u2591\u2592\u2593\u2502\u2524\u00C1\u00C2\u00C0\u00A9\u2563\u2551\u2557\u255D\u00A2\u00A5\u2510
\u2514\u2534\u252C\u251C\u2500\u253C\u00E3\u00C3\u255A\u2554\u2569\u2566\u2560\u2550\u256C\u00A4\u00F0\u00D0\u00CA\u00CB\u00C8\u0131\u00CD\u00CE\u00CF\u2518\u250C\u2588\u2584\u00A6\u00CC\u2580
\u00D3\u00DF\u00D4\u00D2\u00F5\u00D5\u00B5\u00FE\u00DE\u00DA\u00DB\u00D9\u00FD\u00DD\u00AF\u00B4\u00AD\u00B1\u2017\u00BE\u00B6\u00A7\u00F7\u00B8\u00B0\u00A8\u00B7\u00B9\u00B3\u00B2\u25A0\u00A0"""
        self.root.elements['extended'] = Clickable(
            PrintArgs(chars_text, vec(0,2), bbox=Config.WINDOW_SIZE))
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
