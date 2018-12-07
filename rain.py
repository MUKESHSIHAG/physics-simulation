import pygame
import random
import math
from pygame.locals import *

pygame.init()


background_colour = (0,0,0)
(width, height) = (1100, 600)
mass_of_air = 0
drag = 1
elasticity = 0.000001
gravity = (math.pi, 0.02)
intispeed=0.1
initangle=math.pi
def addVectors((angle1, length1), (angle2, length2)):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None
def collide(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy,dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors((p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass), (angle, 2*p2.speed*p2.mass/total_mass))
        (p2.angle, p2.speed) = addVectors((p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass), (angle+math.pi, 2*p1.speed*p1.mass/total_mass))
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)
class Particle():
    def __init__(self, (x, y), size, mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = (self.mass/(self.mass + mass_of_air))**self.size

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag
        if self.x > 1100 or self.x<0:
            self.x=(self.x+1100)%1100
            self.speed=intispeed
            self.angle=initangle
        (self.angle,self.speed)=addVectors((self.angle,self.speed),gravity)
        if self.y > 600 or self.y<0:
            self.y=(self.y+600)%600
            self.speed=intispeed
            self.angle=initangle
#surface = pygame.Surface((width,height), pygame.SRCALPHA)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Rain Simulation')
'''
bg = pygame.image.load(os.path.join("images", "space.png"))


pygame.mouse.set_visible(0)

ship = pygame.image.load(os.path.join("images", "ship.png"))
ship_top = screen.get_height() - ship.get_height()
ship_left = screen.get_width()/2 - ship.get_width()/2
screen.blit(ship, (ship_left,ship_top))

shot = pygame.image.load(os.path.join("images", "space.png"))
shoot_y = 0
'''
number_of_particles = 100
my_particles = []

for n in range(number_of_particles):
    size = 4
    density = random.randint(1,10)
    x = n*11
    y = random.randint(0,600)

    particle = Particle((x, y), size, density*size**2)
    particle.colour = (200-density*20, 200-density*20, 255)
    particle.speed = 0.1+math.sqrt(2*0.005*y)
    particle.angle = math.pi

    my_particles.append(particle)

selected_particle = None
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
            #change color of selected particle
            #if selected_particle:
                #selected_particle.colour = (255,101,190)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if initangle < (math.pi)/2:
                    initangle+=(math.pi)/2
                else :
                    initangle-=(math.pi)/2
            elif event.key == pygame.K_RIGHT:
                if initangle < -(math.pi)/2:
                    initangle+=(math.pi)/2
                else :
                    initangle-=(math.pi)/2
        '''
    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_colour)

    for i, particle in enumerate(my_particles):
        particle.display()
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
        particle.move()
    pygame.display.update()
