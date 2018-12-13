import math,random,sys,os,pygame,time

class UnpreparedParticle(Exception):
    pass

class Particle(object):
    def __init__(self, x, y, m):
        self.x = x
        self.y = y
        self.m = m
        self.dx = 0
        self.dy = 0
        self.color = (random.randint(128,256) - int(12.8 * self.m),
                      random.randint(128,256) - int(12.8 * self.m),
                      random.randint(128,256) - int(12.8 * self.m))

    def interact(self, bodies):
        for other in bodies:
            if other is self:
                continue

            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            factor = other.m / dist**2

            self.dx += dx * factor
            self.dy += dy * factor
            #print "factor %f" % (factor,)

    def move(self):
        ox = self.x
        oy = self.y
        self.x += self.dx
        self.y += self.dy
        #print "(%.2f,%.2f) -> (%.2f,%.2f)" % (ox, oy, self.x, self.y)


class Attractor(Particle):
    def move(self):
        pass


class ParticleViewer(object):
    def __init__(self, particles, size=(640,480)):
        (self.width, self.height) = size
        self.size = size
        self.screen = pygame.display.set_mode(size)
        self.particles = particles
        self.xoff = 0
        self.yoff = 0
        self.scalefactor = 1

    def redraw(self):
        screen = self.screen
        screen.fill((0,0,0)) # black
        for p in self.particles:
            x = int(self.scalefactor * p.x) - self.xoff
            y = int(self.scalefactor * p.y) - self.yoff
            pygame.draw.circle(screen, p.color, (x, y), 2 * p.m * self.scalefactor)
        pygame.display.flip()

    def tick(self):
        for p in particles:
            p.interact(particles)
        for p in particles:
            p.move()

        self.redraw()

    def offset(self, xoff, yoff):
        self.xoff += xoff
        self.yoff += yoff

    def scale(self, factor):
        self.scalefactor += factor

if __name__ == "__main__":
    particles = []
    for i in range(0,10):
        rx = random.randint(1,1000)
        ry = random.randint(1,1000)
        rm = random.randint(1,10)
        particles.append(Particle(rx, ry, rm))

    particles.append(Attractor(320, 200, 10))
    particles.append(Attractor(100, 100, 10))

    win = ParticleViewer(particles)
    try:
        #while sys.stdin.readline() != 'q\n':
        while True:
            win.tick()
            time.sleep(0.01)
            for event in pygame.event.get():
                if event.type == 2: # KeyDown
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_DOWN] == 1:
                        win.offset(0, 20)
                    if keys[pygame.K_UP] == 1:
                        win.offset(0, -20)
                    if keys[pygame.K_LEFT] == 1:
                        win.offset(-20, 0)
                    if keys[pygame.K_RIGHT] == 1:
                        win.offset(20, 0)
                    if keys[pygame.K_2] == 1:
                        win.scale(0.1)
                    if keys[pygame.K_1] == 1:
                        win.scale(-0.1)
                    if keys[pygame.K_q] == 1:
                        exit()

                    #print "Down:  " + str(keys[pygame.K_DOWN])
                    #print "Up:    " + str(keys[pygame.K_UP])
                    #print "Left:  " + str(keys[pygame.K_LEFT])
                    #print "Right: " + str(keys[pygame.K_RIGHT])


    except KeyboardInterrupt:
        pass
