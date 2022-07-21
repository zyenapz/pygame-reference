import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

is_running = True
clock = pygame.time.Clock()
FPS = 60

class Actor:
    def __init__(self, x, y, color, other):
        self.pos = pygame.Vector2(x, y)
        self.color = color
        self.other = other

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, 10)

        if self.other != None:
            pygame.draw.line(screen, "white", self.pos, self.other.pos)

treasure = Actor(50, 50, "yellow", None)
bob = Actor(300, 100, "red", treasure)
carol = Actor(100, 200, "green", bob)

while is_running:

    clock.tick(FPS)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            is_running = False

    mp = pygame.mouse.get_pos()
    mp = pygame.Vector2(mp[0], mp[1])
    kp = pygame.key.get_pressed()

    treasure.pos = mp

    if kp[pygame.K_w]:
        carol.pos.y -= 5
    if kp[pygame.K_s]:
        carol.pos.y += 5
    if kp[pygame.K_a]:
        carol.pos.x -= 5
    if kp[pygame.K_d]:
        carol.pos.x += 5

    screen.fill((10, 10, 10))

    #print((bob.pos + treasure.pos).normalize(), bob.pos, treasure.pos)
    #print((bob.pos + carol.pos).normalize())

    bt = (bob.pos - treasure.pos).normalize() # bob-treasure vector
    bc = (bob.pos - carol.pos).normalize() # bob-carol vector

    print(f"Dot product is: {round(bt.dot(bc), 3)}")
    
    bob.draw(screen)
    carol.draw(screen)
    treasure.draw(screen)
    
    pygame.display.update()

pygame.quit()
quit()
