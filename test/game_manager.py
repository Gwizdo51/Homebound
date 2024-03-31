from scenes import Scene, SceneMainMenu, SceneSubMenu1, SceneSubMenu2, SceneSubMenu3
from game_state import GameState


class GameManager:
    "handles the communication between the window, the game state and the scenes"

    def __init__(self, window_width: int, window_height: int):
        self.game_state = GameState(window_width=window_width, window_height=window_height)
        # print(self.game_state.submenu_1_clicks, self.game_state.submenu_2_clicks, self.game_state.submenu_3_clicks)
        # store the scenes in a dict
        self.scenes: dict[str, Scene] = {
        # self.scenes = {
            "main menu": SceneMainMenu(self.game_state),
            "sub menu 1": SceneSubMenu1(self.game_state),
            "sub menu 2": SceneSubMenu2(self.game_state),
            "sub menu 3": SceneSubMenu3(self.game_state)
        }
        # start the game with the main menu
        self.current_scene = "main menu"

    def on_mouse_press(self, x, y, button, modifiers):
        # print("game manager mouse press")
        self.current_scene = self.scenes[self.current_scene].on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        # pass
        # print(f"mouse position: {x} {y}")
        # print("game manager on_mouse_motion call")
        self.scenes[self.current_scene].on_mouse_motion(x, y)

    # def switch_scene(self, new_scene: str):
    #     self.current_scene = new_scene

    def update(self, dt):
        # update the game state
        self.game_state.update(dt)
