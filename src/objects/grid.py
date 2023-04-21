# grid.py

from src.config import Config as C
import pygame
import random
import numpy as np
from perlin_noise import PerlinNoise


SCREEN = C["SCREEN_SIZE"]
BACKGROUND_COLOR = C["BACKGROUND_COLOR"]
CELLS = C["CELLS"]
FPS = C["FPS"]
DECAY_RATE = C["DECAY_RATE"]


class Grid:
    def __init__(self, cell_size, color):
        self.cell_size = cell_size
        self.color = color

    def draw(self, surface, SCREEN):
        # Get the array representing the surface
        surf_array = pygame.surfarray.array3d(surface)

        # Iterate over the grid using steps equal to cell_size
        for x in range(0, SCREEN[0], self.cell_size):
            for y in range(0, SCREEN[1], self.cell_size):
                if random.choice([True, False]):
                    surf_array[x:x+self.cell_size, y:y+self.cell_size] = self.color

        # Update the surface with the modified arrays
        pygame.surfarray.blit_array(surface, surf_array)


class Layer:

    def __init__(self):
        self.surfSize = (int(SCREEN[0] / CELLS), int(SCREEN[1] / CELLS))
        self.image = pygame.Surface(self.surfSize).convert()
        self.img_array = np.array(pygame.surfarray.array3d(self.image), dtype=float)
        self.last_update = pygame.time.get_ticks()
        self.oct = 15
        self.seed = 1
        self.counter = 0
        self.counterTot = 0
        self.lowest = 0
        self.font18 = pygame.font.Font(None, 18)
        self.text = ""
        self.textDone = ""
        self.lowestX = 0
        self.lowestY = 0

    def update(self, dt):
        # self.img_array -= dt * DECAY_RATE
        self.img_array = self.img_array.clip(0, 255)
        pygame.surfarray.blit_array(self.image, self.img_array)
        return self.image

    def draw(self, surface):
        if self.counter != 0:
            self.text = f"Generating Map, Nr: {self.counter}"
            text_mapsgen_surface = self.font18.render(f"{self.text}", True, pygame.Color("white"))
        else:
            text_mapsgen_surface = self.font18.render(f"{self.textDone}", True, pygame.Color("white"))

        rescaled_img = pygame.transform.scale(self.image, (SCREEN[0], SCREEN[1]))
        pygame.Surface.blit(surface, rescaled_img, (0, 0))
        surface.blit(text_mapsgen_surface, (SCREEN[0]/2-text_mapsgen_surface.get_width()/2, SCREEN[1]-50))
        if self.lowestX != 0 and self.lowestY != 0:
            pygame.draw.circle(
                surface, (255, 255, 255),
                (self.lowestX*CELLS, self.lowestY*CELLS),
                int(SCREEN[0] / CELLS * 0.05))

    def newNoise(self, dt, surface):
        self.counter += 1
        self.counterTot += 1
        self.textDone = f"Cycles: {self.counterTot}"
        self.seed = random.randrange(0, 2000) + (dt * 1000)
        if self.counter < 2:
            surface.fill(BACKGROUND_COLOR)
            self.draw(surface)
            pygame.display.flip()
            self.noise = PerlinNoise(octaves=self.oct, seed=self.seed)
            self.lowestX = 0
            self.lowestY = 0
            for i in range(int(SCREEN[1]/CELLS)):
                for j in range(int(SCREEN[0]/CELLS)):
                    currNoise = self.noise([(i)/SCREEN[0], (j)/SCREEN[1]])
                    self.img_array[i, j] = (0, 0, 0)
                    if currNoise > 0.11:
                        # self.img_array[i, j] += (0, (1 if currNoise > 0.075 else 0)*255, 0)
                        self.img_array[i, j] = (50, 50, 50)
                    elif currNoise < 0.05:
                        if currNoise < self.lowest:
                            self.lowest = currNoise
                            self.lowestX = i
                            self.lowestY = j
            for i in range(int(SCREEN[1]/CELLS)):
                for j in range(int(SCREEN[0]/CELLS)):
                    currNoise = self.noise([(i)/SCREEN[0], (j)/SCREEN[1]])
                    if currNoise < -0.3:
                        if self.lowestX > int(i + 50) or self.lowestX < int(i - 50) or self.lowestY < int(j - 50) or self.lowestY > int(j + 50):
                            self.img_array[i, j] = (0, 255, 0)
                    # elif currNoise < 0.1:
                    #     self.img_array[i, j] = (0, 0, 50+(100*-currNoise))
                    #     # self.img_array[i, j] += (0, (1 if currNoise > 0.075 else 0)*255, 0)
            # Remap-Func
            if self.lowestX < int(SCREEN[0] / CELLS * 0.01) or self.lowestX > int(SCREEN[0] / CELLS * 0.99) or self.lowestY < int(
                    SCREEN[1] / CELLS * 0.01) or self.lowestY > int(SCREEN[1] / CELLS * 0.99):
                self.newNoise(dt, surface)
            else:
                self.img_array[self.lowestX, self.lowestY] = (255, 0, 0)

            self.counter = 0
            self.counterTot = 0
