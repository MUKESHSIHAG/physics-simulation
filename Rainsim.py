def getMousePos():
    p = pygame.mouse.get_pos()
    return [
                p[0] / main.SCALE, p[1] / main.SCALE
            ]

def getDistance(p1, p2):
    return int(
                math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
            )

def colorValid(_color, _min = 0, _max = 255):
    newColor = math.fabs(_color)
    n = _max - _min
    if newColor > n:
        if int(newColor / n) % 2 == 0:
            newColor = newColor % n
        else:
            newColor = n - (newColor % n)
    
    return int(newColor) + _min
def getCirclePos(_pos, _radius, _angle):
    return [
                int(_pos[0] + _radius * math.cos(math.radians(_angle))),
                int(_pos[1] + _radius * math.sin(math.radians(_angle)))
            ]

def boolSwap(_bool):
    if _bool:
        return False
    else:
        return True

class raindrop():
    def __init__(self, _pos, _velocity, _size):
        self.pos = _pos
        self.velocity = _velocity
        self.size = _size
        
        self.dead = False
    
    def render(self, _surface):
        pygame.draw.circle(_surface, [0, 0, 255], self.pos, self.size, 0)
    
    def tick(self):
        self.pos[1] += self.velocity[1]
        if self.pos[1] - (self.size / 2) > main.HEIGHT:
            self.dead = True

def tick():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                sys.exit()
        
        if event.type == pygame.KEYUP:
            if event.key in main.KEYSDOWN:
                main.KEYSDOWN.remove(event.key)
        
        if event.type == pygame.KEYDOWN:
            if event.key not in main.KEYSDOWN:
                main.KEYSDOWN.append(event.key)
    
    if main.TICKS % 1 == 0:
        main.DROPS.append(raindrop([random.randint(0, main.WIDTH), 0], [0, random.randint(2, 10)], random.randint(2, 5)))
    
    for _ in main.DROPS:
        _.tick()
        if _.dead:
            main.DROPS.remove(_)
    
    
def render():
    # fill
    main.SCREEN.fill(main.BACKGROUNDCOLOR)
    if main.FILL:
        main.SURF.fill(main.COLOR)
    
    for _ in main.DROPS:
        _.render(main.SURF)
    
    main.SCREEN.blit(pygame.transform.scale(main.SURF, [int(main.WIDTH * main.SCALE), int(main.HEIGHT * main.SCALE)]), [0, 0])
    pygame.display.flip()

def run():
    ticksPerSecond = 60
    lastTime = time.time() * 1000000000
    nsPerTick =  1000000000.0 / float(ticksPerSecond)
    
    ticks = 0
    frames = 0
    
    lastTimer = time.time() * 1000
    delta = 0.0
    
    while True:
        now = time.time() * 1000000000
        delta += float(now - lastTime) / float(nsPerTick)
        lastTime = now
        shouldRender = False
                
        while delta >= 1:
            ticks += 1
            main.TICKS += 1
            tick()
            delta -= 1
            shouldRender = True
        
        if shouldRender:
            frames += 1
            render()
        
        if time.time() * 1000 - lastTimer >= 1000:
            lastTimer += 1000
            
            # debug
            print("Frames: " + str(frames) + ", ticks: " + str(ticks))
            
            frames = 0
            ticks = 0

class dummy():
    pass

import pygame, sys, time, math, os, random

# main dummy
main = dummy()
main.TICKS = 0

main.RES = 1
main.WIDTH = 1080 / main.RES
main.HEIGHT = 720 / main.RES
main.SIZE = [main.WIDTH, main.HEIGHT]
main.CENTER = [main.WIDTH / 2, main.HEIGHT / 2]
main.CENTERFLOAT = [main.WIDTH / 2.0, main.HEIGHT / 2.0]

main.SCALE = 1 * main.RES
main.SCALEDSIZE = [int(main.WIDTH * main.SCALE), int(main.HEIGHT * main.SCALE)]
main.SCALEDSIZEFLOAT = [main.WIDTH * main.SCALE, main.HEIGHT * main.SCALE]

main.SURF = pygame.Surface(main.SIZE)

main.SCREEN = pygame.display.set_mode(main.SCALEDSIZE)
pygame.display.set_caption("Rain Simulator")

main.BACKGROUNDCOLOR = [0, 0, 0]
main.COLOR = [0, 0, 0]
main.FILL = True

main.KEYSDOWN = []
main.DROPS = []

run()
