import pygame,math
from PyParticles import utils

class Particle(object):
	"""Particle"""
	def __init__(self, pos, size, mass = 1):
		self.x = pos[0]
		self.y = pos[1]
		self.size = size
		self.color = (10, 10, 10)
		self.thickness = size
		self.speed = 0.01
		self.angle = 0
		self.mass = mass
		self.drag = 0
		return
	
	def move(self):
		(self.angle, self.speed) = utils.add_vectors((self.angle, self.speed), (0, 0.00025)) # This mysterious tuple is gravity in polar coordinates
		self.speed *= self.drag
		self.x += (math.sin(self.angle) * self.speed)
		self.y += (math.cos(self.angle) * self.speed)
		return

	def mouse_move(self, pos):
		self.x, self.y = pos[0], pos[1]
		# dx = pos[0] - self.x
		# dy = pos[1] - self.y
		# self.angle = 0.5*math.pi + math.atan2(dy, dx)
		# self.speed += math.hypot(dx, dy) * 0.005
