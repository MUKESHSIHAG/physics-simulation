from pygame import *

size_x = 1200
size_y = 700

class Object:
    def disp(self, screen):
        screen.blit(self.sprite, self.rect)

class Bad (Object):
    def __init__(self):
	self.sprite= image.load("police (1).bmp")
        self.rect = self.sprite.get_rect()
        self.rect.centerx = size_x / 2
        self.rect.centery = size_y / 2

    def chase(self, mouse):
        if self.rect.centerx > S.rect.centerx:
            self.rect.centerx-=10
        if self.rect.centerx< S.rect.centerx:
            self.rect.centerx+= 10
        if self.rect.centery > S.rect.centery:
            self.rect.centery-= 10
        if self.rect.centery< S.rect.centery:
            self.rect.centery+= 10

class gameover (Object):
    def __init__(self):
        self.sprite= image.load("projectgameover.bmp")
        self.rect= self.sprite.get_rect()
        self.rect.centerx=500
        self.rect.centery=500

class Ship(Object):
    def __init__(self):
        self.sprite = image.load("car project.bmp")
        self.rect = self.sprite.get_rect()
        self.rect.centerx = 100
        self.rect.centery = 100

    def cycle (self):
        self.rect.centerx, self.rect.centery=mouse.get_pos()

class shot(Object):
    def __init__(self):

        self.sprite = image.load("car project.bmp")
        self.rect = self.sprite.get_rect()
        self.rect.centerx=100
        self.rect.centery=100
    def cycle (self):
        self.rect.centerx = S.rect.centerx
        self.rect.centery = S.rect.centery-(S.sprite.get_width()/2)
        for e in event.get():
           if e.type==KEYDOWN:
               if e.key==K_SPACE:
                   self.rect.centery-=10   

init()
screen = display.set_mode((size_x, size_y))
B = Bad()
S = Ship()
g= gameover()
shot=shot()
clock = time.Clock()

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()

    B.chase(S)
    S.cycle()
    shot.cycle()
    screen.fill((255,255,255))
    screen=display.set_mode((size_x,size_y))
    screen=display.set_mode((size_x,size_y))
    background=image.load("background (1).bmp")
    background=transform.scale(background,(size_x,size_y))
    screen.blit(background,(0,0))
    S.disp(screen)
    B.disp(screen)
    shot.disp(screen)

    display.flip()
    clock.tick(60)
