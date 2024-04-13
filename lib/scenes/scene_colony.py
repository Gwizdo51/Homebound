from pyglet.text import Label, HTMLLabel
import pyglet.shapes as shapes
from pyglet.sprite import Sprite
from pyglet.window import key, mouse
from pyglet.graphics import Group
import sys
from pathlib import Path

ROOT_DIR_PATH = str(Path(__file__).resolve().parents[2])
if ROOT_DIR_PATH not in sys.path:
    sys.path.insert(0, ROOT_DIR_PATH)

from lib.scenes.scene_interface import Scene
from lib.game_data import GameData


class BuildingWidget:

    def __init__(self, game_data, building_grid_line, building_grid_column):
        self.is_selected = False


class SceneColony(Scene):

    def __init__(self, game_data: GameData):
        super().__init__(game_data)
        # self.displayed_colony = None
        # from background to foreground
        self.groups = [Group(order) for order in range(6)]

        # 7x7 building grid
        self.building_grid_lines = []
        # 8 horizontal lines
        self.building_tile_size = 75
        self.bulding_grid_lines_color = (30, 52, 82, 255)
        for horizontal_line_index in range(8):
            self.building_grid_lines.append(shapes.Line(
                x = (self.game_data.window_width / 2) - (3.5 * self.building_tile_size),
                y = (self.game_data.window_height / 2) - (3.5 * self.building_tile_size) + (horizontal_line_index * self.building_tile_size),
                x2 = (self.game_data.window_width / 2) + (3.5 * self.building_tile_size),
                y2 = (self.game_data.window_height / 2) - (3.5 * self.building_tile_size) + (horizontal_line_index * self.building_tile_size),
                width=5,
                color=self.bulding_grid_lines_color,
                batch=self.batch,
                group=self.groups[1]
            ))
        # 8 vertical lines
        for vertical_line_index in range(8):
            self.building_grid_lines.append(shapes.Line(
                x = (self.game_data.window_width / 2) - (3.5 * self.building_tile_size) + (vertical_line_index * self.building_tile_size),
                y = (self.game_data.window_height / 2) - (3.5 * self.building_tile_size) - 2,
                x2 = (self.game_data.window_width / 2) - (3.5 * self.building_tile_size) + (vertical_line_index * self.building_tile_size),
                y2 = (self.game_data.window_height / 2) + (3.5 * self.building_tile_size) + 3,
                width=5,
                color=self.bulding_grid_lines_color,
                batch=self.batch,
                group=self.groups[1]
            ))

        # self.test_line = shapes.Line(
        #         x = 0,
        #         y = 0,
        #         x2 = 100,
        #         y2 = 100,
        #         color=(0, 0, 0, 255),
        #         width=10,
        #         batch=self.batch,
        #         group=self.middleground_group
        #     )

        # left window
        self.left_window = Sprite(
            img=self.game_data.side_window,
            x=15,
            y=self.game_data.window_height // 2,
            batch=self.batch,
            group=self.groups[1]
        )
        # right window
        self.right_window = Sprite(
            img=self.game_data.side_window,
            x = self.game_data.window_width - self.game_data.side_window.width*2 - 15,
            y=self.game_data.window_height // 2,
            batch=self.batch,
            group=self.groups[1]
        )
        self.left_window.opacity = self.right_window.opacity = 170
        self.left_window.scale = self.right_window.scale = 2
        self.left_window.scale_y = self.right_window.scale_y = 1.5

        # left window static content
        self.left_window_content = {}

        # workers title
        self.left_window_content["workers_label"] = Label("COLONS", font_name=self.game_data.subtitle_font_name, font_size=20,
            x=25, y=self.game_data.window_height - 95, width=315,
            align="center", anchor_y="center", batch=self.batch, group=self.groups[2])
        # worker icons
        self.left_window_content["engineers_icon"] = Sprite(
            img=self.game_data.icon_wrench_light_gray,
            x = self.left_window.width // 2 + 15 - 100,
            y = self.game_data.window_height - 135,
            batch=self.batch,
            group=self.groups[2]
        )
        self.left_window_content["engineers_icon"].scale = .15
        self.left_window_content["scientists_icon"] = Sprite(
            img=self.game_data.icon_vial_light_gray,
            x = self.left_window.width // 2 + 15,
            y = self.game_data.window_height - 135,
            batch=self.batch,
            group=self.groups[2]
        )
        self.left_window_content["scientists_icon"].scale = .13
        self.left_window_content["pilots_icon"] = Sprite(
            img=self.game_data.icon_plane_light_gray,
            x = self.left_window.width // 2 + 15 + 100,
            y = self.game_data.window_height - 135,
            batch=self.batch,
            group=self.groups[2]
        )
        self.left_window_content["pilots_icon"].scale = .15
        # workers counter label
        self.left_window_content["engineers_counter_label"] = Label("XX/XX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 100,
            y = self.game_data.window_height - 180,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["scientists_counter_label"] = Label("XX/XX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15,
            y = self.game_data.window_height - 180,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["pilots_counter_label"] = Label("XX/XX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 100,
            y = self.game_data.window_height - 180,
            anchor_x="center", batch=self.batch, group=self.groups[2])

        # resources title
        self.left_window_content["resources_label"] = Label("RESOURCES", font_name=self.game_data.subtitle_font_name, font_size=20,
            x=25, y=self.game_data.window_height - 210, width=315,
            align="center", anchor_y="center", batch=self.batch, group=self.groups[2])

        # power icon
        self.left_window_content["power_icon"] = Sprite(
            img = self.game_data.icon_bolt_light_gray,
            x = self.left_window.width // 2 + 15 - 30,
            y = self.game_data.window_height - 250,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["power_icon"].scale = .08
        # power counter label
        self.left_window_content["power_counter_label"] = Label("XX/XX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 30,
            y = self.game_data.window_height - 255,
            anchor_x="center", batch=self.batch, group=self.groups[2])

        # water icon
        self.left_window_content["water_icon"] = Sprite(
            img = self.game_data.icon_water_light_gray,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 300,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["water_icon"].scale = .07
        # water counter labels
        self.left_window_content["water_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 340,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["water_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 349,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["water_divide_bar"].scale = .15
        self.left_window_content["water_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 372,
            anchor_x="center", batch=self.batch, group=self.groups[2])

        # food icon
        self.left_window_content["food_icon"] = Sprite(
            img = self.game_data.icon_apple_light_gray,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 298,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["food_icon"].scale = .13
        # food counter labels
        self.left_window_content["food_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 340,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["food_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 349,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["food_divide_bar"].scale = .15
        self.left_window_content["food_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 372,
            anchor_x="center", batch=self.batch, group=self.groups[2])

        # O2 icon
        self.left_window_content["O2_label"] = Label("O2", font_name=self.game_data.subtitle_font_name, font_size=18,
            color=(192, 192, 192, 255),
            x = self.left_window.width // 2 + 15 + 40,
            y=self.game_data.window_height - 300,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
        # O2 counter labels
        self.left_window_content["O2_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 40,
            y = self.game_data.window_height - 340,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["O2_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 + 40,
            y = self.game_data.window_height - 349,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["O2_divide_bar"].scale = .15
        self.left_window_content["O2_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 40,
            y = self.game_data.window_height - 372,
            anchor_x="center", batch=self.batch, group=self.groups[2])

        # H2 icon
        self.left_window_content["H2_label"] = Label("H2", font_name=self.game_data.subtitle_font_name, font_size=18,
            color=(192, 192, 192, 255),
            x = self.left_window.width // 2 + 15 + 120,
            y=self.game_data.window_height - 300,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
        # H2 counter labels
        self.left_window_content["H2_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 120,
            y = self.game_data.window_height - 340,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["H2_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 + 120,
            y = self.game_data.window_height - 349,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["H2_divide_bar"].scale = .15
        self.left_window_content["H2_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 120,
            y = self.game_data.window_height - 372,
            anchor_x="center", batch=self.batch, group=self.groups[2])

        # iron label
        self.left_window_content["iron_label"] = Label("Fe", font_name=self.game_data.subtitle_font_name, font_size=18,
            color=(192, 192, 192, 255),
            x = self.left_window.width // 2 + 15 - 80,
            y=self.game_data.window_height - 390,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
        # iron ore icon
        self.left_window_content["iron_ore_icon"] = Sprite(
            img = self.game_data.icon_ore_light_gray,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 400,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["iron_ore_icon"].scale = .07
        # iron ingot icon
        self.left_window_content["iron_ingot_icon"] = Sprite(
            img = self.game_data.icon_ingot_light_gray,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 400,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["iron_ingot_icon"].scale = .1
        # iron counter labels
        self.left_window_content["iron_ore_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 430,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["iron_ore_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 439,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["iron_ore_divide_bar"].scale = .15
        self.left_window_content["iron_ore_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 462,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["iron_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 430,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["iron_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 439,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["iron_divide_bar"].scale = .15
        self.left_window_content["iron_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 462,
            anchor_x="center", batch=self.batch, group=self.groups[2])

        # aluminium label
        self.left_window_content["aluminium_label"] = Label("Al", font_name=self.game_data.subtitle_font_name, font_size=18,
            color=(192, 192, 192, 255),
            x = self.left_window.width // 2 + 15 + 80,
            y=self.game_data.window_height - 390,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
        # aluminium ore icon
        self.left_window_content["aluminium_ore_icon"] = Sprite(
            img = self.game_data.icon_ore_light_gray,
            x = self.left_window.width // 2 + 15 + 40,
            y = self.game_data.window_height - 400,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["aluminium_ore_icon"].scale = .07
        # aluminium ingot icon
        self.left_window_content["aluminium_ingot_icon"] = Sprite(
            img = self.game_data.icon_ingot_light_gray,
            x = self.left_window.width // 2 + 15 + 120,
            y = self.game_data.window_height - 400,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["aluminium_ingot_icon"].scale = .1
        # aluminium counter labels
        self.left_window_content["aluminium_ore_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 40,
            y = self.game_data.window_height - 430,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["aluminium_ore_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 + 40,
            y = self.game_data.window_height - 439,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["aluminium_ore_divide_bar"].scale = .15
        self.left_window_content["aluminium_ore_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 40,
            y = self.game_data.window_height - 462,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["aluminium_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 120,
            y = self.game_data.window_height - 430,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["aluminium_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 + 120,
            y = self.game_data.window_height - 439,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["aluminium_divide_bar"].scale = .15
        self.left_window_content["aluminium_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 120,
            y = self.game_data.window_height - 462,
            anchor_x="center", batch=self.batch, group=self.groups[2])

        # copper label
        self.left_window_content["copper_label"] = Label("Cu", font_name=self.game_data.subtitle_font_name, font_size=18,
            color=(192, 192, 192, 255),
            x = self.left_window.width // 2 + 15 - 80,
            y=self.game_data.window_height - 480,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
        # copper ore icon
        self.left_window_content["copper_ore_icon"] = Sprite(
            img = self.game_data.icon_ore_light_gray,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 490,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["copper_ore_icon"].scale = .07
        # copper ingot icon
        self.left_window_content["copper_ingot_icon"] = Sprite(
            img = self.game_data.icon_ingot_light_gray,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 490,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["copper_ingot_icon"].scale = .1
        # copper counter labels
        self.left_window_content["copper_ore_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 520,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["copper_ore_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 529,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["copper_ore_divide_bar"].scale = .15
        self.left_window_content["copper_ore_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 552,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["copper_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 520,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["copper_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 529,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["copper_divide_bar"].scale = .15
        self.left_window_content["copper_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 552,
            anchor_x="center", batch=self.batch, group=self.groups[2])

        # titanium label
        self.left_window_content["titanium_label"] = Label("Ti", font_name=self.game_data.subtitle_font_name, font_size=18,
            color=(192, 192, 192, 255),
            x = self.left_window.width // 2 + 15 + 80,
            y=self.game_data.window_height - 480,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
        # titanium ore icon
        self.left_window_content["titanium_ore_icon"] = Sprite(
            img = self.game_data.icon_ore_light_gray,
            x = self.left_window.width // 2 + 15 + 40,
            y = self.game_data.window_height - 490,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["titanium_ore_icon"].scale = .07
        # titanium ingot icon
        self.left_window_content["titanium_ingot_icon"] = Sprite(
            img = self.game_data.icon_ingot_light_gray,
            x = self.left_window.width // 2 + 15 + 120,
            y = self.game_data.window_height - 490,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["titanium_ingot_icon"].scale = .1
        # titanium counter labels
        self.left_window_content["titanium_ore_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 40,
            y = self.game_data.window_height - 520,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["titanium_ore_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 + 40,
            y = self.game_data.window_height - 529,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["titanium_ore_divide_bar"].scale = .15
        self.left_window_content["titanium_ore_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 40,
            y = self.game_data.window_height - 552,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["titanium_available"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 120,
            y = self.game_data.window_height - 520,
            anchor_x="center", batch=self.batch, group=self.groups[2])
        self.left_window_content["titanium_divide_bar"] = Sprite(
            img = self.game_data.icon_minus_white,
            x = self.left_window.width // 2 + 15 + 120,
            y = self.game_data.window_height - 529,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["titanium_divide_bar"].scale = .15
        self.left_window_content["titanium_total"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 120,
            y = self.game_data.window_height - 552,
            anchor_x="center", batch=self.batch, group=self.groups[2])

        # items title
        self.left_window_content["items_label"] = Label("INVENTAIRE", font_name=self.game_data.subtitle_font_name, font_size=20,
            x=25, y=self.game_data.window_height - 580, width=315,
            align="center", anchor_y="center", batch=self.batch, group=self.groups[2])

        # solid cargo module
        self.left_window_content["module_cargo_icon"] = Sprite(
            img = self.game_data.icon_crate_light_gray,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 620,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["module_cargo_icon"].scale = .15
        # solid cargo module counter
        self.left_window_content["module_cargo_counter"] = Label("XX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 90,
            y = self.game_data.window_height - 618,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])

        # liquid cargo module
        self.left_window_content["module_tank_icon"] = Sprite(
            img = self.game_data.icon_barrel_light_gray,
            x = self.left_window.width // 2 + 15 - 120,
            y = self.game_data.window_height - 660,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["module_tank_icon"].scale = .12
        # liquid cargo module counter
        self.left_window_content["module_tank_counter"] = Label("XX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 90,
            y = self.game_data.window_height - 658,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])

        # passengers module icon
        self.left_window_content["module_passengers_icon"] = Sprite(
            img = self.game_data.icon_seat_light_gray,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 620,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["module_passengers_icon"].scale = .1
        # passengers module counter
        self.left_window_content["module_passengers_counter"] = Label("XX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 10,
            y = self.game_data.window_height - 618,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])

        # base module icon
        self.left_window_content["module_base_icon"] = Sprite(
            img = self.game_data.icon_house_light_gray,
            x = self.left_window.width // 2 + 15 - 40,
            y = self.game_data.window_height - 660,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["module_base_icon"].scale = .1
        # base module counter
        self.left_window_content["module_base_counter"] = Label("XX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 - 10,
            y = self.game_data.window_height - 658,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])

        # small spaceship icon
        self.left_window_content["spaceship_small_icon"] = Sprite(
            img = self.game_data.icon_spaceship_light_gray,
            x = self.left_window.width // 2 + 15 + 50,
            y = self.game_data.window_height - 620,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["spaceship_small_icon"].scale = .07
        # small spaceship counter
        self.left_window_content["spaceship_small_counter"] = Label("XX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 50,
            y = self.game_data.window_height - 650,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])

        # medium spaceship icon
        self.left_window_content["spaceship_medium_icon"] = Sprite(
            img = self.game_data.icon_spaceship_light_gray,
            x = self.left_window.width // 2 + 15 + 95,
            y = self.game_data.window_height - 620,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["spaceship_medium_icon"].scale = .11
        # medium spaceship counter
        self.left_window_content["spaceship_medium_counter"] = Label("XX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 95,
            y = self.game_data.window_height - 650,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])

        # large spaceship icon
        self.left_window_content["spaceship_large_icon"] = Sprite(
            img = self.game_data.icon_spaceship_light_gray,
            x = self.left_window.width // 2 + 15 + 140,
            y = self.game_data.window_height - 620,
            batch = self.batch,
            group = self.groups[2]
        )
        self.left_window_content["spaceship_large_icon"].scale = .15
        # large spaceship counter
        self.left_window_content["spaceship_large_counter"] = Label("XX", font_name=self.game_data.default_font_name, font_size=14,
            x = self.left_window.width // 2 + 15 + 140,
            y = self.game_data.window_height - 650,
            anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])

        # test garbage collection
        # self.test_circle = None


    def draw(self):
        self.game_data.game_paused = False

        # udpate the batch

        # background sprite
        if self.game_data.active_colony == "moon":
            colony_name = "LUNE"
            self.background_sprite = Sprite(img=self.game_data.moon_background_img, y = -550, batch=self.batch, group=self.groups[0])
            self.background_sprite.scale = self.game_data.window_width / self.game_data.moon_background_img.width

        # colony name
        self.colony_name_label = Label(colony_name, font_name=self.game_data.subtitle_font_name, font_size=25,
            x=25, y=self.game_data.window_height - 42, width=315,
            align="center", anchor_y="center", batch=self.batch, group=self.groups[2])

        # information to list in left window:
        # - workers (available / total) by type
        # - landed spaceships by type
        # - available spaceship modules by type
        # - resources:
        #     - power consumed / total
        #     - food (available / maximum storage + produced, positive or negative, every minute)
        #     - water (available / maximum storage + produced, positive or negative, every minute)
        #     - liquid oxygen (available / maximum storage + produced, positive or negative, every minute)
        #     - liquid hydrogen (available / maximum storage + produced every minute)
        #     - ore (available / maximum storage + produced every minute)
        #     - metal (available / maximum storage + produced every minute)

        # left window update
        # workers
        colony_workers = self.game_data.colonies[self.game_data.active_colony].data["workers"]
        self.left_window_content["engineers_counter_label"].text = f"{colony_workers["engineers"]["available"]}/{colony_workers["engineers"]["total"]}"
        self.left_window_content["scientists_counter_label"].text = f"{colony_workers["scientists"]["available"]}/{colony_workers["scientists"]["total"]}"
        self.left_window_content["pilots_counter_label"].text = f"{colony_workers["pilots"]}"
        # power
        colony_power = self.game_data.colonies[self.game_data.active_colony].power
        self.left_window_content["power_counter_label"].text = f"{colony_power["consumed"]}/{colony_power["produced"]}"
        # resources
        colony_resources = self.game_data.colonies[self.game_data.active_colony].data["resources"]
        colony_storage_space = self.game_data.colonies[self.game_data.active_colony].max_storage
        # water
        self.left_window_content["water_available"].text = str(colony_resources["water"])
        self.left_window_content["water_total"].text = str(colony_storage_space["water"])
        # food
        self.left_window_content["food_available"].text = str(colony_resources["food"])
        self.left_window_content["food_total"].text = str(colony_storage_space["food"])
        # O2
        self.left_window_content["O2_available"].text = str(colony_resources["oxygen"])
        self.left_window_content["O2_total"].text = str(colony_storage_space["oxygen"])
        # H2
        self.left_window_content["H2_available"].text = str(colony_resources["hydrogen"])
        self.left_window_content["H2_total"].text = str(colony_storage_space["hydrogen"])
        # iron
        self.left_window_content["iron_ore_available"].text = str(colony_resources["iron_ore"])
        self.left_window_content["iron_ore_total"].text = str(colony_storage_space["iron_ore"])
        self.left_window_content["iron_available"].text = str(colony_resources["iron"])
        self.left_window_content["iron_total"].text = str(colony_storage_space["iron"])
        # aluminium
        self.left_window_content["aluminium_ore_available"].text = str(colony_resources["aluminium_ore"])
        self.left_window_content["aluminium_ore_total"].text = str(colony_storage_space["aluminium_ore"])
        self.left_window_content["aluminium_available"].text = str(colony_resources["aluminium"])
        self.left_window_content["aluminium_total"].text = str(colony_storage_space["aluminium"])
        # copper
        self.left_window_content["copper_ore_available"].text = str(colony_resources["copper_ore"])
        self.left_window_content["copper_ore_total"].text = str(colony_storage_space["copper_ore"])
        self.left_window_content["copper_available"].text = str(colony_resources["copper"])
        self.left_window_content["copper_total"].text = str(colony_storage_space["copper"])
        # titanium
        self.left_window_content["titanium_ore_available"].text = str(colony_resources["titanium_ore"])
        self.left_window_content["titanium_ore_total"].text = str(colony_storage_space["titanium_ore"])
        self.left_window_content["titanium_available"].text = str(colony_resources["titanium"])
        self.left_window_content["titanium_total"].text = str(colony_storage_space["titanium"])
        # items
        colony_items = self.game_data.colonies[self.game_data.active_colony].data["items"]
        self.left_window_content["module_cargo_counter"].text = str(colony_items["module_cargo_hold"])
        self.left_window_content["module_tank_counter"].text = str(colony_items["module_liquid_tanks"])
        self.left_window_content["module_passengers_counter"].text = str(colony_items["module_passengers"])
        self.left_window_content["module_base_counter"].text = str(colony_items["module_headquarters"])
        self.left_window_content["spaceship_small_counter"].text = str(colony_items["spaceship_small"])
        self.left_window_content["spaceship_medium_counter"].text = str(colony_items["spaceship_medium"])
        self.left_window_content["spaceship_large_counter"].text = str(colony_items["spaceship_large"])

        # test garbage collection
        # if self.test_circle is None:
        #     self.test_circle = shapes.Circle(
        #         x = self.game_data.window_width // 2,
        #         y = self.game_data.window_height // 2,
        #         radius = 300,
        #         batch=self.batch,
        #         group=self.foreground_group
        #     )
        # else:
        #     self.test_circle = None

        # draw the batch
        self.batch.draw()


    def on_mouse_press(self, x, y, button, modifiers) -> str:
        return "colony"


    def on_mouse_motion(self, x, y):
        self.game_data.mouse_x, self.game_data.mouse_y = x, y
        self.game_data.mouse_clickable_area = False


    def on_key_press(self, symbol, modifiers) -> str:
        return "colony"
