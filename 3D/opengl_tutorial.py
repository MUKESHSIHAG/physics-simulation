import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

class Cube(object):
    distance = 0
    left_key = False
    right_key = False
    up_key = False
    down_key = False
    a_key = False
    s_key = False
    d_key = False
    r_key = False
    f_key = False
    x_axis = 0
    y_axis = 0
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
    #-------------------------------------
    def __init__(self):
        self.coordinates = [0,0,0]
        self.rubik_id = self.load_texture("dirt.jpg")

    def load_texture(self,filename):
        textureSurface = pygame.image.load(filename)
        textureData = pygame.image.tostring(textureSurface,"RGBA",1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,ID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,textureData)
        return ID

    def render_scene(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glTranslatef(0,0,-5)   
        
        glTranslatef(self.x_axis,self.y_axis,self.distance)
        
        glRotatef(self.coordinates[0],1,0,0)
        glRotatef(self.coordinates[1],0,1,0)
        glRotatef(self.coordinates[2],0,0,1)
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,self.rubik_id)
        
        glBegin(GL_QUADS)
        
        for face in self.faces:
            for i,v in enumerate(face):
                glTexCoord2fv(self.texcoord[i])
                glVertex3fv(self.vertices[v -1])
        
        glEnd()
        
        glDisable(GL_TEXTURE_2D)


    def rotate_x(self):
        if self.coordinates[0] > 360:
            self.coordinates[0] = 0
        else:
            self.coordinates[0] += 2
            
    def rotate_y(self):
        if self.coordinates[1] > 360:
            self.coordinates[1] = 0
        else:
            self.coordinates[1] += 2
            
    def rotate_z(self):
        if self.coordinates[2] > 360:
            self.coordinates[2] = 0
        else:
            self.coordinates[2] += 2
            
    def move_away(self):
        self.distance -= 0.1
        
    def move_close(self):
        if self.distance < 0:
            self.distance += 0.1
            
    def move_left(self):
        self.x_axis -= 0.1
        
    def move_right(self):
        self.x_axis += 0.1
        
    def move_up(self):
        self.y_axis += 0.1
        
    def move_down(self):
        self.y_axis -= 0.1
            
    def keydown(self):
        if self.a_key:
            self.rotate_x()
        elif self.s_key:
            self.rotate_y()
        elif self.d_key:
            self.rotate_y()
        elif self.r_key:
            self.move_away()
        elif self.f_key:
            self.move_close()
        elif self.left_key:
            self.move_left()
        elif self.right_key:
            self.move_right()
        elif self.up_key:
            self.move_up()
        elif self.down_key:
            self.move_down()
            
    def keyup(self):
        self.left_key = False
        self.right_key = False
        self.up_key = False
        self.down_key = False
        self.a_key = False
        self.s_key = False
        self.d_key = False
        self.r_key = False
        self.f_key = False
    
    def delete_texture(self):
        glDeleteTextures(self.rubik_id)
    
def main():
    pygame.init()
    pygame.display.set_mode((640,480),pygame.DOUBLEBUF|pygame.OPENGL)
    pygame.display.set_caption("PyOpenGL Tutorial")
    clock = pygame.time.Clock()
    done = False
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(45,640.0/480.0,0.1,200.0)
    
    glEnable(GL_DEPTH_TEST)

    cube = Cube()
    #----------- Main Program Loop -------------------------------------
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    cube.rotate_x()
                    cube.a_key = True
                elif event.key == pygame.K_s:
                    cube.rotate_y()
                    cube.s_key = True
                elif event.key == pygame.K_d:
                    cube.rotate_z()
                    cube.d_key = True
                elif event.key == pygame.K_r:
                    cube.move_away()
                    cube.r_key = True
                elif event.key == pygame.K_f:
                    cube.move_close()
                    cube.f_key = True
                elif event.key == pygame.K_LEFT:
                    cube.move_left()
                    cube.left_key = True
                elif event.key == pygame.K_RIGHT:
                    cube.move_right()
                    cube.right_key = True
                elif event.key == pygame.K_UP:
                    cube.move_up()
                    cube.up_key = True
                elif event.key == pygame.K_DOWN:
                    cube.move_down()
                    cube.down_key = True
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    cube.keyup()
                elif event.key == pygame.K_s:
                    cube.keyup()
                elif event.key == pygame.K_d:
                    cube.keyup()
                elif event.key == pygame.K_r:
                    cube.keyup()
                elif event.key == pygame.K_f:
                    cube.keyup()
                elif event.key == pygame.K_LEFT:
                    cube.keyup()
                elif event.key == pygame.K_RIGHT:
                    cube.keyup()
                elif event.key == pygame.K_UP:
                    cube.keyup()
                elif event.key == pygame.K_DOWN:
                    cube.keyup()
        
        cube.keydown()
        cube.render_scene()
        
        pygame.display.flip()
        clock.tick(30)
    
    cube.delete_texture()
    pygame.quit()

if __name__ == '__main__':
	main()

