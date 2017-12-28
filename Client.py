class UpdateAction
	def __init__(self, pd, graphic, scale):
		self.position_dof = pd
		self.graphic = graphic
		self.scale = scale

	def __call__(self):
		self.graphic.obj.x = pd.x[0] * scale
		self.graphic.obj.y = pd.x[1] * scale

class GuiTrackAction:
	def __init__(self, dof, gui_obj, scale, field=None):
		self.dof = dof
		self.gui_obj = gui_obj
		self.field = field
		self.scale = scale

	def __call__(self):
		nval = self.dof[field] if self.field else self.dof
		self.gui_obj.updateWith(nval*scale)

class Client:
	def __init__(self, display_size):
		self.gui_manager = GuiManager()
		self.world_size = 1e6
		self.screen_size = 1e3

		self.display_scale = display_size/self.world_size
		self.gui_scale = self.screen_size/self.world_size

	def add_new(self):
		raise NotImplementedError

	def display(self, dof):
		graphic = self.add_new()
		ua = UpdateAction(dof, graphic, self.display_scale)
		dof.client_interactions.append(ua)

	def gui_track_pos(self, dof, name, field):
		self.gui_track(dof, name, self.gui_scale, field=field, minval=0, maxval=screen_size)

	def gui_track(self, dof, name, scale, field=None, minval=None, maxval=None):
		gui_obj = self.gui_manager.add(name)
		if minval is not None: gui_obj.min(minval)
		if maxval is not None: gui_obj.max(maxval)

		gta = GuiTrackAction(dof, gui_obj, scale, field=field)
		dof.client_interactions.append(gta)

	def gui_controls(self):
		pass

