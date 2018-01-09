class ObjReference:
	def __init__(self, parent, field=None, prop=None):
		self.parent = parent
		self.field = field
		self.prop = prop
		# self.wrapped_dof = None

	def __getitem__(self, name):
		nparent = self.value
		r = ObjReference(nparent, name)
		return r

	@property
	def value(self):
		if self.prop is not None:
			return getattr(self.parent, self.prop)
		else:
			return self.parent[self.field]

	@value.setter
	def value(self, nval):
		if self.prop is not None:
			setattr(self.parent, self.prop, nval)
			return self
		else:
			self.parent[self.field] = nval
			return self