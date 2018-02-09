import random
from itertools import chain
from Dof import Dof, WorldDof
import copy
from Interaction import Interaction

class World:
	FileExtension = ".world"
	def __init__(self, *, universe):
		self.universe = universe


		self.root_dof = universe.dofs["WorldDof"]() if "WorldDof" in universe.dofs else WorldDof()
		# self.worldSize = self.universe.worldSize
		# self.interactionManager = InteractionManager(self.particleCollections, self.universe.Interactions)
		self.random_source = random.Random()
		self.random_source.seed(1001)


		# self.interactions = []
		# self.client_interactions = []
		self.interaction_list = []
		self.client_interaction_list = []

		self.tag_logic = None



		# self.create_particle_collections() # Intended for subclass override
		# self.copy_type_interactions()
		# self.setup_interactions() # Intended for subclass override

		## self.import_universe_interactions

		# self.initial_conditions() # intended for subclass override
	def initialize(self):
		self.all_interactions()

		# for i in self.interaction_list:
		# 	i.initialize(self)

		# for d in iter(self.root_dof):
		# 	i = getattr(d, "initialize", None)
		# 	if i:
		# 		i(world=self)

			# d.initialize(world=self)

	def all_interactions(self):
		for d in iter(self.root_dof):  # for each dof
			self.client_interaction_list.extend(d.client_interactions)

			for i in d.Interactions:
				ic = copy.copy(i)
				ic.bound_dof = d
				self.interaction_list.append(ic)

			a = getattr(d, "action", None)
			# print(a)
			if a:
				i = Interaction(name="method_interaction", action=a, tag=getattr(d, "tag", None))
				# i.bound_dof = d
				self.interaction_list.append(i)
		# for v in map(lambda d: d.Interactions, iter(self.root_dof)):
		# 	print(v.name)

		# dlist = list(iter(self.root_dof))
		# for d in dlist:
		# 	print(d)

		# for x in chain(*map(lambda d: d.Interactions, list(iter(self.root_dof)))):
		# 	print("iteration", x.name)

		# for x in chain(*map(lambda d: d.client_interactions, list(iter(self.root_dof)))):
		# 	print("c", x.name)
		# self.dof_map(lambda d: d.Interactions)

	def dof_map(self, fn):
		return map(fn, iter(self.root_dof))


	def propagate(self):
		for i in self.interaction_list:
			# print(i.name)
			Dof.perform_interaction(i, tag_logic=self.tag_logic)

		for i in self.client_interaction_list:
			Dof.perform_interaction(i, tag_logic=self.tag_logic)
		# self.root_dof.propagate(tag_logic=self.tag_logic)


	def add_list(name, *, Type, initializer=None):
		self.root_dof.add_list(name, Type=Type, initializer=initializer)

	def initial_conditions():
		raise NotImplementedError

	def import_universe_interactions(self):
		for u_interaction in self.universe.interactions:
			self.root_dof.add_instance_interaction(u_interaction)

	def copy_type_interactions(self):
		type_interactions = self.universe.interactions
		for ti in type_interactions:
			pc_target_names = [self.pcs_of_type(pname) for pname in ti.particles]
			for name_list in product(*pc_target_names):
				new_name = "".join(name_list, "+")
				new_name += "_" + ti.name
				print("new_name: {}".format(new_name))
				self.register_interaction(name=new_name, interaction=ti.interaction, target_names=name_list)


	def pcs_of_type(self, type_name):
		return [pc.name for pc in self.particle_collections if pc.type_name == type_name]

	def loadFromFile(self, filename, start=None):
		trueFileName = self.makeName(filename)
		if start is not None:
			testFile = self.makeName(filename+"."+str(start-1))
			if os.path.isfile(testFile):
				trueFileName = testFile
			else:
				raise ValueError

			#else:
			#	trueFileName = self.makeName(filename)
		#else:
		#	trueFileName = self.makeName(filename)
		
		#trueFileName = self.makeName(trueFileName)
		print("loading from: ",trueFileName)
		with open(trueFileName, "r") as f:
			s = f.read()
			self.fromJSON(json.loads(s))
		return self

	def writeToFile(self, filename):
		trueFileName = self.makeName(filename)
		with open(trueFileName, "w") as f:
			f.write(json.dumps(self.toJSON()))
		print("world written: "+trueFileName)

	def toJSON(self):
		pcs = {}
		for k,v in self.particleCollections.items():
			pcs[k] = v.toJSON()
		ret = {
			"cs":self.current_step,
			"rs":self.random_source.getstate(),
			"pcs":pcs
		}
		return ret

	def fromJSON(self, obj):
		self.current_step = int(obj["cs"])
		#print(obj["rs"])
		a = obj["rs"]
		t = (a[0], tuple(a[1]), a[2]) 	# Necessary hack to set up the random state properly for random_source.setstate
										# It expects the second item to be a tuple, which isn't automatically handled by Json parse.
		#print(t)
		self.random_source.setstate(t)
		return self
		
	def getParticleCollections(self):
		return self.particleCollections

	def run(self):
		pass

	# def performInteractions(self, **kwargs):
	# 	self.interactionManager.propagate(**kwargs)

	def add_pc(self, *, name, type_name):
		self.particle_collections[name] = ParticleCollection(ParticleType=self.universe.particles[type_name])
		# self.particleCollections[name] = ParticleCollection(typeName, ParticleType)
		# return self.particleCollections[name]
		
	def addParticles(self, name, typeName, num):
		ParticleType = self.universe.Particles[typeName]
		c = self.addParticleCollection(name, typeName, ParticleType)
		for i in range(num):
			c.append(ParticleType())

	@classmethod
	def makeName(cls, worldName):
		return worldName + cls.FileExtension


	@staticmethod
	def rename(source, target):
		os.rename(MKConfig.makeName(source), MKConfig.makeName(target))


	@classmethod
	def copy(cls, source, target):
		shutil.copy(cls.makeName(source), cls.makeName(target))

class ClientWorld(World):
	def run(self):
		self.universe.client.run(self.propagate)
