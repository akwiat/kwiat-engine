
from World import World
from Universe import BasicUniverse

class BasicWorld(World):
	def initialize():
		self.add_list("basics", type=self.universe.particles["basics"], initializer=self.initialize_basics)

	def initialize_basics():
		for i in range(1):
			obj = {x:3, y:3}
			yield obj

		return


if __name__ == "__main__":
	bw = BasicWorld(universe=BasicUniverse())