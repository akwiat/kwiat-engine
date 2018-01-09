

def MakeTreeStructure(name_field_arg="name", store_parent_ref=True):

	class TreeStructure:
		name_field = name_field_arg
		def __init__(self):
			# super().__init__()
			self.children = []


		def find_child(self, name, recursive=True):
			# Breadth first search
			for c in self.children:
				if getattr(c, self.name_field) == name:
					return c

			for c in self.children:
				child_response = c.find_child(name)
				if child_response is not None:
					return child_response

			return None

	return TreeStructure


TreeStructure = MakeTreeStructure()