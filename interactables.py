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
        self.state = int(self.datafile.loc['initial_state', '2'])
        self.data = data
        self.end_state = end_state

    def place(self, x, y):
        """
        Place an interactable instance within a room
        """
        self.rect.x = x
        self.rect.y = y

    def highlight(self):
        """
        Highlight an interactable
        """
        self.surf = self.animator.get_next(type=str(self.state) + "h")

    def un_highlight(self):
        """
        Unhighlight an interactable
        """
        self.surf = self.animator.get_next(type=str(self.state))

    def interact(self):
        """
        """
        print('yee')
        self.state = self.animator.get_next_folder()
        self.surf = self.animator.get_next()

    def update(self, screen, player):
        """

        """
        if self.collide(player):
            self.highlight()
            if player.interacting():
                self.interact()
        else:
            self.un_highlight()

        screen.blit(self.surf, self.rect)

    def is_end_state(self):
        """
        Determine if an interactable is in the correct state to move to the
        next room.

        Returns:
             True if it is in the correct state, False otherwise
        """
        return self.state == self.end_state
