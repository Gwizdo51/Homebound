import sys
from pathlib import Path

ROOT_DIR_PATH = str(Path(__file__).resolve().parents[1])
if ROOT_DIR_PATH not in sys.path:
    sys.path.insert(0, ROOT_DIR_PATH)

from lib.scenes.scene_interface import Scene
from lib.scenes.scene_main_menu import SceneMainMenu
from lib.scenes.scene_colony import SceneColony
from lib.scenes.scene_solar_system_map import SceneSolarSystemMap
from lib.scenes.scene_pause_menu import ScenePauseMenu
from lib.game_data import GameData


class GameManager:
    "handles the communication between the window, the game state and the scenes"

    def __init__(self, window_width: int, window_height: int):
        # init the game data
        self.game_data = GameData(window_width=window_width, window_height=window_height)
        # store the scenes in a dict
        self.scenes: dict[str, Scene] = {
            "main menu": SceneMainMenu(self.game_data),
            "colony": SceneColony(self.game_data),
            "solar system map": SceneSolarSystemMap(self.game_data),
            "pause menu": ScenePauseMenu(self.game_data)
        }
        # start the game with the main menu
        # self.current_scene = "main menu"
        self.current_scene = "colony"

    def on_mouse_press(self, x, y, button, modifiers):
        # print("game manager mouse press")
        self.current_scene = self.scenes[self.current_scene].on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        # print(f"mouse position: {x} {y}")
        # print("game manager on_mouse_motion call")
        self.scenes[self.current_scene].on_mouse_motion(x, y)

    def on_key_press(self, symbol, modifiers):
        self.current_scene = self.scenes[self.current_scene].on_key_press(symbol, modifiers)

    def update(self, dt):
        # update the game state
        self.game_data.update(dt)
