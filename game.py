import pygame
from pygame import Surface, draw, display, event, key,mouse
import time
from pygame import cursors
from pygame.cursors import Cursor
from chess import *

class Game:
    current_time: float = 0
    last_time: float = 0
    renderer: Surface
    running: bool = True
    blockFPS = False
    fpsmax = 0

    def __init__(self, size):
        pygame.init()
        self.renderer = display.set_mode(size)

    def fps_max(self,value):
       
        if value <= 0:
            self.blockFPS = False
        else:
            self.blockFPS = True
            self.fpsmax = value

    def start(self):
        while self.running:
            # time.clock_gettime(time.CLOCK_PROCESS_CPUTIME_ID)
            self.current_time = float(time.time())
            deltatime = (self.current_time - self.last_time)
            self.last_time = self.current_time

            self.renderer.fill((0, 0, 0))

            self.update(deltatime)
            self.draw()

            display.flip()
            if self.blockFPS:
                pygame.time.Clock().tick(self.fpsmax)

    def draw(self):
        pass

    def update(self, deltatime):
        pass


