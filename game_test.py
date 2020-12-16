import pytest
import environment
import character
import interactables
import pygame

pygame.init()

# game1 = game.Game()
# 500 / 250 / 125 room height
SCREEN_HEIGHT = 700  # 350 or 175 or 88
SCREEN_WIDTH = 1080  # 540 or 270 or 135

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Initialize one of each type for testing
test_room = environment.Room('testroom')

test_char = character.Player('testcharacter')
test_char.spawn(test_room, 'maze')
test_char.spotlight_on()

test_interact = interactables.Interactable('testinteract')
test_interact.place(50, 490)


@pytest.mark.parametrize("actual,expected", [
    (test_room.name, 'testroom'),
    (len(test_room.get_exits()), 1),
    (test_room.interactables[0].name, 'piano'),
    (test_room.is_clear(), False),
    (test_room.interactables, [['piano', 2]]),
    (test_room.entrances, [[50, 480, 'maze']])
])
def test_room(actual, expected):
    assert actual == expected


@pytest.mark.parametrize("actual,expected", [
    (test_char.name, 'testcharacter'),
    (test_char.get_pos(), [50, 480]),
    (test_char.collide(test_interact), True),
    (test_char._spotlight, True)
])
def test_char(actual, expected):
    assert actual == expected


@pytest.mark.parametrize("actual,expected", [
    (test_interact.name, 'testinteract'),
    (test_interact.is_end_state(), True),

])
def test_interact(actual, expected):
    assert actual == expected
