import pygame
import helpers
from pygame.locals import RLEACCEL
import math
import textwrap
import interactables
import character


class Background(helpers.DataSprite):
    """
    A class representing a background, inheriting from Datasprite

    Extracts attributes from a csv file.

    The reason this is a separate class is to maintain consistency. This
    allows us to set 'dir' as 'backgrounds/' for all instances of this class.
    """
    def __init__(self, data):
        """
        Initialize an instance of class Background.
        Args:
            data:
        """
        super().__init__(data, 'backgrounds/')


class Room(helpers.DataSprite):
    """
    A class representing a room, inheriting from DataSprite.

    Attributes:
        objects: a list of rects to use as obstacles that are impassable
        entrances: a list of lists. Each list represents an entrance, with the
            first two elements representing the x and y coordinates and the
            third element representing the room the player has come from
        exits: a list of lists. Each list represents an exit. The first two
            elements represent the coordinates the exit begins at, and the
            second two represent how many pixels the exit extends in the x and
            y direction. The final element represents the room the exit leads
            to
        interactables: a list of lists. Each list represents an interactable,
            where the first element is a string representing the name of the
            interactable and the second element is an int representing the end
            state of the interactable in that room
        npcs: a list of instances of NPC objects, representing all the NPCs in
            a room
    """

    def __init__(self, data):
        """
        Initializes an instance of Room.

        Args:
            data: string representing the room folder (NOT the path to the
                folder) to find the .csv in.
        """
        super().__init__(data, 'rooms/')
        # Initializes all the objects (boundaries) of the room
        self.objects = []
        for object in self._datafile.loc['objects'].dropna().values.tolist():
            object = [int(obj) for obj in object.split('/')]
            self.objects.append(pygame.Rect(object[0]+self._rect.left,
                                            object[1]+self._rect.top,
                                            object[2], object[3]))
        # Initializes the room's entrances from the csv
        self.entrances = []
        for object in self._datafile.loc['entrances'].dropna().values.tolist():
            object = [obj for obj in object.split('/')]
            self.entrances.append([int(object[0]), int(object[1]), str(object[2])])
        # Initializes the room's exits from the csv
        self.exits = []
        for object in self._datafile.loc['exits'].dropna().values.tolist():
            object = [obj for obj in object.split('/')]
            self.exits.append([pygame.Rect(int(object[0]),
                                           int(object[1]),
                                           int(object[2]), int(object[3])),
                               str(object[4])])
        # Initializes the room's interactables from the csv
        self.interactables = []
        for item in self._datafile.loc['interactables'].dropna().values.tolist():
            item = [i for i in item.split('/')]
            self.interactables.append(interactables.Interactable(str(item[2]), str(item[3])))
            self.interactables[-1].place(int(item[0]), int(item[1]))
        # Initializes the room's npcs from the csv
        self.npcs = []
        for npc in self._datafile.loc['npcs'].dropna().values.tolist():
            npc = [i for i in npc.split('/')]
            self.npcs.append(character.NPC(str(npc[2])))
            self.npcs[-1].spawn(int(npc[0]), int(npc[1]))

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
        Accessor for the room exits.

        Returns:
            a list containing all the exits.
        """
        return self.exits

    def get_objects(self):
        """
        Accessor for the room objects.

        Returns:
             all object rects as a list
        """
        return self.objects

    def draw_objects(self, screen):
        """
        Draw the currently established room boundaries in bright blue.

        This is a debugging function useful for determining and adjusting
        room boundaries in .csv files. It may also be useful in conjunction
        with the `draw_objects` function in the Room class to determine if
        the character rect or boundaries are causing movement problems.

        Args:
            screen: the screen to draw to
        """
        for rect in self.objects:
            pygame.draw.rect(surface=screen, rect=rect,
                             color=pygame.Color(0,0,255))

    def is_clear(self):
        """
        Determine if all the criteria to pass a room have been met.

        This function currently only checks that all interactables are in
        their end state, but in future could also contain other data such as
        whether NPCs have been collided with.

        Returns:
            True if all criteria have been met, False otherwise
        """
        for interactable in self.interactables:
            if not interactable.is_end_state():
                return False
        return True

    def update(self, screen, player):
        """
        Update the room drawing, interactables, and npcs.

        Args:
            screen: The screen to draw to
            player: The player instance to check for interaction
        """
        super().update(screen)
        # Updates all of the room's interactables
        for interactable in self.interactables:
            interactable.update(screen, player)
        # Updates all of the room's npcs
        for npc in self.npcs:
            npc.update(screen)


class Chatbox(pygame.sprite.Sprite):
    """
    Class representing a textbox for characters to speak. Inherits from Pygame
    Sprite class.

    Attributes:
        _surf: the image representing the chatbox
        _rect: contains the location of the chatbox
        _phrase: string containing the phrase to be said
        _index: int representing how many lines are left to say
        _font: the font to render the text in
        _sprite: the character speaking
        _past_phrases: list of phrases (strings) that have already been said.
            Note this does not store all phrases a character says. It is only
            used when the method say_once is called to prevent a character
            repeating things every time an in-game condition is met
    """
    def __init__(self, sprite):
        super().__init__()
        self._surf = pygame.image.load('Media/misc/chatbox-2.png')
        self._surf.set_colorkey((255, 255, 255), RLEACCEL)
        self._rect = self._surf.get_rect()
        self._phrase = ''
        self._index = 0
        self._font = pygame.font.Font('Media/fonts/iAWriterDuospace-Bold.otf', 15)
        self._sprite = sprite
        self._past_phrases = []

    def say(self, phrase):
        """
        Defines a phrase to be said

        Args:
            phrase: string containing the phrase
        """
        self._phrase = phrase

    def say_once(self, phrase):
        """
        Defines a phrase to be said and not repeated.

        This is in contrast to say above. If say is used, the character will
        repeat the phrase every time the appropriate conditions are met. For
        instance, if an NPC says something when a character bumps into them,
        using say() will cause the NPC to say the phrase every time the
        character bumps into them, while using say_once() will cause the NPC
        to say the phrase only the first time the character bumps into them.
        Args:
            phrase: String containing the phrase to be said
        """
        if phrase not in self._past_phrases:
            self._phrase = phrase
            self._past_phrases.append(phrase)

    def is_speaking(self):
        """
        Determine if a character is speaking or not.

        Returns:
            True if phrase is not empty, False otherwise
        """
        return self._phrase != ''

    def _process_speech(self, speed):
        """
        Split the phrase into chunks that will fit in the chatbox.

        Args:
            speed: the speed in ticks that the phrase should scroll in the
                chatbox.

        Returns:
            a list containing the phrase broken into strings that will fit in
                the chatbox

        """
        self._index += 1
        # If there is still stuff left to say, say it at the specified speed
        if math.floor(self._index * speed) <= len(self._phrase):
            processed = self._phrase[0:math.floor(self._index * speed)]
        # If there isn't anything left to say, only terminate the speech after
        # a short delay. The delay is inversely proportional to the length of
        # the phrase.
        elif math.floor(self._index * speed) > len(self._phrase) * \
                        (1 + 50/(len(self._phrase)+1)):
            self._index = 0
            self._phrase = ''
            processed = ''
        # If the short delay hasn't been met, say the full phrase
        else:
            processed = self._phrase

        return processed

    def update(self, screen):
        """
        Draw the text and chatbox in the game.

        For long phrases, this will create a scrolling effect as text from the
        phrase disappears to make space for more

        Args:
            screen: the screen to draw to
        """
        # Split the speech into lines that can fit in the chatbox
        processed = textwrap.fill(self._process_speech(0.6), 19).split('\n')
        # If the phrase length is greater than zero, display the chatbox with
        # the phrase in it
        if len(self._phrase) > 0:
            # Define position of the chatbox based on the character saying it
            x = self._sprite.get_pos()[0]
            y = self._sprite.get_pos()[1]
            self._rect.centerx = x
            self._rect.centery = y-130
            # Show the chatbox
            screen.blit(self._surf, self._rect)
            # Display the text. If it's long, show only the last four lines.
            # This creates a scrolling effect
            i = 0
            for part in processed[-4:]:
                screen.blit(self._font.render(part, True, (0, 0, 0)),
                            (self._rect.left + 8, self._rect.top + 90 + i))
                # Increment line height so text doesn't print on top of itself
                i += 15


class Guide(helpers.DataSprite):
    """
    Class representing the guidebook that assists the player throughout the
    game. Inherits from DataSprite.

    Attributes:
        _state: string representing the current state of the guide. Can be
            'open', 'close', or 'not' (for notification)
        _font: the font to render the guide text in
        _lines: list of lines read from a txt file that the guide will display
        _current_index: int representing the currently displayed line's index
         in _lines
    """
    def __init__(self):
        """
        Initialize an instance of the guide class
        """
        super().__init__('guide', 'misc/')
        self._state = 'close'
        self._font = pygame.font.Font('Media/fonts/iAWriterDuospace-Bold.otf', 30)
        with open('Media/misc/guide/guide.txt') as f:
            lines = f.readlines()
        self._lines = [line.strip() for line in lines]
        self._current_index = 0

    def update(self, screen, player):
        """
        Special update function for Guide. Update graphic to the current
        state the guide is in

        Args:
            screen: the screen to draw to
            player: the instance of Player to check if the guide is in use
        """
        if player.is_guiding():
            self.toggle()
        self._surf = self._animator.get_next(self._state)
        screen.blit(self._surf, self._rect)
        if self._state == 'open':
            self.display_text(screen)

    def get_index(self):
        """
        Accessor for _current_index.

        Returns:
            int representing _current_index
        """
        return self._current_index

    def notification(self):
        """
        Show a notification
        """
        self._state = 'not'

    def toggle(self):
        """
        Toggle the guide state to open or close the guide
        """
        if self._state == 'not' or self._state == 'close':
            self._state = 'open'
        else:
            self._state = 'close'

    def update_text(self, idx=''):
        """
        Display more lines of the guide and show a notification to the player.

        Args:
            idx: the index  to update to. Defaults to '', which causes the
            guide 

        Returns:

        """
        if idx == '':
            self._current_index += 1
            self.notification()
        elif idx > self._current_index:
            self._current_index = idx
            self.notification()

    def display_text(self, screen):
        """

        Args:
            screen:

        Returns:

        """
        # Split the speech into lines that can fit in the chatbox
        processed = []
        numlines = 32  # make this even
        for i in range(min(self._current_index * 2, len(self._lines)-1), -1, -1):
            next_step = textwrap.fill(self._lines[i], 19).split('\n')
            if(len(processed) + len(next_step) > numlines):
                break
            processed = next_step + processed
        # If the phrase length is greater than zero, display the chatbox with
        # the phrase in it
        for i in range(0, min(numlines//2, len(processed))):
            # Display the text. If it's long, show only the last four lines.
            # This creates a scrolling effect
            screen.blit(self._font.render(processed[i], True, (0, 0, 0)),
                        (150, 100 + (i * 30)))
        for j in range(numlines//2, min(numlines, len(processed))):
            screen.blit(self._font.render(processed[j], True, (0, 0, 0)),
                        (570, 100  + ((j - numlines//2) * 30)))



