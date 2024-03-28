import pygame, sys
mainClock = pygame.time.Clock()
from pygame.locals import *
import time, ctypes
from random import *
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (107, 153, 195)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
ORANGE = (255, 145, 0)
RED = (255, 0, 0)

WIDTH = 1280  # ширина экрана
HEIGHT = 720  # высота экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.display.set_mode((1280, 720),0,32)


icon = pygame.image.load('Objects/flyicon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Airplane Routes",("icon.png"))


font = pygame.font.SysFont(None, 20)


pos=0
circle_Color = (0, 255, 0)





def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    image = pygame.image.load('Objects/holl_nobut.png').convert_alpha()
    screen.blit(image, (1, 1))

click = False



def main_menu():
    while True:

        screen.fill((0,0,0))
        draw_text('_', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        game_but = pygame.Rect(500, 220, 330, 90)
        rules_but = pygame.Rect(500, 350, 330, 90)
        save_but = pygame.Rect(500, 490, 330, 90)

        Play = pygame.font.Font(None, 64)
        text_P = Play.render('Играть', True, (255, 255, 255))
        Rules = pygame.font.SysFont(None, 64)
        text_R = Rules.render("Правила", False, (255, 255, 255))
        Save = pygame.font.SysFont(None, 64)
        text_S = Save.render("Сохранения", False, (255, 255, 255))


        pygame.draw.rect(screen, LIGHT_BLUE, game_but)
        pygame.draw.rect(screen, LIGHT_BLUE, rules_but)
        pygame.draw.rect(screen, LIGHT_BLUE, save_but)

        screen.blit(text_P, (598, 243))
        screen.blit(text_R, (575, 370))
        screen.blit(text_S, (535, 512))



        if game_but.collidepoint((mx, my)):
            if click:
                game(circle_Color, pos)
        if rules_but.collidepoint((mx, my)):
            if click:
                rules()
        if save_but.collidepoint((mx, my)):
            if click:
                save()



        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)



def game(circle_Color, pos):

    image = pygame.image.load('Objects/field.png').convert_alpha()
    screen.blit(image, (0, 0))
    dots=[]
    class point():
        def __init__(self,field):
            self.coords=field.pop(randint(0, len(field)-1))
            dots.append((self.coords[0]*80,self.coords[1]*80))

    def r(field):
        return point(field)


    field=[(3,7),(5,8),(7,5),(10,4),(7,8),(9,6),(11,7),(13,6),(15,4),(1,3),(2,1),(4,2),(7,1),(10,2)]


    #-------------------------------------------------------------------------------
    clock = pygame.time.Clock()
    C=[]
    planes=[]
    lines=[]
    running=True
    t_start=time.localtime()
    b=r(field)
    pygame.draw.circle(screen, circle_Color, (b.coords[0]*80, b.coords[1]*80), 13, 2)
    while running:
        clock.tick(60)

        if len(field)==0:
            time.sleep(2)
            running=False
            pygame.quit()

        for i in dots:
            pos += 1
            if pos <= 10:
                circle_Color = GREEN
            elif pos <= 20:
                circle_Color = ORANGE
            elif pos <= 30:
                circle_Color =  RED
            elif pos == 35:
                pass


        t_now=time.localtime()
        if (t_now.tm_sec - t_start.tm_sec) % 10 == 0:
            b=r(field)
            pygame.draw.circle(screen, circle_Color, (b.coords[0]*80, b.coords[1]*80), 13, 2)
            time.sleep(1)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running=False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print(event.pos)
                for i in dots:
                    if ((i[0]-10 <= event.pos[0] and i[0]+10 >= event.pos[0]) and (i[1]-10 <= event.pos[1] and i[1]+10 >= event.pos[1])):
                        C.append((i[0], i[1]))
                        print(C)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: #добавляем линии
                for i in range(1,len(C)):
                    pygame.draw.aaline(screen, PINK, C[i-1], C[i], 2)
                    planes.append({'start': pygame.Rect(C[i-1][0]-10, C[i-1][1]-10, 20, 20), 'end': pygame.Rect(C[i][0]-10, C[i][1]-10, 20, 20)})
                    lines.append({'start': (C[i-1][0], C[i-1][1]), 'end': (C[i][0], C[i][1])})
                    pygame.draw.rect(screen, YELLOW, (C[i-1][0]-10, C[i-1][1]-10, 20, 20), 0)
                    C.clear()

            elif event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    C.clear()

        screen.blit(image, (0, 0))
        for j in dots:
            pygame.draw.circle(screen, circle_Color, (j[0], j[1]), 13, 2)
        for j in lines:
            pygame.draw.aaline(screen, PINK, j['start'], j['end'], 2)

        for i in range(len(planes)):
            planes[i]['start'].move_ip((planes[i]['end'][0]-planes[i]['start'][0])/13 ,(planes[i]['end'][1]-planes[i]['start'][1])/13)
            pygame.draw.rect(screen, YELLOW, planes[i]['start'] ,0)

        pygame.display.update()
        mainClock.tick(60)


def rules():
    rules = pygame.image.load('Objects/rules.png').convert_alpha()
    screen.blit(rules, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)




def save():
    save = pygame.image.load('Objects/save.png').convert_alpha()
    screen.blit(save, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)
main_menu()
