import pygame
import helpers
import environment

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_s,
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

    """
    def __init__(self, img):
        super(Player, self).__init__(img)

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

    def spawn(self, room):
        """

        Args:
            room:

        Returns:

        """
        self.room = room
        self.rect = self.rect.move(self.room.get_spawn()[0],
                                   self.room.get_spawn()[1])


class NPC(Character):
    """

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

