from Interaction import DofInteraction

class BoundingBox:
	def __init__(self, p1=None, p2=None, origin=None, size=None):
		self.p1 = p1 or origin
		self.p2 = p2 if p2 else self.p1 + size

class BoundingBoxInteraction(DofInteraction):
	def __init__(self, *, bbox):
		self.bbox = bbox
		bigs_and_smalls = [(x2,x1) if x1 < x2 else (x1,x2) for x1,x2 in zip(bbox.p1, bbox.p2)]
		# self.bigs = 

	def propagate(*, obj):
		p = obj["position"]
		for (i,x), big, small in zip(enumerate(p), self.bigs, self.smalls):
			if x > big:
				p[i] -= 2*(x - big)
			elif x < small:
				p[i] += 2*(small - x)

def CreateBoundingBoxInteraction(universe=None):
	if universe is not None:
		bbox = universe.objects["bbox"]
		ret = BoundingBoxInteraction(bbox=bbox)
		return ret