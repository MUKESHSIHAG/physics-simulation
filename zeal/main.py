import pygame
from pygame.locals import *
from os.path import dirname, realpath
from random import randint
from math import sin, cos, radians

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit(settings)
    pygame.quit()

def load():
    screen_size = (380, 460)
    screen = pygame.display.set_mode(screen_size)
    pygame.font.init()
    game_object = {
        'posto'     : [],
        'list'      : [],
        'HUD'       : [],
        'bandeira'  : [],
        'nota'      : [],
    }
    var = {
        'folder'        : dirname(realpath(__file__)),
        'exit_request'  : False,
        'valor_nota'    : 100,
        'idle_gain'     : 0,
        'money'         : 0
    }
    game_object['bandeira'].append(Sprite((76, 40), var['folder']+'/assets/bandeira.png', 228, 160))
    game_object['list'].append(PowerUp(var['folder']+'/assets/powerUP/underwear.png', 'Under ware', 30, 1.1, 1, 1))
    return True, {
        'screen_size' : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'var'           : var
    }

def update(settings):
    m = pygame.mouse.get_pressed()[0]
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            settings['var']['exit_request'] = True 
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            pos = pygame.mouse.get_pos()
            if verificar_click(settings['game_object']['bandeira'][0], pos):
                pos = (pos[0]-36, pos[1]-15)
                settings['game_object']['nota'].append(Sprite(pos, settings['var']['folder'] + '/assets/notas/nota' + str(settings['var']['valor_nota'])+'.png', 68, 30))
                settings['var']['money'] += settings['var']['valor_nota']
            for index in range(len(settings['game_object']['list'])):
                if verificar_click(settings['game_object']['list'][index], pos, index):
                    settings['game_object']['list'][index], settings = verificar_se_da_pra_comprar(settings['game_object']['list'][index], settings)
    for gO in settings['game_object']['nota']:
        gO.y_speed += 0.5
        gO.y += gO.y_speed
        gO.rotation += gO.rotate_frame
        if gO.y > settings['screen_size'][1]:
            settings['game_object']['nota'].remove(gO)
    settings = calcular_ganho_idle(settings)
    settings = somar_idle(settings)
    return settings

def calcular_ganho_idle(settings):
    settings['var']['idle_gain'] = 0
    for gO in settings['game_object']['list']:
        if gO.level>0:
            settings['var']['idle_gain'] += (gO.idle_up+(gO.idle_add*gO.level))/300.0
    return settings

def somar_idle(settings):
    settings['var']['money'] += settings['var']['idle_gain']
    return settings

def verificar_se_da_pra_comprar(powerUP, settings):
    money = settings['var']['money']
    if money >= powerUP.price():
        settings['var']['money'] -= powerUP.price()
        powerUP.level += 1
    return powerUP, settings

def draw(settings):
    screen_size = settings['screen_size']
    screen      = settings['screen']
    game_object = settings['game_object']
    font = pygame.font.SysFont("PressStart2P", 20)
    screen.fill((180, 200, 150))

    index = 0
    draw_power_up(screen, game_object['list'])
    draw_other(screen, game_object)
    txt = str(int(settings['var']['money'])) + '(' +str('%.2f' % float(settings['var']['idle_gain']))+ ')'
    screen.blit(font.render(txt, True, (255, 255, 255)), (140-10*(len(str(int(settings['var']['money'])))-1), 220))
    pygame.display.flip()
    fps(60)
    pass

def draw_other(screen, game_object):
    for name in ['bandeira', 'nota']:
        for gO in game_object[name]:
            if gO.__class__==Sprite:
                temp_img = pygame.transform.rotate(gO.img, gO.rotation)
                screen.blit(temp_img, (gO.x, gO.y))

def draw_power_up(screen, game_object):
    index = 0
    for gO in game_object:
        x = 40
        y = 250+40*index
        width = 300
        height = 80
        pygame.draw.rect(screen, (50, 50, 50), (x, y, width, height))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 1)
        screen.blit(gO.img, (x+10, y+12))
        font = pygame.font.SysFont("PressStart2P", 12)
        screen.blit(font.render(gO.name, True, (255, 255, 255)), (x+90, y+10))
        font = pygame.font.SysFont("PressStart2P", 13)
        screen.blit(font.render('Price: ' + str(gO.price()), True, (255, 255, 255)), (x+100, y+40))
        screen.blit(font.render('Gain : ' + str('%.2f' % float((gO.idle_up+gO.idle_add*gO.level)/300.0)), True, (255, 255, 255)), (x+100, y+58))
        index += 1

def check_exit(settings):
    if settings['var']['exit_request']:
        return False
    else:
        return True

def fps(frames):
    pygame.time.Clock().tick(frames)

def verificar_click(box, pos, index=0):
    if box.__class__ == Sprite:
        if pos[0] >box.x and pos[0] < box.x+box.width and \
            pos[1]>box.y and pos[1] < box.y+box.height:
            return True
    elif box.__class__ == PowerUp:
        x = 40
        y = 250+40*index
        width = 300
        height= 80
        if pos[0] > x and pos[0] < x+width and \
            pos[1]> y and pos[1] < y+height:
            return True
    return False

class PowerUp():
    def __init__(self, path, name, init_price, multiplier_per_level, idle_up, idle_add, scale_x=None, scale_y=None):
        self.x = 0
        self.y = 0
        self.level = 0
        self.name = name
        self.img = pygame.image.load(path)
        if scale_x != None:
            self.img = pygame.transform.scale(self.img, (scale_x, scale_y))
        self.width = self.img.get_width()
        self.height= self.img.get_height()
        self.init_price = init_price
        self.multiplier_per_level = multiplier_per_level
        self.idle_up = idle_up
        self.idle_add = idle_add
    def price(self):
        return (self.init_price+(self.multiplier_per_level*self.level))

class Sprite():
    def __init__(self, (x, y), path, scale_x=None, scale_y=None):
        self.x = x
        self.y = y
        self.y_speed = 0
        self.img = pygame.image.load(path)
        self.rotation = 0
        self.rotate_frame = randint(-3, 3)
        if scale_x != None:
            self.img = pygame.transform.scale(self.img, (scale_x, scale_y))
        self.width = self.img.get_width()
        self.height = self.img.get_height()

main()
