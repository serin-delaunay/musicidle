
# coding: utf-8
from euclid3 import Vector2 as vec

vec.__repr__ = lambda self: 'vec({0}, {1})'.format(self.x, self.y)

vec.blt = lambda self: '{0}x{1}'.format(self.x, self.y)
