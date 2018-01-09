from browser import window, timer

from ObjReference import ObjReference

class UpdateAction:
	def __init__(self, position, graphic, scale, y_size):
		self.position = position
		self.graphic = graphic
		self.scale = scale
		self.y_size = y_size

	def __call__(self):
		# print("display x: ", self.position[0])
		self.graphic.obj.x = self.position[0] * self.scale
		self.graphic.obj.y = self.y_size - (self.position[1] * self.scale)
		# print("display: ", self.graphic.obj.x, self.graphic.obj.y)

class GuiManager:
	def __init__(self):
		self.jsobj = window.GuiHandlerObj.new()

class GuiTrackAction:
	def __init__(self, obj_ref, gui_obj, scale):
		self.obj_ref = obj_ref
		self.gui_obj = gui_obj
		self.scale = scale

	def __call__(self):
		nval = self.obj_ref.value *self.scale
		# print("gui setting: ", nval)
		# print(self.gui_obj, self.scale)
		self.gui_obj.setValue(nval)

class GuiControlsAction:
	def __init__(self, obj_ref, gui_obj, scale):
		self.obj_ref = obj_ref
		self.gui_obj = gui_obj
		self.scale = scale

	def __call__(self):
		# print("--action--")
		# print("setting: ", self.gui_obj.getValue())
		self.obj_ref.value = self.gui_obj.getValue()*self.scale

class Client:
	def __init__(self, screen_size, interval=100):
		self.interval = interval
		self.gui_manager = GuiManager()
		self.world_size = 1e6
		self.display_size = 1e1
		self.screen_size = screen_size

		self.world2screen = self.screen_size/self.world_size
		self.display2world = self.world_size/self.display_size
		self.world2display = self.display_size/self.world_size

		self.step2time = 1e3/self.interval # steps per second


	def add_new(self):
		raise NotImplementedError


	def display(self, dof): #dof must be a position dof
		graphic = self.add_new()
		ua = UpdateAction(dof.x, graphic, self.world2screen, self.screen_size)
		dof.add_client_interaction(name="display", action=ua, tag="display")


	def gui_track_time(self, dof, obj_ref, name, gui_controls=False):
		# print(self.step2time)
		interaction = self.gui_track(dof, obj_ref, name, scale=1/self.step2time)
		interaction.action.gui_obj = interaction.action.gui_obj.min(0).max(100).step(1/self.step2time)
		
		if gui_controls:
			ci = self.gui_controls(dof, obj_ref, name, self.step2time)
			return ci
		else:
			return interaction


	def gui_track_pos(self, dof, obj_ref, name, gui_controls=False):
		interaction = self.gui_track(dof, obj_ref, name, scale=self.world2display)
		interaction.action.gui_obj = interaction.action.gui_obj.min(0).max(self.display_size).step(self.display_size/1e4)

		if gui_controls:
			ci = self.gui_controls(dof, obj_ref, name, self.display2world)
			return ci
		else:
			return interaction


	def gui_track_velocity(self, dof, obj_ref, name, gui_controls=False):
		scale = self.world2display*self.step2time
		interaction = self.gui_track(dof, obj_ref, name, scale=scale)
		vscale = self.display_size*3
		interaction.action.gui_obj = interaction.action.gui_obj.min(-vscale).max(vscale).step(vscale/1e4)

		if gui_controls:
			ci = self.gui_controls(dof, obj_ref, name, 1/scale)
			return ci
		else:
			return interaction


	def gui_track_acceleration(self, dof, obj_ref, name, gui_controls=False):
		scale = self.world2display*(self.step2time*self.step2time)
		interaction = self.gui_track(dof, obj_ref, name, scale=scale)
		ascale = self.display_size*1.5
		interaction.action.gui_obj = interaction.action.gui_obj.min(-ascale).max(ascale).step(ascale/1e4)

		if gui_controls:
			ci = self.gui_controls(dof, obj_ref, name, 1/scale)
			return ci
		else:
			return interaction


	def gui_track(self, dof, obj_ref, name, scale=1):
		gui_obj = self.gui_manager.jsobj.add(name, obj_ref.value*scale)
		# if minval is not None: gui_obj = gui_obj.min(minval)
		# if maxval is not None: gui_obj = gui_obj.max(maxval)
		# if step is not None: gui_obj = gui_obj.step(step)

		gta = GuiTrackAction(obj_ref, gui_obj, scale)
		interaction = dof.add_client_interaction(name="gui_track", action=gta)
		return interaction


	def gui_controls(self, dof, obj_ref, name, scale):
		gui_obj = self.gui_manager.jsobj.getObj(name)
		gca = GuiControlsAction(obj_ref, gui_obj, scale)
		ci = dof.add_client_interaction(name="gui_controls", action=gca)
		return ci


	def gui_button(self, name, on_click):
		self.gui_manager.jsobj.add(name, on_click)


	def run(self, fn):
		# self.interval = interval
		self.timer = timer.set_interval(fn, self.interval)



