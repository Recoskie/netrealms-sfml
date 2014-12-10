import pygame
import math
import numpy

class LightMap:

    def __init__(self, screen, alpha):
        self.screen = screen
        self.alpha = alpha
        self.lights = []

    def draw(self):
        if self.alpha > 0: #there is no darkness, no need to draw lights
            self.image = pygame.Surface((self.screen.get_size()), pygame.SRCALPHA)
            self.image.fill((0,0,0, self.alpha))

            for light in self.lights:
                light.draw()


            self.image.unlock()
            self.screen.blit(self.image, (0, 0))
            self.image.lock()

    def addLight(self, size, source, alpha):
        self.lights.append(LightSource(size, source, self, alpha))

class LightSource:

    def __init__(self, size, source, lightMap, alpha):
        self.size = size
        self.source = source
        self.lightMap = lightMap
        self.alpha = alpha

    def draw(self):
        size = self.size
        x, y = self.source.physics['x'], self.source.physics['y'] #position of light source

        #center of player
        x = x + 32
        y = y + 48

        tile_size = 8

        #get the closest tile
        x = math.floor(x / tile_size + 0.5)
        y = math.floor(y / tile_size + 0.5)

        x0 = int(x) # x center
        y0 = int(y) # y center
        r = size  # radius

        tile_alpha = self.alpha

        for x in range(x0 - r, x0 + r + 1):

            ydist = int(round(math.sqrt(r**2 - (x0 - x)**2), 1))
            for y in range(y0 - ydist, y0 + ydist + 1):
                #x * t, y * t, x * t + t, y * t + t
                if pygame.surfarray.pixels_alpha(self.lightMap.image)[x * tile_size, y * tile_size] > tile_alpha:
                    pygame.surfarray.pixels_alpha(self.lightMap.image)[x * tile_size:x * tile_size + tile_size, y * tile_size:y * tile_size + tile_size] = tile_alpha

        #set the tile alpha
