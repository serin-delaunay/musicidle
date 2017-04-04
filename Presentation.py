
# coding: utf-8
from Game import Game
from Mouse import MouseEventType
from DisplayElement import DisplayElement, DisplayDict, PrintArgs, Clickable, TextAlignment, TextAlignmentH, TextAlignmentV
from vec import vec
from Colour import black
from Rectangle import Rectangle
import Config

class Presentation(object):
    game : Game
    stop : bool = False
    root : DisplayElement
    def __init__(self, game : Game):
        self.game = game
        self.root = Clickable(DisplayDict(vec(0,0)),Rectangle(vec(0,0),Config.WINDOW_SIZE))
    def draw(self):
        self.root.element.draw(vec(0,0))
    def set_element(self, name, element, *args, **kwargs) -> Clickable:
        c = Clickable(element, *args, **kwargs)
        self.root.element.elements[name] = c
        return c
    def update(self):
        self.game.advance()
        player_text = 'Name: {0}'.format(self.game.player.name)
        self.set_element('name', PrintArgs(
            player_text, vec(0,0), bbox=Config.WINDOW_SIZE))
        performers_text = 'Performers: {0}.'.format(len(self.game.performers))
        self.set_element('performers',PrintArgs(
            performers_text, vec(0,1),bbox=Config.WINDOW_SIZE))
        performances_text = 'Performances: {0}.'.format(len(self.game.performances))
        self.set_element('performances',PrintArgs(
            performances_text, vec(0,2),bbox=Config.WINDOW_SIZE))
        savings_text = 'Savings: {0}.'.format(self.game.player.savings)
        self.set_element('savings',PrintArgs(
            savings_text, vec(0,3),bbox=Config.WINDOW_SIZE))
        hire_performer = self.set_element('hire_performer',PrintArgs(
            'HIRE\nPERFORMER', vec(0,Config.WINDOW_SIZE.y-2),bbox=vec(11,2),
            colour=black, has_background=True,
            align=TextAlignment(TextAlignmentH.Centre)), mouse_rect_auto = True)
        hire_performer.handlers[MouseEventType.left] = lambda m, g : g.hire_performer()
        start_performance = self.set_element('start_performance', PrintArgs(
            'PERFORM', vec(12, Config.WINDOW_SIZE.y - 2), bbox = vec(9,2),
            colour=black, has_background = True,
            align=TextAlignment(TextAlignmentH.Centre)),
            mouse_rect_auto = True)
        start_performance.handlers[MouseEventType.left] = lambda m, g : g.start_performance()
    def handle(self, event):
        if event.event_type == MouseEventType.close:
            self.game.save()
            self.stop = True
        else:
            target = self.root.find_target(event.xy, event.event_type)
            if target is not None:
                target.handle(event, self.game)
