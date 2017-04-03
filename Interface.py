
# coding: utf-8
from Presentation import Presentation
from bearlibterminal import terminal as blt
from FPSLimiter import FPSLimiter
from vec import vec
from Mouse import set_mouse_only, get_mouse_input
import Config

class Interface(object):
    presentation : Presentation
    fps_limiter : FPSLimiter = FPSLimiter(Config.FRAMES_PER_SECOND)
    def __init__(self, presentation : Presentation):
        set_mouse_only()
        self.presentation = presentation
        blt.set("window: title = {0}, size = {1}, cellsize = {2}".format(
            Config.WINDOW_TITLE, Config.WINDOW_SIZE.blt(), Config.CELL_SIZE.blt()))
        blt.set("font: {0}, size = {1}, codepage = {2}".format(
            Config.FONT_FILE, Config.FONT_SIZE.blt(), Config.FONT_CODEPAGE))
    def draw(self):
        self.presentation.update()
        blt.clear()
        self.presentation.root.draw(vec(0,0))
        blt.refresh()
    def loop(self):
        while not self.presentation.stop:
            self.fps_limiter.wait()
            self.draw()
            while blt.has_input():
                signal = get_mouse_input()
                self.presentation.handle(signal)
                if self.presentation.stop:
                    break
