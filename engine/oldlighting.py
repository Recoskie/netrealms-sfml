import pygame
import math

class LightMap:

    def __init__(self, screen, alpha):
        self.screen = screen
        self.alpha = alpha
        self.lights = []

    def draw(self):
        self.image = pygame.Surface((self.screen.get_size()), pygame.SRCALPHA)
        self.image.fill((0,0,0, self.alpha))

        for light in self.lights:
            light.draw()

        self.image.unlock()
        self.screen.blit(self.image, (0, 0))
        self.image.lock()

    def addLight(self, size, source, luminosity):
        self.lights.append(LightSource(size, source, self, luminosity))

class LightSource:

    def __init__(self, size, source, lightMap, luminosity):
        self.size = size
        self.source = source
        self.lightMap = lightMap
        self.luminosity = luminosity

    def draw(self):
        size = self.size
        x, y = self.source.physics['x'] + 32, self.source.physics['y'] + 48 #position of light source

        if self.lightMap.alpha > self.luminosity:

            tempsize = size - 2

            lumino = self.luminosity
            
            pi = math.pi

            i = 0
            r = size
            while r > 0:
                while i < 360:
                    angle = i
                    x1 = r * math.cos(angle * pi / 180)
                    y1 = r * math.sin(angle * pi / 180)

                    x1 = int(x1)
                    y1 = int(y1)
                    pygame.surfarray.pixels_alpha(self.lightMap.image)[x + x1, y + y1] = lumino

                    i = i + 1

                r = r - 1

            while tempsize < 0:
                if lumino > 0:
                    lumino = lumino - 1


                pygame.surfarray.pixels_alpha(self.lightMap.image)[x - tempsize / 2:x + tempsize / 2, y - tempsize / 2:y + tempsize / 2] = lumino
                tempsize = tempsize - 1
            #tempsize = fraction
            #pygame.surfarray.pixels_alpha(self.lightMap.image)[x - tempsize / 2:x + tempsize / 2, y - tempsize / 2:y + tempsize / 2] = lumino


        