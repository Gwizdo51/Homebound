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

    # def __init__(self, window_width: int, window_height: int):
    def __init__(self, game_config: dict[str]):
        # self.game_config = game_config
        # init the game data
        # self.game_data = GameData(window_width=window_width, window_height=window_height)
        self.game_data = GameData(game_config)
        # store the scenes in a dict
        # self.scenes: dict[str, Scene] = {
        #     "main menu": SceneMainMenu(self.game_data),
        #     "colony": SceneColony(self.game_data),
        #     "solar system map": SceneSolarSystemMap(self.game_data),
        #     "pause menu": ScenePauseMenu(self.game_data)
        # }
        self.scenes_types_dict = {
            "main menu": SceneMainMenu,
            "colony": SceneColony,
            "solar system map": SceneSolarSystemMap,
            "pause menu": ScenePauseMenu
        }
        # start the game with the main menu
        # self.current_scene = "main menu"
        # self.current_scene = "colony"
        # self.current_scene_name = "main menu"
        self.current_scene_name = "colony"
        self.current_scene: Scene = self.scenes_types_dict[self.current_scene_name](self.game_data)

    def switch_scene(self, new_scene_name: str):
        # switch scene only if needed
        if new_scene_name != self.current_scene_name:
            self.current_scene_name = new_scene_name
            self.current_scene: Scene = self.scenes_types_dict[new_scene_name](self.game_data)

    def on_mouse_press(self, x, y, button, modifiers):
        # print("game manager mouse press")
        # self.current_scene = self.scenes[self.current_scene].on_mouse_press(x, y, button, modifiers)
        new_scene_name = self.current_scene.on_mouse_press(x, y, button, modifiers)
        self.switch_scene(new_scene_name)

    def on_mouse_motion(self, x, y, dx, dy):
        # print(f"mouse position: {x} {y}")
        # print("game manager on_mouse_motion call")
        # self.scenes[self.current_scene].on_mouse_motion(x, y)
        self.current_scene.on_mouse_motion(x, y)

    def on_key_press(self, symbol, modifiers):
        # self.current_scene = self.scenes[self.current_scene].on_key_press(symbol, modifiers)
        new_scene_name = self.current_scene.on_key_press(symbol, modifiers)
        self.switch_scene(new_scene_name)

    def update(self, dt):
        # update the game state
        self.game_data.update(dt)
