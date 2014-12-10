import sfml as sf
import pathfinding

class Player:

    def __init__(self, mapObject, window):
        self.window = window
        self.currentMap = mapObject
        self.pathfinder = None
        self.lightShader = sf.Shader.from_file(fragment="resources/shaders/light.frag")
        self.lightShader.set_parameter("lcolor", sf.Color(255,255,255, 50))

        self.properties = dict(
            name = "",
            inventory = [],
            equipment = [],
            sitting = False,
            mounted = False,
            resting = False,
            faction = 0,
            pclass = 0,
            currentMap = 0
        )

        self.network = dict(
            connected = False,
            ping = 0
        )

        self.animations = dict(
            animIdle = 0,
            animLeft = 0, 
            animRight = 0, 
            animUp = 0, 
            animDown = 0
        )
        
        self.sprites = dict(
            playerBody = [],
            playerFeet = [],
            playerLegs = [],
            playerChest = [],
            playerHead = []
        )

        self.pathfinding = dict(
            finderPoints = [],
            currentPoint = 0,
            pathEnd = True
        )

        self.stats = dict(
            level = int,
            experience = int,
            health = float,
            kills = int,
            deaths = int,
            stamina = float,
            mana = float
        )

        self.skills = dict(
            woodcutting = int,
            cooking = int,
            attack = int
        )

        self.physics = dict(
            x = 0,
            y = 0,
            speed = 1.6,
            direction = 0
        )

        self.oldPos = dict(
            x = int,
            y = int
        )
        

    last = 99
    cooldown = 100
    #last = sdl2.timer.SDL_GetTicks()

    def isColliding(self, posX, posY, blockedTiles):

            for i in range(0,len(blockedTiles)-2,2):
                tileX, tileY = int(blockedTiles[i]) * 32, int (blockedTiles[i+1]) * 32
                if (posX + 18 <= tileX + 32 and posX + 48 >= tileX or posX + 48 >= tileX and posX + 18 <= tileX + 32):
                    if(posY + 48 <= tileY + 32 and posY + 64 >= tileY):
                        return True
            return False


    def playerPos(self):
        return(self.physics['x'], self.physics['y'] )

    def setPlayerPos(self, x, y):
        self.physics['x'] = x
        self.physics['y'] = y

    def setPlayerName(self, name):
        self.properties['name'] = name


    def setSpeed(self, speed):
        self.physics['speed'] = speed
        self.cooldown = 100 / speed

    def moveRight(self, window):
        self.oldpos = self.physics['x'], self.physics['y']
        self.physics['x'] += self.physics['speed']
        self.physics['direction'] = 3
        self.drawPlayer(window, self.animations['animRight'])

        now = 99
        if now - self.last >= self.cooldown:
            self.last = now
            self.animations['animRight'] += 1
            if self.animations['animRight'] == 9:
               self.animations['animRight'] = 0
            #pygame.time.wait(60)

    def moveLeft(self, window):
        self.oldpos = self.physics['x'], self.physics['y']
        self.physics['x'] -= self.physics['speed']
        self.physics['direction'] = 1
        self.drawPlayer(window, self.animations['animLeft'])

        now = 99
        if now - self.last >= self.cooldown:
            self.last = now
            self.animations['animLeft'] += 1
            if self.animations['animLeft'] == 9:
                self.animations['animLeft'] = 0
            #pygame.time.wait(60)
        
    def moveUp(self, window):
        self.oldpos = self.physics['x'], self.physics['y']
        self.physics['y'] -= self.physics['speed']
        self.physics['direction'] = 0
        self.drawPlayer(window, self.animations['animUp'])

        now = 99
        if now - self.last >= self.cooldown:
            self.last = now
            self.animations['animUp'] += 1
            if self.animations['animUp'] == 9:
                self.animations['animUp'] = 0
            #pygame.time.wait(60)

    def moveDown(self, window):
        self.oldpos = self.physics['x'], self.physics['y']
        self.physics['y'] += self.physics['speed']
        self.physics['direction'] = 2
        self.drawPlayer(window, self.animations['animDown'])

        now = 99
        if now - self.last >= self.cooldown:
            self.last = now
            self.animations['animDown'] += 1
            if self.animations['animDown'] == 9:
                self.animations['animDown'] = 0
            #pygame.time.wait(60)

    def drawPlayer(self, window, spriteX):
        if self.isColliding(self.physics['x'], self.physics['y'], self.currentMap.tiles['blocked']):
            if self.pathfinder.variables['pathEnd']:
                self.physics['x'], self.physics['y'] = self.oldpos['x'], self.oldpos['y']

        self.lightShader.set_parameter("light", (self.physics['x'], self.physics['y']))

        renderS = sf.RenderStates()
        renderS.blend_mode = sf.BlendMode.BLEND_ADD
        renderS.shader = self.lightShader
        
        self.sprites['playerBody'].tileData['tiles'][spriteX][self.physics['direction']].position = (self.physics['x'], self.physics['y'])
        self.sprites['playerFeet'].tileData['tiles'][spriteX][self.physics['direction']].position = (self.physics['x'], self.physics['y'])
        self.sprites['playerLegs'].tileData['tiles'][spriteX][self.physics['direction']].position = (self.physics['x'], self.physics['y'])
        self.sprites['playerChest'].tileData['tiles'][spriteX][self.physics['direction']].position = (self.physics['x'], self.physics['y'])
        self.sprites['playerHead'].tileData['tiles'][spriteX][self.physics['direction']].position = (self.physics['x'], self.physics['y'])
        
        self.window.draw(self.sprites['playerBody'].tileData['tiles'][spriteX][self.physics['direction']])
        self.window.draw(self.sprites['playerFeet'].tileData['tiles'][spriteX][self.physics['direction']])
        self.window.draw(self.sprites['playerLegs'].tileData['tiles'][spriteX][self.physics['direction']])
        self.window.draw(self.sprites['playerChest'].tileData['tiles'][spriteX][self.physics['direction']])
        self.window.draw(self.sprites['playerHead'].tileData['tiles'][spriteX][self.physics['direction']], renderS)
        #window.blit(ps_copy, (self.physics['x'], self.physics['y']))

        #textFont = pygame.font.Font(None, 20)
        #playername = textFont.render(self.properties['name'], True, (0, 0, 0))
        #window.blit(playername, (self.physics['x'] ,self.physics['y']))