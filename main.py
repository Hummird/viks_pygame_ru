import pygame
import math

#lol
def draw_rect():
    pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5) 
    pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5) 
    pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5) 
    pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5) 

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
    pygame.display.flip()

    clock.tick(60)
     
pygame.quit()
