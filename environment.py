import pygame
import pandas
import animator
from pygame.locals import RLEACCEL
import math
import textwrap


class Background(pygame.sprite.Sprite):
    """
    A class designed to represent a background
        Extracts attributes from a csv file.

    Attributes:
        datafile: the datafile that defines all the stats, a dataframe
        animator: the animator instance that animates the room graphics
        surf: the room surface, displaying the room visually
        rect: the boundary rectangle of the room
    """
    def __init__(self, data, dir='backgrounds/'):
        super(Background, self).__init__()

        # Create path and read the .csv defining the background
        path = 'Media/' + dir + data + '.csv'
        self.datafile = pandas.read_csv(path, index_col=0)

        # Assign the animator path and update speed to a new instance of Animator
        self.animator = animator.Animator(
            pathname='Media/'+ dir + self.datafile.loc['animator', '2'],
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


class Room(Background):
    """
    A class representing a room, inheriting from Background

    Attributes:
        same as background, but with the addition of
        spawn: the location designated as a player spawn, as a list x,y
        borders: the rectangular corners of a room [xmin, xmax, ymin, ymax]
        objects: a list of rects to use as obstacles that are impassable
    """

    def __init__(self, data, dir='rooms/'):
        ''' Initializes an instance of Room
        :param data: the data file to use
        :param dir: the directory (inside Media) to use
        '''
        super(Room, self).__init__(data, dir)

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
        self.font = pygame.font.Font('Media/fonts/iAWriterduospace-Bold.otf', 15)
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

