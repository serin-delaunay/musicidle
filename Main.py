
# coding: utf-8
from bearlibterminal import terminal as blt
blt.open()

from Game import Game
from Presentation import Presentation
from Interface import Interface

if __name__ == '__main__':
    game = Game()
    presentation = Presentation(game)
    interface = Interface(presentation)
    interface.loop()
