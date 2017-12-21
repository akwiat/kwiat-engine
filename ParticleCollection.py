

class ParticleCollection(list):
	def __init__(self, *, ParticleType):
		super().__init__()
		# self.name = name
		self.tensor_representation_flag = False
		self.ParticleType = ParticleType


	def tensor_representation_mode():
		self.tensor_representation_flag = True
		array_rep_size = self.ParticleType.count_int_storage()
		initial_num = len(self) * 2

		initial_data = self.ParticleType.initial_array_rep()

		data = numpy.full((initial_num, array_rep_size), initial_data, dtype='uint32', order='F')
	# def propagate(data={}):
	# 	if not self.tensor_representation_flag:
	# 		# Regular behavior

	# 	else:
	# 		raise NotImplementedError


	# def toJSON(self):
	# 	ret = []
	# 	for item in self:
	# 		if item is None:
	# 			ret.append(None)
	# 		else:
	# 			ret.append(item.toJSON())
	# 	return ret