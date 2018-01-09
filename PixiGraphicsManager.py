from browser import document, window, timer
from PixiGraphic import PixiGraphic

# from Action import Action
from Client import Client

# class UpdateAction:
# 	def __init__(self, pd, pixigraphic):
# 		self.position_dof = pd
# 		self.pixigraphic = pixigraphic

# 	def __call__(self):
# 		self.pixigraphic.obj.x = pd.x[0]
# 		self.pixigraphic.obj.y = pd.x[1]


class PixiGraphicsManager(Client):
	def __init__(self, interval=100):
		h = window.innerHeight
		print("Creating Pixi App of size: ", h)
		super().__init__(h, interval=interval)
		self.app = window.PIXI.Application.new({"width": h, "height": h,
			"backgroundColor":0xd3d3d3})
		document.body.appendChild(self.app.view)

	def add_new(self):
		pg = PixiGraphic()
		self.app.stage.addChild(pg.obj)
		return pg

	def remove(self, pg):
		self.app.stage.remove(pg.obj)

	# def start_loop(self):
	# 	self.pg = self.add_new()
	# 	self.timer = timer.set_interval(self.loop, 100)

	# def loop(self):
	# 	self.pg.obj.x += 1


		# print("inside the loop")