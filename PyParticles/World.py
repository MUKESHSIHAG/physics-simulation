try:
    import PyParticles.PyParticles as pp
except:
    import PyParticles as pp

import pygame
from pygame.locals import *
import time

# World constraints to be used
WIDTH = 400
HEIGHT = 300
FPS = 60
fpsClock = pygame.time.Clock()

class World:
    def __init__(self, Width, Height, grav=0.98, color='k'):
        self.width = Width
        self.height = Height
        self.grav = grav
        self.back_color = pp.colors.get(color,color)
        self.objects = []
        self.update_time = 1

    def _add(self, p):
        self.objects.append(p)

    def display(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('Playground')

        running = True

        while running:
            screen.fill(self.back_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for pars in self.objects:
                pars.move()
                pars.draw(screen)

            time.sleep(self.update_time)
            pygame.display.flip()

        pygame.quit()

if __name__=='__main__':
    w = World(640, 480)
    w._add(pp.Particle(100,100,30,9.8))
    w._add(pp.Particle(220,220,30,9.8,color='g'))
    w.display()






