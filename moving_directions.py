import pygame
pygame.init()


screen = pygame.display.set_mode((831,831),0,32)

clock = pygame.time.Clock()

done = False

count=0

# picture load
background = pygame.image.load('images/GAME.jpg').convert()

PFORWARD = pygame.image.load('images/PFORWARD.png')
PFORWARD = pygame.transform.scale2x(PFORWARD)

PDOWNWARD = pygame.image.load('images/PDOWNWARD.png')
PDOWNWARD = pygame.transform.scale2x(PDOWNWARD)

PLEFT = pygame.image.load('images/PLEFT.png')
PLEFT = pygame.transform.scale2x(PLEFT)

PRIGHT =pygame.image.load('images/PRIGHT.png')
PRIGHT = pygame.transform.scale2x(PRIGHT)

x = 0
y = 0

while not done:
    image = PDOWNWARD or PFORWARD or PRIGHT or PLEFT

    delta_time = clock.tick()
    keys = pygame.key.get_pressed()
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    dy = 0
    dx = 0


    if keys[pygame.K_w]:
        dy -= 1*delta_time/2
        image=PFORWARD

    if keys[pygame.K_a]:
        dx -= 1*delta_time/2
        count += 1
        image=PLEFT


    if keys[pygame.K_s]:
        dy += 1*delta_time/2
        count += 1
        image = PDOWNWARD


    if keys[pygame.K_d]:
        dx += 1*delta_time/2
        count += 1
        image = PRIGHT



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
