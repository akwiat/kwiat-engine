import inspect
import copy

def CustomCopy(**kwargs):
	def real_decorator(cls):
		if not "__copy__" in cls.__dict__:
			# class FakeClass:
			# 	pass


			def clone(self):  ######## Note this is not thread-safe because of the mod to __class__ during the copy
				print("in the method")
				copy_method = self.__copy__

				self.__class__.__copy__ = None
				# self.__class__ = FakeClass
				print(getattr(self, "__copy__"))

				c = copy.copy(self)

				for k,v in kwargs.items():
					setattr(c, k, v(getattr(self, k)))
				self.__class__.__copy__ = copy_method
				return c
			# sig = inspect.signature(cls.__init__)

			# def clone(self):
			# 	dataprops = vars(self)
			# 	print("dataprops: ", dataprops)
			# 	for p in sig.parameters.values():
			# 		print(p.name)
			# 	kwargs = {p.name:dataprops[p.name] for p in sig.parameters.values() if p.name in dataprops}
			# 	for k,v in pDict.items():
			# 		kwargs[k] = getattr(self, v)
			# 	print("kwargs: ",kwargs)

			# 	nObj = cls(**kwargs)
			# 	for a in args:
			# 		setattr(nObj, a, getattr(self, a))
			# 	return nObj

			setattr(cls, "__copy__2", clone)
			return cls
		else:
			raise NotImplementedError("already has a __clone__")

	return real_decorator



