import numpy as np
	



def CreateVector(*, d, discrete=False):

	class NdarraySubclass(np.ndarray):
		def __new__(self, *args, **kwargs):
			if "buffer" not in kwargs:
				kwargs["buffer"] = np.array([0]*d)
				# print(len(args)

			if discrete is True:
				kwargs["dtype"] = np.int32
			result = super().__new__(self, shape=(d,), **kwargs)
			# return result
			if len(args) == 0:
				pass
			elif len(args) == 1:
				# print(args[0])
				result += args[0]
				# kwargs["buffer"] += args[0]
			elif len(args) == d:
				for i,x in enumerate(args):
					result[i] += x
				# kwargs["buffer"] = np.array([x for x in args])
			else:
				raise ValueError("incompatible number of init values in Vector")

			return result

	class HookValueChanges(): # Mixin to hook common changes
		def __valuechange__(self, *args, **kwargs):
			raise NotImplementedError()

		def __setitem__(self, *args, **kwargs):
			# print("__setitem__")
			ret = super().__setitem__(*args, **kwargs)
			self.__valuechange__(nvalue=args[1])
			return ret

		# def __getitem__(self, *args, **kwargs):
		# 	ret = super().__getitem__(*args, **kwargs)
		# 	self.__valuechange__()
		# 	return ret

	class HookArithmeticChanges(): # Mixin to hook common changes
		def __valuechange__(self, *args, **kwargs):
			raise NotImplementedError()

		def __iadd__(self, *args, **kwargs):
			ret = super().__iadd__(*args, **kwargs)
			# print("iadd")
			self.__valuechange__()
			return ret

		def __radd__(self, *args, **kwargs):
			# print("radd")
			ret = super().__radd__(*args, **kwargs)
			self.__valuechange__(ret=ret)
			return ret

		def __add__(self, *args, **kwargs):
			ret = super().__add__(*args, **kwargs)
			# print("add")
			self.__valuechange__(ret=ret)
			return ret

		def __isub__(self, *args, **kwargs):
			ret = super().__isub__(*args, **kwargs)
			self.__valuechange__()
			return ret

		def __rsub__(self, *args, **kwargs):
			# print("radd")
			ret = super().__rsub__(*args, **kwargs)
			self.__valuechange__(ret=ret)
			return ret

		def __sub__(self, *args, **kwargs):
			ret = super().__sub__(*args, **kwargs)
			self.__valuechange__(ret=ret)
			return ret

		def __imul__(self, *args, **kwargs):
			ret = super().__imul__(*args, **kwargs)
			self.__valuechange__()
			return ret

		def __rmul__(self, *args, **kwargs):
			# print("radd")
			ret = super().__rmul__(*args, **kwargs)
			self.__valuechange__(ret=ret)
			return ret

		def __mul__(self, *args, **kwargs):
			ret = super().__mul__(*args, **kwargs)
			self.__valuechange__(ret=ret)
			return ret

		def __idiv__(self, *args, **kwargs):
			ret = super().__idiv__(*args, **kwargs)
			self.__valuechange__()
			return ret

		def __rdiv__(self, *args, **kwargs):
			# print("radd")
			ret = super().__rdiv__(*args, **kwargs)
			self.__valuechange__(ret=ret)
			return ret

		def __div__(self, *args, **kwargs):
			ret = super().__truediv__(*args, **kwargs)
			self.__valuechange__(ret=ret)
			return ret

	class DiscreteNdarray(HookValueChanges, HookArithmeticChanges, NdarraySubclass):
		def __valuechange__(self, ret=None, nvalue=None):
			# print("__didchange__", ret)

			obj_to_check = self
			if ret is not None:
				obj_to_check = ret

			if nvalue is not None:
				# print("checking: {}".format(nvalue))
				if int(nvalue) != nvalue:
					raise ValueError("__setitem__ not discrete: value: {}".format(nvalue))
			for i,val in enumerate(obj_to_check):
				if int(val) != val:
					raise ValueError("Not discrete: index: {}, value: {}".format(i, val))

		def __truediv__(self, *args, **kwargs):
			# orig = self.copy()
			ret = super().__floordiv__(*args, **kwargs)
			print(ret)
			reverse = ret * args[0]

			if not (reverse == self).all():
				raise ValueError("Not discrete: bad division: {}".format(self))
				# print("bad division")

			return ret

		def __itruediv__(self, *args, **kwargs):
			print("__itruediv__")
			orig = self.copy()
			ret = super().__floordiv__(*args, **kwargs)
			print(ret)
			reverse = ret * args[0]

			if not (reverse == orig).all():
				raise ValueError("Not discrete: bad division: {}".format(self))

			return ret



	# name_discrete = "Discrete" if discrete is True else ""
	NdarraySubclass.__name__ = "Vector{}d".format(d)
	DiscreteNdarray.__name__ = "DiscreteVector{}d".format(d)
	return DiscreteNdarray if discrete is True else NdarraySubclass

if __name__ == "__main__":
	Vector2d = VectorClass(d=2, discrete=True)

	# x = Vector2d(buffer=np.array([1,3]))
	x = Vector2d()
	print(x.dtype)

	# x = 2.2 + x
	# x -= [3, 2]
	# x = 2 - x
	# print(x)
	# x *= [2, 3]
	# x = x*1
	# x[0] = 2.1
	x += 3
	x[1] += 9
	# x[1] += 1

	x /= 2
	#y = x / 3
	y = x.copy()
	# z = y[:1]
	print(y)
	print(type(y).__name__)
	# x = x/3
	print(x.dtype)
	# x += 3


	# print(type(x).mro())
	# x = None
	# print(type(x).__name__)