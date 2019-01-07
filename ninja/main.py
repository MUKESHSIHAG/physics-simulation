import pygame, os #import padrao

#import de classes
from Sprite          import * #working- OK
from Animation       import * #working- OK
from Collider2D_AABB import * #working- OK
from Camera          import * #working- OK

#import de variaveis
from pygame.locals   import *
from time            import time

def main():
    init = time()
    maior_update = 0
    maior_draw = 0
    maior_running = 0
    soma_update = 0
    soma_draw = 0
    soma_running = 0
    quant = 0
    running, settings = load()
    print('load: ' + str(time()-init))
    init = time()
    while running:
        quant+=1
        init = time()
        settings = update(settings) #aqui da updade

        if time()-init>maior_update:
            maior_update = time()-init
        soma_update += time()-init
        init = time()

        draw(settings['game_object'], settings['screen'], settings['screen_size'], settings['layers'], settings['var']['camera'][0]) #aqui desenha na tela
        if time()-init>maior_draw:
            maior_draw = time()-init
        soma_draw += time()-init
        init = time()

        running = check_exit()
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

#load
def load():
    settings = load_settings()
    settings['game_object'] = load_map(settings, 1)
    running = True
    return running, settings
    
def load_map(settings, what_map):
    max_maps = settings['var']['total_maps']
    folder   = settings['var']['folder']
    game_object = settings['game_object']
    if what_map > max_maps:
        load_scene('win_game')
    img = pygame.image.load(folder+ '/assets/img/map/map' + str(what_map) + '.png')
    width = img.get_width()
    height = img.get_height()
    for coluna in range(width):
        for linha in range(height):
            x = coluna
            y = linha
            color = str(img.get_at((x, y)))
            game_object = load_object(settings['game_object'], color, x*128, y*128, x, y, img, settings['var']['folder'])
    return game_object
            
def load_scene(what_scene):
    pass

def load_object(game_object, color, x, y, px, py, img, folder):
    imagem = img
    color_left = ""
    color_right = ""
    color_up = ""
    color_down = ""
    if px>0:
    	color_left = str(img.get_at((px-1, py)))
    if px<img.get_width()-1:
    	color_right = str(img.get_at((px+1, py)))
    if py>0:
    	color_up = str(img.get_at((px, py-1)))
    if py<img.get_height()-1:
    	color_down = str(img.get_at((px, py+1)))
    objects = {
    	'(0, 0, 0, 255)'       	: ['tile', 'assets'],  #black
    	'(255, 0, 0, 255)'		: ['objective', '/assets/img/tile/objective.png'],
    	'(0, 0, 255, 255)'		: ['player', '/assets/img/player/idle0.png']
    }
    if color == '(0, 0, 0, 255)':
    	#especial aqui
    	#floor Medio Up = FMU
    	#FMF = Floor Medio Fly
    	sufixo = 'F'
    	#check sides
    	if color_left!=color and color_left!="":
    		sufixo += 'L'
    	elif color_left==color and color_left == color_right:
    		sufixo += 'M'
    	elif color_left != color and color_right != color:
    		sufixo += 'M'
    	elif color_right != color:
    		sufixo += 'R'
    	elif color_left != color:
    		sufixo += 'L'
    
    	#check up&down
        if color_down == color and color != color_up:
    		sufixo += 'U'
    	elif color_up == color:
    		sufixo += 'D'
    	elif color_down == "" and color_down==color_up:
    		sufixo += 'U'
    	elif color==color_up==color_down:
    		sufixo += 'U'
    	else:
    		sufixo += 'F'
    	sufixo += '.png'
    	game_object[objects[color][0]].append(Sprite((x, y), folder+'/assets/img/tile/'+sufixo, (True, [0, 0, 0, 0])))
    elif color in objects:
        if color=='(0, 0, 255, 255)':
            anim = {
                'idle'   : [2, 0.6],
                'running': [3, 0.15],
                'jumping': [3, 0.04]
            }
            collider=(True, [0, 0, 1, 1])
            game_object['player'].append(Sprite((x, y), folder+'/assets/img/player/idle0.png', collider, (anim, folder+'/assets/img/player', 'idle'), 4, True))
        else:
            game_object[objects[color][0]].append(Sprite((x, y), folder+objects[color][1]))
    return game_object

def load_settings():
    screen_size = (700, 550)
    screen = pygame.display.set_mode(screen_size)
    game_object = {
        'player'    : [],
        'tile'      : [],
        'collider'  : [],
        'bg'        : [],
        'objective' : []
    }
    var = {
        'folder'    : os.path.dirname(os.path.realpath(__file__)),
        'total_maps': len(os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/assets/img/map')),
        'camera'    : [Camera(screen_size)]
    }
    game_object['bg'].append(Sprite((0, 0), var['folder'] + '/assets/img/tile/bg.png'))
    game_object['bg'][0].img = pygame.transform.scale(game_object['bg'][0].img, screen_size)
    return {
        'screen_size'   : screen_size,
        'screen'        : screen,
        'game_object'   : game_object,
        'var'           : var,
        'layers'        : ['bg', 'tile', 'player', 'objective']
    }

def update(settings):
    game_object = settings['game_object']
    player = game_object['player'][0]
    camera = settings['var']['camera'][0]
    
    camera.set_focus((player.x, player.y))
    for name in game_object:
        for gO in game_object[name]:
            if gO.animation:
                gO.animation.update()
            if gO.gravity:
                gO.collider[1].update_move(game_object)
    return settings

def draw(game_object, screen, screen_size, layers, camera):
    screen.fill((0, 0, 0))
    cam(screen, screen_size, game_object, layers, camera)
    pygame.display.flip()
    fps(60)
    pass

def fps(frames):
    pygame.time.Clock().tick(frames)

def cam(screen, screen_size, game_object, layers, camera):
    player = game_object['player'][0]
    x = camera.x
    y = camera.y
    for name in layers:
        for gO in game_object[name]:
            img = gO.img
            if name == 'bg':
                screen.blit(img, (0, 0))
            else:
                if gO.flipped:
                    img = pygame.transform.flip(img, True, False)
                if gO.scale > 1:
                        img = pygame.transform.scale(img, (img.get_width()*gO.scale, img.get_height()*gO.scale))
                screen.blit(img, (gO.x-x, gO.y-y))
                #pygame.draw.rect(screen, (255, 0, 0), (gO.x-x, gO.y-y, gO.width, gO.height), 1)
        

def check_exit():
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            return False
    return True

if __name__=='__main__':
    main()
