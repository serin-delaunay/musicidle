
# coding: utf-8
from bearlibterminal import terminal as blt
blt.open()

from Game import Game
from Presentation import Presentation
from Interface import Interface

if __name__ == '__main__':
    game : Game
    try:
        game = Game.load()
    except FileNotFoundError:
        print("No saved game found, starting new game\n")
        game = Game()
    presentation : Presentation = Presentation(game)
    interface : Interface = Interface(presentation)
    interface.loop()
