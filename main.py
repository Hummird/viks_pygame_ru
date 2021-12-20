import pygame #for rendering an output
import math

def coordinates(angle):
    
    height=50
    width=100

    near_angle = 1.570796 - angle
    #calculate the starting pos
    xtl = math.sqrt(pow(math.tan(near_angle) * height,2) + pow(height,2)) #initial X pos of TOP LEFT point 
    xtl_to_xtr = math.cos(angle) * width #length from initial X pos of TOP LEFT point to initial X pos of TOP RIGHT point
    ytr = math.sin(angle) * width #initial Y pos of TOP RIGHT point
    xtl_to_xbl = math.sin(angle) * height #length from initial X pos of TOP LEFT point to initial X pos of BOTTOM LEFT point
    ybl = math.sqrt(pow(height,2) - pow(xtl_to_xbl,2)) #initial Y pos of BOTTOM LEFT point

    #[ax,ay,bx,by,cx,cy,dx,dy]
    return [xtl, 0, xtl_to_xtr+xtl, ytr, xtl-xtl_to_xbl, ybl, xtl_to_xtr+xtl-xtl_to_xbl, ytr+ybl]

def draw_rect(angle,coords,distance):

    #calculate the displacement
    displacement_x = math.cos(angle) * distance
    displacement_y = math.sin(angle) * distance

    a = [coords[0]+displacement_x,coords[1]+displacement_y]
    b = [coords[2]+displacement_x,coords[3]+displacement_y]
    c = [coords[4]+displacement_x,coords[5]+displacement_y]
    d = [coords[6]+displacement_x,coords[7]+displacement_y]

    #draw it out
    pygame.draw.line(screen, RED, a, b, 5) 
    pygame.draw.line(screen, RED, a, c, 5) 
    pygame.draw.line(screen, RED, b, d, 5) 
    pygame.draw.line(screen, RED, c, d, 5) 

def starting_input():
    angle = float(input("define angle\n"))
    mass = float(input("define mass\n"))
    mu = float(input("define how slippery\n"))
    speed0 = float(input("define initial velocity\n"))

    #convert degrees to radian
    angle = angle * 0.01745329 

    #calculate friction force
    force = mu*mass*9.8*math.cos(angle)

    #calculate the acceleration
    acceleration=9.8*(math.sin(angle)-mu*math.cos(angle))
    
    return speed0,angle,force,acceleration

def main():
    #input all of the variables
    speed0,angle,force,acceleration = starting_input()

    #calculate the initial coordinates of a rectangle
    coords = coordinates(angle)

    #opening a window
    pygame.init()
    
    width = 1080
    height = math.tan(angle) * width

    print("opening window ",width," x ",height)
    global screen
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("friction force")
    font = pygame.font.Font('Ubuntu.ttf', 30)

    # Define some colors
    global BLACK,WHITE,GREEN,RED,BLUE
    BLACK = ( 0, 0, 0)
    WHITE = ( 255, 255, 255)
    GREEN = ( 0, 255, 0)
    RED = ( 255, 0, 0)
    BLUE = (0, 0, 255)

    #starting the main render loop
    window_open = True
    render = True
    clock = pygame.time.Clock()
    distance = 0 #travel
    time = 0 
    while window_open:
        for event in pygame.event.get():
            #close button closes the window
            if event.type == pygame.QUIT:
                window_open = False

        
        while render:
            time+=1/60
            speed=speed0 + acceleration*time
            if (speed<0): speed=0

            distance = speed0*time + (acceleration*math.pow(time,2))/2

            screen.fill(WHITE)
            pygame.draw.line(screen, GREEN, [0, 0], [width, height], 5)
            draw_rect(angle,coords,distance)
            
            string_time="time:"+str(round(time,6))
            string_speed="speed:"+str(round(speed,6))
            string_force="force:"+str(round(force,6))
            string_acceleration="acceleration:"+str(round(acceleration,6))
            screen.blit(font.render(string_time, True, BLUE),(width-200,0))
            screen.blit(font.render(string_speed, True, BLUE),(width-200,25))
            screen.blit(font.render(string_force, True, RED),(10,height-65))
            screen.blit(font.render(string_acceleration, True, RED),(10,height-40))

            pygame.display.flip()

            if (speed<=0):
                print("finished")
                render = False

        clock.tick(60)
         
    pygame.quit()

main()
