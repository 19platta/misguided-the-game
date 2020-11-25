import pygame
import character
import environment
import os

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_KP_ENTER,
)


class Game:

    def __init__(self):
        # 500 / 250 / 125 room height
        SCREEN_HEIGHT = 700  # 350 or 175 or 88
        SCREEN_WIDTH = 1080  # 540 or 270 or 135

        # Set up the drawing window
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        self.clock = pygame.time.Clock()

        self.room = environment.Room('innlobby')
        self.background = environment.Background('nightsky')

        self.player = character.Player('turtle2')
        self.npc = character.NPC('turtle')

    def intro(self):
        #pygame.mixer.music.load('Media/music/Theme_Fast.mp3')
        #pygame.mixer.music.play()
        intro = pygame.image.load("Media/wallpaper/copepod-studios.png")
        credit = True
        for i in range(225):
            intro.set_alpha(i)
            self.screen.blit(intro, [265, 200])
            pygame.display.flip()
            self.clock.tick(35)
        self.clock.tick(60)
        filelist = os.listdir('Media/wallpaper/introsequence')
        for file in filelist:
            intro = pygame.image.load('Media/wallpaper/introsequence/'+file)
            self.screen.blit(intro, [0, 0])
            pygame.display.flip()
            self.clock.tick(6)
        pygame.event.clear()
        while credit == True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    credit = False
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
            #self.room.draw_objects(self.screen)
            pygame.display.flip()
            self.screen.fill((0, 0, 0))

            self.clock.tick(30)
        # Done! Time to quit.
        pygame.quit()

