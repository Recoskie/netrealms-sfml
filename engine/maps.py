import sfml as sf
import ConfigParser
import sprite

class Map:

    def __init__(self, window, mapNum):
        self.window = window

        self.properties = dict(
            name = str,
            npcs = [],
            items = [],
            players = [],
            height = int,
            width = int
        )

        self.tiles = dict(
            tileset = [],
            blocked = [],
            height = 0,
            width = 0,
            layers = dict(
                ground = [],
                fringe = []
            )
        )

        self.load(mapNum)

    def load(self, mapNum):
        parser = ConfigParser.ConfigParser()
        parser.read("resources/maps/" + mapNum)
        
        tileset_path = parser.get("level", "tileset")
        
        self.tiles['width'] = int(parser.get("level", "tilewidth"))
        self.tiles['height'] = int(parser.get("level", "tileheight"))

        #loop through the layers in mapfile
        for index, value in parser.items('ground'):
            self.tiles['layers']['ground'].append(value.split("\n"))

        for index, value in parser.items('fringe'):
            self.tiles['layers']['fringe'].append(value.split("\n"))
        
        self.tiles['blocked'] = parser.get("level", "blockedtiles").split(",")
        self.tiles['tileset'] = sprite.Sprite(tileset_path, self.tiles['width'], self.tiles['height'])

    def getPixelCoord(tileX, tileY):
        return tileX * 32, tileY * 32

    def isTileBlocked(self, TilePosX, TilePosY):
        blockedTiles = self.tiles['blocked']
        for i in range(0,len(blockedTiles)-2,2):
            tileX, tileY= int(blockedTiles[i])*32, int (blockedTiles[i+1])*32
            if(TilePosX==tileX and TilePosY==tileY):
                return(True)
        return(False)

    def DrawGround(self):
        for layer in self.tiles['layers']['ground']:
            for map_y, line in enumerate(layer):
                            tilenums = line.split(",")
                            map_x = 0
                            for i in tilenums:
                                    tilex = int(i[0])
                                    tiley = int(i[1])
                                    self.tiles['tileset'].tileData['tiles'][tilex][tiley].position = sf.Vector2(map_x * self.tiles['width'], map_y * self.tiles['height'])
                                    self.window.draw(self.tiles['tileset'].tileData['tiles'][tilex][tiley])
                                    map_x = map_x + 1
                                    if map_y == 32:
                                            map_x = 0

    def DrawFringe(self):
        for layer in self.tiles['layers']['fringe']:
            for map_y, line in enumerate(layer):
                            tilenums = line.split(",")
                            map_x = 0
                            for i in tilenums:
                                    tilex = int(i[0])
                                    tiley = int(i[1])
                                    #self.window.blit(self.tiles['tileset'].tileData['tiles'][tilex][tiley], (map_x*self.tiles['width'], map_y*self.tiles['height']))
                                    map_x = map_x + 1
                                    if map_y == 32:
                                            map_x = 0