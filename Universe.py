from Vector import CreateVector
from PositionDof import CreateStaticPosition, CreateKinematicPosition
from BoundingBox import BoundingBox, CreateBoundingBoxInteraction


from Interaction import SelfCollision, TypeInteraction

class Universe:
	def __init__(self):
		self.dofs = {}
		self.particles = {}
		self.objects = {}
		self.interactions = []

	def __setitem__(self, name, item):
		self.particles[name] = item

	def __getitem__(self, name):
		return self.particles[name]


# class TypeInteraction:
# 	def __init__():
# 		pass

class BasicUniverse(Universe):
	def __init__(self, d=2, bbox_size=1000):
		super().__init__()

		self.dofs["Vector"] = CreateVector(d=d)
		self.dofs["StaticPosition"] = CreateStaticPosition(universe=self)

		Vector = self.dofs["Vector"]
		StaticPosition = self.dofs["StaticPosition"]

		self.objects["bbox"] = BoundingBox(origin=Vector(), size=Vector(bbox_size))

		self.dofs["KinematicPosition"] = CreateKinematicPosition(universe=self)
		KinematicPosition = self.dofs["KinematicPosition"]
		KinematicPosition.interactions.append(CreateBoundingBoxInteraction(universe=self))

		self.particles["Basic"] = KinematicPosition
		# basic_collision = TypeInteraction(name="bc", logic=SelfCollision(), particles=["Basic"])
		basic_collision = TypeInteraction(name="bc", selector=BasicCollision(), action=RemoveAll(), particles=["Basic"])

		# Demo of type interactions
		# self.particles["Basic"] = BasicParticle
		# basic_collision = TypeInteraction(name="bc", logic=SelfCollision(), particles=["Basic"])

if __name__ == "__main__":
	# V = CreateVector(d=2, discrete=True)
	# v0 = V()
	# print(v0)
	# v = V(0)
	# print(v)

	# v2 = V(1, 2)
	# print(v2)
	u = BasicUniverse()


	