import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

is_running = True

a = 0
STEP = 0.05
clock = pygame.time.Clock()

b = 30

while is_running:

    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            is_running = False

    a += STEP
    #print(a)

    x = math.cos(a) * b
    y = math.sin(a) * b
    #y = math.sin(a) * 50 # try this for an elliptical orbit!

    print(x, y)

    #screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 0, 0,), (300 + x, 300 + y), 2)
    pygame.display.update()

pygame.quit()
quit()
