import pygame
import pandas
import animator
from pygame.locals import RLEACCEL
import math
import textwrap


class Background(pygame.sprite.Sprite):
    ''' A class designed to represent a background
        Extracts attributes from a csv file.

        Attributes:
            datafile: the datafile that defines all the stats, a dataframe
            animator: the animator instance that animates the room graphics
            update_speed: the speed with which to update the animator
            surf: the room surface, displaying the room visually
            rect: the boundary rectangle of the room
        '''
    def __init__(self, data, dir='backgrounds/'):
        super(Background, self).__init__()
        path = 'Media/' + dir + data + '.csv'
        self.datafile = pandas.read_csv(path, index_col=0)

        self.animator = animator.Animator(pathname='Media/'+ dir + self.datafile.loc['animator', '2'], types=['main'])
        self.update_speed = self.datafile.loc['animator', '3']

        self.surf = self.animator.get_next('main')
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(left=int(self.datafile.loc['place', '2']), top=int(self.datafile.loc['place', '3']))

    def update(self, screen):
        ''' Updates the Background on a screen and animates it
        :param screen: The screen to update to
        '''
        self.surf = self.animator.get_next('main', self.update_speed)
        screen.blit(self.surf, self.rect)

class Room(Background):
    ''' A class designed to represent a room, inheriting from Background

    Attributes:
        same as background, but with the addition of
        spawn: the location designated as a player spawn, as a list x,y
        borders: the rectangular corners of a room [xmin, xmax, ymin, ymax]
        objects: a list of rects to use as obstacles that are impassable
    '''

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
            self.objects.append(pygame.Rect(object[0], object[1], object[2], object[3]))

    def get_spawn(self):
        ''' Accessor for the spawn location
        :return: the spawn location of the room as an [x,y] list
        '''
        return [self.spawn[0], self.spawn[1]]

    def get_objects(self):
        ''' Accessor for the room objects
        :return: all object rects as a list
        '''
        return self.objects


class Chatbox(pygame.sprite.Sprite):
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
        self.phrase = phrase

    def _process_speech(self, speed):
        self.index += 1
        if math.floor(self.index * speed) <= len(self.phrase):
            processed = self.phrase[0:math.floor(self.index * speed)]
        elif math.floor(self.index * speed) > len(self.phrase) * (1 + 50/(len(self.phrase)+1)):
            self.index = 0
            self.phrase = ''
            processed = ''
        else:
            processed = self.phrase

        return processed

    def update(self, screen):
        processed = textwrap.fill(self._process_speech(0.6), 19).split('\n')
        if len(self.phrase) > 0:
            x = self.sprite.get_pos()[0]
            y = self.sprite.get_pos()[1]
            self.rect.centerx = x
            self.rect.centery = y-130
            screen.blit(self.surf, self.rect)
            i = 0
            for part in processed[-4:]:
                screen.blit(self.font.render(part, True, (0, 0, 0)),
                            (self.rect.left + 8, self.rect.top + 90 + i))
                i += 15

