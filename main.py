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


rectangle = sf.RectangleShape(1366)

darkness = 180
lightMap = lighting.LightMap(window, darkness)
light = lightMap.addLight(10, Player)
lightx = lightMap.addStaticLight(5.5, 500, 500)

#clock = sf.Clock() old way create A clock counter

# start the game loop
while window.is_open:

  #if clock.elapsed_time.milliseconds >= (1000/60): #60 frames A second old way with A if

    #clock.restart() old way reset clock counter than do code below
    
  sf.sleep( sf.milliseconds( 1000 / 60 ) ) #60 frames A second this has A higher performance than clock

  # process events
  for event in window.events:
    # close window: exit
    if type(event) is sf.CloseEvent:
      #stop the player thread
      Player.PlayerLoaded = False
      window.close()
    # the escape key was pressed
    if type(event) is sf.KeyEvent and event.code is sf.Keyboard.ESCAPE:
      #stop the player thread
      Player.PlayerLoaded = False
      window.close()

    if type(event) is sf.MouseButtonEvent:

      Player.pathfinder.resetPathFinder()
      Player.pathfinder.calculatePath(window, event.position.x, event.position.y)

  window.clear() # clear screen
  currentMap.DrawGround()

  if not Player.pathfinder.checkPathEnd():
    Player.pathfinder.pathMoveStep(window )

  Player.drawPlayer(window )

  window.draw(text) # draw the string
  window.display() # update the window
