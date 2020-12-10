import pygame
import pandas
from pygame.locals import RLEACCEL
import os
from pygame import Surface
import math


class Animator:
    """
    """
    def __init__(self, pathname='Media/characters/turtle', speed=0.5):
        """
        Initialize an instance of class Animator
        """
        self.images = {}
        self.index = {}
        self.types = []

        with os.scandir(pathname) as it:
            for entry in it:
                if entry.is_dir():
                    self.types.append(entry.name)

        for type in self.types:
            self.images[type] = []
            self.index[type] = 0
            for filename in sorted(os.listdir(pathname + '/' + type)):
                img = pygame.image.load(os.path.join(pathname, type, filename))
                self.images[type].append(Surface.convert_alpha(img))
        self.types = sorted(self.types)
        self.current_type = self.types[0]
        self.update_speed = speed

    def get_current_type(self):
        """
        """
        return self.current_type

    def get_next(self, type=''):
        """
        Args:
            type:
        Returns:
        """
        if type == '':
            type = self.types[0]
        self.index[type] += 1
        if math.floor(self.index[type]*self.update_speed) >= len(self.images[type]):
            self.index[type] = 0
        self.current_type = type
        return self.images[type][math.floor(self.index[type]*self.update_speed)]

    def get_next_folder(self):
        index = self.types.index(self.current_type) + 1
        if index == len(self.types):
            index = 0
        self.current_type = self.types[index]
        return self.current_type


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
        path = 'Media/' + dir + data + "/" + data + '.csv'
        self.datafile = pandas.read_csv(path, index_col=0)
        self.name = data
        # Assign the animator path and update speed to a new instance of Animator
        self.animator = Animator(
            pathname='Media/' + dir + data,
            speed=float(self.datafile.loc['animator', '2']))

        # Get the first frame of the animation and create the background surface
        self.surf = self.animator.get_next()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # If the file has 'place' set the rectangle to be at that place
        if 'place' in self.datafile.index:
            self.rect = self.surf.get_rect(
                left=int(self.datafile.loc['place', '2']),
                top=int(self.datafile.loc['place', '3']))
        else:
            self.rect = self.surf.get_rect()

    def update(self, screen):
        """
        Update the Background on a screen and animates it

        Args:
            screen: the surface to update to.

        """
        self.surf = self.animator.get_next()
        screen.blit(self.surf, self.rect)

    def collide(self, other):
        """

        Args:
            other:

        Returns:

        """
        return self.rect.colliderect(other.rect)
