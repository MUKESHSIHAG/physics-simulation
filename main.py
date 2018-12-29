import pygame
from pygame.locals import *
from random import randint
from time import time

def main():
    running, settings = load()
    old_time = time()
    while running:
        settings['delta_time'] = (time()-old_time)
        old_time = time()
        settings = update(settings)
        draw((settings['game_object'], settings['camera'], settings['screen'], settings['screen_size'], settings['layers']))
        running = check_exit()
    pygame.quit()

def load():
    screen_size = (400, 400)
    screen = pygame.display.set_mode(screen_size)
    game_object = {
        'player' : [Box2D(40, 30, 30, 50, 1)],
        'objects': []
    }
    for i in range(30):
        game_object['objects'].append(Box2D(30*i, 340, 30, 30, 0))
        game_object['objects'].append(Box2D(70+30*i, 280, 30, 30, 0))
    for j in range(1):
        for i in range(10):
            game_object['objects'].append(Box2D((3*29)*j, 310-30*i, 30, 30, 0))
    camera = Camera((0, 0), 1)
    return True, { #dict with my vars
            'game_object' : game_object,
            'screen_size'  : screen_size,
            'screen'       : screen,
            'camera'       : camera,
            'layers'       : ['objects', 'player'],
            'delta_time'   : 0
    }

def update(settings):
    settings['game_object']['player'][0] = update_key(settings['game_object']['player'][0])
    settings['game_object'] = move(settings['game_object'], settings['delta_time'])
    return settings

def update_key(player):
    k = pygame.key.get_pressed()
    if k[K_d]:
        player.x_speed += 8
    elif k[K_a]:
        player.x_speed -= 8
    if k[K_SPACE] and player.is_grounded:
        player.y_speed = -40
        player.is_grounded = False
    return player


def draw(settings):
    reset_screen(settings[2])      #settings[2] == screen
    draw_on_camera(settings)    #settings = {'game_objects', 'screen_size', 'screen', 'camera', 'layers'}
    display_screen()               #settings[2] == screen
    fps()

def fps(frames=10):
    pygame.time.Clock().tick(frames)
    pygame.display.set_caption('2D Collider')
    

def reset_screen(screen):
    screen.fill((0, 0, 0))

def display_screen():
    pygame.display.flip()

def draw_on_camera(settings):
    game_object = settings[0]
    camera = settings[1]
    screen = settings[2]
    screen_size = settings[3]
    layers = settings[4]
    for name in layers:
        for gO in game_object[name]:
            if gO.__class__ == Box2D:
                if gO.x<=screen_size[0] and gO.x>=0:
                    pygame.draw.rect(screen, gO.color, (gO.x, gO.y, gO.width, gO.height))

def check_exit():
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

class Camera():
    def __init__(self, (x, y), scale):
        self.x = x
        self.y = y
        self.bounds = (0, 0)
        self.scale = scale
    def set_focus((x, y)):
        self.x = x #deixar fluido
        self.y = y
    def setScale(self, new_scale):
        self.scale = new_scale
        #self.bounds = calcularBounds() 

class Box2D():
    def __init__(self, x, y, width, height, gravity):
        self.x       = x
        self.y       = y
        self.x_speed = 0
        self.y_speed = 0
        self.is_grounded = False
        self.width   = width
        self.height  = height
        self.color   = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.gravity = gravity

def move(game_object, delta_time):
    game_object = gravity(game_object)
    move_space(game_object, delta_time)
    return game_object

def gravity(game_object):
    for name in game_object:
        for gO in game_object[name]:
            if gO.gravity:
                gO.y_speed += 8
    return game_object

def move_space(game_object, delta_time):
    k = pygame.key.get_pressed()
    for name in game_object:
        for gO in game_object[name]:
            collider = Collider(gO, game_object)
            if collider['left']:
                if gO.x_speed < 0:
                    gO.x_speed = 0
            if collider['right']:
                if gO.x_speed > 0:
                    gO.x_speed = 0
            if collider['top']:
                gO.y_speed = 0
            if collider['bottom']:
                gO.y_speed = 0
                gO.is_grounded = True

            if abs(gO.x_speed) > 12:
                if gO.x_speed <0:
                    gO.x_speed = -12
                else:
                    gO.x_speed = 12 

            gO.x += gO.x_speed
            gO.y += gO.y_speed

            if not k[K_d] and not k[K_a]:
                gO.x_speed /= 2
                if abs(gO.x_speed<0.1):
                    gO.x_speed = 0

def Collider(gO, game_object):
    left   = check_left    (gO, game_object)
    right  = check_right   (gO, game_object)
    top    = check_top     (gO, game_object)
    bottom = check_bottom  (gO, game_object)
    return {
        'left'   : left,
        'right'  : right,
        'top'    : top, 
        'bottom' : bottom
    }

def check_left(obj, game_object):
    for name in game_object:
        for gO in game_object[name]:
            if obj != gO:
                if obj.x+obj.x_speed<=gO.x+gO.width and obj.x>=gO.x:
                    if (obj.y>gO.y and obj.y<gO.y+gO.height) or \
                    (obj.y+obj.height>gO.y and obj.y+obj.height<gO.y+gO.height) or \
                    (obj.y==gO.y and obj.y+obj.height == gO.y+gO.height) or \
                    (obj.y<gO.y and obj.y+obj.height>gO.y+gO.height):
                        return True
    return False

def check_right(obj, game_object):
    for name in game_object:
        for gO in game_object[name]:
            if obj != gO:
                if obj.x+obj.width+obj.x_speed>=gO.x and obj.x<gO.x:
                    if (obj.y>gO.y and obj.y<gO.y+gO.height) or \
                    (obj.y+obj.height>gO.y and obj.y+obj.height<gO.y+gO.height) or \
                    (obj.y==gO.y and obj.y+obj.height == gO.y+gO.height) or \
                    (obj.y<gO.y and obj.y+obj.height>gO.y+gO.height):
                        return True
    return False

def check_top(obj, game_object):
    for name in game_object:
        for gO in game_object[name]:
            if obj != gO:
                if (obj.y+obj.y_speed<=gO.y+gO.height and obj.y>gO.y):
                    if (obj.x>=gO.x and obj.x<=gO.x+gO.width) or (obj.x+obj.width>=gO.x and obj.x+obj.width<=gO.x+gO.width):
                        return True
    return False

def check_bottom(obj, game_object):
    for name in game_object:
        for gO in game_object[name]:
            if gO != obj:
                if (obj.y+obj.height+obj.y_speed>gO.y) and (obj.y+obj.height<gO.y+gO.height):
                    if (obj.x>gO.x and obj.x<gO.x+gO.width) or (obj.x+obj.width>gO.x and obj.x+obj.width<gO.x+gO.width):
                        return True
    return False

if __name__=='__main__':
    main()
