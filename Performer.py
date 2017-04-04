
# coding: utf-8
from Agent import Agent

class PerformerBase(object):
    performing : bool
    def __init__(self):
        super().__init__()
        self.performing = False

class Performer(Agent, PerformerBase):
    def __init__(self):
        super().__init__()
