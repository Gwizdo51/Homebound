from pyglet.text import Label
import pyglet.shapes as shapes
from pyglet.sprite import Sprite
from pyglet.window import key, mouse
from pyglet.graphics import Group
import sys
from pathlib import Path

ROOT_DIR_PATH = str(Path(__file__).resolve().parents[1])
if ROOT_DIR_PATH not in sys.path:
    sys.path.insert(0, ROOT_DIR_PATH)

from lib.scenes.scene_interface import Scene
from lib.game_data import GameData


class SceneColony(Scene):

    def __init__(self, game_data: GameData):
        super().__init__(game_data)
        # self.displayed_colony = None
        self.background_group = Group(order=0)
        self.middleground_group = Group(order=1)
        self.foreground_group = Group(order=2)

        # 7x7 building grid
        self.building_grid_lines = []
        # 8 horizontal lines
        self.building_tile_size = 75
        bulding_grid_lines_color = (30, 52, 82, 255)
        for horizontal_line_index in range(8):
            self.building_grid_lines.append(shapes.Line(
                x = (self.game_data.window_width / 2) - (3.5 * self.building_tile_size),
                y = (self.game_data.window_height / 2) - (3.5 * self.building_tile_size) + (horizontal_line_index * self.building_tile_size),
                x2 = (self.game_data.window_width / 2) + (3.5 * self.building_tile_size),
                y2 = (self.game_data.window_height / 2) - (3.5 * self.building_tile_size) + (horizontal_line_index * self.building_tile_size),
                width=7,
                color=bulding_grid_lines_color,
                batch=self.batch,
                group=self.middleground_group
            ))
        # 8 vertical lines
        for vertical_line_index in range(8):
            self.building_grid_lines.append(shapes.Line(
                x = (self.game_data.window_width / 2) - (3.5 * self.building_tile_size) + (vertical_line_index * self.building_tile_size) + 4,
                y = (self.game_data.window_height / 2) - (3.5 * self.building_tile_size),
                x2 = (self.game_data.window_width / 2) - (3.5 * self.building_tile_size) + (vertical_line_index * self.building_tile_size) + 4,
                y2 = (self.game_data.window_height / 2) + (3.5 * self.building_tile_size) + 7,
                width=7,
                color=bulding_grid_lines_color,
                batch=self.batch,
                group=self.middleground_group
            ))

        # left window
        self.left_window = Sprite(
            img=self.game_data.side_window,
            x=15,
            y=self.game_data.window_height // 2,
            batch=self.batch,
            group=self.middleground_group
        )
        # right window
        self.right_window = Sprite(
            img=self.game_data.side_window,
            x = self.game_data.window_width - self.game_data.side_window.width*2 - 15,
            y=self.game_data.window_height // 2,
            batch=self.batch,
            group=self.middleground_group
        )
        self.left_window.opacity = self.right_window.opacity = 170
        self.left_window.scale = self.right_window.scale = 2
        self.left_window.scale_y = self.right_window.scale_y = 1.5

        # left window static content
        self.left_window_content = {}
        # workers
        self.left_window_content["workers_label"] = Label("WORKERS", font_name=self.game_data.subtitle_font_name, font_size=20,
            x=25, y=self.game_data.window_height - 110, width=315,
            align="center", anchor_y="center", batch=self.batch, group=self.foreground_group)
        # worker icons
        self.left_window_content["engineers_icon"] = Sprite(
            img=self.game_data.icon_wrench_light_gray,
            x = self.left_window.width // 2 + 15 - 100,
            y = self.game_data.window_height - 160,
            batch=self.batch,
            group=self.foreground_group
        )
        self.left_window_content["engineers_icon"].scale = .15
        self.left_window_content["scientists_icon"] = Sprite(
            img=self.game_data.icon_vial_light_gray,
            x = self.left_window.width // 2 + 15,
            y = self.game_data.window_height - 160,
            batch=self.batch,
            group=self.foreground_group
        )
        self.left_window_content["scientists_icon"].scale = .15
        self.left_window_content["pilots_icon"] = Sprite(
            img=self.game_data.icon_plane_light_gray,
            x = self.left_window.width // 2 + 15 + 100,
            y = self.game_data.window_height - 160,
            batch=self.batch,
            group=self.foreground_group
        )
        self.left_window_content["pilots_icon"].scale = .15
        # workers counter label
        self.left_window_content["engineers_counter_label"] = Label("", font_name=self.game_data.default_font_name, font_size=12,
            x = self.left_window.width // 2 + 15 - 100,
            y = self.game_data.window_height - 200,
            anchor_x="center", batch=self.batch, group=self.foreground_group)
        self.left_window_content["scientists_counter_label"] = Label("", font_name=self.game_data.default_font_name, font_size=12,
            x = self.left_window.width // 2 + 15,
            y = self.game_data.window_height - 200,
            anchor_x="center", batch=self.batch, group=self.foreground_group)
        self.left_window_content["pilots_counter_label"] = Label("", font_name=self.game_data.default_font_name, font_size=12,
            x = self.left_window.width // 2 + 15 + 100,
            y = self.game_data.window_height - 200,
            anchor_x="center", batch=self.batch, group=self.foreground_group)
        # resources
        # spaceships
        # spaceship modules


    def draw(self):
        self.game_data.game_paused = False

        # udpate the batch

        # background sprite
        if self.game_data.active_colony == "moon":
            self.background_sprite = Sprite(img=self.game_data.moon_background_img, y = -550, batch=self.batch, group=self.background_group)
            self.background_sprite.scale = self.game_data.window_width / self.game_data.moon_background_img.width

        # colony name
        self.colony_name_label = Label(self.game_data.active_colony.upper(), font_name=self.game_data.subtitle_font_name, font_size=25,
            x=25, y=self.game_data.window_height - 42, width=315,
            align="center", anchor_y="center", batch=self.batch, group=self.foreground_group)

        # information to list in left window:
        # - workers (available / total) by type
        # - landed spaceships by type
        # - available spaceship modules by type
        # - resources:
        #     - power available / total
        #     - food (available + produced, positive or negative, every minute)
        #     - water (available + produced, positive or negative, every minute)
        #     - liquid oxygen (available / maximum storage + produced, positive or negative, every minute)
        #     - liquid hydrogen (available / maximum storage + produced every minute)
        #     - ore (available / maximum storage + produced every minute)
        #     - metal (available / maximum storage + produced every minute)

        # left window update
        self.left_window_content["engineers_counter_label"].text = f"{self.game_data.colonies[self.game_data.active_colony].workers["engineers"]["available"]}/{self.game_data.colonies[self.game_data.active_colony].workers["engineers"]["total"]}"
        self.left_window_content["scientists_counter_label"].text = f"{self.game_data.colonies[self.game_data.active_colony].workers["scientists"]["available"]}/{self.game_data.colonies[self.game_data.active_colony].workers["scientists"]["total"]}"
        self.left_window_content["pilots_counter_label"].text = f"{self.game_data.colonies[self.game_data.active_colony].workers["pilots"]}"

        # draw the batch
        self.batch.draw()


    def on_mouse_press(self, x, y, button, modifiers) -> str:
        return "colony"


    def on_mouse_motion(self, x, y):
        self.game_data.mouse_x, self.game_data.mouse_y = x, y
        self.game_data.mouse_clickable_area = False


    def on_key_press(self, symbol, modifiers) -> str:
        return "colony"
