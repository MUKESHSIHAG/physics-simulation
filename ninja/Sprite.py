import pygame
from Collider2D_AABB import *
from Animation       import *

class Sprite():
    all_Sprites = []
    def __init__(self, (x, y), path, collider=(False, [0, 0, 0, 0]), animation=((False)), scale=None, gravity = False):
        self.x = x
        self.y = y
        self.flipped = False
        self.gravity = gravity
        self.scale = scale
        self.img = pygame.image.load(path)
        if scale != None:
            self.img = pygame.transform.scale(self.img, (self.img.get_width()*scale, self.img.get_height()*scale))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        if collider[0]:
            if collider[1][2] == 0 or collider[1][3] == 0:
                collider[1][2] = self.width
                collider[1][3] = self.height
            self.collider = (True, Collider2D_AABB(self, (collider[1][0], collider[1][1]), collider[1][2], collider[1][3]))
            self.is_grounded = False
            self.x_speed = 0
            self.y_speed = 0
        else:
            self.collider = (False, False)
        if animation != False:
            self.animation = Animation(animation[0], animation[1], animation[2], self)
        else:
            self.animation = False
        self.all_Sprites.append(self)

    def teleport(self, (x, y)):
        self.x = x
        self.y = y