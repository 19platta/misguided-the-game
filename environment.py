import pygame
import helpers
from pygame.locals import RLEACCEL
import math
import textwrap
import interactables
import character


class Background(helpers.DataSprite):
    """
    A class designed to represent a background
    Extracts attributes from a csv file.

    The reason this is a separate class is to maintain consistency. This
    allows us to set 'dir' as 'backgrounds/' for all instances of this class.
    """
    def __init__(self, data):
        super().__init__(data, 'backgrounds/')


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
        super().__init__(data, 'rooms/')

        self.borders = self.datafile.loc['borders'].dropna().values.tolist()
        self.borders = [int(border) for border in self.borders]

        self.objects = []
        for object in self.datafile.loc['objects'].dropna().values.tolist():
            object = [int(obj) for obj in object.split('/')]
            self.objects.append(pygame.Rect(object[0]+self.rect.left,
                                            object[1]+self.rect.top,
                                            object[2], object[3]))

        self.entrances = []
        for object in self.datafile.loc['entrances'].dropna().values.tolist():
            object = [obj for obj in object.split('/')]
            self.entrances.append([int(object[0]), int(object[1]), str(object[2])])

        self.exits = []
        for object in self.datafile.loc['exits'].dropna().values.tolist():
            object = [obj for obj in object.split('/')]
            self.exits.append([pygame.Rect(int(object[0]) + self.rect.left,
                                           int(object[1]) + self.rect.top,
                                           int(object[2]), int(object[3])),
                               str(object[4])])
        self.interactables = []
        for item in self.datafile.loc['interactables'].dropna().values.tolist():
            item = [i for i in item.split('/')]
            self.interactables.append(interactables.Interactable(str(item[2]), str(item[3])))
            self.interactables[-1].place(int(item[0]), int(item[1]))
        self.npcs = []
        for npc in self.datafile.loc['npcs'].dropna().values.tolist():
            npc = [i for i in npc.split('/')]
            self.npcs.append(character.NPC(str(npc[2])))
            self.npcs[-1].move(int(npc[0]), int(npc[1]))

    def get_entrance(self, str):
        """
        Finds the correct entrance to a room based on where the player
        is entering from.

        Returns:
            the spawn location of the room as an [x,y] list
        """
        for entrance in self.entrances:
            if entrance[2] == str:
                return [entrance[0], entrance[1]]

    def get_exits(self):
        """
        Access all possible exits from the room.

        Returns:
            a list containing all the exits.
        """
        return self.exits

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

    def is_clear(self):
        """
        Determine if all the criteria to pass a room have been met.

        Returns:
            True if all criteria have been met, False otherwise
        """
        for interactable in self.interactables:
            if not interactable.is_end_state():
                return False
        return True

    def update(self, screen, player):
        """

        """
        super().update(screen)
        for interactable in self.interactables:
            interactable.update(screen, player)
        for npc in self.npcs:
            npc.update(screen)


class Chatbox(pygame.sprite.Sprite):
    """

    """
    def __init__(self, sprite):
        super().__init__()
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
        """
        Initialize an instance of the guide class
        """
        super().__init__('guide', 'misc/')
        self.state = 'close'
        self.font = pygame.font.Font('Media/fonts/iAWriterDuospace-Bold.otf', 30)
        with open('Media/misc/guide/guide.txt') as f:
            lines = f.readlines()
        self.lines = [line.strip() for line in lines]
        self.current_index = 0

    def update(self, screen, player):
        """
        Special update function for Guide. Update graphic to the current
        state the guide is in
        """
        if player.is_guiding():
            self.toggle()
        self.surf = self.animator.get_next(self.state)
        screen.blit(self.surf, self.rect)
        if self.state == 'open':
            self.display_text(screen)

    def notification(self):
        """
        Show a notification
        """
        self.state = 'not'

    def toggle(self):
        """
        Toggle the guide state to open or close the guide
        """
        if self.state == 'not' or self.state == 'close':
            self.state = 'open'
        else:
            self.state = 'close'

    def update_text(self):
        self.current_index += 1

    def display_text(self, screen):
        """

        Args:
            screen:

        Returns:

        """
        # Split the speech into lines that can fit in the chatbox
        processed = []
        numlines = 32  # make this even
        for i in range(min(self.current_index * 2, len(self.lines)-1), -1, -1):
            next_step = textwrap.fill(self.lines[i], 19).split('\n')
            if(len(processed) + len(next_step) > numlines):
                break
            processed = next_step + processed
        # If the phrase length is greater than zero, display the chatbox with
        # the phrase in it
        for i in range(0, min(numlines//2, len(processed))):
            # Display the text. If it's long, show only the last four lines.
            # This creates a scrolling effect
            screen.blit(self.font.render(processed[i], True, (0, 0, 0)),
                        (150, 100 + (i * 30)))
        for j in range(numlines//2, min(numlines, len(processed))):
            screen.blit(self.font.render(processed[j], True, (0, 0, 0)),
                        (570, 100  + ((j - numlines//2) * 30)))



