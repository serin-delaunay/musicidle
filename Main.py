
# coding: utf-8
from bearlibterminal import terminal as blt
blt.open()

from Game import Game
from Presentation import Presentation
from Interface import Interface
from json import JSONDecodeError
from Updates import update

if __name__ == '__main__':
    game : Game
    try:
        game = Game.load()
        update(game)
    except (FileNotFoundError, JSONDecodeError):
        print("No saved game found, starting new game\n")
        game = Game()
    presentation : Presentation = Presentation(game)
    interface : Interface = Interface(presentation)
    interface.loop()
