
import pygame
import player
import room

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
white = (255, 255, 255)

pygame.init()

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1080

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

player = player.Player()

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Im Sorry', True, white)
textRect = text.get_rect()
textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Run until the user asks to quit
running = True

while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    player.move(pygame.key.get_pressed(), SCREEN_HEIGHT, SCREEN_WIDTH)
    screen.blit(text, textRect)
    player.update(screen)
    pygame.display.flip()
    screen.fill((0, 0, 0))

    clock.tick(30)
# Done! Time to quit.
pygame.quit()