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
        super().__init__(data, 'characters/')
        self._room = None
        self._chatbox = environment.Chatbox(self)

    def get_pos(self):
        """
        Get the current position of the character

        Returns:
            The x and y coordinate representing the character's position
        """
        return [self._rect.centerx, self._rect.centery]

    def update(self, screen):
        """

        Args:
            screen:

        Returns:

        """
        screen.blit(self._surf, self._rect)
        self._chatbox.update(screen)

    def say(self, phrase):
        """
        Have the character say something in a chatbox.

        Args:
            phrase: string containing the phrase for the character to say.
        """
        self._chatbox.say(phrase)

    def say_once(self, phrase):
        """
        Have the character say something in a chatbox, only once

        Args:
            phrase: string containing the phrase for the character to say.
        """
        self._chatbox.say_once(phrase)

    def is_speaking(self):
        """
        Determine whether or not a character is currently speaking.

        Returns:
            True if character is currently speaking, False otherwise
        """
        return self._chatbox.is_speaking()


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
        super().__init__(img)
        self._interact = False
        self._guiding = False
        self._spotlight_surf = pygame.image.load(
            'Media/misc/spotlight/pixil-frame-0.png')
        self._spotlight_rect = self._spotlight_surf.get_rect()
        self._spotlight = False
        self._start_time = pygame.time.get_ticks()

    def move(self, pressed_keys):
        """
        Move the character based on which key is pressed and prevent it from
        walking into obstacles.

        Args:
            pressed_keys: Pygame event containing all pressed keys

        """
        if pressed_keys[K_UP]:
            self._surf = self._animator.get_next('back')
            self._rect.move_ip(0, -5)
            if pygame.Rect.collidelist(self._rect,
                                       self._room.get_objects()) >= 0:
                self._rect.move_ip(0, 5)
        if pressed_keys[K_DOWN]:
            self._surf = self._animator.get_next('front')
            self._rect.move_ip(0, 5)
            if pygame.Rect.collidelist(self._rect,
                                       self._room.get_objects()) >= 0:
                self._rect.move_ip(0, -5)
        if pressed_keys[K_LEFT]:
            self._surf = self._animator.get_next('left')
            self._rect.move_ip(-5, 0)
            if pygame.Rect.collidelist(self._rect,
                                       self._room.get_objects()) >= 0:
                self._rect.move_ip(5, 0)
        if pressed_keys[K_RIGHT]:
            self._surf = self._animator.get_next('right')
            self._rect.move_ip(5, 0)
            if pygame.Rect.collidelist(self._rect,
                                       self._room.get_objects()) >= 0:
                self._rect.move_ip(-5, 0)
        if pressed_keys[K_s]:
            self.say('Oi get off my piano')
            #self.say('Did you ever hear the Tragedy of Darth Plagueis the wise? I thought not. Its not a story the Jedi would tell you. Its a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life... He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful... the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Its ironic he could save others from death, but not himself')
        if pressed_keys[K_SPACE]:
            if pygame.time.get_ticks() - self._start_time > 500:
                self._interact = True
                self._start_time = pygame.time.get_ticks()
        if pressed_keys[K_TAB]:
            if pygame.time.get_ticks() - self._start_time > 500:
                self._guiding = True
                self._start_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self._start_time > 100:
            self._interact = False

    def interacting(self):
        """
        Determine if the player is currently attempting to interact with an
        object of class Interactable.

        Returns:
            True is the player is interacting, False otherwise.
        """
        if self._interact:
            self._interact = False
            return True
        else:
            return False

    def is_guiding(self):
        """
        Determine if the player is attempting to interact with the Guide.

        Returns:
            True if the player is attempting to interact, False otherwise.
        """
        if self._guiding:
            self._guiding = False
            return True
        else:
            return False

    def spawn(self, room, str):
        """
        Spawn the player at the spawn location of a room, designated by the
        room's .csv file

        Args:
            room: the room object to spawn the character in
            index: the specific entrance of the room at which to spawn
                (defaults to the first entrance, index 0)
        """
        self._room = room
        print(room.get_name())
        self._rect.centerx = self._room.get_entrance(str)[0]
        self._rect.centery = self._room.get_entrance(str)[1]

    def is_exiting(self):
        for exit in self._room.get_exits():
            if self._rect.colliderect(exit[0]):
                return [exit[1], self._room.get_name()]
        return None

    def spotlight_on(self):
        """
        Switches the spotlight on.

        A spotlight is a transparent circle in a black background that moves
        as the player moves. It creates the effect of a small circle of light
        around the player while obscuring the rest of the room.
        """
        self._spotlight = True

    def spotlight_off(self):
        """
        Switches the spotlight off.

        A spotlight is a transparent circle in a black background that moves
        as the player moves. It creates the effect of a small circle of light
        around the player while obscuring the rest of the room.
        """
        self._spotlight = False

    def spotlight_image(self, img_path='Media/misc/spotlight/pixil-frame-0.png'):
        self._spotlight_surf = pygame.image.load(img_path)
        self._spotlight_rect = self._spotlight_surf.get_rect()

    def draw_rect(self, screen):
        """

        Args:
            screen:

        Returns:

        """
        pygame.draw.rect(surface=screen, rect=self._rect,
                         color=pygame.Color(0, 255, 0))


    def update(self, screen):
        """
        Update the player, and spotlight if necessary
        """
        screen.blit(self._surf, self._rect)
        if self._spotlight:
            self._spotlight_rect.center = (self.get_pos()[0], self.get_pos()[1])
            screen.blit(self._spotlight_surf, self._spotlight_rect)
        self._chatbox.update(screen)



class NPC(Character):
    """
    Creates a non-playable character (NPC) sprite from a .csv file
    """
    def __init__(self, img):
        """

        Args:
            img:
        """
        super().__init__(img)

    def spawn(self, x, y):
        """

        Args:
            x:
            y:

        Returns:

        """
        self._rect = self._rect.move(x, y)

    def move(self, direction):
        """
        Move the NPC in a given direction. Will not allow walking into
        obstacles.

        Assumes input will one of 'up', 'down', 'left', or 'right'.

        Args:
            direction: string containing the direction to move the character.

        """
        if direction == 'up':
            self._surf = self._animator.get_next('back')
            self._rect.move_ip(0, -5)
        if direction == 'down':
            self._surf = self._animator.get_next('front')
            self._rect.move_ip(0, 5)
        if direction == 'left':
            self._surf = self._animator.get_next('left')
            self._rect.move_ip(-5, 0)
        if direction == 'right':
            self._surf = self._animator.get_next('right')
            self._rect.move_ip(5, 0)
