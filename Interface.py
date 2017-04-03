
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
        self.presentation.size.x = blt.state(blt.TK_WIDTH)
        self.presentation.size.y = blt.state(blt.TK_HEIGHT)
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
