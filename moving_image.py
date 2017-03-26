import time,pygame
from pygame.locals import *
from datetime import datetime, date, time
pygame.init()

'''
__author__ = {'name' : 'SCOTT',
               'mail' : 'coreblade@163.com',
               'wechat' : 'ATK_777',
               'QQ'   : '2420904447',
              'Version' : '1.0.BETA'}
'''

screen = pygame.display.set_mode((831,831),0,32)

clock = pygame.time.Clock()

pygame.display.set_caption("SCP-701")

done = False

full_screen = False

count=0

# picture load
background = pygame.image.load('GAME.jpg').convert()

PFORWARD = pygame.image.load('PFORWARD.png')
PFORWARD = pygame.transform.scale2x(PFORWARD)

PDOWNWARD = pygame.image.load('PDOWNWARD.png')
PDOWNWARD = pygame.transform.scale2x(PDOWNWARD)

PLEFT = pygame.image.load('PLEFT.png')
PLEFT = pygame.transform.scale2x(PLEFT)

PRIGHT =pygame.image.load('PRIGHT.png')
PRIGHT = pygame.transform.scale2x(PRIGHT)

RIGHTDICK = pygame.image.load('RIGHTDICK.png')
LEFTDICK = pygame.image.load('LEFTDICK.png')

mouse_cursor = pygame.image.load('H1.png').convert_alpha()

# Player Moving
def DICKMOVING(image1,image2,count):
    if 10 < count%20 <= 20:
        return image2
    else:
        return image1

def print_text(font, x, y, text, color=(255,255,255)):
      imgText = font.render(text, True, color)
      screen.blit(imgText, (x,y))
font3 = pygame.font.Font(None, 34)
white = 255,255,255




x = 400
y = 400
battery = 20


while not done:

    delta_time = clock.tick()
    keys = pygame.key.get_pressed()
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    dy = 0
    dx = 0
    image = DICKMOVING(RIGHTDICK,LEFTDICK,count)

    if keys[pygame.K_w]:
        dy -= 1*delta_time/2
        count += 1
        image = DICKMOVING(RIGHTDICK,LEFTDICK,count)


    if keys[pygame.K_a]:
        dx -= 1*delta_time/2
        count += 1
        image = DICKMOVING(RIGHTDICK, LEFTDICK, count)

    if keys[pygame.K_s]:
        dy += 1*delta_time/2
        count += 1
        image = DICKMOVING(RIGHTDICK, LEFTDICK, count)

    if keys[pygame.K_d]:
        dx += 1*delta_time/2
        count += 1
        image = DICKMOVING(RIGHTDICK, LEFTDICK, count)

    if pygame.event.get() == KEYDOWN:
        if event.key == K_t:
            battery = battery-1

    today = datetime.today()
    print_text(font3, 500, 0, "Battery: " + str(battery))

    # x1, y1 = pygame.mouse.get_pos()
    # x1 -= mouse_cursor.get_width() / 2
    # y1 -= mouse_cursor.get_height() / 2
    # print(x1,y1)
    if keys[pygame.K_f]:
        full_screen = not full_screen
        if full_screen:
            print('Open the Fullscreen model!')
        else:
            print('Open the Default model!')
        if full_screen:
            screen = pygame.display.set_mode((831,831), FULLSCREEN, 32)
        else:
            screen = pygame.display.set_mode((831,831),0,32)

    x+=dx
    y+=dy

    screen.blit(image, (x, y))
    if x < 0 or x > (831 - image.get_width()):
        x-=dx

    if y < 0 or y > (831 - image.get_height()):
        y-=dy

    # Lock down data


    screenrate = clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.update()

pygame.quit()
