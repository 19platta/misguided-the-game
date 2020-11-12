
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

pygame.init()

SCREEN_HEIGHT = 960
SCREEN_WIDTH = 1280

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

player = player.Player()

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
    player.update(screen)
    pygame.display.flip()
    screen.fill((0, 0, 0))
# Done! Time to quit.
pygame.quit()