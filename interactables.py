import pygame
import helpers
import pandas
from pygame.locals import RLEACCEL


class Interactable(helpers.DataSprite):
    """
    A class for objects which the player can interact with.
    """
    def __init__(self, data):
        super(Interactable, self).__init__(data, 'interactables/')
        self.within_range = False

    def check_range(self, player):

