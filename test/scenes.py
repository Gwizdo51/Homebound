import pyglet.shapes as shapes
from pyglet.graphics import Batch
from pyglet.text import Label
from pyglet.window import key, mouse
import abc

from game_state import GameState


# class Scene:

#     def __init__(self, game_state: GameState):
#         self.game_state = game_state
#         self.batch = Batch()

#     def draw(self):
#         # prototype
#         raise NotImplementedError("method not implemented")

#     def on_mouse_press(self, x, y, button, modifiers) -> str:
#         # prototype
#         return ""


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
        "Reacts to the mouse position"
        raise NotImplementedError


class SceneMainMenu(Scene):

    def __init__(self, game_state: GameState):
        # self.game_state = game_state
        # self.batch = Batch()
        super().__init__(game_state)

        # populate the batch

        # menu title
        self.title = Label("MAIN MENU", font_name=self.game_state.font, font_size=32, bold=True,
                           x=self.game_state.window_width/2, y=self.game_state.window_height*3/4,
                           anchor_x="center", anchor_y="center", batch=self.batch)

        # submenu 1 button + counter
        self.button_submenu_1 = shapes.Rectangle(x=self.game_state.window_width/2 - 100, y=self.game_state.window_height/2 - 25,
                                                 width = 200, height=45, batch=self.batch)
        self.button_submenu_1_label = Label("Option 1", font_name=self.game_state.font, font_size=25,
                                            x=self.game_state.window_width/2 - 100, y=self.game_state.window_height/2, anchor_y="center",
                                            width = 200, align="center", batch=self.batch,
                                            color=(0,0,0,255))
        self.submenu_1_clicks_label = Label(f"submenu 1 clicks : {self.game_state.submenu_1_clicks}", font_name=self.game_state.font, font_size=13,
                                            x=self.game_state.window_width/2 + 125, y=self.game_state.window_height/2, anchor_y="center",
                                            batch=self.batch)

        # submenu 2 button + counter
        self.button_submenu_2 = shapes.Rectangle(x=self.game_state.window_width/2 - 100, y=self.game_state.window_height/2 - 100,
                                                 width = 200, height=45, batch=self.batch)
        self.button_submenu_2_label = Label("Option 2", font_name=self.game_state.font, font_size=25,
                                            x=self.game_state.window_width/2 - 100, y=self.game_state.window_height/2 - 75, anchor_y="center",
                                            width = 200, align="center", batch=self.batch,
                                            color=(0,0,0,255))
        self.submenu_2_clicks_label = Label(f"submenu 2 clicks : {self.game_state.submenu_2_clicks}", font_name=self.game_state.font, font_size=13,
                                            x=self.game_state.window_width/2 + 125, y=self.game_state.window_height/2 - 75, anchor_y="center",
                                            batch=self.batch)

        # submenu 3 button + counter
        self.button_submenu_3 = shapes.Rectangle(x=self.game_state.window_width/2 - 100, y=self.game_state.window_height/2 - 175,
                                                 width = 200, height=45, batch=self.batch)
        self.button_submenu_3_label = Label("Option 3", font_name=self.game_state.font, font_size=25,
                                            x=self.game_state.window_width/2 - 100, y=self.game_state.window_height/2 - 150, anchor_y="center",
                                            width = 200, align="center", batch=self.batch,
                                            color=(0,0,0,255))
        self.submenu_3_clicks_label = Label(f"submenu 3 clicks : {self.game_state.submenu_3_clicks}", font_name=self.game_state.font, font_size=13,
                                            x=self.game_state.window_width/2 + 125, y=self.game_state.window_height/2 - 150, anchor_y="center",
                                            batch=self.batch)

    def draw(self):
        # update the batch according to the game state
        self.submenu_1_clicks_label.text = f"submenu 1 clicks : {self.game_state.submenu_1_clicks}"
        self.submenu_2_clicks_label.text = f"submenu 2 clicks : {self.game_state.submenu_2_clicks}"
        self.submenu_3_clicks_label.text = f"submenu 3 clicks : {self.game_state.submenu_3_clicks}"
        # update the mouse cursor
        # self.on_mouse_motion(self.game_state.mouse_x, self.game_state.mouse_y)
        # draw the batch
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers) -> str:
        # print("scene mouse press")
        new_scene = "main menu"
        if button & mouse.LEFT:
            # if self.game_state.window_width/2 - 100 <= x <= self.game_state.window_width/2 + 100:
            #     if self.game_state.window_height/2 - 25 <= y <= self.game_state.window_height/2 + 20:
            #         # print("submenu 1 left-clicked")
            #         new_scene = "sub menu 1"
            #     elif self.game_state.window_height/2 - 100 <= y <= self.game_state.window_height/2 - 55:
            #         # print("submenu 2 left-clicked")
            #         new_scene = "sub menu 2"
            #     elif self.game_state.window_height/2 - 175 <= y <= self.game_state.window_height/2 - 130:
            #         # print("submenu 3 left-clicked")
            #         new_scene = "sub menu 3"
            if (x, y) in self.button_submenu_1:
                new_scene = "sub menu 1"
            elif (x, y) in self.button_submenu_2:
                new_scene = "sub menu 2"
            elif (x, y) in self.button_submenu_3:
                new_scene = "sub menu 3"
        return new_scene

    def on_mouse_motion(self, x, y):
        # print(f"scene on_mouse_motion call {x} {y}")
        self.game_state.mouse_x, self.game_state.mouse_y = x, y
        self.game_state.mouse_clickable_area = ((x, y) in self.button_submenu_1) or ((x, y) in self.button_submenu_2) or ((x, y) in self.button_submenu_3)


class SceneSubMenu1(Scene):

    def __init__(self, game_state: GameState):
        # self.game_state = game_state
        # self.batch = Batch()
        super().__init__(game_state)

        # populate the batch

        # menu title
        self.title = Label("SUBMENU 1", font_name=self.game_state.font, font_size=32, bold=True,
                           x=self.game_state.window_width/2, y=self.game_state.window_height*3/4,
                           anchor_x="center", anchor_y="center", batch=self.batch)

        # clickable shape
        self.clickable_shape = shapes.Circle(x=self.game_state.window_width/2, y=self.game_state.window_height/2, radius=75, batch=self.batch)
        self.clicks_counter = Label(f"clicks : {self.game_state.submenu_1_clicks}", font_name=self.game_state.font, font_size=15,
                                    x=self.game_state.window_width/2, y=self.game_state.window_height/2 - 150, anchor_x="center", batch=self.batch)

    def draw(self):
        # update the scene according to the game state
        self.clicks_counter.text = f"clicks : {self.game_state.submenu_1_clicks}"
        # draw the batch
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers) -> str:
        new_scene = "main menu"
        if button & mouse.LEFT:
            if (x, y) in self.clickable_shape:
                # print("clicked on shape")
                self.game_state.submenu_1_clicks += 1
                new_scene = "sub menu 1"
        return new_scene

    def on_mouse_motion(self, x, y):
        self.game_state.mouse_x, self.game_state.mouse_y = x, y
        self.game_state.mouse_clickable_area = (x, y) in self.clickable_shape


class SceneSubMenu2(Scene):

    def __init__(self, game_state: GameState):
        # self.game_state = game_state
        # self.batch = Batch()
        super().__init__(game_state)

        # populate the batch

        # menu title
        self.title = Label("SUBMENU 2", font_name=self.game_state.font, font_size=32, bold=True,
                           x=self.game_state.window_width/2, y=self.game_state.window_height*3/4,
                           anchor_x="center", anchor_y="center", batch=self.batch)

        # clickable shape
        self.clickable_shape = shapes.Rectangle(x=self.game_state.window_width/2 - 50, y=self.game_state.window_height/2 - 50, width=100, height=100, batch=self.batch)
        self.clicks_counter = Label(f"clicks : {self.game_state.submenu_2_clicks}", font_name=self.game_state.font, font_size=15,
                                    x=self.game_state.window_width/2, y=self.game_state.window_height/2 - 150, anchor_x="center", batch=self.batch)

    def draw(self):
        # update the scene according to the game state
        self.clicks_counter.text = f"clicks : {self.game_state.submenu_2_clicks}"
        # draw the batch
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers) -> str:
        new_scene = "main menu"
        if button & mouse.LEFT:
            if (x, y) in self.clickable_shape:
                # print("clicked on shape")
                self.game_state.submenu_2_clicks += 1
                new_scene = "sub menu 2"
        return new_scene

    def on_mouse_motion(self, x, y):
        self.game_state.mouse_x, self.game_state.mouse_y = x, y
        self.game_state.mouse_clickable_area = (x, y) in self.clickable_shape


class SceneSubMenu3(Scene):

    def __init__(self, game_state: GameState):
        # self.game_state = game_state
        # self.batch = Batch()
        super().__init__(game_state)

        # populate the batch

        # menu title
        self.title = Label("SUBMENU 3", font_name=self.game_state.font, font_size=32, bold=True,
                           x=self.game_state.window_width/2, y=self.game_state.window_height*3/4,
                           anchor_x="center", anchor_y="center", batch=self.batch)

        # clickable shape
        self.clickable_shape = shapes.Star(x=self.game_state.window_width/2, y=self.game_state.window_height/2, outer_radius=100, inner_radius=30, num_spikes=5, rotation=-90, batch=self.batch)
        self.clicks_counter = Label(f"clicks : {self.game_state.submenu_3_clicks}", font_name=self.game_state.font, font_size=15,
                                    x=self.game_state.window_width/2, y=self.game_state.window_height/2 - 150, anchor_x="center", batch=self.batch)

    def draw(self):
        # update the scene according to the game state
        self.clicks_counter.text = f"clicks : {self.game_state.submenu_3_clicks}"
        # draw the batch
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers) -> str:
        new_scene = "main menu"
        if button & mouse.LEFT:
            if (x, y) in self.clickable_shape:
                # print("clicked on shape")
                self.game_state.submenu_3_clicks += 1
                new_scene = "sub menu 3"
        return new_scene

    def on_mouse_motion(self, x, y):
        self.game_state.mouse_x, self.game_state.mouse_y = x, y
        self.game_state.mouse_clickable_area = (x, y) in self.clickable_shape


if __name__ == "__main__":
    print(issubclass(SceneMainMenu, Scene))
    print(issubclass(SceneSubMenu1, Scene))
    print(issubclass(SceneSubMenu2, Scene))
    print(issubclass(SceneSubMenu3, Scene))
