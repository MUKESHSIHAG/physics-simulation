import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def main():
    running, settings = load()
    while running:
        settings = update(settings)
        draw(settings)
        running = check_exit()
    pygame.quit()
    quit()

class Cube(object):
    distance = 0
    vertices = (
        (1,-1,-1),
        (1,-1,1),
        (-1,-1,1),
        (-1,-1,-1),
        (1,1,-1),
        (1,1,1),
        (-1,1,1),
        (-1,1,-1)
    )
    faces = (
        (1,2,3,4),
        (5,8,7,6),
        (1,5,6,2),
        (2,6,7,3),
        (3,7,8,4),
        (5,1,4,8)
    )
    texcoord = ((0,0),(1,0),(1,1),(0,1))

    def __init__(self):
        self.coordinates = [0,0,0]
        self.rubik_id = self.load_texture("rubik.png")

    def load_texture(self,filename):
        textureSurface = pygame.image.load(filename)
        textureData = pygame.image.tostring(textureSurface,"RGBA",1)
        print(textureData)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,ID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,textureData)
        return ID

def load():
    screen_size = (500, 500)
    screen = pygame.display.set_mode(screen_size, DOUBLEBUF|OPENGL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentify()

    gluPerspective(45, screen_size[0]/screen_size[1], 0.1, 50)

    glEnable(GL_DEPTH_TEST)

    cube = Cube()