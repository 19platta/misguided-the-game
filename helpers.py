import pygame
import pandas
from pygame.locals import RLEACCEL
import os
from pygame import Surface
import math


class Animator:
    """
    Class animator is used to create animations from series of images
    that can be displayed to create the appearance of motion. A single
    animator instance is designed to work for an entire object that
    may have different types of motion, ie. forwards, backwards, left,
    right, etc, and defines 'types' within itself to handle these different
    motions. These types are defined from the folders inside the directory
    animator is given, and the animator will assume that all folders inside
    the directory are to be used as animator types, with images in each.

    Attributes:
        _images: a dictionary containing lists of images for each type, where
            the type is the key, and images are the values
        _index: a dictionary equivalent to images that instead contains the
            current index of each type (ie. how much of the motion has
            completed)
        _types: a list containing all the types as strings
        _update_speed: a float representing how fast to update the animator,
            where 1 is 1 frame per tick and 0.1 is 1 frame every 10 ticks
    """
    def __init__(self, pathname='Media/characters/turtle', speed=0.5):
        """
        Initialize an instance of class Animator

        Args:
            pathname: the path to the folder to use, defaults to turtle
            speed: the speed at which the animator should change frames.
                Defaults to 0.5
        """
        self._images = {}
        self._index = {}
        self._types = []
        # Identifies all of the types as folders
        with os.scandir(pathname) as it:
            for entry in it:
                if entry.is_dir():
                    self._types.append(entry.name)
        # Identifies all the images in each type, and adds them to the _images
        for type in self._types:
            self._images[type] = []
            self._index[type] = 0
            for filename in sorted(os.listdir(pathname + '/' + type)):
                img = pygame.image.load(os.path.join(pathname, type, filename))
                self._images[type].append(Surface.convert_alpha(img))
        # Sort _types so that it is correctly ordered
        self._types = sorted(self._types)
        self._current_type = self._types[0]
        self._update_speed = speed

    def get_current_type(self):
        """
        Gets the current type of the animator (ie. which motion is currently
        being used

        Returns:
            the current type of the animator as a string
        """
        return self._current_type

    def get_next(self, type=''):
        """
        Updates the animator and increments the current type by 1, thereby
        creating motion visually. The type can also be changed with the
        type parameter. Uses the _update_speed as a rate to increment at.

        Args:
            type: The type of the animator to update and get the next of, if
            blank, sets to the default first type (index 0)
        Returns:
            The next image in the specified type of the animator
        """
        if type == '':
            type = self._types[0]
        self._index[type] += 1
        # If the index is out of bounds, it needs to revert to the first image
        if math.floor(self._index[type] * self._update_speed) \
                >= len(self._images[type]):
            self._index[type] = 0
        self._current_type = type
        # Return the image based on the update speed (a smaller update speed
        # means it takes more get_next() calls to update the image, so a
        # slower change
        return self._images[type][math.floor(
            self._index[type] * self._update_speed)]

    def get_next_folder(self):
        """
        Sets the current type of the animator to the next folder alphabetically
        setting it to the first if the current one is the last

        Returns:
            The new type as a string
        """
        index = self._types.index(self._current_type) + 1
        if index == len(self._types):
            index = 0
        self._current_type = self._types[index]
        return self._current_type


class DataSprite(pygame.sprite.Sprite):
    """
    Class to create a generic animated object from a .csv file.

    This could be used to create backgrounds, characters, interactables,
    and more. Assumes the files structure of this project with an overarching
    Media folder

    Attributes:
        _datafile: a pandas dataframe created from the .csv file
        _animator: an instance of the class Animator with properties derived
            from datafile
        _surf: a Sprite surf displaying the current state of animator
        _rect: a Sprite rect representing the current location of the Sprite,
            specified by datafile
    """
    def __init__(self, data, dir):
        """
        Initializes an instance of class datasprite with given specifications
        derived from a given directory. The reason that the dir and data
        parameters are split up is to allow the .csv file to easily be read,
        and also because children of datasprite will often have a fixed dir
        value (ie. 'rooms', 'characters') but a variable data value

        Args:
            data: the name of the file to look in to define the datasprite
            dir: the directory to get to the file that holds the datasprite
        """
        super().__init__()

        # Create path and read the .csv defining the background
        path = 'Media/' + dir + data + "/" + data + '.csv'
        self._datafile = pandas.read_csv(path, index_col=0)
        self._name = data
        # Assign the animator path and update speed to a new instance of
        # Animator
        self._animator = Animator(
            pathname='Media/' + dir + data,
            speed=float(self._datafile.loc['animator', '2']))

        # Get the first frame of the animation and create the background surface
        self._surf = self._animator.get_next()
        self._surf.set_colorkey((255, 255, 255), RLEACCEL)
        # If the file has 'place' set the rectangle to be at that place
        if 'place' in self._datafile.index:
            self._rect = self._surf.get_rect(
                left=int(self._datafile.loc['place', '2']),
                top=int(self._datafile.loc['place', '3']))
        else:
            self._rect = self._surf.get_rect()

    def collide(self, other):
        """
        Test if a given sprite is in contact (colliding) with another
        datasprite or a datasprite inherited object

        Args:
            other: the other object to test collision against

        Returns:
           True if they are colliding, False otherwise
        """
        return self._rect.colliderect(other.get_rect())

    def get_rect(self):
        """
        Accessor for the datasprite's rect

        Returns:
            the datasprite's rect
        """
        return self._rect

    def get_name(self):
        """
        Accessor for the datasprite's name

        Returns:
            the datasprite's name
        """
        return self._name

    def update(self, screen):
        """
        Update the Background on a screen and animates it

        Args:
            screen: the surface to update to.
        """
        self._surf = self._animator.get_next()
        screen.blit(self._surf, self._rect)
