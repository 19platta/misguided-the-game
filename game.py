import pygame
import character
import environment
import os

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
        screen: the window to draw visuals on
        clock: Pygame clock object, keeps track of ingame time
        rooms: a list of all the room instances in the game
        current_room: the room instance the player is currently in
        backgrounds: a list of all the background instances in the game
        current_background: the background instance currently being displayed
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
        self.current_room = self.rooms[0]
        self.backgrounds = [
            environment.Background('daysky'),
            environment.Background('nightsky'),
            environment.Background('twilightsky')
        ]
        self.current_background = self.backgrounds[0]

        self.player = character.Player('player')

        self.guide = None

        self.conversations = []

    def intro(self):
        """
        Play an introduction animation at the beginning of the game.
        """
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
        self.player.update(self.screen)
        if self.guide is not None:
            self.guide.update(self.screen, self.player)

    def run(self):
        """
        Run the game.

        This function contains the main game loop and game logic. It will run
        the game until the player quits.
        """
        self.intro()
        running = True

        self.player.spawn(self.current_room, 'initial')

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

        Assumes that self.conversations is a list, and that its elements
        have been set to contain the lines the characters will say, beginning
        with the first speaker's first line.

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
        elif self.current_room == self.rooms[7]:
            return self.room7()

    def room0(self):
        """
        Run first room of the game.

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
        Run second room of the game.

        In this room, the player walks through unthreatening forest.
        Mostly for establishment.

        Returns:
            True if the room is clear, False otherwise. 
        """
        if self.current_room.is_clear():
            return True
        return False

    def room2(self):
        """
        Run third room of the game.

        In this room, the player discovers a mushroom ring. When they interact
        with it, it teleports them to a different world.

        Returns:
            True if the player has interacted with the mushroom ring and the
                teleportation animation has played, False otherwise.
        """
        if self.current_room.is_clear():
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
        """
        Run the fourth room of the game.

        In this room, the player finds the guide, initializing an instance of
        the Guide class, and talks to a turtle who explains how to open the
        guide. The turtle also explains that to get home the player needs to
        find another mushroom ring to get home, establishing the goal.

        Returns:
            True if the player has picked up the guide and finished talking to
                the turtle, False otherwise.
        """
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
                                      ' mushroom ring.', 'How do I get back home?',
                                      'I think you\'ll have to find another'
                                      'mushroom ring. They only work once you know.'
                                      ]
            if turtle.get_pos()[0] < 490:
                turtle.move('right')
                turtle.say_once('What have you got there?')
            if not self.conversations:
                return True
        return False

    def room4(self):
        """
        Run the fifth room of the game.

        In this room, the player meets another turtle who needs help looking
        for his keys in the leaf pile. The player can interact with multiple
        leaf piles, but a trapdoor exit is hidden under one pile that the
        player "falls" through.

        Returns:
            True if the player has interacted with the trapdoor leaf pile,
                False otherwise
        """
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
        """
        Run the sixth room of the game.

        This room is a maze the player must solve in the dark, with only a
        small transparent circle of illumination around them. They must first
        find the turtle's key, which is hidden in the maze, then find the exit.
        The player's chatbox provides hints as to how to proceed.

        Returns:
            True if the player has collected the key and is at the maze exit,
                False otherwise
        """
        self.guide.update_text(3)
        self.player.spotlight_image()
        self.player.spotlight_on()
        self.player.say_once('Oof! I fell down a hole. I wonder if my guide'
                             ' has any advice.')
        if self.current_room.is_clear():
            if len(self.current_room.interactables) > 0:
                del self.current_room.interactables[0]
                self.player.inventory.append('key')
                self.player.say_once('Found the key! Now I just have to'
                                     ' get out of this maze.')
            return True
        return False

    def room6(self):
        """
        Run the sixth room of the game.

        In this room, the player attempts to enter the inn. THey are not able
        to at first, but the turtle enters and upon returning his key, he
        provides the player with a megaphone, allowing them to shout loudly
        enough to be heard in the inn.

        Returns:
            True if the megaphone is in the player's inventory and the player
                is at the exit, False otherwise
        """
        turtle = self.current_room.npcs[0]
        self.guide.update_text(4)
        self.current_background = self.backgrounds[1]
        self.player.spotlight_off()
        # Check to see if the player is at the inn door
        if 600 < self.player.get_pos()[0] < 700 and self.player.get_pos()[1] < 470:
            # If the player doesn't have the megaphone yet, the guide will update
            # with a hint
            if 'megaphone' not in self.player.inventory:
                self.player.say_once('Is anybody there?')
                self.guide.update_text(5)
                if not self.player.is_speaking():
                    self.player.say_once('Maybe the guide can help.')
            # If the player has the megaphone, the stage is complete and the
            # room is clear
            else:
                return True
        # If the guide has given its hint, have the turtle walk in and set up
        # the conversation
        if not self.player.is_speaking() and turtle.get_pos()[0] < 300 and self.guide.get_index() == 5:
            turtle.move('right')
            self.conversations = [
                'Hey! Did you find my key?',
                ' I sure did, here you go.',
                'Thanks! I don\'t have much to give you but you can have this'
                ' old megaphone I found lying around if you want.'
            ]
        # If the player collides with the turtle, have the conversation and
        # spawn the megaphone in the right place
        if self.player.collide(turtle):
            self.conversation(turtle, self.player)
            if not (self.player.is_speaking() and turtle.is_speaking()):
                if len(self.current_room.interactables) > 0 and len(self.conversations) == 0:
                    self.current_room.interactables[0].place(300, 550)
        # If the megaphone has been interacted with and is still in the room,
        # remove it from the room and add to the player's inventory
        # Also remove the key from the inventory
        if self.current_room.is_clear() and len(self.current_room.interactables) > 0:
            del self.current_room.interactables[0]
            del self.player.inventory[self.player.inventory.index('key')]
            self.player.inventory.append('megaphone')
        return False

    def room7(self):
        """
        Run the final room of the game.

        This is the final room so far, though we hope to add more in future.
        In this room the player enters the lobby of the inn and interacts with
        the turtle innkeeper. The innkeeper tells them they will be safe here
        until they set out again and thanks them for playing the first chapter,
        indicating that this first part of the game is over.

        To be continued...

        Returns:
            True if the player has interacted with the innkeeper and the
                innkeeper has made his speech, False otherwise.
        """
        innkeeper = self.current_room.npcs[0]
        if self.player.collide(innkeeper):
            innkeeper.say_once('Welcome to the inn! You\'ll be safe here until'
                               ' you start on the next part of your journey.'
                               ' Thanks for playing chapter one! Come back soon'
                               ' for more adventures.')
            return True
        return False
