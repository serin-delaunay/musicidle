
# coding: utf-8
import itertools as it
from typing import NamedTuple, TypeVar, Callable, Iterator, Tuple
from vec import vec
from enum import Enum

class RectangleEdgeH(Enum):
    Left : int = 0
    Centre : int = 1
    Right : int = 2
class RectangleEdgeV(Enum):
    Top : int = 0
    Middle : int = 3
    Bottom : int = 6

class RectangleEdge(NamedTuple):
    horizontal : RectangleEdgeH
    vertical: RectangleEdgeV

class _Rectangle(NamedTuple):
    top_left : vec
    size : vec

#T = TypeVar('T',bound='Rectangle')
class Rectangle(_Rectangle):
    def bottom_right(self) -> vec:
        return self.top_left + self.size
    def __contains__(self, xy : vec) -> bool:
        return self.contains(xy)
    def contains(self, xy : vec) -> bool:
        return (self.top_left.x <= xy[0] < self.top_left.x + self.size.x and
                self.top_left.y <= xy[1] < self.top_left.y + self.size.y)
    def contains_rectangle(self, other : 'Rectangle'):
        return (self.top_left.x <= other.top_left.x and
                self.top_left.y <= other.top_left.y and
                self.bottom_right().x >= other.bottom_right().x and
                self.bottom_right().y >= other.bottom_right().y)
    def copy(self, f : Callable[[vec],vec] = lambda x: x.copy()) -> 'Rectangle':
        return Rectangle(f(self.top_left),f(self.size))
    def border_code(self, xy : vec) -> RectangleEdge:
        if xy.x == self.top_left.x:
            h = RectangleEdgeH.Left
        elif xy.x == self.top_left.x+self.size.x-1:
            h = RectangleEdgeH.Right
        else:
            h = RectangleEdgeH.Centre
        if xy.y == self.top_left.y:
            v = RectangleEdgeV.Top
        elif xy.y == self.top_left.y+self.size.y-1:
            v = RectangleEdgeV.Bottom
        else:
            v = RectangleEdgeV.Middle
        return RectangleEdge(h,v)
    def __iter__(self) -> Iterator[vec]:
        br : vec = self.bottom_right()
        return (vec(x,y) for (x,y) in it.product(range(self.top_left.x, br.x),
                                                  range(self.top_left.y, br.y)))
    def iter_codes(self) -> Iterator[Tuple[vec,RectangleEdge]]:
        br : vec = self.bottom_right()
        for (x,y) in it.product(range(self.top_left.x, br.x),
                                range(self.top_left.y, br.y)):
            yield (vec(x,y), self.border_code(vec(x,y)))
