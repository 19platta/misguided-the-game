import pygame
import helpers
import pandas
from pygame.locals import RLEACCEL


class Interactable(helpers.DataSprite):
    """
    A class for objects which the player can interact with.
    """
    def __init__(self, data, end_state=1):
        """
        Initialize an instance of the Interactable class
        """
        super().__init__(data, 'interactables/')
        self._state = int(self._datafile.loc['initial_state', '2'])
        self._data = data
        self._end_state = end_state

    def place(self, x, y):
        """
        Place an interactable instance within a room
        """
        self._rect.x = x
        self._rect.y = y

    def highlight(self):
        """
        Highlight an interactable
        """
        self._surf = self._animator.get_next(type=str(self._state) + "h")

    def un_highlight(self):
        """
        Unhighlight an interactable
        """
        self._surf = self._animator.get_next(type=str(self._state))

    def interact(self):
        """
        """
        print('yee')
        self._state = self._animator.get_next_folder()
        self._surf = self._animator.get_next()

    def update(self, screen, player):
        """

        """
        if self.collide(player):
            self.highlight()
            if player.interacting():
                self.interact()
        else:
            self.un_highlight()

        screen.blit(self._surf, self._rect)

    def is_end_state(self):
        """
        Determine if an interactable is in the correct state to move to the
        next room.

        Returns:
             True if it is in the correct state, False otherwise
        """
        return self._state == self._end_state
