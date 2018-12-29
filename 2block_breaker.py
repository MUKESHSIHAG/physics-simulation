import pygame, os
from pygame.locals import *
from random import randint
from time import time

def main():
    #Debug Var
    init = time()
    maior_update = 0
    maior_draw = 0
    maior_running = 0
    soma_update = 0
    soma_draw = 0
    soma_running = 0
    quant = 0
    running, settings = load()
    
    #debug
    print('load: ' + str(time()-init))
    init = time()
    while running:

        quant+=1
        init = time()

        running, settings = update(running, settings)

        if time()-init>maior_update:
            maior_update = time()-init
        soma_update += time()-init
        init = time()

        draw(settings['screen_size'], settings['screen'], settings['game_object'], \
            settings['var']['life'], settings['var']['font'], settings['var']['score'])

        if time()-init>maior_draw:
            maior_draw = time()-init
        soma_draw += time()-init
        init = time()

        if running:
            running = check_exit()
        if time()-init>maior_running:
            maior_running = time()-init
        soma_running += time()-init
    print
    print('maior_update  : %.4f sec' % (maior_update))
    print('maior_draw    : %.4f sec' % (maior_draw))
    print('maior_running : %.4f sec' % (maior_running))
    print
    print('media_update  : %.4f sec' % (soma_update/quant))
    print('media_draw    : %.4f sec' % (soma_draw/quant))
    print('media_running : %.4f sec' % (soma_running/quant))
    pygame.quit()

def load():
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Block Breaker - Ulisses Gandini")
    pygame.font.init()
    game_object = {
        'block' : [],
        'player': [],
        'ball'  : []
    }
    var = {
        'folder' : os.path.dirname(os.path.realpath(__file__)),
        'life'   : 5,
        'font'   : pygame.font.SysFont("arial", 20),
        'playing': False,
        'score'  : 0,
    }
    game_object = load_level(1, game_object)
    return True, {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'var'           : var
    }

def load_level(what_level, game_object):
    game_object = {
        'block' : [],
        'player': [],
        'ball'  : []
    }
    what_level = 2000
    if what_level == 1:
        for i in range(12):
            for j in range(15):
                if i%4 != 0:
                    game_object['block'].append(Block2D(10 + 780/15 * j, 40+15*i, 780/15, 15, \
                (230/12*i, 250, 100/8*j), 80))
                else:
                    game_object['block'].append(Block2D(10 + 780/15 * j, 40+15*i, 780/15, 15, \
                (250, 230/12*i, 100/8*j), 100))
        game_object['player'].append(Block2D(320, 550, 160, 20, (100, 100, 200), 0))
        game_object['ball'].append(Circle2D(400, 540, 10))
    if what_level == 2000:
        for i in range(12):
            for j in range(15):
                if j<10 or j>12:
                    game_object['block'].append(Block2D(10 + 780/15 * j, 40+15*i, 780/15, 15, (230/12*i, 250, 100/8*j), 80))
        game_object['player'].append(Block2D(320, 550, 160, 20, (100, 100, 200), 0))
        game_object['ball'].append(Circle2D(400, 540, 10))
    return game_object

def game_over(screen, font, screen_size):
    while True:
        k = pygame.key.get_pressed()
        sair = False
        for e in pygame.event.get():
            if e.type == QUIT or k[K_ESCAPE]:
                sair = True
        if sair:
            break
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("arial", 56)
        screen.blit(font.render('Game Over', True, (255, 255, 255)), (25, 7))
        pygame.display.flip()
    return False

def update(running, settings):
    game_object = settings['game_object']
    screen_size = settings['screen_size']
    ball        = game_object['ball']
    player      = game_object['player'][0]
    life        = settings['var']['life']
    playing     = settings['var']['playing']
    font        = settings['var']['font']
    screen      = settings['screen']

    for gO in game_object['block']:
        if gO.life <= 0:
            game_object['block'].remove(gO)

    if ball[0].y>550:
        settings['var']['life'] -= 1
        if settings['var']['life'] < 0:
            running = game_over(screen, font, screen_size)
        else:
            player.x = 320
            ball[0].x = 400
            ball[0].y = 540
            if ball[0].y_speed > 0:
                ball[0].y_speed = -ball[0].y_speed
            settings['var']['playing'] = False
    k = pygame.key.get_pressed()
    if not playing:
        if k[K_SPACE]:
            settings['var']['playing'] = True
            ball[0].x_speed = randint(-4, 4)
        if k[K_d]:
            player.x += 8
        elif k[K_a]:
            player.x -= 8
        if player.x<0:
            player.x = 0
        if player.x+player.width>screen_size[0]:
            player.x = screen_size[0]-player.width
        ball[0].x = player.x+player.width/2
    else:
        if k[K_d]:
            player.x += 8
        elif k[K_a]:
            player.x -= 8
        if player.x<0:
            player.x = 0
        if player.x+player.width>screen_size[0]:
            player.x = screen_size[0]-player.width
        ball, settings['var']['score'] = update_ball(ball, game_object, screen_size, settings['var']['score'])
    return running, settings

def draw(screen_size, screen, game_object, life, font, score):
    screen.fill((0, 0, 0))
    for name in game_object:
        for gO in game_object[name]:
            if gO.__class__==Block2D:
                pygame.draw.rect(screen, gO.color, (gO.x, gO.y, gO.width, gO.height))
                pygame.draw.rect(screen, (255, 255, 255), (gO.x, gO.y, gO.width, gO.height), 1)
            elif gO.__class__==Circle2D:
                pygame.draw.circle(screen, (255, 255, 255), (gO.x, gO.y), gO.radius)
            elif gO.__class__==Sprite:
                screen.blit(gO.img, (gO.x, gO.y))
    for i in range(life):
        pygame.draw.circle(screen, (255, 255, 255), (90+30*i, 20), 13)
        c = 255/10*i
        if c < 100:
            c = 100
        pygame.draw.circle(screen, (c, 100/5*i, 250/5*i), (90+30*i, 20), 13, 2)
    screen.blit(font.render('Lifes:', True, (255, 255, 255)), (25, 7))
    screen.blit(font.render('Score: ' + str(score), True, (255, 255, 255)), (400, 7))
    pygame.display.flip()
    fps(60)
    pass

def update_ball(ball, game_object, screen_size, score):
    for gO in ball:
        gO, score = intersects(gO, game_object, screen_size, score)
        gO.x += gO.x_speed
        gO.y += gO.y_speed
    return ball, score

def fps(frames):
    pygame.time.Clock().tick(frames)

def check_exit():
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

class Block2D():
    def __init__(self, x, y, width, height, color, score=0):
        self.x = x
        self.y = y
        self.width = width
        self.score = score
        self.height = height
        self.life = 1
        self.color = color

class Circle2D():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_speed = 3
        self.y_speed = -6

class Sprite():
    def __init__(self, x, y, path):
        self.x = x
        self.y = y
        self.img = pygame.image.load(path)

def intersects(circle, game_object, screen_size, score):
    if circle.x+circle.radius>screen_size[0] or circle.x-circle.radius<0:
        circle.x_speed = -circle.x_speed
    if circle.y-circle.radius<20:
        circle.y_speed = -circle.y_speed
    for name in ['block', 'player']:
        for gO in game_object[name]:
            if ((circle.x+circle.radius>gO.x and circle.x<gO.x) or (circle.x-circle.radius<gO.x and circle.x+circle.radius>gO.x)) and \
            ((circle.y-circle.radius>gO.y and circle.y-circle.radius<gO.y+gO.height) or (circle.y+circle.radius>gO.y and \
            circle.y+circle.radius<gO.y+gO.height)):
                if name != 'player':
                    gO.life -= 1
                    score += gO.score
                    if (circle.x+circle.radius > gO.x and circle.x_speed > 0) or (circle.x-circle.radius< gO.x+gO.width and circle.x_speed < 0):
                        circle.x_speed = -circle.x_speed
                    break
                else:
                    if circle.x>gO.x+gO.width/2:
                        circle.x_speed = randint(1, 4)
                    else:
                        circle.x_speed = -randint(1, 4)
            if ((circle.y+circle.radius>gO.y and circle.y-circle.radius<gO.y) or \
            (circle.y-circle.radius<gO.y+gO.height and circle.y+circle.radius>gO.y)) \
            and (circle.x+circle.radius>gO.x and circle.x-circle.radius<gO.x+gO.width):
                circle.y_speed = -circle.y_speed
                if name != 'player':
                    gO.life -= 1
                    score += gO.score
                    break
                else:
                    if circle.x>gO.x+gO.width/2:
                        circle.x_speed = randint(1, 4)
                    else:
                        circle.x_speed = -randint(1, 4)
    return circle, score

main()
