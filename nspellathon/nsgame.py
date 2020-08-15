# -*- coding: utf-8 -*-
import math
import pygame
from pygame.locals import *
from nspellathon.nspellathon import create_spellathon


class App:
    def __init__(self, width=640, height=400, fps=30):
        self._running = True
        self._display_surf = None
        self.background = None
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.playtime = 0.0
        self.size = self.width, self.height = width, height
        self.spellathon = create_spellathon()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.background = pygame.Surface(
            self._display_surf.get_size()).convert()
        self.font = pygame.font.SysFont('arial', 40, bold=True)
        self._running = True
        self.spellathon.print_puzzle()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self.draw_polygon((0.9 * self.height)/2, 6, (255, 204, 255), self.width/2, self.height/2)
        self.draw_polygon((0.4 * self.height)/2, 6, (255, 204, 204), self.width/2, self.height/2)

        upper_letters = self.spellathon.letters.upper()
        central_letter = upper_letters[self.spellathon.central_index]
        upper_letters = upper_letters[:self.spellathon.central_index] + upper_letters[self.spellathon.central_index+1:]
        x = self.width/2
        y = self.height/2
        r = (0.65 * self.height)/2
        n = 6
        for i in range(n):
            j = i + 0.5
            px = x + (r * math.cos(2 * math.pi * j / n))
            py = y + (r * math.sin(2 * math.pi * j / n))
            self.draw_alpha(upper_letters[i].upper(), px, py)
        self.draw_alpha(self.spellathon.get_central_char().upper(), self.width/2, self.height/2)
        milliseconds = self.clock.tick(self.fps)
        self.playtime += milliseconds / 1000.0
        self.draw_text("FPS: {:6.3}{}PLAYTIME: {:6.3} SECONDS".format(
            self.clock.get_fps(), " "*5, self.playtime))
        pygame.display.flip()
        self._display_surf.blit(self.background, (0, 0))

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
                                   2, (self.height - fh)))

    def draw_alpha(self, text, locx, locy):
        fw, fh = self.font.size(text)  # fw: font width,  fh: font height
        surface = self.font.render(text, True, (0, 0, 0))
        # // makes integer division in python3
        self._display_surf.blit(surface, ((locx - fw//2), (locy - fh//2)))

    def draw_polygon(self, r, n, c=(0, 0, 255), x=200, y=200):
        # https://stackoverflow.com/questions/3436453/calculate-coordinates-of-a-regular-polygons-vertices
        # for (i = 0; i < n; i++) {
        #  printf("%f %f\n",r * Math.cos(2 * Math.PI * i / n), r * Math.sin(2 * Math.PI * i / n));
        #}
        pts = []
        for i in range(n):
            px = x + (r * math.cos(2 * math.pi * i / n))
            py = y + (r * math.sin(2 * math.pi * i / n))
            #print("{x}={y}".format(x=x, y=y))
            pts.append((px, py))
        pygame.draw.polygon(self._display_surf, c, pts)

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
