from __future__ import print_function, division

import time
import pygame
from pygame.locals import *
import math, random

try:
    from PyParticles.Maths import *
except ImportError:
    from Maths import *

# Standard colors to be used with particles
colors = {
    'r': (255, 0, 0),
    'b': (0, 0, 255),
    'g': (0, 255, 0),
    'w': (255, 255, 255),
    'k': (0, 0, 0)
}

delta_t = 0.1


class Rod:
    """
    defines rods with physical properties
    """

    def __init__(self, x1, y1, x2, y2, mass=0, color='k'):
        self.pos1 = Vector(x1, y1, False)
        self.pos2 = Vector(x2, y2, False)
        self.mass = mass
        self.size = 0
        self.color = colors.get(color, color)

    def draw(self, screen):
        s_height = screen.get_rect()[-1]
        pygame.draw.line(screen, self.color, (int(self.pos1.x), s_height - int(self.pos1.y)),
                         (int(self.pos2.x), s_height - int(self.pos2.y)), 3)


class Particle:
    """
    A circular object with physical properties
    (x,y) => position of the particle
    size  => radius of the particle in space
    mass  => mass of the particle (default = 1)
    color => color of the particle (default = red) ('r'=red,'b'=blue,'g'=green,
             'w'=white,'k'=black, or any (R,G,B) tuple)
    """

    def __init__(self, x, y, size, grav, mass=1, color='r', vel=(0, 0)):
        self.pos = Vector(x, y)
        self.size = size
        self.thickness = 1
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.5
        self.vel = Vector(*vel)
        self.acc = Vector(0, grav)
        if isinstance(color, str):
            self.color = colors[color]
        elif isinstance(color, tuple) and len(color) == 3 and max(color) <= 255:
            self.color = color
        else:
            raise TypeError("wrong value for color argument")

    def move(self):
        """
        Update the position based on the velocity of the particle
        :return:
        """
        self.vel = self.vel + self.acc * delta_t
        self.pos = self.pos + self.vel * delta_t

    def experienceDrag(self):
        self.vel = self.vel * self.drag

    def dist(self, q):
        if isinstance(q, Particle):
            return dist(q.pos.x, q.pos.y, self.pos.x, self.pos.y)

        elif isinstance(q, Rod):
            B = q.pos1 - q.pos2
            P = self.pos
            X = (P * B) * B * (1 / (B.r) ** 2)
            res = P - X
            return res.r

    def if_collided(self, par):
        return self.dist(par) < self.size + par.size

    def collide(self, par):
        if self.if_collided(par):
            print("c")
            if isinstance(par, Particle):
                rv = par.vel - self.vel
                d = self.dist(par)
                if(round(d,3)==0):
                    normal = rv
                else:
                    normal = rv * (1 / self.dist(par))

                velAlongNormal = rv * normal
                e = min(self.elasticity, par.elasticity)
                j = (-(1 + e) * velAlongNormal) / (1 / self.mass + 1 / par.mass)
                impulse = normal * j
                self.vel = self.vel - impulse * (1 / self.mass)
                par.vel = par.vel + impulse * (1 / par.mass)

    def draw(self, screen):
        """
        Display particle on the screen
        """
        s_height = screen.get_rect()[-1]
        pygame.draw.circle(screen, self.color, (round(self.pos.x), s_height - round(self.pos.y)), self.size, 0)


class World:
    def __init__(self, Width=640, Height=480, grav=0.98, color='w', fps=60):
        self.width = Width
        self.height = Height
        self.grav = grav
        self.back_color = colors.get(color, color)
        self.objects = []
        self.update_time = 1
        self.fps = fps
        self.fpsClock = pygame.time.Clock()

    def _add_objects(self, p):
        self.objects.append(p)

    def display(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Playground')

        running = True

        while running:
            screen.fill(self.back_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for i, pars in enumerate(self.objects):
                pars.move()
                for ps in self.objects[i + 1:]:
                    pars.collide(ps)
                if pars.pos.y<0 or pars.pos.y>self.height:
                    pars.vel = Vector(pars.vel.x,-pars.vel.y)
                if pars.pos.x<0 or pars.pos.x>self.width:
                    pars.vel = Vector(-pars.vel.x,pars.vel.y)

                pars.draw(screen)

            pygame.display.flip()
            self.fpsClock.tick(self.fps)

        pygame.quit()


if __name__ == '__main__':
    w = World()
    w._add_objects(Particle(20, 130, 30, -9.8, vel=(30, 50)))
    w._add_objects(Particle(110, 210, 10, -9.8))
    w.display()
