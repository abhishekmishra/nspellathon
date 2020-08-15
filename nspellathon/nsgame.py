# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *


class App:
    def __init__(self, width=640, height=400, fps=30):
        self._running = True
        self._display_surf = None
        self.background = None
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.size = self.width, self.height = width, height

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.background = pygame.Surface(
            self._display_surf.get_size()).convert()
        self.font = pygame.font.SysFont('arial', 20, bold=True)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        milliseconds = self.clock.tick(self.fps)
        self.playtime += milliseconds / 1000.0
        self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
            self.clock.get_fps(), " "*5, self.playtime))

        pygame.display.flip()
        self._display_surf.blit(self.background, (0, 0))
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def draw_text(self, text):
        """Center text in window
        """
        fw, fh = self.font.size(text)  # fw: font width,  fh: font height
        surface = self.font.render(text, True, (0, 255, 0))
        # // makes integer division in python3
        self._display_surf.blit(surface, ((self.width - fw) //
                                   2, (self.height - fh) // 2))


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
