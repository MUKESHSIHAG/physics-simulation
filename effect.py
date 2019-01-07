import pygame, os
from pygame.locals import *
from random import randint


def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit(settings)
    pygame.quit()

def load():
    screen_size = (300, 300)
    screen = pygame.display.set_mode(screen_size)
    game_object = {
        'circle' : [Circle2D(150, 150, 10, (255, 0, 0))],
    }
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
    }

def update(settings):
    return settings

def draw(settings):
    game_object = settings['game_object']
    screen = settings['screen']
    screen.fill((0, 0, 0))
    for name in game_object:
        for gO in game_object[name]:
            if gO.__class__ == Circle2D:
                pygame.draw.circle(screen, gO.color, (gO.x, gO.y), gO.radius)
    pygame.display.flip()
    fps(60)
    pass

def fps(frames):
    pygame.time.Clock().tick(frames)

class Circle2D():
    def __init__(self, x, y, radius, color):
        self.x       = x
        self.y       = y
        self.y_speed = 0
        self.x_speed = 0
        self.radius  = radius
        self.color   = color


def check_exit(settings):
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

main()
