from Dof import Dof

def CreateClientVector(d):
	class Vector(list):
		def __init__(self):
			for i in range(d):
				self.append(0)

		def __iadd__(self, other):
			for i, v in enumerate(self):
				self[i] += other[i]
			return self

		def set(self, *args):
			for i,a in enumerate(args):
				self[i] = a

	return Vector