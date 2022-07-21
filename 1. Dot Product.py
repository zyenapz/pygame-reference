# Dot Product reference
# By zyenapz
# Tested on pygame version 2.1.2, Python version 3.9.7

import pygame
import math
from PIL import Image, ImageDraw

# Game variables
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dot Product Demonstration")
is_running = True
clock = pygame.time.Clock()
FPS = 60
my_font = pygame.font.SysFont('Comic Sans MS', 16)

# Actor class


class Actor:

    def __init__(self, x, y, color, other, radius=10):
        self.pos = pygame.Vector2(x, y)
        self.color = color
        self.other = other
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

        if self.other != None:
            pygame.draw.line(screen, "white", self.pos, self.other.pos)

# Some maths


def normalize(val, mincap, maxcap):
    return (val - mincap) / (maxcap - mincap)


def calc_conesize(nt, a):
    # nt - normalized visibility threshold
    # a - alpha (the higher it is, the larger the cone is)
    return ((360 - (nt * 360)) / 2) + (nt * a)


def clip(val, mincap, maxcap):
    if val < mincap:
        return mincap
    elif val > maxcap:
        return maxcap

    return val


# Visibility constants
VISIBLE_THRESHOLD = 0.7
VISIBLE_DISTANCE = 120

# This is an arbitrary number, play around with it!
# The higher it is, the larger the cone is ...
# ... This has the consequence of the cone appearing "larger" than the actual threshold
CONE_ALPHA = 18

# Create actors
cursor = Actor(50, 50, "yellow", None, 5)
alice = Actor(300, 200, "green", None)
# Bob's viewing direction is towards the cursor's position
bob = Actor(300, 150, "red", cursor)

while is_running:

    clock.tick(FPS)

    # Get input -----------------------------------------------
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            is_running = False

        # Keyboard input
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_F1:
                VISIBLE_THRESHOLD += 0.1
                VISIBLE_THRESHOLD = clip(VISIBLE_THRESHOLD, -1, 1)
            elif e.key == pygame.K_F2:
                VISIBLE_THRESHOLD -= 0.1
                VISIBLE_THRESHOLD = clip(VISIBLE_THRESHOLD, -1, 1)

    # Keyboard input...again
    kp = pygame.key.get_pressed()

    if kp[pygame.K_w]:
        bob.pos.y -= 1
    if kp[pygame.K_s]:
        bob.pos.y += 1
    if kp[pygame.K_a]:
        bob.pos.x -= 1
    if kp[pygame.K_d]:
        bob.pos.x += 1

    # Mouse input
    m_pos = pygame.mouse.get_pos()
    m_pos = pygame.Vector2(m_pos[0], m_pos[1])

    # Update -----------------------------------------------
    try:  # Lazy fix for calculating dot product using 0
        cursor.pos = m_pos
        bob_cursor = (bob.pos - cursor.pos).normalize()  # bob-cursor vector
        bob_alice = (bob.pos - alice.pos).normalize()  # bob-alice vector
        dot_product = bob_cursor.dot(bob_alice)
        dist_bob_alice = bob.pos.distance_to(alice.pos)
    except:
        pass

    # Calculate angle of bob's position with respect to the cursor's position
    rel_y = cursor.pos.y - bob.pos.y
    rel_x = cursor.pos.x - bob.pos.x
    radians = math.atan2(rel_y, rel_x)
    degrees = (radians / math.pi) * 180

    # Draw -----------------------------------------------

    screen.fill("black")

    # Draw view cone
    size = VISIBLE_DISTANCE * 2
    viewcone = Image.new("RGBA", (size, size))
    cone_size = calc_conesize(
        normalize(VISIBLE_THRESHOLD, -1, 1), CONE_ALPHA)
    # PIL pie slices starts from 3 o'clock, and goes clockwise
    start = degrees - cone_size
    end = degrees + cone_size
    ImageDraw.Draw(viewcone).pieslice(
        (0, 0, size-1, size-1), start, end, fill="gray")

    # Convert PIL image to pygame image
    viewcone_img = pygame.image.fromstring(
        viewcone.tobytes(), viewcone.size, viewcone.mode)
    viewcone_rect = viewcone_img.get_rect(center=bob.pos)

    # Draw objects
    screen.blit(viewcone_img, viewcone_rect)
    bob.draw(screen)
    alice.draw(screen)
    cursor.draw(screen)

    # Draw texts
    dot_text = my_font.render(
        f"Dot: {round(dot_product, 3)}, THRESH: {round(VISIBLE_THRESHOLD, 3)}, a = {CONE_ALPHA}", False, "white")
    dist_text = my_font.render(
        f"Distance (Bob-Alice): {round(dist_bob_alice, 3)}", False, "white")
    instr1_text = my_font.render(f"WASD = move Bob", False, "cyan")
    instr2_text = my_font.render(
        f"F1/F2 = +/- threshold", False, "cyan")

    alice_text = my_font.render(f"Alice", False, "green")
    bob_text = my_font.render(f"Bob", False, "red")

    title_text = my_font.render(f"Dot Product Demo", False, "green")

    screen.blit(dot_text, (300, 300))
    screen.blit(dist_text, (300, 330))
    screen.blit(instr1_text, (300, 400))
    screen.blit(instr2_text, (300, 430))
    screen.blit(alice_text, alice.pos)
    screen.blit(bob_text, bob.pos)
    screen.blit(title_text, (0, 0))

    if dot_product > VISIBLE_THRESHOLD and dist_bob_alice < VISIBLE_DISTANCE:
        warn_text = my_font.render("Bob sees Alice !", False, "green")
        screen.blit(warn_text, (300, 500))
    else:
        warn_text = my_font.render(
            "Bob does not see Alice !", False, "red")
        screen.blit(warn_text, (300, 500))

    pygame.display.update()

pygame.quit()
quit()
