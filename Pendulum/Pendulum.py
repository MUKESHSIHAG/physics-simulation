import pygame, math, time

class Pendulum():
    def __init__(self, angle, pivot_x, pivot_y):
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
        self.length = 250
        self.angle = angle
        self.x = self.length*math.sin(self.angle)
        self.y = self.length*math.cos(self.angle)
        self.v_x = 0
        self.a_x = 0
        self.ID = None
        self.mass = 1

    def swing(self):
        """Calculate change in x & y in a time dt"""
        g = 9.8
        dt = 0.01
        self.angle = 0.5*math.pi - math.atan2(self.y, self.x)
        self.a_x = g*math.sin(self.angle)*math.sin((0.5*math.pi)-self.angle)
        self.v_x += self.a_x*dt
        self.x -= self.v_x
        self.y = self.pivot_y + (((self.length**2 - self.x**2)**2)**0.5)**0.5
        time.sleep(dt)

    def draw(self, screen):
        """Display pendulum on the screen"""
        bobSize = 25
        pygame.draw.line(screen, (0,0,255), (self.pivot_x, self.pivot_y),
                         (self.pivot_x + self.x, self.y), 3)
        pygame.draw.circle(screen, (230,10,10),
                           (int(self.pivot_x + self.x), int(self.y)),
                           bobSize, 0)


def dist(a, b, x, y):
    """Return distance between 2 points"""
    d = math.hypot(a-x, b-y)
    return d

def onPath(a, b, length, pivot_y):
    """
    Move coordinates (a, b) to closest point on path of the pendulum
    Used to ensure pendulum sticks to it's path when it's selected 
    i.e. it doesn't just follow the mouse position
    x"""

    angle = 0.5*math.pi - math.atan2(b, a)
    # Limit the range of motion to 0.48pi radians either side of rest
    if math.fabs(angle) > 0.48*math.pi:
        angle = 0.48*math.pi
    x = round(length*math.sin(angle))
    y = round(pivot_y + length*math.cos(angle))
    return (int(x), int(y))

def collide(p1, p2):
    """Check if 2 pendulums have collided and if so alter v_x"""
    # If centre to centre distance < bobSize they have collided
    if dist(p1.x + p1.pivot_x, p1.y, p2.x + p2.pivot_x, p2.y) < 50:
        # Assume totally elastic collision i.e.i swap velocities
        (p1.v_x, p2.v_x) = (p2.v_x, p1.v_x)
        # move the pendulums slightly apert to avoid 'sticking'
        if p1.x < p2.x:
            p2.x - 3
            p2.x + 3
        else: 
            p1.x + 3
            p2.x - 3
