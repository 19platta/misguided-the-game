
import pygame
import player
import environment

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
white = (255, 255, 255)

pygame.init()

# 500 / 250 / 125 room height
SCREEN_HEIGHT = 700 #350 or 175
SCREEN_WIDTH = 1080 #540 or 270

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


room = environment.Room('innlobby')
player = player.Player(room)
player.spawn(room)
background = environment.Background('daysky')
clock = pygame.time.Clock()

#room1 = room.Room('room1')

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


    background.update(screen)
    room.update(screen)
    player.move(pygame.key.get_pressed())
    player.update(screen)
    pygame.display.flip()
    screen.fill((0, 0, 0))

    clock.tick(30)
# Done! Time to quit.
pygame.quit()