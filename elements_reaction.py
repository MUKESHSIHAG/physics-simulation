#Display info
print("""Falling sand.pyw

    This code is a python clone of Falling sand game, Element dots, Powder toy, and javagame/dust.
    It also displays a panel showing you statistics like frames per second and the number of dots.

    w = water
    k = solid
    r = solid (fire-resistant)
    b = bomb
    o = oil
    m = substrate for fire
    e = fire extinguisher
    x = acid
    g = methane
    t = salt
    
    s = bigger
    a = smaller
    
    p = pause/play
    
    c = clear screen

    """)

#Get window size
winsize = input("Window size. STANDARD, HD, FSGSMALL, FSGLARGE")

if winsize == "STANDARD":
    winsize = (1000,510)

if winsize == "HD":
    winsize = (1180,575)

if winsize == "FSGSMALL":
    winsize = (640,480)

if winsize == "FSGLARGE":
    winsize = (800,600)
    
#Imports
import pygame,sys,os,random
pygame.init()

#Colors

#Standard
BLANKCOLOR = (255,255,255)
SOLIDCOLOR = (255,0,255)
RESISTCOLOR = (128,0,128)
WATERCOLOR = (0,128,255)
FIRECOLOR = (255,128,0)
STEAMCOLOR = (174,174,174)
SMOKECOLOR = (96,96,96)
OILCOLOR = (96,64,64)
BOMBCOLOR = (0,192,0)
SUBSTRATECOLOR = (128,128,0)
EXTINGUISHCOLOR = (128,128,255)
METHANECOLOR = (192,192,192)
SALTCOLOR = (255,255,192)
ACIDCOLOR = (0,255,0)
PANELCOLOR = (164,164,164)
PANELTEXTCOLOR = (24,48,64)
MSGCOLOR = (24,48,64)


"""
#Falling sand game
BLANKCOLOR = (0,0,0)
SOLIDCOLOR = (128,128,128)
RESISTCOLOR = (128,0,128)
WATERCOLOR = (0,0,255)
FIRECOLOR = (255,0,0)
STEAMCOLOR = (174,174,174)
SMOKECOLOR = (96,96,96)
OILCOLOR = (96,64,64)
BOMBCOLOR = (0,192,0)
SUBSTRATECOLOR = (128,128,0)
EXTINGUISHCOLOR = (128,128,255)
METHANECOLOR = (1,1,1)
SALTCOLOR = (255,255,255)
ACIDCOLOR = (192,255,0)
PANELCOLOR = (98,98,98)
PANELTEXTCOLOR = (255,255,248)
MSGCOLOR = (255,255,255)

#Element dots
BLANKCOLOR = (255,255,255)
SOLIDCOLOR = (0,192,0)
RESISTCOLOR = (128,0,128)
WATERCOLOR = (0,128,255)
FIRECOLOR = (255,128,0)
STEAMCOLOR = (174,174,174)
SMOKECOLOR = (96,96,96)
OILCOLOR = (0,12,0)
BOMBCOLOR = (0,255,0)
SUBSTRATECOLOR = (128,128,0)
EXTINGUISHCOLOR = (128,128,255)
METHANECOLOR = (204,204,204)
SALTCOLOR = (255,255,192)
ACIDCOLOR = (192,255,0)
PANELCOLOR = (192,192,255)
PANELTEXTCOLOR = (0,0,0)
MSGCOLOR = (0,0,0)

#Standard
BLANKCOLOR = (255,255,255)
SOLIDCOLOR = (255,0,255)
RESISTCOLOR = (128,0,128)
WATERCOLOR = (0,128,255)
FIRECOLOR = (255,128,0)
STEAMCOLOR = (174,174,174)
SMOKECOLOR = (96,96,96)
OILCOLOR = (96,64,64)
BOMBCOLOR = (0,192,0)
SUBSTRATECOLOR = (128,128,0)
EXTINGUISHCOLOR = (128,128,255)
METHANECOLOR = (192,192,192)
SALTCOLOR = (255,255,192)
ACIDCOLOR = (0,255,0)
PANELCOLOR = (164,164,164)
PANELTEXTCOLOR = (24,48,64)
MSGCOLOR = (24,48,64)
"""

LIQUIDCOLORS = (SOLIDCOLOR,WATERCOLOR,OILCOLOR,BOMBCOLOR,SUBSTRATECOLOR,EXTINGUISHCOLOR)
FIRECOLORS = (SOLIDCOLOR,WATERCOLOR,OILCOLOR,BOMBCOLOR,SUBSTRATECOLOR,EXTINGUISHCOLOR,FIRECOLOR)

#The width of the panel on the right
PANELWIDTH = 160

#A clock object for keeping track of fps
clock = pygame.time.Clock()

#The font used on the panel. 18 pixels high
font = pygame.font.Font("freesansbold.ttf",18)

substanceType = "SOLID" #The default substance is solid.
substanceSize = 5       #The size is 5 px
paused = 1              #The game starts paused
solidCount = 0          #The number of solid pixels (for the panel)
highFPS = 1             #Max fps

#A group for every type of substance
water = pygame.sprite.Group()
fire = pygame.sprite.Group()
steam = pygame.sprite.Group()
oil = pygame.sprite.Group()
substrate = pygame.sprite.Group()
bombs = pygame.sprite.Group()
extinguish = pygame.sprite.Group()
methane = pygame.sprite.Group()
acid = pygame.sprite.Group()
salt = pygame.sprite.Group()

#A water dot
class WaterDot(pygame.sprite.Sprite):
    
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]

    def update(self):

        #Remove the old pixel
        screen.set_at((self.x,self.y),BLANKCOLOR)

        #Kill if it can go off the screen
        if self.y > screen.get_height()-3 or self.x > screen.get_width()-4 or self.x < 4:
            self.kill()
            return

        #Move down if possible
        if screen.get_at((self.x,self.y+1)) == BLANKCOLOR:
            self.y += 1
        #When to behave as a liquid
        elif screen.get_at((self.x,self.y+1)) in LIQUIDCOLORS:
            #Find the pixels to the sides
            r1 = screen.get_at((self.x+1,self.y))
            r2 = screen.get_at((self.x+2,self.y))
            r3 = screen.get_at((self.x+3,self.y))
            l1 = screen.get_at((self.x-1,self.y))
            l2 = screen.get_at((self.x-2,self.y))
            l3 = screen.get_at((self.x-3,self.y))

            #The name w is meaningless, but it was used in dots.js
            wr = 0; wl = 0

            #Find the closest pixels to the right and left
            if r3 == BLANKCOLOR:
                wr = 3
            if r2 == BLANKCOLOR:
                wr = 2
            if r1 == BLANKCOLOR:
                wr = 1

            if l3 == BLANKCOLOR:
                wl = 3
            if l2 == BLANKCOLOR:
                wl = 2
            if l1 == BLANKCOLOR:
                wl = 1

            #Pick a side and move there
            if random.randint(0,100) > 50:
                #Right
                if wr == 3:
                    self.x += 3
                elif wr == 2:
                    self.x += 2
                elif wr == 1:
                    self.x += 1

            else:
                #Left
                if wl == 3:
                    self.x -= 3
                elif wl == 2:
                    self.x -= 2
                elif wl == 1:
                    self.x -= 1

        #Turn to steam if there is fire nearby
        if screen.get_at((self.x,self.y-1)) == FIRECOLOR:
            s = SteamDot((self.x,self.y),"STEAM")
            s.add(steam)
            self.kill() #Kill

        #Salt absorbs water
        if screen.get_at((self.x,self.y-1)) == SALTCOLOR:
            self.kill() #Kill

        #Draw with WATERCOLOR
        screen.set_at((self.x,self.y),WATERCOLOR)

#An acid dot
class AcidDot(pygame.sprite.Sprite):
    
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]

    def update(self):

        #Remove the old pixel
        screen.set_at((self.x,self.y),BLANKCOLOR)

        self.y += 1

        #Kill if it can go off the screen
        if self.y > screen.get_height()-3 or self.x > screen.get_width()-4 or self.x < 4:
            self.kill()
            return
            
        #When to behave as a liquid
        elif screen.get_at((self.x,self.y+1)) == RESISTCOLOR:
            #Find the pixels to the sides
            r1 = screen.get_at((self.x+1,self.y))
            r2 = screen.get_at((self.x+2,self.y))
            r3 = screen.get_at((self.x+3,self.y))
            l1 = screen.get_at((self.x-1,self.y))
            l2 = screen.get_at((self.x-2,self.y))
            l3 = screen.get_at((self.x-3,self.y))

            #The name w is meaningless, but it was used in dots.js
            wr = 0; wl = 0

            #Find the closest pixels to the right and left
            if r3 == BLANKCOLOR:
                wr = 3
            if r2 == BLANKCOLOR:
                wr = 2
            if r1 == BLANKCOLOR:
                wr = 1

            if l3 == BLANKCOLOR:
                wl = 3
            if l2 == BLANKCOLOR:
                wl = 2
            if l1 == BLANKCOLOR:
                wl = 1

            #Pick a side and move there
            if random.randint(0,100) > 50:
                #Right
                if wr == 3:
                    self.x += 3
                elif wr == 2:
                    self.x += 2
                elif wr == 1:
                    self.x += 1

            else:
                #Left
                if wl == 3:
                    self.x -= 3
                elif wl == 2:
                    self.x -= 2
                elif wl == 1:
                    self.x -= 1

        #Draw with ACIDOLOR
        screen.set_at((self.x,self.y),ACIDCOLOR)

#An extinguisher dot
class ExtDot(pygame.sprite.Sprite):
    
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]

    def update(self):

        #Remove the old pixel
        screen.set_at((self.x,self.y),BLANKCOLOR)

        #Kill if it can go off the screen
        if self.y > screen.get_height()-3 or self.x > screen.get_width()-4 or self.x < 4:
            self.kill()
            return

        #Move down if possible
        if screen.get_at((self.x,self.y+1)) == BLANKCOLOR:
            self.y += 1
        #When to behave as a liquid
        elif screen.get_at((self.x,self.y+1)) in LIQUIDCOLORS:
            #Find the pixels to the sides
            r1 = screen.get_at((self.x+1,self.y))
            r2 = screen.get_at((self.x+2,self.y))
            r3 = screen.get_at((self.x+3,self.y))
            l1 = screen.get_at((self.x-1,self.y))
            l2 = screen.get_at((self.x-2,self.y))
            l3 = screen.get_at((self.x-3,self.y))

            #The name w is meaningless, but it was used in dots.js
            wr = 0; wl = 0

            #Find the closest pixels to the right and left
            if r3 == BLANKCOLOR:
                wr = 3
            if r2 == BLANKCOLOR:
                wr = 2
            if r1 == BLANKCOLOR:
                wr = 1

            if l3 == BLANKCOLOR:
                wl = 3
            if l2 == BLANKCOLOR:
                wl = 2
            if l1 == BLANKCOLOR:
                wl = 1

            #Pick a side and move there
            if random.randint(0,100) > 50:
                #Right
                if wr == 3:
                    self.x += 3
                elif wr == 2:
                    self.x += 2
                elif wr == 1:
                    self.x += 1

            else:
                #Left
                if wl == 3:
                    self.x -= 3
                elif wl == 2:
                    self.x -= 2
                elif wl == 1:
                    self.x -= 1

        #Turn to steam if there is fire nearby
        if screen.get_at((self.x,self.y-1)) == FIRECOLOR:
            s = SteamDot((self.x,self.y),random.choice(("STEAM","SMOKE")))
            s.add(steam)

        #Draw with EXTINGUISHCOLOR
        screen.set_at((self.x,self.y),EXTINGUISHCOLOR)

#An oil dot
class OilDot(pygame.sprite.Sprite):

    def __init__(self,pos):

        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]

    def update(self):

        #Remove the old pixel
        screen.set_at((self.x,self.y),BLANKCOLOR)

        #Kill if it can go off the screen
        if self.y > screen.get_height()-3 or self.x > screen.get_width()-4 or self.x < 4:
            self.kill()
            return

        #Move down if possible
        if screen.get_at((self.x,self.y+1)) == BLANKCOLOR:
            self.y += 1

        #When to behave as a liquid
        elif screen.get_at((self.x,self.y+1)) in LIQUIDCOLORS:
            #Find the pixels to the sies
            r1 = screen.get_at((self.x+1,self.y))
            l1 = screen.get_at((self.x-1,self.y))

            #The name w is meaningless, but it was used in dots.js
            wr = 0; wl = 0

            #Find the closest pixels to the right and left
            if r1 == BLANKCOLOR:
                wr = 1
       
            if l1 == BLANKCOLOR:
                wl = 1

            #Pick a side and move there
            if random.randint(0,100) > 50:
                #Right
                if wr == 3:
                    self.x += 3
                elif wr == 2:
                    self.x += 2
                elif wr == 1:
                    self.x += 1

            else:
                #Left
                if wl == 3:
                    self.x -= 3
                elif wl == 2:
                    self.x -= 2
                elif wl == 1:
                    self.x -= 1

        #Fire multiplies if nearby
        if screen.get_at((self.x,self.y-1)) == FIRECOLOR:
            f = FireDot((self.x,self.y)) #Make fire
            f.add(fire)
            s = SteamDot((self.x,self.y),"SMOKE") #Make smoke
            s.add(steam)
            self.kill() #Kill

        #Draw with OILCOLOR
        screen.set_at((self.x,self.y),OILCOLOR)

#A substrate dot
class SubDot(pygame.sprite.Sprite):

    def __init__(self,pos):

        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]

    def update(self):

        #Remove the old pixel
        screen.set_at((self.x,self.y),BLANKCOLOR)

        #Kill if it can go off the screen
        if self.y > screen.get_height()-3 or self.x > screen.get_width()-4 or self.x < 4:
            self.kill()
            return

        #Move down if possible
        if screen.get_at((self.x,self.y+1)) == BLANKCOLOR:
            self.y += 1
        """
        #When to behave as a liquid
        elif screen.get_at((self.x,self.y+1)) in LIQUIDCOLORS:
            #Find the pixels to the sides
            r1 = screen.get_at((self.x+1,self.y))
            r2 = screen.get_at((self.x+2,self.y))
            r3 = screen.get_at((self.x+3,self.y))
            l1 = screen.get_at((self.x-1,self.y))
            l2 = screen.get_at((self.x-2,self.y))
            l3 = screen.get_at((self.x-3,self.y))

            #The name w is meaningless, but it was used in dots.js
            wr = 0; wl = 0

            #Find the closest pixels to the right and left
            if r3 == BLANKCOLOR:
                wr = 3
            if r2 == BLANKCOLOR:
                wr = 2
            if r1 == BLANKCOLOR:
                wr = 1

            if l3 == BLANKCOLOR:
                wl = 3
            if l2 == BLANKCOLOR:
                wl = 2
            if l1 == BLANKCOLOR:
                wl = 1

            #Pick a side and move there
            if random.randint(0,100) > 50:
                #Right
                if wr == 3:
                    self.x += 3
                elif wr == 2:
                    self.x += 2
                elif wr == 1:
                    self.x += 1

            else:
                #Left
                if wl == 3:
                    self.x -= 3
                elif wl == 2:
                    self.x -= 2
                elif wl == 1:
                    self.x -= 1
            """
        #Fire multiplies if nearby
        if screen.get_at((self.x,self.y-1)) == FIRECOLOR:
            f = FireDot((self.x,self.y-2)) #Make fire
            f.add(fire)

        #Draw with SUBSTRATECOLOR
        screen.set_at((self.x,self.y),SUBSTRATECOLOR)

#A salt dot
class SaltDot(pygame.sprite.Sprite):

    def __init__(self,pos):

        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]

    def update(self):

        #Remove the old pixel
        screen.set_at((self.x,self.y),BLANKCOLOR)

        #Kill if it can go off the screen
        if self.y > screen.get_height()-3 or self.x > screen.get_width()-4 or self.x < 4:
            self.kill()
            return

        #Move down if possible
        if screen.get_at((self.x,self.y+1)) == BLANKCOLOR:
            self.y += 1

        #Draw with SALTCOLOR
        screen.set_at((self.x,self.y),SALTCOLOR)

#A fire dot
class FireDot(pygame.sprite.Sprite):

    def __init__(self,pos,dx=0,dy=0): #Requires dx and dy incase it is from a bomb
        
        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]
        self.dx = dx 
        self.dy = dy

    def update(self):

        #Remove the old pixel
        screen.set_at((self.x,self.y),BLANKCOLOR)

        #Increment x/y
        self.x += self.dx
        self.y += self.dy

        #Kill if it can go off the screen
        if self.y > screen.get_height()-3 or self.y < 4 or self.x > screen.get_width()-4 or self.x < 4:
            self.kill()
            return

        #Move down if possible
        if screen.get_at((self.x,self.y+1)) == BLANKCOLOR:
            self.y += 1
            """
            #Fire can move sideways (sparks)
            if random.randint(0,100) > 20:
                self.x += 1
            else:
                self.x -= 1
        """

         #When to behave as a liquid
        elif screen.get_at((self.x,self.y+1)) in FIRECOLORS:
            #Find the pixels to the sies
            r1 = screen.get_at((self.x+1,self.y))
            l1 = screen.get_at((self.x-1,self.y))

            #The name w is meaningless, but it was used in dots.js
            wr = 0; wl = 0

            #Find the closest pixels to the right and left
            if r1 == BLANKCOLOR:
                wr = 1
       
            if l1 == BLANKCOLOR:
                wl = 1

            #Pick a side and move there
            if random.randint(0,100) > 50:
                #Right
                if wr == 3:
                    self.x += 3
                elif wr == 2:
                    self.x += 2
                elif wr == 1:
                    self.x += 1

            else:
                #Left
                if wl == 3:
                    self.x -= 3
                elif wl == 2:
                    self.x -= 2
                elif wl == 1:
                    self.x -= 1
                    
        #Burn through solid    
        if screen.get_at((self.x,self.y+1)) == SOLIDCOLOR:
            self.y += 1

            #Fire spread
            if random.randint(0,100) > 50:
                self.x += 1
            else:
                self.x -= 1

            #Multiply
            if random.randint(0,100) > 80:
                f = FireDot((self.x-1,self.y))
                f.add(fire)
                f = FireDot((self.x+1,self.y))
                f.add(fire)

            #Die out sometimes
            if random.randint(0,100) > 90:
                self.kill()
                return

        #Kill if touching water
        elif screen.get_at((self.x,self.y+1)) == WATERCOLOR or screen.get_at((self.x,self.y-1)) == WATERCOLOR or screen.get_at((self.x,self.y+1)) == EXTINGUISHCOLOR or screen.get_at((self.x,self.y-1)) == EXTINGUISHCOLOR:
            self.kill()
            return

        #Draw with FIRECOLOR
        screen.set_at((self.x,self.y),FIRECOLOR)

#A bomb dot
class BombDot(pygame.sprite.Sprite):

    def __init__(self,pos):

        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]

    def update(self):

        #Remove the old pixel
        screen.set_at((self.x,self.y),BLANKCOLOR)

        #Kill if it can go off the screen
        if self.y > screen.get_height()-3 or self.y < 4 or self.x > screen.get_width()-4 or self.x < 4:
            self.kill()
            return

        #Move down if possible
        if screen.get_at((self.x,self.y+1)) == BLANKCOLOR:
            self.y += 1

        #When to behave as a liquid
        elif screen.get_at((self.x,self.y+1)) in LIQUIDCOLORS:
            #Find the pixels to the sides
            r1 = screen.get_at((self.x+1,self.y))
            r2 = screen.get_at((self.x+2,self.y))
            l1 = screen.get_at((self.x-1,self.y))
            l2 = screen.get_at((self.x-2,self.y))
      
            #The name w is meaningless, but it was used in dots.js
            wr = 0; wl = 0

            #Find the closest pixels to the right and left
            if r2 == BLANKCOLOR:
                wr = 2
            if r1 == BLANKCOLOR:
                wr = 1

            if l2 == BLANKCOLOR:
                wl = 2
            if l1 == BLANKCOLOR:
                wl = 1

            #Pick a side and move there
            if random.randint(0,100) > 50:
                #Right
                if wr == 3:
                    self.x += 3
                elif wr == 2:
                    self.x += 2
                elif wr == 1:
                    self.x += 1

            else:
                #Left
                if wl == 3:
                    self.x -= 3
                elif wl == 2:
                    self.x -= 2
                elif wl == 1:
                    self.x -= 1

        #If near fire, explode
        elif screen.get_at((self.x,self.y-1)) == FIRECOLOR:
            #Make smoke
            for i in range(10):
                s = SteamDot((self.x,self.y-i),"SMOKE")
                s.add(steam)
            #Make fire
            for i in range(40):
                f = FireDot((self.x,self.y-i),random.randint(0,10)-5,random.randint(0,10)-5)
                f.add(fire)
            
            self.kill() #Kill
            return

        #Draw with BOMBCOLOR
        screen.set_at((self.x,self.y),BOMBCOLOR)

#A steam dot
class SteamDot(pygame.sprite.Sprite):

    def __init__(self,pos,typ): #Needs typ for steam or smoke

        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]
        self.typ = typ

    def update(self):

        #Remove the old pixel
        screen.set_at((self.x,self.y),BLANKCOLOR)

        #Kill if it can go off the screen
        if self.y > screen.get_height()-3 or self.y < 3 or self.x > screen.get_width()-4 or self.x < 4:
            self.kill()
            return

        #When to move up
        if screen.get_at((self.x,self.y-1)) == BLANKCOLOR or screen.get_at((self.x,self.y-1)) == BOMBCOLOR or screen.get_at((self.x,self.y-1)) == OILCOLOR or screen.get_at((self.x,self.y-1)) == FIRECOLOR or screen.get_at((self.x,self.y-1)) == WATERCOLOR:
            self.y -= 1
            if random.randint(0,100) > 50: #Move to the side(s)
                self.x += 1
            else:
                self.x -= 1

        #Very rarely kill
        if random.randint(0,100) > 99:
            self.kill()
            return

        #Draw
        if self.typ == "STEAM":
            screen.set_at((self.x,self.y),STEAMCOLOR) #Draw with STEAMCOLOR
        else:
            screen.set_at((self.x,self.y),SMOKECOLOR) #Draw with SMOKECOLOR

#A methane dot
class MethaneDot(pygame.sprite.Sprite):

    def __init__(self,pos):

        pygame.sprite.Sprite.__init__(self)
        self.x = pos[0]
        self.y = pos[1]

    def update(self):

        #Remove the old pixel
        screen.set_at((self.x,self.y),BLANKCOLOR)

        #Kill if it can go off the screen
        if self.y > screen.get_height()-3 or self.y < 3 or self.x > screen.get_width()-4 or self.x < 4:
            self.kill()
            return

        #When to move up
        if screen.get_at((self.x,self.y-1)) == BLANKCOLOR or screen.get_at((self.x,self.y-1)) == BOMBCOLOR or screen.get_at((self.x,self.y-1)) == OILCOLOR or screen.get_at((self.x,self.y-1)) == FIRECOLOR or screen.get_at((self.x,self.y-1)) == WATERCOLOR:
            self.y -= 1
            if random.randint(0,100) > 50: #Move to the side(s)
                self.x += 1
            else:
                self.x -= 1

        if screen.get_at((self.x,self.y-1)) == FIRECOLOR or screen.get_at((self.x,self.y+1)) == FIRECOLOR:
            f = FireDot((self.x,self.y-1),0,-2) #Make fire
            f.add(fire)
            self.kill()

        #Draw
        screen.set_at((self.x,self.y),METHANECOLOR) #Draw with METHANECOLOR
        
#Phase for loop monitoring
phase = 0

#Set up the window
screen = pygame.display.set_mode(winsize)
pygame.display.set_caption("Falling Sand Game") #Title is Falling Sand Game
screen.fill(BLANKCOLOR)

#Main Loop
while True:

    #Check for new events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Substance size events
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "a": #Smaller
            if substanceSize >= 1:
                substanceSize -= 1
                
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "s": #Bigger
            substanceSize += 1

        #Substance type events
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "k": #Solid
            substanceType = "SOLID"
            
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "r": #Resist
            substanceType = "RESIST"
            
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "w": #Water
            substanceType = "WATER"
            
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "f": #Fire
            substanceType = "FIRE"
            
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "o": #Oil
            substanceType = "OIL"
            
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "b": #Bomb
            substanceType = "BOMB"
            
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "m": #Substrate
            substanceType = "SUB"
            
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "e": #Extinguish
            substanceType = "EXT"
            
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "g": #Methane
            substanceType = "METHANE"

        if event.type == pygame.KEYDOWN and event.unicode.lower() == "x": #Acid
            substanceType = "ACID"

        if event.type == pygame.KEYDOWN and event.unicode.lower() == "t": #Salt
            substanceType = "SALT"

        
        #Pause or play (toggle)
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "p":
            if paused == 0:
                paused = 1
            else:
                paused = 0

        #Clear
        if event.type == pygame.KEYDOWN and event.unicode.lower() == "c":
            screen.fill(BLANKCOLOR)
            solidCount = 0          #The number of solid pixels (for the panel)

            #A group for every type of substance
            water = pygame.sprite.Group()
            fire = pygame.sprite.Group()
            steam = pygame.sprite.Group()
            oil = pygame.sprite.Group()
            substrate = pygame.sprite.Group()
            bombs = pygame.sprite.Group()
            extinguish = pygame.sprite.Group()
            methane = pygame.sprite.Group()
            salt = pygame.sprite.Group()
            acid = pygame.sprite.Group()

            
    #Paint events (end loop)
    if pygame.mouse.get_pressed()[0]: #If left mouse pressed
        
        if substanceType == "SOLID": #Paint solid
            pygame.draw.circle(screen,SOLIDCOLOR,pygame.mouse.get_pos(),5)
            solidCount += 1 #increment solidCount

        if substanceType == "RESIST": #Paint resistant
            pygame.draw.circle(screen,RESISTCOLOR,pygame.mouse.get_pos(),5)
            solidCount += 1 #increment solidCount


        #Other paint events
        if substanceType == "WATER": #Paint water
            for i in range(substanceSize): #This is where substanceSize comes in
                w = WaterDot((pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]+i))
                w.add(water)
                
        if substanceType == "FIRE": #Paint fire
            for i in range(substanceSize):
                f = FireDot((pygame.mouse.get_pos()[0]+i,pygame.mouse.get_pos()[1]+i))
                f.add(fire)
                
        if substanceType == "OIL": #Paint oil
            for i in range(substanceSize):
                o = OilDot((pygame.mouse.get_pos()[0]+i,pygame.mouse.get_pos()[1]+i))
                o.add(oil)
                
        if substanceType == "SUB": #Paint substrate
            for i in range(substanceSize):
                m = SubDot((pygame.mouse.get_pos()[0]+i,pygame.mouse.get_pos()[1]+i))
                m.add(substrate)
                
        if substanceType == "BOMB": #Paint bomb
            for i in range(substanceSize):
                b = BombDot((pygame.mouse.get_pos()[0]+i,pygame.mouse.get_pos()[1]+i))
                b.add(bombs)
                
        if substanceType == "EXT": #Paint extinguish
            for i in range(substanceSize):
                e = ExtDot((pygame.mouse.get_pos()[0]+i,pygame.mouse.get_pos()[1]+i))
                e.add(extinguish)

        if substanceType == "ACID": #Paint acid
            for i in range(substanceSize):
                x = AcidDot((pygame.mouse.get_pos()[0]+i,pygame.mouse.get_pos()[1]+i))
                x.add(acid)
                
        if substanceType == "METHANE": #Paint methane
            for i in range(substanceSize):
                g = MethaneDot((pygame.mouse.get_pos()[0]+i,pygame.mouse.get_pos()[1]-i)) #Methane floats up, so -1
                g.add(methane)

        if substanceType == "SALT": #Paint salt
            for i in range(substanceSize):
                t = SaltDot((pygame.mouse.get_pos()[0]+i,pygame.mouse.get_pos()[1]-i))
                t.add(salt)

    #If not paused, update
    if paused == 0:
        water.update()
        fire.update()
        steam.update()
        oil.update()
        substrate.update()
        bombs.update()
        extinguish.update()
        methane.update()
        acid.update()
        salt.update()

    #Is it time to show the statistics?
    if phase % 20 == 0 and clock.get_fps() > 25:
        #Clear the panel
        pygame.draw.rect(screen,PANELCOLOR,(screen.get_width()-PANELWIDTH,0,PANELWIDTH,screen.get_height()))
        
        #Render     the amount of substance         antialiased
        screen.blit(font.render(str(len(water))+" WATER",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,20))
        
        screen.blit(font.render(str(len(oil))+" OIL",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,40))
        
        screen.blit(font.render(str(len(fire))+" FIRE",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,60))
        
        screen.blit(font.render(str(len(steam))+" STEAM",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,80))

        screen.blit(font.render(str(len(bombs))+" BOMB",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,100))
        
        screen.blit(font.render(str(len(substrate))+" SUBSTRATE",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,120))
        
        screen.blit(font.render(str(len(extinguish))+" EXTINGUISHER",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,140))
        
        screen.blit(font.render(str(len(methane))+" METHANE",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,160))

        screen.blit(font.render(str(len(acid))+" ACID",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,180))

        screen.blit(font.render(str(len(salt))+" SALT",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,200))
        
        #Render     the amount of solid                 antialiased
        screen.blit(font.render(str(solidCount)+" SOLID",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,300))
        
        #Render the             clock.get_fps()       2 digits                     antialiased
        screen.blit(font.render(str(round(clock.get_fps(),2))+" FPS",
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,320))

        #Generate a message for whether the game is paused
        if paused == 1:
            pausetext = "PAUSED"    #Paused
        else:
            pausetext = "RUNNING!"  #Running
        
        #Render the             state       antialiased
        screen.blit(font.render(pausetext,
                                1,
                                PANELTEXTCOLOR),
                    (screen.get_width()-PANELWIDTH,280))

        #Find the total number of dots
        totalDots = len(steam)+len(fire)+len(oil)+len(water)+len(bombs)+len(substrate)+len(extinguish)+len(methane)+len(acid)+len(salt)

        #Make up a funny message
        if totalDots < 300: message = "try it!"
        
        elif totalDots > 300 and totalDots < 1700: message = "having fun?"
        
        elif totalDots > 1700 and totalDots < 10000: message = "lots of dots!"
        
        elif totalDots > 10000: message = "explosive!"

        #Clear the bottom
        pygame.draw.rect(screen,BLANKCOLOR,(5,screen.get_height()-23,400,23))
        
        #Render the             message antialiased
        screen.blit(font.render(message,
                                1,
                                MSGCOLOR),
                    (5,screen.get_height()-23))


    #Update the screen
    pygame.display.update()
    
    #Increase the phase
    phase += 1

    #Required for fps metering
    clock.tick(2000)
