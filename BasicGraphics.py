from PixiGraphicsManager import PixiGraphicsManager

class GraphicsDecorator:
	# logic to get copied over via the decorator
	# class members to allow subclass override for customization
	GraphicsManagerObject = None

	def __call__(self, Cls):
		if not hasattr(Cls, "add_new"):
			setattr(Cls, "add_new", self.add_new)
		# actually decorate the thing
		return Cls

	def add_new(self):
		print("add_new")

	def remove(self, graphics_obj):
		pass

	def update(self, graphics_obj):
		pass

class PixiDecoratorClass(GraphicsDecorator):
	GraphicsManagerObject = PixiGraphicsManager()

	def __init__(self):
		print(self.GraphicsManagerObject)


PixiDecorator = PixiDecoratorClass() # singleton


if __name__ == "__main__":
	pd = PixiDecorator()
	print(pd.GraphicsManagerObject)

	# pd = PixiDecorator()
	# pd.add_new()

	# @pd
	# class First:
	# 	pass

	# f = First()
	# f.add_new()
	# print("now try child decorator")

	# class Child(PixiDecorator):
	# 	def add_new(self):
	# 		print("child_add_new")

	# @Child()
	# class DumbClass:
	# 	pass

	# dc = DumbClass()
	# dc.add_new()