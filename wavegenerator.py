import pygame
from pygame.locals import*
import time
import math
import sys
pygame.init()

class LongWave_Point(object):
    def __init__(self, pos, number, color, end_point=False, init_speed=0.0):
        if not end_point:
            self.color = color
        else:
            self.color = [250,250,250]

        self.init_speed = init_speed/10.0 # becomes frequency when end point
            
        self.number = number
        self.pos = pos
        if end_point:
            self.speed = init_speed/10.0
        else:
            self.speed = init_speed
        self.is_end_point=end_point

        self.next_speed = self.speed
        
        if end_point:
            self.center_pull = pos


            
    def prepare(self, wave_points):
        self.next_speed = self.speed
        
        if not self.is_end_point: # if this point is between the end points
            
            for point in wave_points:
                if point.number==self.number-1 or point.number==self.number+1:
                    distance = self.pos-point.pos
                    if point.is_end_point and  abs(distance)<tolerance:
                        if abs(distance)<tolerance*2:
                            self.next_speed+= ( tolerance-abs(distance) )/ float(tolerance) * speed * (abs(distance)/distance)
                        
                    else:
                        if abs(distance)<tolerance:
                            self.next_speed+= ( tolerance-abs(distance) )/ float(tolerance) * speed * (abs(distance)/distance)

                    if point.number==self.number-1 and distance<=0:
                        self.next_speed = point.speed*0.5
                        self.pos = point.pos+0.00000001
                    if point.number==self.number+1 and distance>=0:
                        self.next_speed = point.speed*0.5
                        self.pos = point.pos-0.00000001

        else: # if this point is an end point
            distance = self.pos-self.center_pull
            if distance != 0:
                self.next_speed-= abs(distance)/ float(tolerance) * self.init_speed * (abs(distance)/distance)

            self.speed = self.next_speed
                


    def update(self):
        self.pos+=self.next_speed
        self.speed = self.next_speed*friction


        
    def render(self, screen):
        #pygame.draw.circle(screen, self.color, [self.pos, 150], 3, 0)
        #return ["circle", [self.pos, 150], 3, 0]
        pygame.draw.aaline(screen, self.color, [self.pos, 140], [self.pos, 160], 2)
        return ["aaline", [self.pos, 140], [self.pos, 160], 2]
                



class DelaySwitch(object):
    
    def __init__(self, frame_rate):
        self.frame_rate = 1.0/(frame_rate/100.0) # should be in milliseconds
        self.time = 0
        self.prev_time = 0
        self.time_passed = 0
        self.skip = False
        
    def update(self):
        if self.skip==True:
            self.skip=False
            
        self.time=time.time()
        self.time_passed = self.time-self.prev_time
        
        if self.time_passed<self.frame_rate:
            time.sleep((self.frame_rate-self.time_passed)/100.0)
        else:
            self.skip=True
            
        self.prev_time = self.time
        
        








def render_machine(render_list,screen, bg_color):
    for rend_obj in render_list:
        if rend_obj[0]=="circle":
            pygame.draw.circle(screen, bg_color, rend_obj[1], rend_obj[2], rend_obj[3])
        elif rend_obj[0]=="line":
            pygame.draw.line(screen, bg_color, rend_obj[1], rend_obj[2], rend_obj[3])
        elif rend_obj[0]=="aaline":
            pygame.draw.line(screen, bg_color, rend_obj[1], rend_obj[2], 5)
        elif rend_obj[0]=="rect":
            pygame.draw.rect(screen, bg_color, rend_obj[1])
        else:
            raise "not a render format!"



def get_input():
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()



def draw_waves(wave_points, screen, type = "pos"):
    index = len(wave_points)-1

    points =[]

    while index!=-1:
        if type=="pos":
            distance = wave_points[index].pos-wave_points[index-1].pos-spreed
        elif type=="acc":
            distance = wave_points[index].speed-wave_points[index-1].speed-spreed
        height=(distance/float(tolerance))*50+50
        pos = index*spreed+nudge-(spreed/2)#(wave_points[index].pos+wave_points[index-1].pos)/2.0

        points.append([pos, height])

        index-=1


    index = len(wave_points)-2
    render_list=[]
    
    while index!=-0:
        if type=="pos":
            color = [0,0,255]
        elif type=="acc":
            color = [255,0,0]
        pygame.draw.aaline(screen, color, points[index], points[index-1], 2)
        render_list.append( ["aaline", points[index], points[index-1],2] )
        index-=1

    return render_list

    
        
            
        
    




############################################
############################################


def main():
    text = pygame.font.SysFont(pygame.font.get_default_font(), 18)
    
    size = (800,200)
    screen = pygame.display.set_mode(size)

    bg_color = [0,0,0]

    delay = DelaySwitch(60)

    
    
    global tolerance, speed, friction, nudge, spreed




    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    spreed = 5
    tolerance = 15 # how close do the dots have to be before they effect each other
    speed = 5 # natural frequency
    friction = 0.9975

    number = 155
    nudge = 15
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #




    points = []

    for x in xrange(number):
        color = [255,255,0]
        if x == number-1:
            print x
            points.append( LongWave_Point(  x*spreed+nudge, x, color, True) )
        elif x == 0:
            points.append( LongWave_Point(  x*spreed+nudge, x, color, True  ) )
        elif x == 1:
            points.append( LongWave_Point(  x*spreed+nudge, x, color, False, 0  ) )
        elif x == number-2:
            points.append( LongWave_Point(  x*spreed+nudge, x, color, False, 0) )
        else:
            points.append( LongWave_Point(  x*spreed+nudge, x, color, False  ) )
        


     #=#=#=#=#=#=#=#=#=#

    time.sleep(1)

    prev_press = False
    
    while True:
        if pygame.mouse.get_pressed()[0] and not prev_press:
            
            prev_press = True
            mouse_pos = pygame.mouse.get_pos()[0]
            
            left_point = points[1]
            right_point = points[1]
            
            for point in points:
                
                if point.pos<mouse_pos and point.pos>right_point.pos:
                    right_point = point

            if right_point.number!=0: left_point = points[right_point.number-1]

            if not right_point.is_end_point:  right_point.speed+=speed/2.0+0.00000001
            if not left_point.is_end_point:  left_point.speed-=speed/2.0+0.00000001
            
        elif not pygame.mouse.get_pressed()[0]:
            prev_press = False
                    
                
            
        render_objects=[]
        
        
        for point in points:
            point.prepare(points)
        for point in points:
            point.update()
            render_objects.append( point.render(screen) )
        
        for object in draw_waves(points, screen, "pos"):
            render_objects.append(object)

        for object in draw_waves(points, screen, "acc"):
            render_objects.append(object)

        
        delay.update()

        pygame.display.flip()
        render_machine(render_objects, screen, bg_color)

        get_input()
        
    #=#=#=#=#=#=#=#=#=#


if __name__ == "__main__":
    main()
    

        
