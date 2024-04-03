from pyglet.text import Label
import pyglet.shapes as shapes
from pyglet.sprite import Sprite
from pyglet.window import key, mouse
import sys
from pathlib import Path

ROOT_DIR_PATH = str(Path(__file__).resolve().parents[1])
if ROOT_DIR_PATH not in sys.path:
    sys.path.insert(0, ROOT_DIR_PATH)

from lib.scenes.scene_interface import Scene
from lib.game_data import GameData


class SceneSolarSystemMap(Scene):

    def __init__(self, game_data: GameData):
        super().__init__(game_data)


    def draw(self):
        self.game_data.game_paused = False

        # udpate the batch

        # draw the batch
        self.batch.draw()


    def on_mouse_press(self, x, y, button, modifiers) -> str:
        return "solar system map"


    def on_mouse_motion(self, x, y):
        self.game_data.mouse_x, self.game_data.mouse_y = x, y
        self.game_data.mouse_clickable_area = False


    def on_key_press(self, symbol, modifiers) -> str:
        return "solar system map"
