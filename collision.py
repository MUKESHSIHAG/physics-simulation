import pygame
import random
import math

background_color = (255,255,255)
(width, height) = (400, 300)

#particle class
class Particle:
    def __init__(self, position, size):
        self.x, self.y = position
        self.size = size
        self.color = (10,20,55)
        self.thickness = 1
        self.speed = 0.1
        self.angle = 0.1
        
    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle)*self.speed
        self.y += math.cos(self.angle)*self.speed

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = -self.angle

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = -self.angle

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle


screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('collision')

number_of_particles = 10
my_particles = []

for n in range(number_of_particles):
    size = random.randint(10,20)
    x = random.randint(size, width-size)
    y = random.randint(size, height-size)

    particle = Particle((x,y),size)
    particle.speed = random.random()
    particle.angle = random.uniform(0, math.pi*2)
    
    my_particles.append(particle)

running  = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(background_color)

    for particle in my_particles:
        particle.move()
        particle.bounce()
        particle.display()
    pygame.display.flip()

