import random
import math

from PyParticles import pyparticles
from PyParticles import utils


class Environment(object):
	def __init__(self, dim):
		self.width = dim[0]
		self.height = dim[1]
		self.particles = []

		self.color = (55, 56, 45)
		self.mass_of_air = 0.2
		self.ELASTICITY = 0.95
		return
	def add_particles(self, n=1, **kargs):
		for i in range(n):
			size = kargs.get('size', random.randint(10, 20))
			mass = kargs.get('mass', random.randint(100, 10000))
			x = kargs.get('x', random.uniform(size, self.width-size))
			y = kargs.get('y', random.uniform(size, self.height-size))

			p = pyparticles.Particle((x, y), size, mass)
			p.speed = kargs.get('speed', random.random())
			p.angle = kargs.get('angle', random.uniform(0, math.pi*2))
			p.color = kargs.get('color', (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
			p.drag = (p.mass/(p.mass + self.mass_of_air)) ** p.size

			self.particles.append(p)
		return

	def update(self):
		for i, particle in enumerate(self.particles):
			particle.move()
			self.bounce(particle)
			for particle2 in self.particles[i+1:]:
				self.collide(particle, particle2)
		return

	def bounce(self, particle):
		if particle.x > self.width - particle.size:
			particle.x = 2*(self.width-particle.size) - particle.x
			particle.angle = -particle.angle
			particle.speed *= self.ELASTICITY
		elif particle.x < particle.size:
			particle.x = 2*particle.size - particle.x
			particle.angle = -particle.angle
			particle.speed *= self.ELASTICITY

		if particle.y > self.height - particle.size:
			particle.y = 2*(self.height - particle.size) - particle.y
			particle.angle = math.pi - particle.angle
			particle.speed *= self.ELASTICITY

		elif particle.y < particle.size:
			particle.y = 2*particle.size - particle.y
			particle.angle = math.pi - particle.angle
			particle.speed *= self.ELASTICITY
		return

	def collide(self, p1, p2):
		dx = p1.x - p2.x
		dy = p1.y - p2.y

		dist = math.hypot(dx, dy)
		if dist < p1.size + p2.size:
			angle = math.atan2(dy, dx) + math.pi/2
			total_mass = p1.mass + p2.mass

			(p1.angle, p1.speed) = utils.add_vectors((p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass),
												(angle+math.pi, 2*p1.speed/total_mass))

			overlap = 0.5*(p1.size + p2.size - dist+1)
			p1.x += math.sin(angle)*overlap
			p1.y -= math.cos(angle)*overlap
			p2.x -= math.sin(angle)*overlap
			p2.y += math.cos(angle)*overlap

			p1.speed *= self.ELASTICITY
			p2.speed *= self.ELASTICITY
		return
	def find_particle(self, pos):
		x, y = pos
		for p in self.particles:
			if math.hypot(p.x - x, p.y - y) <= p.size:
				return p
		return
