# Misguided: The Game

This is a repository for the game *Misguided*, created by Annabelle Platt and Tigey Jewell-Alibhai.

The game is built on a modular framework. It can be downloaded and played as is or it can be easily modified. Or, the game content can be ignored and a new game can be built on the same framework. For details, see the sections *File Structure* and *Using CSVs as a Framework*. 

## Installation and Setup

The main installation required for this project is conda python (3.8) which can be installed from the following link: https://docs.conda.io/projects/conda/en/latest/user-guide/install/

This project also requires pygame, which can be installed from https://www.pygame.org/wiki/GettingStarted

Although not required to be able to run the game, the test framework for this project requires pytest, which can be found here https://docs.pytest.org/en/stable/getting-started.html

## File Structure

The file structure for this project consists of the following .py files:

* `main.py` runs the game. Run this file to play the game.

* `game.py` contains the overarching game loop and integration of objects into a storyline.

* `game_test.py` contains the pytests to veryfy the game works.

* `character.py`, `environment.py`, `interactables.py` contain objects that represent features in the game, such as the player, rooms, backgrounds, interactables, etc.

* `helpers.py` contains helper classes that assist the main classes in completing actions such as speaking and displaying images in motion.

The project also contains a `/docs` folder with the website content that displays through github pages.

The `/Media` folder contains most of the project information not stored in `.py` files including:

* Animator folders and CSV files for each instance of the feature objects (backgrounds, characters, interactables, and rooms) inside folders of the same name. Read *Using CSVs as a Framework* for more info on this.

* Misc animations not directly linked to an object, including Guide, Teleport, and Spotlight.

* Music for the game inside the `/music` folder (composed by Tigey)

* Backgrounds for the intro inside `/wallpaper` folder

* Fonts for the game inside `/fonts` (all open CC licenses)

## Using CSVs as a Framework 

Each folder for an object will contain subfolders for specific types of that object. For example, the `/character` folder will contain subfolders for `/turtle`, `/player`, `/tutorial_man`, etc.

These subfolders, contain a `.pixil` file which is the original pixel art format, along with a `.csv` with the same name as the folder, and a set of subfolders of various names.

The subfolders are used by the animator in `helpers.py` to define sets of motion, and each subfolder contains a set of images for that specific type. For example, the `/player` folder contains subfolders for `/front`, `/back`, `/left`, and `/right`, which each depict the player walking in that specific direction.

The `.csv` files contain data that varies from object to object. The first row defines what data the rest of the row includes. The first row of each .csv is numbered starting at 1 and ascending, to be used as the headers. The following are the `.csv` data that are used:

* animator: col 2 specifies the speed at which to animate the object. Smaller is slower, and must be 0 < speed <= 1. Can be changed in the code. Common among rooms, backgrounds, interactables, and characters.
* place: col 2 and col 3 contain x and y positions respectively of where to initially place the top left corner of the object. Common among rooms and backgrounds.
* initial_state: col 2 specifies the starting state of an interactable as an integer. Common among interactables.
* objects: each col represents the `topleft_x/topleft_y/width_x/height_y` of a boundary rectangle in the room that a player cannot pass. Common among rooms.
* entrances: each col represents an entrance point for a player in the form `x/y/name_of_room_to_enter_from`. Common among rooms.
* exits: each col represents an exit rectangle for a player in the form `topleft_x/topleft_y/width_x/height_y/room_to_exit_to`. Common among all rooms.
* interactables: define interactables contained in a room instance, which will be initialized by the room in the form `x_pos/y_pox/name_of_interactable/end_state` where end state determines if the room is clear based on the state of all interactables. Common among all rooms.
* npcs: define npcs contained in a room instance, which will be initialized by the room in the form `x_pos/y_pos/name_of_npc/`. Common among all rooms.