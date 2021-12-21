import tkinter #для нахождения разрешения экрана
import math
import pygame #для рендера модели
#для рандомизации входных данных
from random import randrange 
from random import random

#переводит градусы в радианы
def rad(angle):
    return angle * 0.01745329 

def coordinates(angle,move_x,move_y):
    
    #размеры блока 
    height=50
    width=100

    near_angle = rad(90) - angle #смежный угол в радианах

    #вычисление стартовой позиции
    xtl = math.sqrt(pow(math.tan(near_angle) * height,2) + pow(height,2)) #стартовая X позиция верхней левой точки (XTopLeft) 
    xtl_to_xtr = math.cos(angle) * width #расстояние от стартовой X позиции верхней левой точки до стартовой X позиции верхней правой точки (XTopLeft_to_XTopRight)
    ytr = math.sin(angle) * width #стартовая Y позиция верхней правой точки (YTopRight)
    xtl_to_xbl = math.sin(angle) * height #расстояние от стартовой X позиции верхней левой точки до стартовой X позиции нижней левой точки (XTopLeft_to_XBottomLeft)
    ybl = math.sqrt(pow(height,2) - pow(xtl_to_xbl,2)) #стартовая Y позиция нижней левой точки (YBottomLeft)
    
    #если мы двигаем модель вниз, то мы двигаем блок влево на хорошую позицию
    if (move_y >= 50):
        move_y -= 50
        move_x = math.tan(near_angle) * ybl * -1

    #[ax,ay,bx,by,cx,cy,dx,dy]
    output = [xtl+move_x, 0+move_y, xtl_to_xtr+xtl+move_x, ytr+move_y, xtl-xtl_to_xbl+move_x, ybl+move_y, xtl_to_xtr+xtl-xtl_to_xbl+move_x, ytr+ybl+move_y]
    return output

def draw_track(angle,distance,move_x,move_y):
    x_a = math.sqrt(pow(math.tan(rad(90)-angle) * 20,2) + pow(20,2)) - math.sin(angle) * 20
    y_a = math.sqrt(pow(20,2) - pow(math.sin(angle)*20,2))
    x_b = x_a - math.sin(angle)*20
    y_b = y_a * 2

    #если мы двигаем модель вниз, то мы двигаем штрихи влево на более удачную позицию
    if (move_y >= 20):
        move_y -= 20
        move_x = math.tan(rad(90)-angle) * y_a * -1

    #мы рисуем 100 штрихов с запасом на любой размер окна
    for i in range(-10,90):
        d_x = math.cos(angle)*(i*20 + distance)
        d_y = math.sin(angle)*(i*20 + distance)
        pygame.draw.line(screen,GREEN,[x_a+move_x+d_x,y_a+move_y+d_y],[x_b+move_x+d_x,y_b+move_y+d_y],5)
    
def draw_rect(angle,coords,distance):

    #вычисление сдвига
    displacement_x = math.cos(angle) * distance
    displacement_y = math.sin(angle) * distance

    a = [coords[0]+displacement_x,coords[1]+displacement_y]
    b = [coords[2]+displacement_x,coords[3]+displacement_y]
    c = [coords[4]+displacement_x,coords[5]+displacement_y]
    d = [coords[6]+displacement_x,coords[7]+displacement_y]

    #отрисовка
    pygame.draw.line(screen, RED, a, b, 5) 
    pygame.draw.line(screen, RED, a, c, 5) 
    pygame.draw.line(screen, RED, b, d, 5) 
    pygame.draw.line(screen, RED, c, d, 5)

    return displacement_x,displacement_y

def starting_input():
    randomize=bool(int(input("рандомизировать входные данные? введите 1 или 0\n")))
    if (randomize==True):
        angle=randrange(0,90)
        mass=randrange(0,9000)
        mu=random()
        speed0=randrange(0,100)
    else:
        angle=float(input("введите угол\n"))
        while (angle<0) or (angle>90):
            angle = float(input("пожалуйста, введите угол между 0 и 90 градусами\n"))
        mass = float(input("введите массу\n"))
        while (mass<0):
            mass = float(input("к сожалению, это не гелиевый шарик, пожалуйста введите массу хотя бы 0\n"))
        mu = float(input("введите коэффициент скольжения\n"))
        while (mu<0) or (mu>1):
            mu = float(input("эта величина не может быть меньше 0 или больше 1, попробуйте снова\n"))
        speed0 = float(input("введите начальную скорость\n"))
        while (speed0<0):
            speed0 = float(input("пожалуйста, введите скорость хотя бы 0\n"))

    print("ваши входные параметры:")
    print("угол =",angle)
    print("масса =",mass)
    print("коэф. скольжения =",mu)
    print("начальная скорость =",speed0)

    #переводим угол в радианы
    angle = rad(angle)

    #подправляем погрешность в вычислениях
    if(angle==rad(90)):
        force=0
        acceleration=9.8
    else:
        #вычисляем силу трения
        force = mu*mass*9.8*math.cos(angle)

        #вычисляем ускорение
        acceleration=9.8*(math.sin(angle)-mu*math.cos(angle))
    
    return speed0,angle,force,acceleration

def main():
    #вводим все переменные
    speed0,angle,force,acceleration = starting_input()

    #получае разрешение экрана
    root = tkinter.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    #вычисляем высоту и ширину окна
    #и высоту и ширину плоскости
    if (screen_width >= 1080): screen_width = 1080

    height = math.tan(angle) * screen_width
    if (height < 400):
        screen_height = 400
    elif (height > screen_height-100):
        screen_height -= 100
        height = screen_height
    else:
        screen_height = height

    #без этого он почему-то не отрисовывает плоскость
    if (angle==rad(0)):
        width=screen_width
    else:
        width = math.tan(rad(90) - angle) * height

    #вычисляем нужный сдвиг чтоб модель была в центре
    move_x=(screen_width - abs(width))/2
    #предотвращение сдвига вверх на крутых спусках
    move_y=0
    if(height < screen_height): move_y=(screen_height - height)/2

    #вычисляем стартовую позицию блока
    coords = coordinates(angle,move_x,move_y)

    #открываем окно
    pygame.init()
    print("открываем окно ",screen_width," x ",screen_height)
    global screen
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("сила трения")
    font = pygame.font.Font('Ubuntu.ttf', 30)#для вывода текста в окне

    #задаем необходимые цвета
    global BLACK,WHITE,GREEN,RED,BLUE
    BLACK = ( 0, 0, 0)
    WHITE = ( 255, 255, 255)
    GREEN = ( 0, 255, 0)
    RED = ( 255, 0, 0)
    BLUE = (0, 0, 255)

    #запускаем главный цикл отрисовки
    window_open = True
    render = True
    im_centered = False #доехал ли блок до центра окна
    clock = pygame.time.Clock()
    distance = 0 #пройденный путь
    time = 0 
    while window_open:
        for event in pygame.event.get():
            #крестик закрывает окно
            if event.type == pygame.QUIT:
                window_open = False
        
        while render:
            #дубликат того же цикла, чтоб крестик закрывал окно
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    window_open = False
                    render = False
            time+=1/60 #60 кардров в секунду
            speed=speed0 + acceleration*time
            if (speed<0): speed=0

            distance = speed0*time + (acceleration*math.pow(time,2))/2
            #оптическая иллюзия что штрихи движутся бесконечно влево хотя они время от времени возвращаются на исходную позицию
            track_distance = -1 * distance % 20

            screen.fill(WHITE)
            pygame.draw.line(screen, GREEN, [0+move_x, 0+move_y], [width+move_x, height+move_y], 5)
            
            #если блок не в центре, то...
            if (im_centered==False):
                #...двигаем блок
                draw_track(angle,0,move_x,move_y)
                d_x,d_y=draw_rect(angle,coords,distance)
                if (d_x>0.45*screen_width) or (d_y>0.45*screen_height):
                    im_centered=True
                    frozen_distance = distance #заморозка позиции блока на экране
            else:
                #иначе двигаем штрихи
                draw_track(angle,track_distance,move_x,move_y)
                d_x,d_y=draw_rect(angle,coords,frozen_distance)


            string_time="время:"+str(round(time,6))
            string_speed="скорость:"+str(round(speed,6))
            string_distance="расстояние:"+str(round(distance,6))
            string_force="сита трения:"+str(round(force,6))
            string_acceleration="ускорение:"+str(round(acceleration,6))

            screen.blit(font.render(string_time, True, BLUE),(screen_width-300,0))
            screen.blit(font.render(string_speed, True, BLUE),(screen_width-300,25))
            screen.blit(font.render(string_distance, True, BLUE),(screen_width-300,50))
            screen.blit(font.render(string_force, True, RED),(10,screen_height-65))
            screen.blit(font.render(string_acceleration, True, RED),(10,screen_height-40))

            if (speed<=0):
                screen.blit(font.render("ФИНИШ",True,BLACK),(10,screen_height-90))
                render = False

            pygame.display.flip()#отрсовка всего что сверху

        clock.tick(60)#60 кадров/сек
         
    pygame.quit()

main()
