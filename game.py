import pygame
import character
import environment
import os
import interactables

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Game:
    """
    Class representing the Game state, controlling the interactions between
    the other classes, and running the game.

    Attributes:
        screen:
        clock:
        rooms: a list of all the room instances in the game
        current_room: the room the player is currently in
        backgrounds: a list of all the background instances in the game
        current_background: the background currently being displayed
        player: player controlled character, instance of the Player class
        guide: starts as None, becomes instance of Guide at appropriate
            point in the story

    """
    def __init__(self):
        """
        Initialize an instance of the Game class.
        """
        # 500 / 250 / 125 room height
        SCREEN_HEIGHT = 700  # 350 or 175 or 88
        SCREEN_WIDTH = 1080  # 540 or 270 or 135

        # Set up the drawing window
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.key.set_repeat(100, 100)

        self.clock = pygame.time.Clock()
        self.rooms = [
            environment.Room('lightforestentrance'),
            environment.Room('lightforest1'),
            environment.Room('lightforest2'),
            environment.Room('darkforestcampfire'),
            environment.Room('darkforest1'),
            environment.Room('maze'),
            environment.Room('innoutside'),
            environment.Room('innlobby')
        ]
        self.current_room = self.rooms[6]
        self.backgrounds = [
            environment.Background('daysky'),
            environment.Background('nightsky'),
            environment.Background('twilightsky')
        ]
        self.current_background = self.backgrounds[0]

        self.player = character.Player('player')

        self.guide = environment.Guide() #None

        self.conversations = []

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
        filelist = sorted(os.listdir('Media/wallpaper/introsequence'))
        for file in filelist:
            intro = pygame.image.load('Media/wallpaper/introsequence/'+file)
            self.screen.blit(intro, [0, 0])
            pygame.display.flip()
            self.clock.tick(6)
        pygame.event.clear()
        while credit is True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    credit = False
            self.clock.tick(30)

    def update(self):
        """
        Update all game components
        """
        self.current_background.update(self.screen)
        self.current_room.update(self.screen, self.player)
        #self.npc.update(self.screen)
        self.player.update(self.screen)
        if self.guide != None:
            self.guide.update(self.screen, self.player)

    def run(self):
        """
        Run the game.

        This function contains the main game loop and game logic. It will run
        the game until it is over or the player quits the game.
        """
        #self.intro()
        running = True

        self.player.spawn(self.current_room, 'maze')

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
            #if self.player.collide(self.npc):
                #self.npc.say('Ow!!')
            if self.room_manager() and (self.player.is_exiting() is not None):
                rooms = self.player.is_exiting()
                self.current_room = [room for room in self.rooms if room.get_name() == rooms[0]][0]
                self.player.spawn(self.current_room, rooms[1])

            self.player.move(pygame.key.get_pressed())
            self.update()
            # This line is for debugging boundaries
            #self.current_room.draw_objects(self.screen)
            #self.player.draw_rect(self.screen)
            pygame.display.flip()
            self.screen.fill((0, 0, 0))

            self.clock.tick(30)
        # Done! Time to quit.
        pygame.quit()

    def conversation(self, p1, p2):
        """
        Have a conversation between two characters where neither interrupts
        the other.

        Assumes that self.conversations has been set to contain the lines the
        characters will say, beginning with p1's first line.

        Args:
            p1: the first character to speak
            p2: the second character to speak
        """
        # Check to see if there is anything to say
        if len(self.conversations) > 0:
            # Make sure the characters don't talk over each other
            if not p2.is_speaking() and not p1.is_speaking():
                if len(self.conversations) % 2 == 1:
                    p1.say_once(self.conversations[0])
                    del self.conversations[0]
                else:
                    p2.say_once(self.conversations[0])
                    del self.conversations[0]
            return True
        else:
            return False

    def room_manager(self):
        """
        Run the correct room function based on which room the character is in.

        """
        if self.current_room == self.rooms[0]:
            return self.room0()
        elif self.current_room == self.rooms[1]:
            return self.room1()
        elif self.current_room == self.rooms[2]:
            return self.room2()
        elif self.current_room == self.rooms[3]:
            return self.room3()
        elif self.current_room == self.rooms[4]:
            return self.room4()
        elif self.current_room == self.rooms[5]:
            return self.room5()
        elif self.current_room == self.rooms[6]:
            return self.room6()

    def room0(self):
        """
        First room of the game.

        In this room the player meets the tutorial NPC who tells them how to
        interact with objects.

        Returns:
            True if the NPC has finished talking and the room is clear, False
                otherwise
        """
        tutorial_man = self.current_room.npcs[0]
        if (self.player.get_pos()[0] > 200 or tutorial_man.get_pos()[0] < 1090) and tutorial_man.get_pos()[0] > 500:
            tutorial_man.move('left')
            tutorial_man.say_once('Don\'t go into that forest, it\'s big and spooky!')
        if self.player.get_pos()[0] > 600 and tutorial_man.get_pos()[0] <= 500 and tutorial_man.is_speaking() == False:
            tutorial_man.say_once('If you must go into the forest, at least take this advice: if you'
                                  ' see anything that highlights in yellow, you can'
                                  ' interact with it by pressing spacebar')
        if tutorial_man.is_speaking() is False and self.player.collide(tutorial_man):
            tutorial_man.say('if you see anything that highlights in yellow, you can'
                             ' interact with it by pressing spacebar')
        if self.current_room.is_clear() and tutorial_man.is_speaking() is False:
            return True
        return False

    def room1(self):
        """
        Second room of the game. Player walks through unthreatening forest.
        Mostly for establishment.

        Returns:
            True if the room is clear, False otherwise. 
        """
        if self.current_room.is_clear():
            return True
        return False

    def room2(self):
        if self.rooms[2].is_clear():
            self.player.spotlight_on()
            for filename in sorted(os.listdir('Media/misc/teleport')):
                self.player.spotlight_image(os.path.join('Media/misc/teleport', filename))
                self.update()
                pygame.display.flip()
                pygame.time.wait(200)
            self.player.spotlight_off()
            return True
        return False

    def room3(self):
        turtle = self.current_room.npcs[0]
        self.current_background = self.backgrounds[2]
        if self.player.collide(turtle):
            self.conversation(turtle, self.player)
        if self.rooms[3].is_clear():
            if len(self.rooms[3].interactables) > 0:
                del self.rooms[3].interactables[0]
                self.guide = environment.Guide()
                self.guide.update_text()
                self.conversations = ['Oh look, it\'s a book! I bet you can'
                                      ' open it by pressing TAB. Those guides'
                                      ' are never wrong but I wouldn\'t trust'
                                      ' it if I were you.', 'Where am I?',
                                      'Well you\'re here, obviously. You just '
                                      'appeared. You must have come through the'
                                      ' mushroom ring.'
                                      ]
            if turtle.get_pos()[0] < 490:
                turtle.move('right')
                turtle.say_once('What have you got there?')
            if not self.conversations:
                return True
        return False

    def room4(self):
        self.guide.update_text(2)
        self.current_background = self.backgrounds[2]
        turtle = self.current_room.npcs[0]
        if self.player.collide(turtle) and not turtle.is_speaking():
            turtle.say('Help help I lost my keys! They must be in one'
                       ' of these leaf piles but I\'m too small to search'
                       ' all of them. Will you help me find them?')
        if self.rooms[4].interactables[0].is_end_state():
            self.update()
            pygame.display.flip()
            pygame.time.wait(1000)
            return True
        return False

    def room5(self):
        self.guide.update_text(3)
        self.player.spotlight_image()
        self.player.spotlight_on()
        self.player.say_once('Oof! I fell down a hole. I wonder if my guide'
                             ' has any advice.')
        if self.current_room.is_clear():
            if len(self.current_room.interactables) > 0:
                del self.current_room.interactables[0]
                self.player.say_once('Found the key! Now I just have to'
                                     ' get out of this maze.')
            return True
        return False

    def room6(self):
        self.guide.update_text(4)
        self.current_background = self.backgrounds[1]
        self.player.spotlight_off()
        if 650 < self.player.get_pos()[0] < 750 and self.player.get_pos()[1] < 500:
            self.player.say_once('Is anybody there?')
            self.guide.update_text(5)
            if not self.player.is_speaking():
                self.player.say_once('Maybe that turtle can help me. I should go'
                                     ' return his key.')
        if self.current_room.is_clear():
            return True
        return False

    def room7(self):
        if self.rooms[1].is_clear():
            return True
        return False
