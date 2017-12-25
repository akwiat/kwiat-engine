class UpdateAction
	def __init__(self, pd, graphic):
		self.position_dof = pd
		self.graphic = graphic

	def __call__(self):
		self.graphic.obj.x = pd.x[0]
		self.graphic.obj.y = pd.x[1]

class GuiTrackAction:
	def __init__(self, dof, gui_obj, field=None):
		self.dof = dof
		self.gui_obj = gui_obj
		self.field = field

	def __call__(self):
		self.gui_obj.updateWith(self.dof[field] if self.field else self.dof)

class Client:
	def __init__(self):
		self.gui_manager = GuiManager()

	def add_new(self):
		raise NotImplementedError

	def display(self, dof):
		graphic = self.add_new()
		ua = UpdateAction(dof, graphic)
		dof.client_interactions.append(ua)

	def gui_track(self, dof, name, field=None, minval=None, maxval=None):
		gui_obj = self.gui_manager.add(name)
		if minval: gui_obj.min(minval)
		if maxval: gui_obj.max(maxval)
		
		gta = GuiTrackAction(dof, gui_obj, field)
		dof.client_interactions.append(gta)

	def gui_controls(self):