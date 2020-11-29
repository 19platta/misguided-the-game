import pygame
import helpers
import pandas
from pygame.locals import RLEACCEL


class Interactable(helpers.DataSprite):
    """
    A class for objects which the player can interact with.
    """
    def __init__(self, data):
        """
        Initialize an instance of the Interactable class
        """
        super(Interactable, self).__init__(data, 'interactables/')
        self.state = int(self.datafile.loc['initial_state', '2'])
        self.data = data

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

    def update(self, screen, player):
        """

        """
        if self.collide(player):
            self.highlight()
        else:
            self.un_highlight()

        screen.blit(self.surf, self.rect)

