from browser import window

class GuiClient:
	def __init__(self):
		self.gui = window.dat.GUI.new();
		self.data_obj = {}

	# def track(self, dof, attribute):

	def add(self, name):
		self.data_obj[name] = 0
		gui_obj = self.gui.add(self.data_obj, name)
		return gui_obj
