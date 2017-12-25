from Universe import Universe
# from BasicGraphics import PixiDecorator
from Dof import Dof

# Graphics = PixiDecorator

def Particle(*, universe):

	class Particle(Dof):
		def __init__(self):
			self.add_dof("position", universe.dofs["KinematicPosition"])

			universe.client.display(self.dofs["position"]) # adds the client interaction
			universe.client.gui_track(self.dofs["position"], "0") # does gui stuff, adds an update interaction

			universe.client.gui_controls(self.dofs["position"], filter=isPaused) # adds a controls interaction and filters on the custom filter

	return Particle


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

		self.dofs["Particle"] = Particle(universe=self)
		# KinematicPosition.interactions.append(CreateBoundingBoxInteraction(universe=self))

		# self.particles["Basic"] = KinematicPosition
		# basic_collision = TypeInteraction(name="bc", logic=SelfCollision(), particles=["Basic"])
		# basic_collision = TypeInteraction(name="bc", selector=BasicCollision(), action=RemoveAll(), particles=["Basic"])

