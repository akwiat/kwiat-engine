from Universe import Universe
from BasicGraphics import PixiDecorator
from Dof import Dof

Graphics = PixiDecorator

class Particle(Dof):
	def __init__(self):
		self.add()

class BDUniverse(Universe):
	def __init__(self, d=2):
		super().__init__()

		self.dofs["Vector"] = CreateVector(d=d)
		self.dofs["StaticPosition"] = CreateStaticPosition(universe=self)

		Vector = self.dofs["Vector"]
		StaticPosition = self.dofs["StaticPosition"]

		# self.objects["bbox"] = BoundingBox(origin=Vector(), size=Vector(bbox_size))

		self.dofs["KinematicPosition"] = CreateKinematicPosition(universe=self)
		KinematicPosition = self.dofs["KinematicPosition"]
		# KinematicPosition.interactions.append(CreateBoundingBoxInteraction(universe=self))

		# self.particles["Basic"] = KinematicPosition
		# basic_collision = TypeInteraction(name="bc", logic=SelfCollision(), particles=["Basic"])
		# basic_collision = TypeInteraction(name="bc", selector=BasicCollision(), action=RemoveAll(), particles=["Basic"])

