import sfml as sf
import sys, os

from engine import player
from engine import maps
from engine import sprite
from engine import shader_lighting
from engine import pathfinding

window = sf.RenderWindow(sf.VideoMode.get_desktop_mode(), "netrealms")
image = sf.Image.from_file("icon.png")


currentMap = maps.Map(window, "0")

try:
   window.icon = image.pixels

   # create some graphical text to display
   font = sf.Font.from_file("resources/gfx/fonts/netrealms.ttf")
   text = sf.Text("test", font, 13)

   # load music to play
   music = sf.Music.from_file("resources/music/tjungle.ogg")

except IOError: exit(1)

# play the music
music.play()


Player = player.Player(currentMap, window)
Player.pathfinder = pathfinding.Pathfinder(currentMap, Player, window)

Player.sprites['playerBody'] = sprite.Sprite("resources/gfx/sprites/BODY_male.png", 64, 64)
Player.sprites['playerFeet'] = sprite.Sprite("resources/gfx/sprites/FEET_shoes_brown.png", 64, 64)
Player.sprites['playerLegs'] = sprite.Sprite("resources/gfx/sprites/LEGS_robe_skirt.png", 64, 64)
Player.sprites['playerHead'] = sprite.Sprite("resources/gfx/sprites/HEAD_robe_hood.png", 64, 64)
Player.sprites['playerChest'] = sprite.Sprite("resources/gfx/sprites/TORSO_robe_shirt_brown.png", 64, 64)

fps = sf.system.Clock()

#get the shader

s =  shader_lighting.MyShader() #instance the shader

# initialize

s.load(1440, 900 ) # create the shader and set texture size

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

  window.clear()
  currentMap.DrawGround()

  if Player.pathfinder.checkPathEnd():
    Player.drawPlayer(window, 0)
  else:
    Player.pathfinder.pathMoveStep(window)

  #shader update method inputs
  #Player X , Y position also centered
  #100 is the luminosity
  #0.3 is the darkness

  s.update( Player.playerPos()[0]+50-16 , Player.playerPos()[1]+50+48 , 100 , 0.3 )

  window.draw(s)

  #calculate the FPS

  CalcFPS = int( 1000 / ( fps.elapsed_time.milliseconds - 2.59 ) )

  FPStext = sf.Text( "FPS " + str( CalcFPS ), font, 13 )
  window.draw( FPStext )

  window.display() # update the window
