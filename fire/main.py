import pygame, os
from pygame.locals import *
from random import randint
from math import cos, sin, tan, radians
from time import time


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
        update(settings['game_object'], settings['var'])

        if time()-init>maior_update:
            maior_update = time()-init
        soma_update += time()-init
        init = time()

        draw(settings)

        if time()-init>maior_draw:
            maior_draw = time()-init
        soma_draw += time()-init
        init = time()

        running = check_exit(settings['var']['exit_request'])

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
    screen_size = (500, 500)
    screen = pygame.display.set_mode(screen_size)
    pygame.mouse.set_visible(0)
    game_object = {
        'particles'     : [],
        'tocha'         : [],
        'shader'        : []
    }
    var = {
        'folder'        : os.path.dirname(os.path.realpath(__file__)),
        'exit_request'  : False,
    }
    img = { #carrega todas as imagens
        'fire'          : pygame.image.load(var['folder'] + '/fire.png')
    }
    #fazer 240
    game_object['tocha'].append(Sprite((0, 0), var['folder'] + '/tocha.png', 1.4))
    game_object['shader'].append(Sprite((0, 0), var['folder'] + '/shader.png'))
    return True, { #retorna todas as variaveis, faz isso para nao existir variavel global.
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'img'           : img,
        'var'           : var
    }

def update(game_object, var):
    
    for part in game_object['particles']:
        part.x += part.delta_x
        part.y += part.delta_y
        part.size -= 2
        part.img = change_alpha(part.img, (part.width, part.height))
        if part.size <=0 or part.img.get_at((8,8))[3] <= 13:
            game_object['particles'].remove(part)
    if len(game_object['particles']) < 150:
        m_pos = pygame.mouse.get_pos()
        game_object['particles'].append(Particle((m_pos[0], m_pos[1]), var['folder'] + '/fire.png'))
        game_object['particles'].append(Particle((m_pos[0], m_pos[1]), var['folder'] + '/fire.png'))
        game_object['particles'].append(Particle((m_pos[0], m_pos[1]), var['folder'] + '/fire.png'))
        game_object['particles'].append(Particle((m_pos[0], m_pos[1]), var['folder'] + '/fire.png'))
        

def draw(settings):
    screen = settings['screen']
    game_object = settings['game_object']
    img = settings['img']
    screen.fill((20, 20, 20))
    m_pos = pygame.mouse.get_pos()
    for name in ['shader', 'tocha']:
        for gO in game_object[name]:
            if gO.__class__==Sprite:
                if name == 'shader':
                    screen.blit(gO.img, (m_pos[0]-gO.img.get_width()/2+10, m_pos[1]-gO.img.get_height()/2+20))
                else:
                    screen.blit(gO.img, (m_pos[0]+6, m_pos[1]+15))
    for particle in game_object['particles']:
        temp_img = pygame.transform.scale(particle.img, (int(particle.img.get_width()*particle.size/100), int(particle.img.get_height()*particle.size/100)))
        screen.blit(temp_img, (particle.x, particle.y))

    pygame.display.flip()
    pass

def fps(frames):
    pygame.time.Clock().tick(frames)

def change_alpha(img, (width, height)):
    for linha in range(height):
        for coluna in range(width):
            r, g, b, a = img.get_at((linha, coluna))
            
            img.set_at((linha, coluna), (r, g, b, a/1.2))
    return img

def check_exit(request):
    if request:
        return False
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

class Sprite():
    def __init__(self, (x, y), path, scale=1):
        self.x = x
        self.y = y
        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img, (int(self.img.get_width()*scale), int(self.img.get_height()*scale)))

class Particle():
    def __init__(self, (x, y), path):
        self.x          = x+randint(-4, 3)
        self.y          = y
        self.size       = randint(50, 200)
        self.img        = pygame.image.load(path)
        self.width      = self.img.get_width()
        self.height     = self.img.get_height()
        speed           = randint(150, 250)/100
        angle           = radians(randint(230, 310))
        self.delta_x    = speed*cos(angle)
        self.delta_y    = speed*sin(angle)

main()
