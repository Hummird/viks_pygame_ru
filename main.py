import tkinter #for getting screen resolution
import pygame #for rendering an output
import math

#converts any angle to rad
def rad(angle):
    return angle * 0.01745329 

def coordinates(angle,move_x,move_y):
    
    #block dimentions 
    height=50
    width=100

    near_angle = rad(90) - angle #adjacent angle in rad

    #calculate the starting pos
    xtl = math.sqrt(pow(math.tan(near_angle) * height,2) + pow(height,2)) #initial X pos of TOP LEFT point 
    xtl_to_xtr = math.cos(angle) * width #length from initial X pos of TOP LEFT point to initial X pos of TOP RIGHT point
    ytr = math.sin(angle) * width #initial Y pos of TOP RIGHT point
    xtl_to_xbl = math.sin(angle) * height #length from initial X pos of TOP LEFT point to initial X pos of BOTTOM LEFT point
    ybl = math.sqrt(pow(height,2) - pow(xtl_to_xbl,2)) #initial Y pos of BOTTOM LEFT point
    
    #if we move down tne we move the block back to a good position
    if (move_y >= 50):
        move_y -= 50
        move_x = math.tan(near_angle) * ybl * -1

    #[ax,ay,bx,by,cx,cy,dx,dy]
    output = [xtl+move_x, 0+move_y, xtl_to_xtr+xtl+move_x, ytr+move_y, xtl-xtl_to_xbl+move_x, ybl+move_y, xtl_to_xtr+xtl-xtl_to_xbl+move_x, ytr+ybl+move_y]
    print(output)
    return output

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
    angle = rad(angle)

    if (angle > rad(90)):
        force = 0
        acceleration = 9.8
    else:
        #calculate friction force
        force = mu*mass*9.8*math.cos(angle)

        #calculate the acceleration
        acceleration=9.8*(math.sin(angle)-mu*math.cos(angle))
    
    return speed0,angle,force,acceleration

def main():
    #input all of the variables
    speed0,angle,force,acceleration = starting_input()

    #getting screen resolution
    root = tkinter.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    #calculating width and height of a window
    #and width and heigth of a track
    if (screen_width >= 1080): screen_width = 1080

    height = math.tan(angle) * screen_width
    if (height < 600):
        screen_height = 600
    elif (height > screen_height-100):
        screen_height -= 100
        height = screen_height
    else:
        screen_height = height

    #w/o it the line won't draw out for some reason
    if (angle==rad(0)):
        width=screen_width
    else:
        width = math.tan(1.570796 - angle) * height


    #calculating needed x and y displacement for a center aligned track
    move_x=(screen_width - abs(width))/2
    #prevents it from moving up in case of extreme angles
    move_y=0
    if(height < screen_height):
        move_y=(screen_height - height)/2

    #calculate the initial coordinates of a rectangle
    coords = coordinates(angle,move_x,move_y)

    #opening a window
    pygame.init()
    print("opening window ",screen_width," x ",screen_height)
    global screen
    screen = pygame.display.set_mode((screen_width,screen_height))
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
            #duplicate the same loop here or  else the close button breaks
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    window_open = False
                    render = False
            time+=1/60
            speed=speed0 + acceleration*time
            if (speed<0): speed=0

            distance = speed0*time + (acceleration*math.pow(time,2))/2

            screen.fill(WHITE)
            pygame.draw.line(screen, GREEN, [0+move_x, 0+move_y], [width+move_x, height+move_y], 5)
            draw_rect(angle,coords,distance)
            
            string_time="time:"+str(round(time,6))
            string_speed="speed:"+str(round(speed,6))
            string_force="force:"+str(round(force,6))
            string_acceleration="acceleration:"+str(round(acceleration,6))
            screen.blit(font.render(string_time, True, BLUE),(screen_width-200,0))
            screen.blit(font.render(string_speed, True, BLUE),(screen_width-200,25))
            screen.blit(font.render(string_force, True, RED),(10,screen_height-65))
            screen.blit(font.render(string_acceleration, True, RED),(10,screen_height-40))

            pygame.display.flip()

            if (speed<=0):
                print("finished")
                render = False

        clock.tick(60)
         
    pygame.quit()

main()
