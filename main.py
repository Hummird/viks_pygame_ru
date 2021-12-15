import pygame
import math

#lol
def draw_rect(angle):
    height=50
    width=100

    #calculate the starting pos
    new_angle = 90- angle

    hypo = math.sqrt(pow(math.tan(new_angle*0.01745329) * height,2) + pow(height,2))
    side1 = math.cos(angle*0.01745329) * width
    side2 = math.sin(angle*0.01745329) * width
    side3 = math.sin(angle*0.01745329) * height
    side4 = math.sqrt(pow(height,2) - pow(side3,2))

    #a = [ax+c,ay+c]
    #...
    i=side2*2
    j=hypo*2
    a = [hypo+j,0+i]
    b = [side1+hypo+j,side2+i]
    c = [hypo-side3+j,side4+i]
    d = [side1+hypo-side3+j,side2+side4+i]

    #draw it out
    pygame.draw.line(screen, RED, a, b, 5) 
    pygame.draw.line(screen, RED, a, c, 5) 
    pygame.draw.line(screen, RED, b, d, 5) 
    pygame.draw.line(screen, RED, c, d, 5) 

def force():
    print("define angle")
    angle = int(input())
    print("define mass")
    mass = int(input())
    print("define how slippery")
    mu = int(input())
    print("define initial velocity")
    speed = int(input())

    force = mu*mass*9.8*math.cos(angle)
    print(force)
    return angle,force

angle,force = force()
#opening a window
pygame.init()
width = 720
height = math.tan(angle*0.01745329) * width
print(height)
size=(width,height)
screen= pygame.display.set_mode(size)
pygame.display.set_caption("ajhla")

# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)

carryOn = True
clock = pygame.time.Clock()
 
while carryOn:
    screen.fill(WHITE)
    pygame.draw.line(screen, GREEN, [0, 0], [width, height], 5)
    draw_rect(angle)
    pygame.display.flip()

    clock.tick(60)
     
pygame.quit()
