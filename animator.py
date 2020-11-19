import pygame
import os
from pygame import Surface
import math


class Animator:
    """

    """
    def __init__(self, pathname='Media/characters/turtle',
                 types=['left', 'right'], speed=0.5):
        self.images = {}
        self.index = {}
        for type in types:
            self.images[type] = []
            self.index[type] = 0
            for filename in os.listdir(pathname + '/' + type):
                img = pygame.image.load(os.path.join(pathname, type, filename))
                self.images[type].append(Surface.convert_alpha(img))
        self.update_speed = speed

    def get_next(self, type):
        """

        Args:
            type:

        Returns:

        """
        self.index[type] += 1
        if math.floor(self.index[type]*self.update_speed) >= len(self.images[type]):
            self.index[type] = 0
        return self.images[type][math.floor(self.index[type]*self.update_speed)]

