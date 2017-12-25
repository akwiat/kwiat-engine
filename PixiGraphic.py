from browser import window

class PixiGraphic:
	def __init__(self):
		self.obj = window.PIXI.Graphics.new();

		self.obj.lineStyle(4, 0xFF3300, 1)
		self.obj.beginFill(0x66CCFF)
		self.obj.drawRect(0, 0, 64, 64)
		self.obj.endFill()
		self.obj.x = 170
		self.obj.y = 170