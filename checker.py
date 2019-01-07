import pygame
from pygame.locals import *

lista = [(150, 150, 150), (200, 150, 150), (150, 150, 150),
         (200, 150, 150), (150, 150, 150), (200, 150, 150),
         (150, 150, 150), (200, 150, 150), (150, 150, 150)
    ]

jogando = True
tamanho = (400, 400)
screen  = pygame.display.set_mode(tamanho)

for linha in range(3):
    for coluna in range(3):
        pygame.draw.rect(screen, lista[3*coluna+linha], ((400/3)*linha, (400/3)*coluna, 400/3, 400/3))
pygame.display.flip()
while jogando:
    k = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == QUIT or k[K_ESCAPE]:
            jogando = False
pygame.quit()
