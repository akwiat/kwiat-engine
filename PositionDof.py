from Dof import Dof
from Vector import CreateVector
from BasicKinematics import BasicKinematics

def CreatePosition(universe=None, VectorType=None):
	V = universe.dofs["Vector"]
	# V = VectorType or universe.get_type("Vector") or CreateVector(d=2)
	# V = None
	# if VectorType: 
	# 	V = VectorType
	# elif "Vector" in universe:
	# 	V = universe["Vector"]
	# else:
	# 	V = CreateVector(d=2)

	class PositionDegree(Dof):
		def __init__(self):
			self.x = V()
			self.v = V()
			self.a = V()

	return PositionDegree

def CreateStaticPosition(universe=None):
	V = universe.dofs["Vector"]

	class StaticPosition(Dof):
		def __init__(self):
			self.position = V()

	return StaticPosition

def CreateKinematicPosition(universe=None):
	KP = CreatePosition(universe=universe)
	bk = Interaction.Build(logic=BK) # Selector is none, filter is none
	KP.register_interaction("basic_kinematics", bk)
	# KP.Interactions.append(BasicKinematics(name="basic_kinematics"))
	return KP
