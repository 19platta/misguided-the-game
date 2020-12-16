import pygame
import helpers
import pandas
from pygame.locals import RLEACCEL


class Interactable(helpers.DataSprite):
    """
    A class for objects which the player can interact with.

    Attributes:
        _state: int representing the state the interactable is in.
            Increments when the player interacts with an instance
        _data: string representing the interactable to create
        _end_state: int representing the state the interactable must be in for
            the game to progress. Defaults to 1
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
        Place an interactable instance within a room at the given coordinates.

        Args:
            x: int representing the x coordinate, from left to right, to place
                the interactable at
            y: int representing the y coordinate, from top to bottom, to place
                the interactable at
        """
        self._rect.x = x
        self._rect.y = y

    def highlight(self):
        """
        Highlight an interactable.

        Assumes each interactable state has a highlighted version, with a
        folder named in the format of state + h. So for instance, an
        interactable in state 1 should have a folder 1h containing the images
        to represent the highlighted state.
        """
        self._surf = self._animator.get_next(type=str(self._state) + "h")

    def un_highlight(self):
        """
        Unhighlight an interactable

        Assumes each interactable state has a highlighted version, with a
        folder named in the format of state + h. So for instance, an
        interactable in state 1 should have a folder 1h containing the images
        to represent the highlighted state.
        """
        self._surf = self._animator.get_next(type=str(self._state))

    def interact(self):
        """
        Increment the state and visuals of an interactable upon interaction.
        """
        self._state = self._animator.get_next_folder()
        self._surf = self._animator.get_next()

    def update(self, screen, player):
        """
        Update the interactables on the screen.

        If the player is within interaction range of an interaction, it will
        highlight in yellow. If the player is interacting with the interactable
        it will update accordingly. If the player moves out of range, the
        interactable will de-highlight itself.
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
