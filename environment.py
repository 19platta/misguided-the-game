import pygame
import helpers
from pygame.locals import RLEACCEL
import math
import textwrap


class Background(helpers.DataSprite):
    """
    A class designed to represent a background
        Extracts attributes from a csv file.
    """
    def __init__(self, data):
        super(Background, self).__init__(data, 'backgrounds/')

    def update(self, screen):
        """
        Update the Background on a screen and animates it

        Args:
            screen: the surface to update to.

        """
        self.surf = self.animator.get_next('main')
        screen.blit(self.surf, self.rect)


class Room(helpers.DataSprite):
    """
    A class representing a room, inheriting from Background

    Attributes:
        spawn: the location designated as a player spawn, as a list x,y
        borders: the rectangular corners of a room [xmin, xmax, ymin, ymax]
        objects: a list of rects to use as obstacles that are impassable
    """

    def __init__(self, data):
        """
        Initializes an instance of Room

        Args:
            data: the .csv file to use
        """
        super(Room, self).__init__(data, 'rooms/')

        self.spawn = [int(self.datafile.loc['spawn', '2']), int(self.datafile.loc['spawn', '3'])]

        self.borders = self.datafile.loc['borders'].dropna().values.tolist()
        self.borders = [int(border) for border in self.borders]

        self.objects = []
        for object in self.datafile.loc['objects'].dropna().values.tolist():
            object = [int(obj) for obj in object.split('/')]
            self.objects.append(pygame.Rect(object[0]+self.rect.left,
                                            object[1]+self.rect.top,
                                            object[2], object[3]))

    def get_spawn(self):
        """
        Accessor for the spawn location

        Returns:
            the spawn location of the room as an [x,y] list
        """
        return [self.spawn[0], self.spawn[1]]

    def get_objects(self):
        """
        Accessor for the room objects

        Returns:
             all object rects as a list
        """
        return self.objects

    def draw_objects(self, screen):
        """

        Args:
            screen:

        Returns:

        """
        for rect in self.objects:
            pygame.draw.rect(surface=screen, rect=rect,
                             color=pygame.Color(0,0,255))


class Chatbox(pygame.sprite.Sprite):
    """

    """
    def __init__(self, sprite):
        super(Chatbox, self).__init__()
        self.surf = pygame.image.load('Media/misc/chatbox-2.png')
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.phrase = ''
        self.index = 0
        self.font = pygame.font.Font('Media/fonts/iAWriterDuospace-Bold.otf', 15)
        self.sprite = sprite

    def say(self, phrase):
        """
        Defines a phrase to be said

        Args:
            phrase: string containing the phrase
        """
        self.phrase = phrase

    def is_speaking(self):
        """
        Determine if a character is speaking or not.

        Returns:
            True if phrase is not empty, False otherwise
        """
        return self.phrase != ''

    def _process_speech(self, speed):
        """

        Args:
            speed:

        Returns:

        """
        self.index += 1
        # If there is still stuff left to say, say it at the specified speed
        if math.floor(self.index * speed) <= len(self.phrase):
            processed = self.phrase[0:math.floor(self.index * speed)]
        # If there isn't anything left to say, only terminate the speech after
        # a short delay. The delay is inversely proportional to the length of
        # the phrase.
        elif math.floor(self.index * speed) > len(self.phrase) * (1 + 50/(len(self.phrase)+1)):
            self.index = 0
            self.phrase = ''
            processed = ''
        # If the short delay hasn't been met, say the full phrase
        else:
            processed = self.phrase

        return processed

    def update(self, screen):
        """

        Args:
            screen:

        Returns:

        """
        # Split the speech into lines that can fit in the chatbox
        processed = textwrap.fill(self._process_speech(0.6), 19).split('\n')
        # If the phrase length is greater than zero, display the chatbox with
        # the phrase in it
        if len(self.phrase) > 0:
            # Define position of the chatbox based on the character saying it
            x = self.sprite.get_pos()[0]
            y = self.sprite.get_pos()[1]
            self.rect.centerx = x
            self.rect.centery = y-130
            # Show the chatbox
            screen.blit(self.surf, self.rect)
            # Display the text. If it's long, show only the last four lines.
            # This creates a scrolling effect
            i = 0
            for part in processed[-4:]:
                screen.blit(self.font.render(part, True, (0, 0, 0)),
                            (self.rect.left + 8, self.rect.top + 90 + i))
                # Increment line height so text doesn't print on top of itself
                i += 15


class Guide(helpers.DataSprite):
    """

    """
    def __init__(self):
        super(Guide, self).__init__()
        self.animator = helpers.Animator(pathname='Media/misc/Guide',
                                         types=['openclose', 'close', 'open', 'not'],
                                         speed=0.5)


