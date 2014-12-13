import sfml as sf
import pathfinding
from threading import Thread


class Player:

    #these variables are used to manage the players animatio and when to move
    PlayerLoaded = False
    PlayerMove = False

    def __init__(self, mapObject, window):
        self.window = window
        self.currentMap = mapObject
        self.pathfinder = None
        self.lightShader = sf.Shader.from_file(fragment="resources/shaders/light.frag")
        self.lightShader.set_parameter("lcolor", sf.Color(255,255,255, 50))

        #start the players animation thread and keep it runing to animate and move player with delayes sepratly
        #reaon to do it this way is that phython starts threads slowly

        t = Thread(target=self.MoveThread, args=( window, ) )
        t.start()

        #set up player Dictonayiy values

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
            speed = 5,
            direction = 0
        )

        self.oldPos = dict(
            x = int,
            y = int
        )
        
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

    #multy player threaded Animation and movment

    #Move Up is Direction 0
    #Move Left is Diection 1
    #Move Down is Direction 2
    #Move Right is Direction 3

    def MoveThread(self, window ):

        print "Thread Start"

        #clock = sf.Clock() sucks that clock has A lower performance

        self.PlayerLoaded = True

        while self.PlayerLoaded:

            if self.PlayerMove:

                #if clock.elapsed_time.milliseconds >= self.cooldown: old way

                    #clock.restart() old way

                sf.sleep(sf.milliseconds(self.cooldown)) #as player is moveing dellay amination thread to the rate of cool down

                if self.physics['direction'] == 0:
                    self.oldpos = self.physics['x'], self.physics['y']
                    self.physics['y'] -= self.physics['speed']
                    self.animations['animUp'] += 1
                    if self.animations['animUp'] == 9:
                        self.animations['animUp'] = 0

                if self.physics['direction'] == 1:
                    self.oldpos = self.physics['x'], self.physics['y']
                    self.physics['x'] -= self.physics['speed']
                    self.animations['animLeft'] += 1
                    if self.animations['animLeft'] == 9:
                        self.animations['animLeft'] = 0

                if self.physics['direction'] == 2:
                    self.oldpos = self.physics['x'], self.physics['y']
                    self.physics['y'] += self.physics['speed']
                    self.animations['animDown'] += 1
                    if self.animations['animDown'] == 9:
                        self.animations['animDown'] = 0

                if self.physics['direction'] == 3:
                    self.oldpos = self.physics['x'], self.physics['y']
                    self.physics['x'] += self.physics['speed']
                    self.animations['animRight'] += 1
                    if self.animations['animRight'] == 9:
                        self.animations['animRight'] = 0

            #player is not moving

            else:

                self.animations['animUp'] = 0
                self.animations['animLeft'] = 0
                self.animations['animDown'] = 0
                self.animations['animRight'] = 0

                sf.sleep( sf.milliseconds( 1000 / 60 ) ) #update at 60 times A second this stops the player thread amimation from killing cpu

    def drawPlayer(self, window ):

        #find sprite X

        spriteX = 0

        if self.physics['direction'] == 0:
            spriteX = self.animations['animUp']
        if self.physics['direction'] == 1:
            spriteX = self.animations['animLeft']
        if self.physics['direction'] == 2:
            spriteX = self.animations['animDown']
        if self.physics['direction'] == 3:
            spriteX = self.animations['animRight']

        if self.isColliding(self.physics['x'], self.physics['y'], self.currentMap.tiles['blocked']):
            if self.pathfinder.variables['pathEnd']:
                self.physics['x'], self.physics['y'] = self.oldpos['x'], self.oldpos['y']

        #self.lightShader.set_parameter("light", (self.physics['x'], self.physics['y']))

        #renderS = sf.RenderStates()
        #renderS.blend_mode = sf.BlendMode.BLEND_ADD
        #renderS.shader = self.lightShader
        
        self.sprites['playerBody'].tileData['tiles'][spriteX][self.physics['direction']].position = (self.physics['x'], self.physics['y'])
        self.sprites['playerFeet'].tileData['tiles'][spriteX][self.physics['direction']].position = (self.physics['x'], self.physics['y'])
        self.sprites['playerLegs'].tileData['tiles'][spriteX][self.physics['direction']].position = (self.physics['x'], self.physics['y'])
        self.sprites['playerChest'].tileData['tiles'][spriteX][self.physics['direction']].position = (self.physics['x'], self.physics['y'])
        self.sprites['playerHead'].tileData['tiles'][spriteX][self.physics['direction']].position = (self.physics['x'], self.physics['y'])
        
        self.window.draw(self.sprites['playerBody'].tileData['tiles'][spriteX][self.physics['direction']])
        self.window.draw(self.sprites['playerFeet'].tileData['tiles'][spriteX][self.physics['direction']])
        self.window.draw(self.sprites['playerLegs'].tileData['tiles'][spriteX][self.physics['direction']])
        self.window.draw(self.sprites['playerChest'].tileData['tiles'][spriteX][self.physics['direction']])
        self.window.draw(self.sprites['playerHead'].tileData['tiles'][spriteX][self.physics['direction']])
        
        #window.blit(ps_copy, (self.physics['x'], self.physics['y']))

        #textFont = pygame.font.Font(None, 20)
        #playername = textFont.render(self.properties['name'], True, (0, 0, 0))
        #window.blit(playername, (self.physics['x'] ,self.physics['y']))
