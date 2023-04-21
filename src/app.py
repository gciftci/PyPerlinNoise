# app.py
import pygame
import random
# Modules
from src.config import Config as C
from src.objects import grid
'''
@TODO
- Add ants
- add proper deltatiming
- cleanup
- docstring
- cavegen?
'''


SCREEN = C["SCREEN_SIZE"]
BACKGROUND_COLOR = C["BACKGROUND_COLOR"]
CELLS = C["CELLS"]
FPS = C["FPS"]


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.font24 = pygame.font.Font(None, 24)
        self.layer = grid.Layer()
        self.running = True

    def event_handler(self, py_event, dt):
        for event in py_event:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r:
                    self.layer.newNoise(dt, self.screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                i = int(pygame.mouse.get_pos()[0]/CELLS)
                j = int(pygame.mouse.get_pos()[1]/CELLS)
                print([i, j], self.layer.noise([(i)/SCREEN[0], (j)/SCREEN[1]]), self.layer.img_array[i, j])

    def update_handler(self, dt):
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_SHIFT:
            i = int(pygame.mouse.get_pos()[0] / CELLS)
            j = int(pygame.mouse.get_pos()[1] / CELLS)
            self.layer.img_array[i, j] = (0, 150, 0)
        elif mods & pygame.KMOD_CTRL:
            i = int(pygame.mouse.get_pos()[0] / CELLS)
            j = int(pygame.mouse.get_pos()[1] / CELLS)
            self.layer.img_array[i, j] += (150, 0, 0)
        elif mods & pygame.KMOD_ALT:
            i = int(pygame.mouse.get_pos()[0] / CELLS)
            j = int(pygame.mouse.get_pos()[1] / CELLS)
            self.layer.img_array[i, j] += (0, 0, 150)
        self.layer.update(dt)

    def draw_handler(self):
        self.screen.fill(BACKGROUND_COLOR)
        # self.red_grid.draw(self.screen, SCREEN)
        # self.green_grid.draw(self.screen, SCREEN)
        self.layer.draw(self.screen)

        text_fps_surface = self.font24.render(f"{int(self.clock.get_fps())}", True, pygame.Color("white"))
        self.screen.blit(text_fps_surface, (10, 10))

        text_pressr_surface = self.font24.render('Press "R" to generate map', True, pygame.Color("white"))
        self.screen.blit(text_pressr_surface, (SCREEN[0]/2-text_pressr_surface.get_width()/2, 10))
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.event_handler(pygame.event.get(), dt)
            self.update_handler(dt)
            self.draw_handler()
        pygame.quit()
