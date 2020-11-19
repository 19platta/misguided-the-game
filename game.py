import pygame
import character
import environment

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_KP_ENTER,
)

class Game:


    def __init__(self):
        # 500 / 250 / 125 room height
        SCREEN_HEIGHT = 700  # 350 or 175
        SCREEN_WIDTH = 1080  # 540 or 270

        # Set up the drawing window
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        self.clock = pygame.time.Clock()

        self.room = environment.Room('innlobby')
        self.background = environment.Background('nightsky')

        self.player = character.Player('turtle2')
        self.npc = character.NPC('turtle')

    def intro(self):
        intro = pygame.image.load("Media/wallpaper/copepod-studios.png")
        for i in range(225):
            intro.set_alpha(i)
            self.screen.blit(intro, [265, 200])
            pygame.display.flip()
            self.clock.tick(50)
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    return
            self.clock.tick(30)

    def update(self):
        self.background.update(self.screen)
        self.room.update(self.screen)
        self.player.update(self.screen)
        self.npc.update(self.screen)

    def run(self):
        self.intro()
        running = True
        self.npc.move(500, 500)
        self.player.spawn(self.room)

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
            if self.player.collide(self.npc):
                self.npc.say('Ow!!')

            self.player.move(pygame.key.get_pressed())
            self.update()
            # room.draw_objects(screen)
            pygame.display.flip()
            self.screen.fill((0, 0, 0))

            self.clock.tick(30)
        # Done! Time to quit.
        pygame.quit()

