import pygame
import helpers
import environment

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_TAB,
)


class Character(helpers.DataSprite):
    """
    Generic class to create a character from a .csv file

    Attributes:
        Same as DataSprite, with the addition of
        _room: the room the character is currently in
        _chatbox: an instance of Chatbox used by the character
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
        Update the character visuals on the screen.

        Args:
            screen: the screen to update to
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
        _interact: boolean indicating whether the player is
            interacting with an object of class Interactable
        _guiding: boolean indicating whether the player is interacting with
            the guide
        _spotlight: boolean indicating whether the spotlight is on
            or off
        _spotlight_surf: the image representing the spotlight
        _spotlight_rect: contains the coordinates defining the
            spotlight's position
        _start_time: marks the in-game time of initialization, used for
        _start_time: marks the in-game time of initialization, used for
            interaction
        inventory: a list representing the items the character is currently
            carrying
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
        self.inventory = []

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
            str: string containing the name of the room for the character to
                spawn in
        """
        self._room = room
        self._rect.centerx = self._room.get_entrance(str)[0]
        self._rect.centery = self._room.get_entrance(str)[1]

    def is_exiting(self):
        """
        Determine if the character is at an exit to a room.

        Returns:
            True if the character is at an exit, False otherwise.
        """
        for room_exit in self._room.get_exits():
            if self._rect.colliderect(room_exit[0]):
                return [room_exit[1], self._room.get_name()]
        return None

    def spotlight_on(self):
        """
        Switch the spotlight on.

        A spotlight is a transparent circle in a black background that moves
        as the player moves. It creates the effect of a small circle of light
        around the player while obscuring the rest of the room.
        """
        self._spotlight = True

    def spotlight_off(self):
        """
        Switch the spotlight off.

        A spotlight is a transparent circle in a black background that moves
        as the player moves. It creates the effect of a small circle of light
        around the player while obscuring the rest of the room.
        """
        self._spotlight = False

    def spotlight_image(self,
                        img_path='Media/misc/spotlight/pixil-frame-0.png'):
        """
        Set the image used for the spotlight.

        This allows the spotlight to be anything that should remain at the
        same location as the character, even if they move.

        Args:
            img_path: path to the image to use. Defaults to the black screen
                with a transparent circle
        """
        self._spotlight_surf = pygame.image.load(img_path)
        self._spotlight_rect = self._spotlight_surf.get_rect()

    def draw_rect(self, screen):
        """
        Debug function used to see the full space the character is taking up.

        This function is useful in conjunction with the `draw_objects`
        function in the Room class to determine if the character rect or
        boundaries are causing movement problems.

        Args:
            screen: the screen to draw to
        """
        pygame.draw.rect(surface=screen, rect=self._rect,
                         color=pygame.Color(0, 255, 0))

    def update(self, screen):
        """
        Update the player, and spotlight if necessary

        Args:
            screen: the screen to draw to
        """
        screen.blit(self._surf, self._rect)
        # If the spotlight is active, show it at the same place as the
        # character
        if self._spotlight:
            self._spotlight_rect.center = (self.get_pos()[0], self.get_pos()[1])
            screen.blit(self._spotlight_surf, self._spotlight_rect)
        self._chatbox.update(screen)


class NPC(Character):
    """
    Create a non-playable character (NPC) sprite from a .csv file

    Inherits from Character
    """
    def __init__(self, img):
        """
        Initialize an instance of class NPC.

        Args:
            img: the name of the NPC folder to use (for animation purposes)
        """
        super().__init__(img)

    def spawn(self, x, y):
        """
        Spawn the NPC at the given coordinates.

        Args:
            x: an int representing the x coordinate (from left to right)
                to spawn the NPC at
            y: an int representing the y coordinate (from top to bottom)
                to spawn the NPC at
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
