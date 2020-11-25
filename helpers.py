import pygame
import pandas
from pygame.locals import RLEACCEL
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
            print(sorted(os.listdir(pathname + '/' + type)))
            for filename in sorted(os.listdir(pathname + '/' + type)):
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


class DataSprite(pygame.sprite.Sprite):
    """
    Class to create a generic animated object from a .csv file.

    This could be used to create backgrounds, characters, interactables,
    and more. Assumes the files structure of this project with an overarching
    Media folder

    Attributes:
        datafile: a pandas dataframe created from the .csv file
        animator: an instance of the class Animator with properties derived
            from datafile
        surf: a Sprite surf displaying the current state of animator
        rect: a Sprite rect representing the current location of the Sprite,
            specified by datafile
    """
    def __init__(self, data, dir):
        super(DataSprite, self).__init__()

        # Create path and read the .csv defining the background
        path = 'Media/' + dir + data + '.csv'
        self.datafile = pandas.read_csv(path, index_col=0)

        # Assign the animator path and update speed to a new instance of Animator
        self.animator = Animator(
            pathname='Media/' + dir + self.datafile.loc['animator', '2'],
            types=['main'], speed=float(self.datafile.loc['animator', '3']))

        # Get the first frame of the animation and create the background surface
        self.surf = self.animator.get_next('main')
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            left=int(self.datafile.loc['place', '2']),
            top=int(self.datafile.loc['place', '3']))

    def update(self, screen):
        """
        Update the Background on a screen and animates it

        Args:
            screen: the surface to update to.

        """
        self.surf = self.animator.get_next('main')
        screen.blit(self.surf, self.rect)
