
# coding: utf-8
from Names import make_name

class Agent(object):
    name : str
    def __init__(self):
        self.name = make_name()
