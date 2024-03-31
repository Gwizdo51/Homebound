from pyglet.graphics import Batch
import abc
import sys
from pathlib import Path

ROOT_DIR_PATH = str(Path(__file__).resolve().parents[1])
if ROOT_DIR_PATH not in sys.path:
    sys.path.insert(0, ROOT_DIR_PATH)

from lib.game_state import GameState


class Scene(metaclass=abc.ABCMeta):

    # @classmethod
    # def __subclasshook__(cls, subclass):
    #     return (hasattr(subclass, 'draw') and callable(subclass.draw) and
    #             hasattr(subclass, 'extract_text') and callable(subclass.extract_text) or
    #             NotImplemented)

    def __init__(self, game_state: GameState):
        if type(self) is Scene:
            raise TypeError("The Scene class should not be instanciated directly")
        self.game_state = game_state
        self.batch = Batch()

    @abc.abstractmethod
    def draw(self) -> None:
        "Updates and draws the scene in the window"
        raise NotImplementedError

    @abc.abstractmethod
    def on_mouse_press(self, x, y, button, modifiers) -> str:
        "Reacts to the user pressing a mouse button"
        raise NotImplementedError

    @abc.abstractmethod
    def on_mouse_motion(self, x, y):
        "Reacts to the user moving the mouse"
        raise NotImplementedError

    @abc.abstractmethod
    def on_key_press(self, symbol, modifiers) -> str:
        "Reacts to the user pressing a key"
        raise NotImplementedError
