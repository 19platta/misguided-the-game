import pytest
import environment
import character
import interactables
import game
import pygame

pygame.init()

#game1 = game.Game()
# 500 / 250 / 125 room height
SCREEN_HEIGHT = 700  # 350 or 175 or 88
SCREEN_WIDTH = 1080  # 540 or 270 or 135

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
#pygame.key.set_repeat(100, 100)

#clock = pygame.time.Clock()

# Initialize one of each type for testing
test_room = environment.Room('testroom')
test_char = character.Player('testcharacter')
test_background = environment.Background('testbackground')
test_interact = interactables.Interactable('testinteract')
test_char.spawn(test_room, 'maze')

@pytest.mark.parametrize("actual,expected", [
  (test_room.name, 'testroom'),
  (len(test_room.get_exits()), 1),
  (test_room.interactables[0].name, 'piano'),
  (test_room.is_clear(), False)
])
def test_room(actual, expected):
    assert actual == expected

@pytest.mark.parametrize("actual,expected", [
  (test_char.name, 'testcharacter'),
  (test_char.get_pos(), [50,480]),

])
def test_char(actual, expected):
    assert actual == expected
