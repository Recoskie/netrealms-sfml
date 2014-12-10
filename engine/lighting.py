import sfml as sf
import math
import numpy

class Static:

    def __init__(self, xpos, ypos):
        self.physics = dict(
            x = xpos,
            y = ypos
        )

class LightMap:

    def __init__(self, window, alpha):
        self.window = window
        self.alpha = alpha
        self.tiles = []
        self.lights = []
        self.tile_size = 32
        self.max_width = 1024 / self.tile_size
        self.max_height = 768 / self.tile_size
        self.lightpoints = []
        self.drawpoints = []
        self.create()

    def create(self):   
        columns = []
        for row in range(self.max_width):
            for column in range(self.max_height):           #These dimensions mean that the window is broken up into a grid of ten by ten smaller tiles for lighting.
                tile = sf.RectangleShape()
                tile.size = (self.tile_size, self.tile_size)
                tile.fill_color = sf.Color(0, 0, 0, self.alpha)
                columns.append(tile)
            self.tiles.append(columns)#this now gives you a matrix of surfaces to set alphas to
            columns = []

    def draw(self):
        for light in self.lights:
            light.draw()

        for point in self.drawpoints:
                self.tiles[point[0]][point[1]].fill_color = sf.Color(0, 0, 0, point[2])

        for row in range(self.max_width):
            for column in range(self.max_height):
                if self.tiles[row][column].fill_color.a > 0:
                    self.tiles[row][column].position = (row * self.tile_size, column * self.tile_size)
                    self.window.draw(self.tiles[row][column])
                self.tiles[row][column].fill_color = sf.Color(0, 0, 0, self.alpha)

        self.lightpoints = []
        self.drawpoints = []

    def addLight(self, size, source):
        self.lights.append(LightSource(size, source, self))

    def addStaticLight(self, size, x, y):
        self.lights.append(LightSource(size, Static(x, y), self))

    def set_alpha(self, alpha):
        for column in self.tiles:
            for tile in column:
                self.alpha = alpha
                tile.fill_color = sf.Color(0, 0, 0, alpha)
                return

    def add_tile(self, x, y, alpha):
        should_draw = True
        if len(self.lightpoints) > 0:
            for p in self.lightpoints:
                if p[0] == x and p[1] == y:
                    if p[2] < alpha:
                        should_draw = False

            if should_draw:
                point = [x, y, alpha]
                self.drawpoints.append(point) 

            point = [x, y, alpha]
            self.lightpoints.append(point)
                
        else:
            point = [x, y, alpha]
            self.lightpoints.append(point)

class LightSource:

    def __init__(self, size, source, lightMap):
        self.size = size
        self.source = source
        self.lightMap = lightMap

    def draw(self):
        size = self.size
        x, y = self.source.physics['x'], self.source.physics['y'] #position of light source

        #center of player
        x = x + 32
        y = y + 48

        #get the closest tile
        x = math.floor(x / self.lightMap.tile_size + 0.5)
        y = math.floor(y / self.lightMap.tile_size + 0.5)

        x0 = int(x) # x center
        y0 = int(y) # y center
        r = int(round(size))  # radius

        for x in range(x0 - r, x0 + r + 1):
            ydist = int(round(math.sqrt(r**2 - (x0 - x)**2), 1))
            for y in range(y0 - ydist, y0 + ydist + 1):
                if x >= 0 and x < self.lightMap.max_width and y >= 0 and y < self.lightMap.max_height:
                    tile_alpha = int(self.lightMap.alpha * math.sqrt((x0 - x)**2 + (y0 - y)**2) / r)
                    self.lightMap.add_tile(x, y, tile_alpha)