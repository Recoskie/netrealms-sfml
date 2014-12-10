import sfml as sf

class Sprite:

    #tileData.tiles returns a matrix of sf.Sprite objects

    def __init__(self, spritesheet, tilewidth, tileheight):
        self.tileData = dict(
            tiles = [],
            tilewidth = 0,
            tileheight = 0
        )

        self.load(spritesheet, tilewidth, tileheight)

    def load(self, spritesheet, tilewidth, tileheight):
        self.texture = sf.Texture.from_file(spritesheet)

        sheetwidth, sheetheight = self.texture.width, self.texture.height

        sprites = []
        
        for tile_x in range(0, sheetwidth / tilewidth):
            line = []
            sprites.append(line)
            for tile_y in range(0, sheetheight/tileheight):
                rect = sf.Rectangle((tile_x * tilewidth, tile_y * tileheight), (tilewidth, tileheight))
                line.append(sf.Sprite(self.texture, rect))

        self.tileData['tiles'], self.tileData['tileheight'], self.tileData['tilewidth'] = sprites, tileheight, tilewidth