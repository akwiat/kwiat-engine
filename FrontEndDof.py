
class FrontEndDofMeta(type):
	def __init__(cls, *args, **kwargs):
		super().__init__(*args, **kwargs)
		cls.GraphicsManager = None

		@classmethod
		def register_interaction(self, name, logic):
			self.Interactions.append(DofInteraction(name=name, logic=logic))

		cls.register_interaction = register_interaction