
# coding: utf-8
from typing import NamedTuple, Optional, Union, Iterator, Dict, Callable, Any, TypeVar, List
from bearlibterminal import terminal as blt
from abc import ABCMeta, abstractmethod
from vec import vec
from Colour import Colour, black, white
from enum import Enum, auto
from Game import Game
from Rectangle import Rectangle
from Mouse import MouseEventBase, MouseEventType

class DisplayElement(metaclass=ABCMeta):
    @abstractmethod
    def draw(self, xy : vec, layer : int = 0) -> None: pass

class _PutArgs(NamedTuple):
    char : Union[int,str]
    xy : vec
    dxy : vec = vec(0,0)
    colour : Colour = white
    has_background : bool = False

class PutArgs(DisplayElement, _PutArgs):
    def draw(self, xy : vec, layer : int = 0) -> None:
        blt.layer(layer)
        rxy : vec = xy + self.xy
        if self.has_background:
            blt.color(self.colour.opposite().blt_colour())
            blt.put_ext(rxy.x, rxy.y, self.dxy.x, self.dxy.y, '█')
        blt.color(self.colour.blt_colour())
        blt.put_ext(rxy.x, rxy.y, self.dxy.x, self.dxy.y, self.char)

class TextAlignmentH(Enum):
    Left : int = blt.TK_ALIGN_LEFT
    Centre : int = blt.TK_ALIGN_CENTER
    Right : int = blt.TK_ALIGN_RIGHT
    Default : int = blt.TK_ALIGN_DEFAULT
class TextAlignmentV(Enum):
    Top : int = blt.TK_ALIGN_TOP
    Middle : int = blt.TK_ALIGN_MIDDLE
    Bottom : int = blt.TK_ALIGN_BOTTOM
    Default : int = blt.TK_ALIGN_DEFAULT

class _TextAlignment(NamedTuple):
    horizontal : TextAlignmentH = TextAlignmentH.Default
    vertical : TextAlignmentV = TextAlignmentV.Default

class TextAlignment(_TextAlignment):
    def code(self) -> int:
        return self.horizontal.value + self.vertical.value

class _PrintArgs(NamedTuple):
    text : str
    xy : vec
    colour : Colour = white
    has_background : bool = False
    bbox : Optional[vec] = None
    align : TextAlignment = TextAlignment()

class PrintArgs(DisplayElement, _PrintArgs):
    def draw(self, xy : vec, layer : int = 0) -> None:
        rxy : vec = xy + self.xy
        if self.has_background:
            background = ('█'*self.bbox.x+'\n')*self.bbox.y
            blt.color(self.colour.opposite().blt_colour())
            if self.bbox is None:
                blt.print_(rxy.x,rxy.y, background)
            else:
                blt.print_(rxy.x,rxy.y, background,
                           self.bbox.x, self.bbox.y,
                           self.align.code())
        blt.color(self.colour.blt_colour())
        if self.bbox is None:
            blt.print_(rxy.x, rxy.y, self.text)
        else:
            blt.print_(rxy.x, rxy.y, self.text,
                       self.bbox.x, self.bbox.y,
                       self.align.code())

Handlers = Dict[MouseEventType, Callable[[MouseEventBase],Any]]

class Clickable(object):
    element : DisplayElement
    mouse_rect : Rectangle
    handlers : Handlers
    def __init__(self, element : DisplayElement,
                 mouse_rect : Rectangle = Rectangle(vec(0,0), vec(0,0)),
                 mouse_rect_auto : bool = False,
                 handlers : Handlers = {}) -> None:
        self.element = element
        self.mouse_rect = mouse_rect
        if mouse_rect_auto:
            self.mouse_rect = Rectangle(self.element.xy, self.element.bbox)
        self.handlers = handlers.copy()
    def find_target(self, xy : vec,  event_type : MouseEventType) -> Optional['Clickable']:
        if xy in self.mouse_rect:
            if isinstance(self.element, DisplayGroup):
                for clickable in self.element:
                    result = clickable.find_target(
                        xy - self.mouse_rect.top_left,
                        event_type)
                    if result is not None:
                        return result
            if event_type in self.handlers:
                return self
        return None
    def handle(self, event : MouseEventBase, game : Game) -> None:
        self.handlers[event.event_type](event, game)

class DisplayGroup(DisplayElement, metaclass=ABCMeta):
    xy : vec
    def __init__(self, xy : vec) -> None:
        self.clear_elements()
        self.xy = xy
    def draw(self, xy : vec, layer : int = 0) -> None:
        rxy : vec = self.xy + xy
        for clickable in self:
            element : DisplayElement = clickable.element
            if isinstance(element, DisplayGroup):
                element.draw(xy, layer + 1)
            else:
                element.draw(xy, layer)
    @abstractmethod
    def clear_elements(self) -> None: pass
    @abstractmethod
    def __iter__(self) -> Iterator[Clickable]: pass

class DisplayList(DisplayGroup):
    elements : List[Clickable]
    def clear_elements(self) -> None:
        self.elements = []
    def __iter__(self) -> Iterator[Clickable]:
        return iter(self.elements)

class DisplayDict(DisplayGroup):
    elements : Dict[str,Clickable]
    def clear_elements(self) -> None:
        self.elements = {}
    def __iter__(self) -> Iterator[Clickable]:
        return iter(self.elements.values())
