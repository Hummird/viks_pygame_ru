import pygame
import math

def coordinates(angle):
    
    height=50
    width=100

    #calculate the starting pos
    near_angle = 90 - angle

    xtl = math.sqrt(pow(math.tan(near_angle*0.01745329) * height,2) + pow(height,2)) #initial X pos of TOP LEFT point 
    xtl_to_xtr = math.cos(angle*0.01745329) * width #length from initial X pos of TOP LEFT point to initial X pos of TOP RIGHT point
    ytr = math.sin(angle*0.01745329) * width #initial Y pos of TOP RIGHT point
    xtl_to_xbl = math.sin(angle*0.01745329) * height #length from initial X pos of TOP LEFT point to initial X pos of BOTTOM LEFT point
    ybl = math.sqrt(pow(height,2) - pow(xtl_to_xbl,2)) #initial Y pos of BOTTOM LEFT point

    #[ax,ay,bx,by,cx,cy,dx,dy]
    return [xtl, 0, xtl_to_xtr+xtl, ytr, xtl-xtl_to_xbl, ybl, xtl_to_xtr+xtl-xtl_to_xbl, ytr+ybl]


def draw_rect(coords):

   # displacement_x=
    #displacement_y=

    a = [coords[0],coords[1]]
    b = [coords[2],coords[3]]
    c = [coords[4],coords[5]]
    d = [coords[6],coords[7]]

    #draw it out
    pygame.draw.line(screen, RED, a, b, 5) 
    pygame.draw.line(screen, RED, a, c, 5) 
    pygame.draw.line(screen, RED, b, d, 5) 
    pygame.draw.line(screen, RED, c, d, 5) 

def starting_input():
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

def main():
    #input all of the variables
    angle,force = starting_input()

    #calculate the initial coordinates of a rectangle
    coords = coordinates(angle)

    #opening a window
    pygame.init()
    width = 720
    height = math.tan(angle*0.01745329) * width

    print("opening window ",width," x ",height)
    global screen
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("friction force")

    # Define some colors
    global BLACK,WHITE,GREEN,RED,BLUE
    BLACK = ( 0, 0, 0)
    WHITE = ( 255, 255, 255)
    GREEN = ( 0, 255, 0)
    RED = ( 255, 0, 0)
    BLUE = (0, 0, 255)

    #starting the main render loop
    carryOn = True
    clock = pygame.time.Clock()
    while carryOn:

        for event in pygame.event.get():
            #close button closes the window
            if event.type == pygame.QUIT:
                carryOn = False
        
        screen.fill(WHITE)
        pygame.draw.line(screen, GREEN, [0, 0], [width, height], 5)
        draw_rect(coords)

        pygame.display.flip()
        clock.tick(60)
         
    pygame.quit()

main()
