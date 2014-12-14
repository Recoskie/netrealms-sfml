import sfml as sf

class LoadEffect(sf.Drawable):
	def __init__(self, name ):
		sf.Drawable.__init__(self)

		self._name = name
		self.is_loaded = False

	def _get_name(self):
		return self._name

	def load(self, Width, Height ):
		self.is_loaded = sf.Shader.is_available() and self.on_load(Width, Height )

	def update(self, x, y , lum , darkness ):
		if self.is_loaded:
			self.on_update(x, y , lum , darkness )

	def draw(self, target, states):
		if self.is_loaded:
			self.on_draw(target, states)
		else:
			error = sf.Text("Shader not\nsupported")
			error.font = sf.Font.from_file("resources/gfx/fonts/netrealms.ttf")
			error.position = (320, 200)
			error.character_size = 36
			target.draw(error, states)

	name = property(_get_name)

class MyShader(LoadEffect):
	def __init__(self ):
		LoadEffect.__init__(self, 'MyLightShader')

	def on_load(self, Width, Height ):
		try:
			# load the texture and initialize the sprite for drawing

			self.texture = sf.Texture.create(Width, Height ) # the size of window

			self.sprite = sf.Sprite(self.texture) # make the texture A drawable sprite

			# load the shader

			self.shader = sf.Shader.from_file(fragment="resources/shaders/MyFrag.frag") #load the GLSL frag shader

			self.shader.set_parameter("TextureSize", Width, Height )

		except IOError as error:
			print("An error occured: {0}".format(error))
			exit(1)

		return True

	def on_update(self, x, y, lum , darkness ):
		self.shader.set_parameter("LightPos", x, y)
		self.shader.set_parameter("darkness", darkness)
		self.shader.set_parameter("luminosity", lum )

	def on_draw(self, target, states):
		states.shader = self.shader
		target.draw(self.sprite, states)
