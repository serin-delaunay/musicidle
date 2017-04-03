
# coding: utf-8
from bearlibterminal import terminal as blt
from typing import NamedTuple, Any
from enum import Enum
from abc import ABCMeta, abstractmethod
from vec import vec
from FPSLimiter import FPSLimiter

class MouseEventType(Enum):
    left = blt.TK_MOUSE_LEFT
    right = blt.TK_MOUSE_RIGHT
    middle = blt.TK_MOUSE_MIDDLE
    move = blt.TK_MOUSE_MOVE
    scroll = blt.TK_MOUSE_SCROLL
    close = blt.TK_CLOSE

class MouseEventBase(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def _read(cls) -> 'MouseEventBase': pass
    @staticmethod
    def mouse_position() -> vec:
        return vec(blt.state(blt.TK_MOUSE_X, blt.TK_MOUSE_Y))

class _MouseClickEvent(NamedTuple):
    event_type : MouseEventType
    xy : vec
    clicks : int

class MouseClickEvent(_MouseClickEvent, MouseEventBase):
    @classmethod
    def _read(cls) -> 'MouseClickEvent':
        return cls(MouseEventType(blt.read()),
                   cls.mouse_position(),
                   blt.state(blt.TK_MOUSE_CLICKS))

class _MouseMoveEvent(NamedTuple):
    event_type : MouseEventType
    xy : vec

class MouseMoveEvent(_MouseMoveEvent, MouseEventBase):
    @classmethod
    def _read(cls) -> 'MouseMoveEvent':
        return cls(MouseEventType(blt.read()),
                   cls.mouse_position())

class _MouseScrollEvent(NamedTuple):
    event_type : MouseEventType
    xy : vec
    wheel : int

class MouseScrollEvent(_MouseScrollEvent, MouseEventBase):
    @classmethod
    def _read(cls) -> 'MouseScrollEvent':
        return cls(MouseEventType(blt.read()),
                   cls.mouse_position(),
                   blt.state(blt.TK_MOUSE_WHEEL))

class MouseCloseEvent(MouseEventBase):
    event_type : MouseEventType = MouseEventType.close
    @classmethod
    def _read(cls) -> 'MouseCloseEvent':
        blt.read()
        return cls()
    def __repr__(self) -> str:
        return 'MouseMoveEvent(event_type={0})'.format(self.event_type)

def set_mouse_only():
    blt.set('input.filter = [mouse]')

def get_mouse_input():
    event_type = blt.peek()
    if event_type == MouseEventType.move.value:
        return MouseMoveEvent._read()
    elif event_type == MouseEventType.scroll.value:
        return MouseScrollEvent._read()
    elif event_type == MouseEventType.close.value:
        return MouseCloseEvent()
    else:
        return MouseClickEvent._read()

if __name__ == '__main__':
    blt.open()
    set_mouse_only()
    blt.refresh()
    fl = FPSLimiter()
    stop = False
    while not stop:
        fl.wait()
        while blt.has_input():
            event = get_mouse_input()
            print(event)
            if event.event_type == MouseEventType.close:
                blt.close()
                stop = True
                break
