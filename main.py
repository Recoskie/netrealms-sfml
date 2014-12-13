import sfml as sf
import sys, os

from engine import player
from engine import maps
from engine import sprite
from engine import lighting
from engine import pathfinding

window = sf.RenderWindow(sf.VideoMode.get_desktop_mode(), "netrealms")
image = sf.Image.from_file("icon.png")


currentMap = maps.Map(window, "0")

try:
   window.icon = image.pixels

   # load a sprite to display
   #texture = sf.Texture.from_file("resources/gfx/sprites/BODY_male.png")
   #sprite = sf.Sprite(texture)

   # create some graphical text to display
   font = sf.Font.from_file("resources/gfx/fonts/netrealms.ttf")
   text = sf.Text("test", font, 13)

   # load music to play
   #music = sf.Music.from_file("resources/music/tjungle.ogg")

except IOError: exit(1)


# play the music
#music.play()


Player = player.Player(currentMap, window)
Player.pathfinder = pathfinding.Pathfinder(currentMap, Player, window)

Player.sprites['playerBody'] = sprite.Sprite("resources/gfx/sprites/BODY_male.png", 64, 64)
Player.sprites['playerFeet'] = sprite.Sprite("resources/gfx/sprites/FEET_shoes_brown.png", 64, 64)
Player.sprites['playerLegs'] = sprite.Sprite("resources/gfx/sprites/LEGS_robe_skirt.png", 64, 64)
Player.sprites['playerHead'] = sprite.Sprite("resources/gfx/sprites/HEAD_robe_hood.png", 64, 64)
Player.sprites['playerChest'] = sprite.Sprite("resources/gfx/sprites/TORSO_robe_shirt_brown.png", 64, 64)


#rectangle = sf.RectangleShape(1366, 768)


#darkness = 180
#lightMap = lighting.LightMap(window, darkness)
#light = lightMap.addLight(10, Player)
#lightx = lightMap.addStaticLight(5.5, 500, 500)

# start the game loop

#use A sfml clock to calculate the Frames Per Second

fps = sf.system.Clock()

while window.is_open:

  fps.restart()
  
  sf.sleep( sf.milliseconds( 1000 / 60 ) ) #60 FPS 

  # process events
  for event in window.events:
    # close window: exit
    if type(event) is sf.CloseEvent:
      window.close()
  # the escape key was pressed
    if type(event) is sf.KeyEvent and event.code is sf.Keyboard.ESCAPE:
      window.close()

    if type(event) is sf.MouseButtonEvent:

      Player.pathfinder.resetPathFinder()
      Player.pathfinder.calculatePath(window, event.position.x, event.position.y)

  window.clear() # clear screen
  currentMap.DrawGround()

  #self.lightShader.set_parameter("light", (self.physics['x'], self.physics['y']))

  #renderS = sf.RenderStates()
  #renderS.blend_mode = sf.BlendMode.BLEND_ADD
  #renderS.shader = self.lightShader

  if Player.pathfinder.checkPathEnd():
    Player.drawPlayer(window, 0)
  else:
    Player.pathfinder.pathMoveStep(window)

  #lightMap.draw()
  #window.draw(text) # draw the string
  
  #calculate the FPS

  CalcFPS = int( 1000 / ( fps.elapsed_time.milliseconds - 2.59 ) ) # small percision fix

  FPStext = sf.Text( "FPS " + str( CalcFPS ), font, 13 )
  window.draw( FPStext )

  window.display() # update the window
