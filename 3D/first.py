import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


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

surfaces = (
    (1,2,3,4),
    (5,8,7,6),
    (1,5,6,2),
    (2,6,7,3),
    (3,7,8,4),
    (5,1,4,8)
)

#texcoord = ((0,0),(1,0),(1,1),(0,1))
texcoord = ((0, 0), (0, 1), (1, 1), (1, 0))

#(1,0)#1
#(0,0)#2
#(0,1)#3
#(1,1)#4
#
#(0,0)#2
#(0,1)#3
#(1,1)#4
#(1,0)#1


class Cube(object):
    def __init__(self):
        self.coordinates = [50,50,0]
        self.dirt_id = self.load_texture("dirt.jpg")

    def load_texture(self, path):
        textureSurface = pygame.image.load(path)
        textureData = pygame.image.tostring(textureSurface,"RGBA",1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,ID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,textureData)
        return ID
    
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glTranslatef(0,0,-15)

        glRotatef(self.coordinates[0],1,0,0)
        glRotatef(self.coordinates[1],0,1,0)
        glRotatef(self.coordinates[2],0,0,1)


        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,self.dirt_id)

        glBegin(GL_QUADS)

        for surface in surfaces:
            for i,v in enumerate(surface):
                glTexCoord2fv(texcoord[i])
                glVertex3fv(vertices[v-1])
        
        glEnd()

        glDisable(GL_TEXTURE_2D)
        
    def delete_texture(self):
        glDeleteTextures(self.dirt_id)

def main():
    pygame.init()
    display = (600, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()


    gluPerspective(45, (display[0]/display[1]), 0.1, 50)

    glEnable(GL_DEPTH_TEST)

    cube = Cube()
    while True:
        k = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or k[K_ESCAPE]:
                cube.delete_texture()
                pygame.quit()
                quit()
        glRotatef(1, 3, 1, 1)
        
        cube.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    

main()