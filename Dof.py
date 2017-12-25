import json
from Tree import TreeStructure

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
class Dof(metaclass=DofMeta, TreeStructure):
	# Interactions are functions defined on the class
	# Interactions = [] # list of interaction instances, which all have names

	# __getattr__ and __setattr__ are configured so dofs can be acessed as if they were attributes
	def __new__(self, *args, **kwargs):
		# We need this instead of __init__ to avoid calling __getattr__ and __setattr__ during initialization
		ret = super().__new__(self, *args, **kwargs)
		ret.__dict__["dofs"] = {}
		ret.__dict__["client_interactions"] = []
		return ret


	def propagate(self, data=None):
		for name, dof in self.dofs.items():
			dof.propagate(data)

		for name,interaction in self.Interactions.items():
			interaction(entity=self, data=data) # interaction is implemented via __call__
			# Also, Dof interactions are SelfInteractions - so they are called with entity= and data=

	def add_dof(self, name, dof):
		self.__setitem__(name, dof)

	def __setitem__(self, name, subdof):
		d = self.dofs
		d[name] = subdof
		# self.dofs[name] = subdof

	def __getitem__(self, name):
		return self.__getattr__(self, name)

	def __getattr__(self, name):
		if name not in self.dofs:
			raise AttributeError
		return self.dofs[name]

	def __setattr__(self, name, obj):
		print("dof.setattr")
		return self.__setitem__(name, obj)

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

