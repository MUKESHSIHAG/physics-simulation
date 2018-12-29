import pygame
from pygame.locals import *
from time import time
from os.path import dirname, realpath
from random import randint

def main():
    tempo = time()
    maior_update = 0
    maior_draw = 0
    maior_running = 0
    soma_update = 0
    soma_draw = 0
    soma_running = 0
    quant = 0
    running, settings = load()
    print("load: %.4f" %(time()-tempo))
    while running:
        quant+=1
        init = time()
        #settings = update(settings)
        settings = update(settings)

        if time()-init>maior_update:
            maior_update = time()-init
        soma_update += time()-init
        init = time()

        draw(settings)

        if time()-init>maior_draw:
            maior_draw = time()-init
        soma_draw += time()-init
        init = time()

        running = check_exit(settings)

        if time()-init>maior_running:
            maior_running = time()-init
        soma_running += time()-init
    
    print
    print('maior_update : %.4f sec' % (maior_update))
    print('maior_draw   : %.4f sec' % (maior_draw))
    print('maior_running: %.4f sec' % (maior_running))
    print
    print('media_update : %.4f sec' % (soma_update/quant))
    print('media_draw   : %.4f sec' % (soma_draw/quant))
    print('media_running: %.4f sec' % (soma_running/quant))
    pygame.quit()

def load():
    screen_size = (670, 515)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('SHADERS TEST')
    #pygame.mouse.set_visible(0)
    game_object = {
        'bg'            : [],
        'text'          : [], #not printed in the screen, just invert the color behind
    }
    var = {
        'folder'        : dirname(realpath(__file__)),
        'exit_request'  : False
    }

    game_object['bg'].append(Sprite(0, 0, var['folder']+'/bg.png'))
    game_object['bg'][0].img = pygame.transform.scale(game_object['bg'][0].img, screen_size)

    game_object['text'].append(Sprite(screen_size[0]/2, screen_size[1]/2, var['folder']+'/level1.png', True))

    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'var'           : var,
    }

def update(settings):
    m_pos = pygame.mouse.get_pos()
    screen_size = settings['screen_size']
    game_object = settings['game_object']
    txt = game_object['text'][0]
    txt.x = m_pos[0]-(txt.width/2)
    txt.y = m_pos[1]-(txt.height/2)
    if txt.x<0:
        txt.x = 0
    if txt.y<0:
        txt.y = 0
    if txt.x+txt.width>screen_size[0]:
        txt.x = screen_size[0]-txt.width
    if txt.y+txt.height>screen_size[1]:
        txt.y = screen_size[1]-txt.height
    return settings

def draw(settings):
    screen = settings['screen']
    game_object = settings['game_object']
    screen.fill((0, 0, 0))
    for name in ['bg', 'text']:
        for gO in game_object[name]:
            if name == 'bg':
                screen.blit(gO.img, (gO.x, gO.y))
            else:
                invert(screen, gO.img, (gO.x, gO.y))
    pygame.display.flip()   
    pass

def invert(surface, mask, (x, y)):
    maximo = mask.get_height()*mask.get_width()
    for row in range(mask.get_height()):
        for column in range(mask.get_width()):
            if mask.get_at((column, row))[3] == 255:
                rgba = [255-i for i in surface.get_at((column+x, row+y))]
                surface.set_at((column+x, row+y), tuple(rgba))

def check_exit(settings):
    if settings['var']['exit_request']:
        return False
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

class Sprite():
    def __init__(self, x, y, path, center=False):
        self.x = x
        self.y = y
        self.img = pygame.image.load(path)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        if center:
            self.x = x-self.width/2
            self.y = y-self.height/2

main()
