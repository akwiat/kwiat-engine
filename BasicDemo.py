# from Universe import Universe
# from BasicGraphics import PixiDecorator
from Dof import Dof, WorldDof
from ObjReference import ObjReference
from World import ClientWorld
from PositionDof import CreateKinematicPosition
from ClientVector import CreateClientVector as CreateVector

from PixiGraphicsManager import PixiGraphicsManager as PixiClient
# Graphics = PixiDecorator

def Particle(*, universe):

	class Particle(Dof):
		def __init__(self, init_fn, name):
			super().__init__()
			self.add("position", universe.dofs["KinematicPosition"]())
			init_fn(self)
			universe.client.display_obj(self, ObjReference(self["position"], prop="x"), "add_basic_particle") # adds the client interaction
			posx_ref = ObjReference(self["position"].x, field=0)
			posy_ref = ObjReference(self["position"].x, field=1)

			vely_ref = ObjReference(self["position"].v, field=1)
			accy_ref = ObjReference(self["position"].a, field=1)


			# ci_x = universe.client.gui_track(self["position"], "PosX", posx_ref, 
			# 	gui_controls=True, display_type="position", gui_name=name)
			# ci_x.tag = "paused"

			ci_y = universe.client.gui_track(self["position"], "PosY", posy_ref,
			 gui_controls=True, display_type="position", gui_name=name)
			ci_y.tag = "paused"

			ci_vy = universe.client.gui_track(self["position"], "VelY", vely_ref, 
				gui_controls=True, display_type="velocity", gui_name=name)
			ci_vy.tag = "paused"

			ci_ay = universe.client.gui_track(self["position"], "AccY", accy_ref, 
				gui_controls=True, display_type="acceleration", gui_name=name)
			ci_ay.tag = "paused"

			ci_rpx = universe.client.gui_track(self["position"], "RelY", fn=lambda: self.relative()[1], 
				display_type="position", gui_name=name, minval=-10)
			ci_rpx.tag = "display"

			ci_ke = universe.client.gui_track(self["position"], "KE",
				fn=self.kinetic_energy, display_type="energy", gui_name=name+"energy", minval=-150, maxval=150)
			ci_ke.tag = "display"

			ci_ke = universe.client.gui_track(self["position"], "PE",
				fn=self.potential_energy, display_type="energy", gui_name=name+"energy", minval=-150, maxval=150)
			ci_ke.tag = "display"

			ci_ke = universe.client.gui_track(self["position"], "Total E",
				fn=self.total_energy, display_type="energy", gui_name=name+"energy", maxval=150, minval=-150)
			ci_ke.tag = "display"
			# self.tag = "paused"

		# def action(self):
			# print("particle action")
			# self["position"].x[0] -= 1000

		# def action(self):
		# 	print(self.relative())

		def initialize(self, *, world):
			# raise ValueError
			print("Particle::initialize")
			self.origin = world.root_dof.origin

		def potential_energy(self):
			g = -self["position"].a[1]
			h = self.relative()[1]
			return g*h

		def kinetic_energy(self):
			v = self["position"].v.mag()**2 / 2
			return v

		def total_energy(self):
			return self.potential_energy() + self.kinetic_energy()

		def relative(self):
			# print(type(self.origin))
			# print(type(self["position"].x))
			return self["position"].x - self.origin

	return Particle

def BDWorldDof(*, universe):
	class BDWorldDof(WorldDof):
		def __init__(self):
			super().__init__()
			ct = universe.client.gui_track(self, "time", ObjReference(self, prop="current_step"), 
				gui_controls=True, display_type="time", gui_name="global")
			ct.tag = "paused"

			self.origin = universe.dofs["Vector"]()
			universe.client.display_obj(self, ObjReference(self, prop="origin"), "add_origin") # adds the client interaction


			# self.origin += [0, 2]
			# self.origin[1] += universe.client.world_pos(5)
			# print(self.origin)
			ot = universe.client.gui_track(self, "originY", ObjReference(self.origin, field=1), 
				gui_controls=True, display_type="position", gui_name="global")
			ot.tag = "paused"

	return BDWorldDof


class BDClient(PixiClient):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.iscalled = False

	def add_basic_particle(self):
		pg = self.make_new()
		o = pg.obj

		o.lineStyle(2, 0x004400, 1)
		o.beginFill(0x228B22)
		size = 20
		if self.iscalled: 
			size = 10
		o.drawRect(-size/2, -size/2, size, size)
		o.endFill()
		o.x = 0
		o.y = 0
		self.iscalled = True
		return pg	

	def add_origin(self):
		pg = self.make_new()
		o = pg.obj

		o.lineStyle(2, 0x004400, 1)
		o.beginFill(0x000000)
		size = 4
		o.drawRect(0, 0, self.screen_size, size)
		o.endFill()
		o.x = 0
		o.y = 0

		return pg

class BDUniverse:
	def __init__(self, d=2):
		# super().__init__()
		self.dofs = {}
		self.client = BDClient(interval=20)

		self.dofs["Vector"] = CreateVector(d=d)
		# self.dofs["StaticPosition"] = CreateStaticPosition(universe=self)

		Vector = self.dofs["Vector"]
		# StaticPosition = self.dofs["StaticPosition"]

		# self.objects["bbox"] = BoundingBox(origin=Vector(), size=Vector(bbox_size))

		self.dofs["KinematicPosition"] = CreateKinematicPosition(universe=self)
		KinematicPosition = self.dofs["KinematicPosition"]

		self.dofs["WorldDof"] = BDWorldDof(universe=self)

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
		Dof.world = self
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
		# self.tag_logic = self.tag_logic_playing
		self.tag_logic = self.tag_logic_paused


		
		self.universe.client.gui_button("PausePlay", self.pause_play, gui_name="global")

		
		# ot.add_action(lambda: print(self.root_dof.origin))

	def initial_conditions(self):
		def init_particle(p):
			c = self.universe.client
			p.position.x[0] = c.world_pos(5)
			p.position.x[1] = c.world_pos(10)
			p.position.v.set(0, 0)
			p.position.a[1] = c.world_acc(-10)

		def init_second(p):
			c = self.universe.client
			p.position.x.set(c.world_pos(5), c.world_pos(5))
			p.position.v[1] = c.world_vel(10)
			p.position.a[1] = c.world_acc(-10)

		self.root_dof.add("p1", self.universe.dofs["Particle"](init_particle, "p1"))
		# self.root_dof.add("p2", self.universe.dofs["Particle"](init_second, "p2"))
		

	# def propagate(self):
	# 	# raise NotImplementedError
	# 	self.root_dof.propagate(tag_logic=self.tag_logic)

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
	# w.prep_interactions()
	# w.all_interactions()
	w.initialize()
	w.run()
