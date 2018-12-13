import pygame, sys, math

pygame.init()

FPS = 10 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
screen = pygame.display.set_mode((700, 600), 0, 32)
pygame.display.set_caption('Mass Spring System')

BLACK = (10, 105, 255)
WHITE = (255, 0, 0)

delta_t = 0.01
m = 1
k = 1 #Spring Constant

x = 0
y = 250

vx = 30
vy = 0

while True:
    #screen.fill(BLACK)

    fx = 0
    fy = -k * (y-150)

    vx = vx + (fx / m) * delta_t
    vy = vy + (fy / m) * delta_t

    x = x + vx * delta_t
    y = y + vy * delta_t

    if x > 700:
        screen.fill(BLACK)
        x = 0
        
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
fpsClock.tick(FPS)
