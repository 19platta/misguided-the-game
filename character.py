import pygame
import helpers
import environment

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_s,
    K_SPACE,
    K_TAB,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)


class Character(helpers.DataSprite):
    """
    Generic class to create a character from a .csv file

    Attributes:
        Same as DataSprite, with the addition of
        room: the room the character is currently in
        chatbox: an instance of Chatbox used by the character
    """
    def __init__(self, data):
        super(Character, self).__init__(data, 'characters/')
        self.room = None
        self.chatbox = environment.Chatbox(self)

    def get_pos(self):
        """
        Get the current position of the character

        Returns:
            The x and y coordinate representing the character's position
        """
        return [self.rect.centerx, self.rect.centery]

    def update(self, screen):
        """

        Args:
            screen:

        Returns:

        """
        screen.blit(self.surf, self.rect)
        self.chatbox.update(screen)

    def say(self, phrase):
        """
        Have the character say something in a chatbox.

        Args:
            phrase: string containing the phrase for the character to say.
        """
        self.chatbox.say(phrase)

    def is_speaking(self):
        """
        Determine whether or not a character is currently speaking.

        Returns:
            True if character is currently speaking, False otherwise
        """
        return self.chatbox.is_speaking()


class Player(Character):
    """
    Class representing a user-controlled character.

    Attributes:
        interact: boolean indicating whether the player is
            interacting with an object of class Interactable
        guiding: boolean indicating whether the player is interacting with
            the guide
        spotlight: boolean indicating whether the spotlight is on
            or off
        spotlight_surf: the image representing the spotlight
        spotlight_rect: contains the coordinates defining the
            spotlight's position
        start_time: marks the in-game time of initialization, used for
            interaction
    """
    def __init__(self, img):
        super(Player, self).__init__(img)
        self.interact = False
        self.guiding = False
        self.spotlight_surf = pygame.image.load(
            'Media/misc/spotlight/pixil-frame-0.png')
        self.spotlight_rect = self.spotlight_surf.get_rect()
        self.spotlight = True
        self.start_time = pygame.time.get_ticks()

    def move(self, pressed_keys):
        """
        Move the character based on which key is pressed and prevent it from
        walking into obstacles.

        Args:
            pressed_keys: Pygame event containing all pressed keys

        """
        if pressed_keys[K_UP]:
            self.surf = self.animator.get_next('right')
            self.rect.move_ip(0, -5)
            if pygame.Rect.collidelist(self.rect,
                                       self.room.get_objects()) >= 0:
                self.rect.move_ip(0, 5)
        if pressed_keys[K_DOWN]:
            self.surf = self.animator.get_next('right')
            self.rect.move_ip(0, 5)
            if pygame.Rect.collidelist(self.rect,
                                       self.room.get_objects()) >= 0:
                self.rect.move_ip(0, -5)
        if pressed_keys[K_LEFT]:
            self.surf = self.animator.get_next('left')
            self.rect.move_ip(-5, 0)
            if pygame.Rect.collidelist(self.rect,
                                       self.room.get_objects()) >= 0:
                self.rect.move_ip(5, 0)
        if pressed_keys[K_RIGHT]:
            self.surf = self.animator.get_next('right')
            self.rect.move_ip(5, 0)
            if pygame.Rect.collidelist(self.rect,
                                       self.room.get_objects()) >= 0:
                self.rect.move_ip(-5, 0)
        if pressed_keys[K_s]:
            self.say('Did you ever hear the Tragedy of Darth Plagueis the wise? I thought not. Its not a story the Jedi would tell you. Its a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life... He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful... the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Its ironic he could save others from death, but not himself')
        if pressed_keys[K_SPACE]:
            if pygame.time.get_ticks() - self.start_time > 500:
                self.interact = True
                self.start_time = pygame.time.get_ticks()
        if pressed_keys[K_TAB]:
            if pygame.time.get_ticks() - self.start_time > 500:
                self.guiding = True
                self.start_time = pygame.time.get_ticks()

    def interacting(self):
        """
        Determine if the player is currently attempting to interact with an
        object of class Interactable.

        Returns:
            True is the player is interacting, False otherwise.
        """
        if self.interact:
            self.interact = False
            return True
        else:
            return False

    def is_guiding(self):
        """
        Determine if the player is attempting to interact with the Guide.

        Returns:
            True if the player is attempting to interact, False otherwise.
        """
        if self.guiding:
            self.guiding = False
            return True
        else:
            return False

    def spawn(self, room):
        """
        Spawn the player at the spawn location of a room, designated by the
        room's .csv file

        Args:
            room: the room object to spawn the character in
        """
        self.room = room
        self.rect = self.rect.move(self.room.get_spawn()[0],
                                   self.room.get_spawn()[1])

    def spotlight_on(self):
        """
        Switches the spotlight on.

        A spotlight is a transparent circle in a black background that moves
        as the player moves. It creates the effect of a small circle of light
        around the player while obscuring the rest of the room.
        """
        self.spotlight = True

    def spotlight_off(self):
        """
        Switches the spotlight off.

        A spotlight is a transparent circle in a black background that moves
        as the player moves. It creates the effect of a small circle of light
        around the player while obscuring the rest of the room.
        """
        self.spotlight = False

    def update(self, screen):
        """
        Update the player, and spotlight if necessary
        """
        if self.spotlight:
            self.spotlight_rect.center = (self.get_pos()[0], self.get_pos()[1])
            screen.blit(self.spotlight_surf, self.spotlight_rect)
        super(Player, self).update(screen)


class NPC(Character):
    """
    Creates a non-playable character (NPC) sprite from a .csv file
    """
    def __init__(self, img):
        """

        Args:
            img:
        """
        super(NPC, self).__init__(img)

    def move(self, x, y):
        """

        Args:
            x:
            y:

        Returns:

        """
        self.rect = self.rect.move(x, y)
