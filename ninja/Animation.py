import pygame
from time import time

class Animation():
    def __init__(self, sprites, path, first, obj):
        self.sprites     = sprites
        self.path        = path
        self.tile        = first
        self.pos         = 0
        self.last_update = time()
        self.obj         = obj
        self.obj.img     = pygame.image.load(path + '/' + first + str(self.pos) + '.png')

    def change(self, tile, pos=0):
        self.tile        = tile
        self.pos         = 0 
        self.obj.img     = pygame.image.load(self.path + '/' + tile + str(pos) + '.png')


    def update(self):
        if time()-self.last_update>self.sprites[self.tile][1]:
            if self.pos == self.sprites[self.tile][0]-1:
                self.pos     = 0
            else:
                self.pos    += 1
            self.obj.img         = pygame.image.load(self.path + '/' + self.tile + str(self.pos) + '.png')
            self.last_update = time()
