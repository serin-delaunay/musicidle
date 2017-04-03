
# coding: utf-8
from bearlibterminal import terminal as blt

BLT_BLACK : int = blt.color_from_name('black')
BLT_WHITE : int = blt.color_from_name('white')

class Colour(object):
    colour : bool
    def __init__(self, colour : bool) -> None:
        self.colour = colour
    def blt_colour(self) -> int:
        return BLT_WHITE if self.colour else BLT_BLACK
    def __repr__(self) -> str:
        return 'Colour(white)' if self.colour else 'Colour(black)'
    def opposite(self) -> 'Colour':
        return Colour(not self.colour)

white = Colour(True)
black = Colour(False)
