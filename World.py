import random

from Dof import Dof

class World():
	FileExtension = ".world"
	def __init__(self, *, universe, world_dof):
		self.universe = universe


		self.world_dof = Dof()
		# self.worldSize = self.universe.worldSize
		# self.interactionManager = InteractionManager(self.particleCollections, self.universe.Interactions)
		self.random_source = random.Random()
		self.random_source.seed(1001)
		self.current_step = 0


		# self.create_particle_collections() # Intended for subclass override
		# self.copy_type_interactions()
		# self.setup_interactions() # Intended for subclass override

		## self.import_universe_interactions

		self.initialize() # intended for subclass override




	def propagate(self, dt=1):
		# self.perform_interactions(random_source = self.random_source, universe = self.universe, step_num = self.current_step)
		
		# for k,v in self.particleCollections.items():
		# 	v.propagate(dt, random_source = self.random_source)
		self.world_dof.process_inputs()

		self.world_dof.propagate()

		if self.graphics_manager:
			self.graphics_manager.update()



		self.current_step += 1

	def add_list(name, *, Type, initializer=None):
		self.world_dof.add_list(name, Type=Type, initializer=initializer)

	def initialize():
		pass

	def import_universe_interactions(self):
		for u_interaction in self.universe.interactions:
			self.world_dof.add_instance_interaction(u_interaction)

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