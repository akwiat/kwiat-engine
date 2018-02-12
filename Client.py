from browser import window, timer

from ObjReference import ObjReference, ObjReferenceFnWrapper

class UpdateAction:
	def __init__(self, obj_ref, graphic, scale, y_size):
		self.obj_ref = obj_ref
		self.graphic = graphic
		self.scale = scale
		self.y_size = y_size

	def __call__(self):
		# print("display x: ", self.position[0])
		position = self.obj_ref.value
		self.graphic.obj.x = position[0] * self.scale
		self.graphic.obj.y = self.y_size - (position[1] * self.scale)
		# print("display: ", self.graphic.obj.x, self.graphic.obj.y)

class GuiManager:
	def __init__(self):
		self.jsobj = window.GuiHandlerObj.new()

class GuiTrackAction:
	def __init__(self, obj_ref, gui_obj, transform):
		self.obj_ref = obj_ref
		self.gui_obj = gui_obj
		self.transform = transform

	def __call__(self):
		nval = self.transform(self.obj_ref.value)
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

	def display_pos(self, p):
		return p*self.world2display

	def world_pos(self, p):
		return p*self.display2world

	def world_vel(self, v):
		return v*self.display2world / self.step2time

	def world_acc(self, a):
		return a*self.display2world / self.step2time**2


	def display(self, dof, fn_name): #dof must be a position dof
		fn = getattr(self, fn_name)
		graphic = fn()
		ua = UpdateAction(dof.x, graphic, self.world2screen, self.screen_size)
		dof.add_client_interaction(name="display", action=ua, tag="display")

	def display_obj(self, dof, obj_ref, fn_name):
		fn = getattr(self, fn_name)
		graphic = fn()
		ua = UpdateAction(obj_ref, graphic, self.world2screen, self.screen_size)
		dof.add_client_interaction(name="display", action=ua, tag="display")


	# def gui_track_time(self, dof, name, obj_ref, gui_controls=False):
	# 	# print(self.step2time)
	# 	interaction = self.gui_track(dof, name, obj_ref, scale=1/self.step2time)
	# 	interaction.action.gui_obj = interaction.action.gui_obj.min(0).max(10).step(1/self.step2time)
		
	# 	if gui_controls:
	# 		ci = self.gui_controls(dof, name, obj_ref, self.step2time)
	# 		return ci
	# 	else:
	# 		return interaction


	# def gui_track_pos(self, dof, name, obj_ref, gui_controls=False):
	# 	interaction = self.gui_track(dof, name, obj_ref, scale=self.world2display)
	# 	interaction.action.gui_obj = interaction.action.gui_obj.min(0).max(self.display_size).step(self.display_size/1e4)

	# 	if gui_controls:
	# 		ci = self.gui_controls(dof, name, obj_ref, self.display2world)
	# 		return ci
	# 	else:
	# 		return interaction


	# def gui_track_velocity(self, dof, name, obj_ref, gui_controls=False):
	# 	scale = self.world2display*self.step2time
	# 	interaction = self.gui_track(dof, name, obj_ref, scale=scale)
	# 	vscale = self.display_size*3
	# 	interaction.action.gui_obj = interaction.action.gui_obj.min(-vscale).max(vscale).step(vscale/1e4)

	# 	if gui_controls:
	# 		ci = self.gui_controls(dof, name, obj_ref, 1/scale)
	# 		return ci
	# 	else:
	# 		return interaction


	# def gui_track_acceleration(self, dof, name, obj_ref, gui_controls=False):
	# 	scale = self.world2display*(self.step2time*self.step2time)
	# 	interaction = self.gui_track(dof, name, obj_ref, scale=scale)
	# 	ascale = self.display_size*1.5
	# 	interaction.action.gui_obj = interaction.action.gui_obj.min(-ascale).max(ascale).step(ascale/1e4)

	# 	if gui_controls:
	# 		ci = self.gui_controls(dof, name, obj_ref, 1/scale)
	# 		return ci
	# 	else:
	# 		return interaction


	def gui_track(self, dof, name, obj_ref=None, fn=None, scale=None, 
		transform=None, display_type=None, gui_controls=False, gui_name=None, **kwargs):
		if display_type == "position":
			scale = self.world2display
			invscale = self.display2world
			minval = 0
			maxval = self.display_size
			step = maxval/1e3
		elif display_type == "acceleration":
			scale = self.world2display*(self.step2time**2)
			invscale = 1/scale
			minval = -self.display_size*1.5
			maxval = -minval
			step = maxval/1e3
		elif display_type == "velocity":
			scale = self.world2display*self.step2time
			invscale = 1/scale
			minval = -1*self.display_size*3
			maxval = -minval
			step = maxval/1e3
		elif display_type == "time":
			scale = 1/self.step2time
			invscale = 1/scale
			minval = 0
			maxval = 10
			step = 1/self.step2time
		elif display_type == "energy":
			scale = (self.world2display*self.step2time)**2
			invscale = 1/scale
			minval = 0
			maxval = 100
			step = maxval/1e3

		if "minval" in kwargs:
			minval = kwargs["minval"]
		if "maxval" in kwargs:
			maxval = kwargs["maxval"]
		if "step" in kwargs:
			step = kwargs["step"]

		if scale is not None:
			transform = lambda x: x*scale

		if fn:
			if obj_ref:
				raise ValueError("fn and obj_ref both defined")
			obj_ref = ObjReferenceFnWrapper(fn)


		ival = obj_ref.value
		gui_obj = self.gui_manager.jsobj.add(name, transform(ival), gui_name)
		gui_obj = gui_obj.min(minval).max(maxval).step(step)
		gta = GuiTrackAction(obj_ref, gui_obj, transform)
		interaction = dof.add_client_interaction(name="gui_track", action=gta)

		if gui_controls:
			ci = self.gui_controls(dof, gui_obj, obj_ref, invscale)
			return ci

		return interaction


	def gui_controls(self, dof, gui_obj, obj_ref, scale):
		# gui_obj = self.gui_manager.jsobj.getObj(name)
		gca = GuiControlsAction(obj_ref, gui_obj, scale)
		ci = dof.add_client_interaction(name="gui_controls", action=gca)
		return ci


	def gui_button(self, name, on_click, gui_name=None):
		self.gui_manager.jsobj.add(name, on_click, gui_name)


	def run(self, fn):
		# self.interval = interval
		self.timer = timer.set_interval(fn, self.interval)



