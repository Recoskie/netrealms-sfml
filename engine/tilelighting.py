import pygame
import math
import numpy

class Static:

    def __init__(self, xpos, ypos):
        self.physics = dict(
            x = xpos,
            y = ypos
        )

class LightMap:

    def __init__(self, screen, alpha):
        self.screen = screen
        self.alpha = alpha
        self.lights = []
        self.background = sf.Image.create(20, 20, sf.Color(0,0,0,alpha))

    def draw(self):
        if self.alpha > 0: #there is no darkness, no need to draw lights
            self.image = pygame.Surface((self.screen.get_size()), pygame.SRCALPHA)
            self.image.fill((0,0,0, self.alpha))

            for light in self.lights:
                light.draw()


            self.image.unlock()
            self.screen.blit(self.image, (0, 0))
            self.image.lock()

    def set_alpha(self, alpha):
        self.alpha = alpha

    def addLight(self, size, source):
        self.lights.append(LightSource(size, source, self))

    def addStaticLight(self, size, x, y):
        self.lights.append(LightSource(size, Static(x, y), self))

class LightSource:

    def __init__(self, size, source, lightMap):
        self.size = size
        self.source = source
        self.lightMap = lightMap

    def draw(self):
        size = self.size
        x, y = self.source.physics['x'], self.source.physics['y'] #position of light source

        #Light tile size

        tile_size =  16

        #center of player
        x = x + 32
        y = y + 48

        x = int( x / tile_size + 0.5 ) * tile_size # x center
        y = int( y / tile_size + 0.5 ) * tile_size # y center

        x0 = x
        y0 = y

        r = size # radius

        #to calculate the difference from the circle center

        CurX = x0
        CurY = y0

        t1 = 0
        t2 = 0

        #calculate the circle points

        for x in range(x0 - r, x0 + r + 1):
            ydist = int(round(math.sqrt(r**2 - (x0 - x)**2), 1))
            for y in range(y0 - ydist, y0 + ydist + 1):
                #x * t, y * t, x * t + t, y * t + t

                t1 = x0 + ( (x-CurX) * tile_size )
                t2 = y0 + ( (y-CurY) * tile_size )

                px = math.floor(t1 / tile_size + 0.5)
                py = math.floor(t2 / tile_size + 0.5)
                if px >= 0 and px < 64 and py >= 0 and py < 48:
                    tile_alpha = int(self.lightMap.alpha * math.sqrt((x0 - x)**2 + (y0 - y)**2) / r)
                    if pygame.surfarray.pixels_alpha(self.lightMap.image)[t1+1, t2+1 ] > tile_alpha:
                        pygame.surfarray.pixels_alpha(self.lightMap.image)[t1:t1 + ( tile_size + 1 ), t2:t2 + ( tile_size + 1 ) ] = tile_alpha