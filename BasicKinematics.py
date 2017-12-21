# from Interaction import DofInteraction
from Interaction import InteractionLogic

class BasicKinematics(InteractionLogic):
	def __call__(self, *, entity, data=None):
		# object should be a "composite position" Dof
		# This will use super basic 'integration' (others can use Verlet, etc)
		raise ValueError("reached")
		dt = data["dt"] 
		p = entity
		p.x += p.v*dt
		p.v += p.a*dt
		return p


def BK(x, y, z, dt):
	x += v * dt
	v += a * dt
	


