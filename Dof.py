import json
from Tree import TreeStructure
from Interaction import Interaction

from itertools import chain
def get_dataprops(obj):
	dataprops = None
	if hasattr(obj, "__dataprops__"):
		dataprops = obj.__dataprops__()
	else:
		dataprops = vars(obj)
	return dataprops

def JsonSerialize(cls):
	# print("cls: {}".format(cls))
	# print("cls has __toJSON__: {}".format(hasattr(cls, "__toJSON__")))

	# print("Is in the dict: {}".format("__toJSON__" in cls.__dict__))
	# print("\n")
	toJson_in_class_tree = hasattr(cls, "__toJSON__")
	toJson_in_class_dict = "__toJSON__" in cls.__dict__

	# print("cls: {}".format(cls))
	# print("In tree: {}".format(toJson_in_class_tree))
	# print("In dict: {}".format(toJson_in_class_dict))
	# print("\n")


	if not toJson_in_class_dict:
		def __toJSON__(self, current_result_object=None): # current_result_object not strictly necessary at this point
			if toJson_in_class_tree:
				current_result_object = super(cls, self).__toJSON__()
			dataprops = get_dataprops(self)
			result = current_result_object or {}
			for k,v in dataprops.items():
				print("key: "+k)
				print(v)

				if hasattr(v, "__toJSON__"):
					result[k] = v.__toJSON__()
				else:
					result[k] = v
			
			return result

		setattr(cls, "__toJSON__", __toJSON__)

	fromJson_in_class_tree = hasattr(cls, "__fromJSON__")
	fromJson_in_class_dict = "__fromJSON__" in cls.__dict__

	if not fromJson_in_class_dict:
		@classmethod
		def __fromJSON__(cls, obj, current_result_object=None):
			if isinstance(obj, str):
				obj = json.loads(obj)

			result = current_result_object or cls() # currently must not need arguments to initialize

			if fromJson_in_class_tree:
				result = super(cls, result).__fromJSON__(obj, current_result_object=current_result_object)
			for k,v in obj.items():
				val = getattr(result, k)
				if val is not None:
					if hasattr(val, "__fromJSON__"):
						setattr(result, k, val.__fromJSON__(v))
					else:
						if isinstance(v, dict):
							setattr(result, k, v)
						else:
							setattr(result, k, type(val)(v))

			return result
		
		setattr(cls, "__fromJSON__", __fromJSON__)

	return cls

def JsonCopy(cls):
	def mycopy(self):
		s = self.__toJSON__()
		return type(self).__fromJSON__(s)


	if not "copy" in cls.__dict__:
		setattr(cls, "copy", mycopy)

	return cls

def BasicEq(cls):
	def my__eq__(self, other):
		# print("my__eq__")
		# print(other)
		if not isinstance(other, type(self)):
			return NotImplemented

		dataprops = get_dataprops(self)
		# print(dataprops)
		for k,v in dataprops.items():
			# print(k, v)
			# print(getattr(other, k))
			if v != getattr(other, k):
				return False

		return True

	if not "__eq__" in cls.__dict__:
		setattr(cls, "__eq__", my__eq__)

	return cls

def AllowOnAssignment(cls):
	orig__setattr__ = None
	if "__setattr__" in cls.__dict__:
		orig__setattr__ = cls.__dict__["__setattr__"]
		# raise BaseException("AllowOnAssignment would overwrite __setattr__")

	def __setattr__(self, name, value):
		print("mysetattr", name)
		if hasattr(self, name):
			obj = getattr(self, name)
			if hasattr(obj, "__onassignment__"):
				print("calling __onassignment__")
				result = obj.__onassignment__(value)
				if result is False:
					return


		if orig__setattr__ is not None:
			return orig__setattr__(self, name, value)
		else:
			return super(cls, self).__setattr__(name, value) # Actually set it

	setattr(cls, "__setattr__", __setattr__)
	return cls




# @JsonSerialize
# @BasicEq
# class IntContainer(object):
# 	def __init__(self):
# 		self.value = 3

# 	def __onassignment__(self, v):
# 		print("onassignment: {}".format(v))
# 	# def __toJSON__(self):
# 	# 	return {"v":self.value}

# @JsonSerialize
# class PosIntContainer(IntContainer):
# 	def __init__(self):
# 		super().__init__()
# 		self.value = 2
# 		self.othervalue = 5
from Interaction import DofInteraction
class DofMeta(type):
	def __init__(cls, *args, **kwargs):
		super().__init__(*args, **kwargs)
		cls.Interactions = []

		@classmethod
		def register_interaction(self, name, logic):
			self.Interactions.append(DofInteraction(name=name, logic=logic))

		cls.register_interaction = register_interaction

	# def __call__(self, *args, **kwargs):
	# 	obj = super().__call__(*args, **kwargs)
	# 	obj.Interactions = []
	# 	return obj


@JsonSerialize
@JsonCopy
@BasicEq
# @AllowOnAssignment
class Dof(metaclass=DofMeta):
	# Interactions are functions defined on the class
	# Interactions = [] # list of interaction instances, which all have names

	# __getattr__ and __setattr__ are configured so dofs can be acessed as if they were attributes
	# def __new__(self, *args, **kwargs):
	# 	# We need this instead of __init__ to avoid calling __getattr__ and __setattr__ during initialization
	# 	ret = super().__new__(self, *args, **kwargs)
	# 	ret.__dict__["dofs"] = {}
	# 	ret.__dict__["client_interactions"] = []
	# 	# ret.__dict__["initial_conditions"] = []
	# 	return ret

	def __init__(self):
		self.dofs = {}
		self.parent = None

		self.client_interactions = []
		self.initial_conditions = []

		self.tag = None

		w = getattr(self, "world", None)
		if w:
			self.initialize(world=w)

	def __iter__(self):
		# def ret_vals(t):
		# 	print("tuple: ", t)
		# 	return iter(t[1])

		# for v in chain(*map(ret_vals, self.dofs.items())):
		# 	print("yielding: ", v)
		# 	yield v
		# iter_list = [iter(v) for k,v in self.dofs.items()]
		iter_list = list(map(lambda t: iter(t[1]), self.dofs.items()))
		# return iter_list
		for c in chain(*iter_list):
			yield c
		yield self
		# return [v for k,v in self.dofs.items()]

	def propagate(self, data=None, tag_logic=None):
		for name, dof in self.dofs.items():
			# print("propagating dof: ", name)

			dof.propagate(data=data, tag_logic=tag_logic)

		# for i in self.Interactions:
		# 	self.perform_interaction(i, self, tag_logic=tag_logic)
			# i.perform(self)

		# if tag_logic is None or tag_logic(self) is True:
		# 	self.action()

		for ci in self.client_interactions:
			self.perform_interaction(ci, tag_logic=tag_logic)
			# ci.perform()

	@staticmethod 
	def perform_interaction(interaction, *args, tag_logic=None):
		if tag_logic is None:
			if interaction.tag is None:
				interaction.perform(*args)
		else:
			if tag_logic(interaction):
				interaction.perform(*args)

		## for name,interaction in self.Interactions.items():
		##	interaction(entity=self, data=data) # interaction is implemented via __call__
			# Also, Dof interactions are SelfInteractions - so they are called with entity= and data=

	def add(self, name, dof):
		dof.parent = self
		self.__setitem__(name, dof)
		return dof

	def reference(self):
		return DofReference(self)

	# def action(self):
	# 	pass

	def initialize(self, *args, **kwargs):
		print("parent Dof::initialize")

	@classmethod
	def add_interaction(cls, *, name, action, selector=None, tag=None):
		i = Interaction(name=name, action=action, selector=selector, tag=tag)
		cls.Interactions.append(i)
		return i

	def add_client_interaction(self, *, name, action, selector=None, tag=None):
		i = Interaction(name=name, action=action, selector=selector, tag=tag)
		self.client_interactions.append(i)
		return i

	def __setitem__(self, name, subdof):
		d = self.dofs
		d[name] = subdof
		# self.dofs[name] = subdof

	def __getitem__(self, name):
		return self.__getattr__(name)

	def __getattr__(self, name):
		if name not in self.dofs:
			raise AttributeError
		return self.dofs[name]

	def __dataprops__(self):
		return self.dofs



class WorldDof(Dof):
	def __init__(self):
		super().__init__()
		self.current_step = 0

	def action(self):
		self.current_step += 1
		print("current step", self.current_step)

	# def __setattr__(self, name, obj):
	# 	print("dof.setattr")
	# 	return self.__setitem__(name, obj)
# class DofReference:
# 	def __init__(self, dof):
# 		self.wrapped_dof = dof
# 		self.parent = None
# 		self.field = None
# 		# self.wrapped_dof = None

# 	def __getitem__(self, name):
# 		child = self.wrapped_dof[name]
# 		if isinstance(child, Dof):
# 			return DofReference(child)
# 		else:
# 			r = DofReference(None)
# 			r.parent = self
# 			r.field = name
# 			return r

# 	@property
# 	def value(self):
# 		if self.wrapped_dof is not None:
# 			return self.wrapped_dof
# 		else:
# 			return self.parent[fieldx]

if __name__ == "__main__":
	class PP(Dof):
		pass
	PP.Interactions.append(6)
	PP.register_interaction("test", 7)
	print(PP.Interactions)

	d = Dof()
	d.Interactions.append(4)

	class P(Dof):
		pass
	P.Interactions.append(5)
	print(P.Interactions)
	# d = Dof()
	# d["x"] = 7
	# d = PositionDegree()

	# d.i = 2
	# print(d.__toJSON__())
	# i = PosIntContainer()
	# s = i.__toJSON__()
	# print(s)
	# i2 = PosIntContainer.__fromJSON__(s)
	# print(i2.__toJSON__())
	# # i2.value = 3
	# ireg = IntContainer()
	# print(i == i2)
	# print(isinstance(ireg, PosIntContainer))
	# print(isinstance(i, IntContainer))

	# i.value2 = 2
	# print(isinstance("str", PosIntContainer))
	# d = Dof()
	# print(Dof.__dict__)
	# print("__eq__" in Dof.__dict__)
	# print(type(d).__dict__)
	# print(hasattr(type(d), "__eq__"))
	# print(d.__eq__)
	# print(d.__eq__(4))
	# dump = json.dumps(d.__toJSON__())
	# # obj = json.loads(dump)

	# nobj = Dof.__fromJSON__(dump)
	# print(nobj.__toJSON__())

	# print("is equal? ")
	# print(d == nobj)


	# nd = d.copy()
	# d.x = 7
	# print(nd == d)
	# print(d != nd)

