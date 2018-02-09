from Dof import Dof
import math
import functools

def CreateClientVector(d):
	class Vector(list):
		def __init__(self):
			for i in range(d):
				self.append(0)

		def __iadd__(self, other):
			for i, v in enumerate(self):
				self[i] += other[i]
			return self

		def __mul__(self, scalar):
			result = Vector().set(*list(map(lambda x: -x, self)))
			return result

		def __add__(self, other):
			result = Vector().set(*list(map(lambda x: x[0] + x[1], zip(self, other))))
			# print(result)
			return result

		def __sub__(self, other):
			return self.__add__(other*-1)

		def mag(self):
			ip = functools.reduce(lambda total, v: total + v**2, self)
			return math.sqrt(ip)

		def set(self, *args):
			for i,a in enumerate(args):
				self[i] = a
			return self

	return Vector


if __name__ == "__main__":
	V = CreateClientVector(2)
	x1 = V().set(3,4)
	x2 = V().set(1,2)
	print(x1 - x2*4)