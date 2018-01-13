# from Universe import Universe
# from BasicGraphics import PixiDecorator
from Dof import Dof
from ObjReference import ObjReference
from World import ClientWorld
from PositionDof import CreateKinematicPosition
from ClientVector import CreateClientVector as CreateVector

from PixiGraphicsManager import PixiGraphicsManager as PixiClient
# Graphics = PixiDecorator

def Particle(*, universe):

	class Particle(Dof):
		def __init__(self, init_fn):
			super().__init__()
			self.add("position", universe.dofs["KinematicPosition"]())
			init_fn(self)
			universe.client.display(self["position"]) # adds the client interaction
			posx_ref = ObjReference(self["position"].x, field=0)
			posy_ref = ObjReference(self["position"].x, field=1)

			vely_ref = ObjReference(self["position"].v, field=1)
			accy_ref = ObjReference(self["position"].a, field=1)


			ci_x = universe.client.gui_track_pos(self["position"], posx_ref, "PosX", gui_controls=True) 
			ci_x.tag = "paused"

			ci_y = universe.client.gui_track_pos(self["position"], posy_ref, "PosY", gui_controls=True)
			ci_y.tag = "paused"

			ci_vy = universe.client.gui_track_velocity(self["position"], vely_ref, "VelY", gui_controls=True)
			ci_vy.tag = "paused"

			ci_ay = universe.client.gui_track_acceleration(self["position"], accy_ref, "AccY", gui_controls=True)
			ci_ay.tag = "paused"

			# self.tag = "paused"

		# def action(self):
			# print("particle action")
			# self["position"].x[0] -= 1000

	return Particle


class BDUniverse:
	def __init__(self, d=2):
		# super().__init__()
		self.dofs = {}
		self.client = PixiClient(interval=20)

		self.dofs["Vector"] = CreateVector(d=d)
		# self.dofs["StaticPosition"] = CreateStaticPosition(universe=self)

		Vector = self.dofs["Vector"]
		# StaticPosition = self.dofs["StaticPosition"]

		# self.objects["bbox"] = BoundingBox(origin=Vector(), size=Vector(bbox_size))

		self.dofs["KinematicPosition"] = CreateKinematicPosition(universe=self)
		KinematicPosition = self.dofs["KinematicPosition"]

		self.dofs["Particle"] = Particle(universe=self)
		# KinematicPosition.interactions.append(CreateBoundingBoxInteraction(universe=self))

		# self.particles["Basic"] = KinematicPosition
		# basic_collision = TypeInteraction(name="bc", logic=SelfCollision(), particles=["Basic"])
		# basic_collision = TypeInteraction(name="bc", selector=BasicCollision(), action=RemoveAll(), particles=["Basic"])

class BDWorld(ClientWorld):
	def __init__(self):
		super().__init__(universe=BDUniverse())
		# self.interval = 100
		# self.step2time = self.interval/1e3
		self.isPaused = True
		def tag_logic_paused(interaction):
			if interaction.tag is None:
				return False
			elif interaction.tag == "paused":
				return True
			elif interaction.tag == "display":
				return True
			else:
				raise NotImplementedError

		self.tag_logic_paused = tag_logic_paused

		def tag_logic_playing(interaction):
			if interaction.tag is None:
				return True
			elif interaction.tag == "display":
				return True
			elif interaction.tag == "paused":
				return False
			else:
				raise NotImplementedError

		self.tag_logic_playing = tag_logic_playing
		self.tag_logic = self.tag_logic_paused


		ct = self.universe.client.gui_track_time(self.root_dof, ObjReference(self.root_dof, prop="current_step"), "time", gui_controls=True)
		ct.tag = "paused"
		self.universe.client.gui_button("PausePlay", self.pause_play)
		

	def initial_conditions(self):
		def init_particle(p):
			p.position.x[0] = 5e5
			p.position.x[1] = 10e5
			p.position.v.set(0, 0)
			p.position.a[1] = -4e2

		self.root_dof.add("p1", self.universe.dofs["Particle"](init_particle))
		

	def propagate(self):
		# raise NotImplementedError
		self.root_dof.propagate(tag_logic=self.tag_logic)

	def pause_play(self):
		print("pauseplay")
		# raise NotImplementedError
		if self.isPaused is True:
			self.isPaused = False
			self.tag_logic = self.tag_logic_playing
		else:
			self.isPaused = True
			self.tag_logic = self.tag_logic_paused


if __name__ == "__main__":
	w = BDWorld()
	w.initial_conditions()
	w.run()
