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
    """
    Represents each building tile on the building grid.
    Can be clicked on to select a building tile.
    If the tile is selected, displays a selector over the tile.
    """

    def __init__(self, game_data: GameData, line_index: int, column_index: int, batch, groups):
        self.game_data = game_data
        self.line_index = line_index
        self.colum_index = column_index
        self.batch = batch
        self.groups = groups
        # self.icon = None
        # the area covered by the widget
        self.tile_area = shapes.Rectangle(
            x = self.game_data.window_width // 2 - 260 + self.colum_index * 75,
            y = self.game_data.window_height // 2 + 190 - self.line_index * 75,
            width = 70,
            height = 70,
            color = (0, 0, 0, 0),
            batch=self.batch,
            group=self.groups[2]
        )
        # selector sprite
        self.selector_sprite = Sprite(
            img = self.game_data.icon_selector,
            x = self.game_data.window_width // 2 - 3 * 75 + self.colum_index * 75,
            y = self.game_data.window_height // 2 + 3 * 75 - self.line_index * 75,
            batch=self.batch,
            group=self.groups[3]
        )
        self.selector_sprite.scale = 2.25
        self.selector_sprite.opacity = 0
        # building display parameters
        # each building is represented by a color and an icon
        self.building_display_parameters = {
            "headquarters": {
                # white
                "color": (255, 255, 255, 255),
                "icon_img": self.game_data.icon_house_black,
                "icon_scale": .15
            },
            "solar_panels": {
                # #C7C400
                # yellow
                "color": (199, 199, 0, 255),
                "icon_img": self.game_data.icon_solar_panels_black,
                "icon_scale": .15
            },
            "drilling_station": {
                # violet
                # #44236E
                "color": (68, 35, 110, 255),
                "icon_img": self.game_data.icon_drill_white,
                "icon_scale": .15
            },
            "warehouse": {
                # dark gray
                "color": (85, 85, 85, 255),
                "icon_img": self.game_data.icon_crate_white,
                "icon_scale": .15
            },
            "liquid_tank": {
                # dark gray
                "color": (85, 85, 85, 255),
                "icon_img": self.game_data.icon_barrel_white,
                "icon_scale": .15
            },
            "electrolysis_station": {
                # orange
                # #C27818
                "color": (194, 120, 24, 255),
                "icon_img": self.game_data.icon_bubbles_black,
                "icon_scale": .15
            },
            "furnace": {
                # red
                # #912A24
                "color": (145, 41, 36, 255),
                "icon_img": self.game_data.icon_flame_white,
                "icon_scale": .15
            },
            "spaceport": {
                # black
                "color": (0, 0, 0, 255),
                "icon_img": self.game_data.icon_spaceship_white,
                "icon_scale": .18
            },
            "greenhouse": {
                # green
                # #367304
                "color": (54, 115, 4, 255),
                "icon_img": self.game_data.icon_tree_white,
                "icon_scale": .15
            },
            "school": {
                # bright cyan
                # #69ADA8
                "color": (105, 173, 168, 255),
                "icon_img": self.game_data.icon_book_black,
                "icon_scale": .15
            },
            "factory": {
                # dark cyan
                # #2A6179
                "color": (42, 97, 121, 255),
                "icon_img": self.game_data.icon_factory_white,
                "icon_scale": .15
            }
        }

    def on_draw(self):
        # print(f"building widget ({self.colum_index}, {self.line_index}) on_draw() called")
        # update the widget -> display the associated building, and whether or not it is selected
        current_colony = self.game_data.colonies[self.game_data.active_colony]
        # draw the building if it exists
        associated_building = current_colony.building_grid[self.line_index][self.colum_index]
        if associated_building is None:
            # hide the tile
            self.tile_area.color = (0, 0, 0, 0)
            self.icon = None
        else:
            # color the tile area with the color of the building
            self.tile_area.color = self.building_display_parameters[associated_building.name]["color"]
            self.icon = Sprite(
                img = self.building_display_parameters[associated_building.name]["icon_img"],
                x = self.game_data.window_width // 2 - 3 * 75 + self.colum_index * 75,
                y = self.game_data.window_height // 2 + 3 * 75 - self.line_index * 75,
                batch = self.batch,
                group = self.groups[3]
            )
            self.icon.scale = self.building_display_parameters[associated_building.name]["icon_scale"]
        # if (selected_building_tile_coords is not None):
        #     if current_colony.selected_building is not None:
        #         self.tile_area.color = self.building_display_parameters[current_colony.selected_building.name]["color"]
        #     # show the selector if the tile is selected
        #     if (selected_building_tile_coords[1] == self.line_index) and (selected_building_tile_coords[0] == self.colum_index):
        #         self.selector_sprite.opacity = 255
        selected_building_tile_coords = current_colony.selected_building_tile_coords
        # if the current building tile is selected ...
        if (selected_building_tile_coords is not None) and (selected_building_tile_coords[1] == self.line_index) and (selected_building_tile_coords[0] == self.colum_index):
            self.selector_sprite.opacity = 255
        else:
            # if the mouse is over the tile ...
            if (self.game_data.mouse_x, self.game_data.mouse_y) in self.tile_area:
                self.selector_sprite.opacity = 127
                self.game_data.mouse_clickable_area = True
            else:
                self.selector_sprite.opacity = 0

    def on_mouse_press(self, x, y):
        # if (x, y) in the building tile, select it
        if (x, y) in self.tile_area:
            self.game_data.colonies[self.game_data.active_colony].selected_building_tile_coords = (self.colum_index, self.line_index)

    # def on_mouse_motion(self):
    #     # if (mouse_x, mouse_y) in self.button_area, show a faded selector
    #     # set mouse_clickable_area to True if in self.button_area and associated bulding is not selected
    #     selected_building_tile_coords = self.game_data.colonies[self.game_data.active_colony].selected_building_tile_coords
    #     building_selected = (selected_building_tile_coords is not None) and (selected_building_tile_coords[1] == self.line_index) and (selected_building_tile_coords[0] == self.colum_index)
    #     if not building_selected and (self.game_data.mouse_x, self.game_data.mouse_y) in self.tile_area:
    #             self.game_data.mouse_clickable_area = True


class RightWindowWidget:

    name_translation_en2fr = {
        "headquarters": "QG",
        "solar_panels": "PANNEAUX SOLAIRES",
        "drilling_station": "FOREUSE",
        "warehouse": "ENTREPOT",
        "liquid_tank": "RESERVOIR",
        "electrolysis_station": "STATION D'ELECTROLYSE",
        "furnace": "FOURNEAU",
        "spaceport": "PORT SPACIAL",
        "greenhouse": "SERRE",
        "school": "ECOLE",
        "factory": "USINE"
    }

    def __init__(self, game_data: GameData, batch, groups):
        self.game_data = game_data
        self.batch = batch
        self.groups = groups
        self.building_icons = {
            "solar_panels": {
                # dark gray
                "icon_img_impossible": self.game_data.icon_solar_panels_dark_gray,
                # white
                "icon_img_possible": self.game_data.icon_solar_panels_white,
                # light green
                # #68B842
                "icon_img_hovered": self.game_data.icon_solar_panels_green,
                "icon_scale": .15
            },
            "drilling_station": {
                "icon_img_impossible": self.game_data.icon_drill_dark_gray,
                "icon_img_possible": self.game_data.icon_drill_white,
                "icon_img_hovered": self.game_data.icon_drill_green,
                "icon_scale": .15
            },
            "warehouse": {
                "icon_img_impossible": self.game_data.icon_crate_dark_gray,
                "icon_img_possible": self.game_data.icon_crate_white,
                "icon_img_hovered": self.game_data.icon_crate_green,
                "icon_scale": .15
            },
            "liquid_tank": {
                "icon_img_impossible": self.game_data.icon_barrel_dark_gray,
                "icon_img_possible": self.game_data.icon_barrel_white,
                "icon_img_hovered": self.game_data.icon_barrel_green,
                "icon_scale": .15
            },
            "electrolysis_station": {
                "icon_img_impossible": self.game_data.icon_bubbles_dark_gray,
                "icon_img_possible": self.game_data.icon_bubbles_white,
                "icon_img_hovered": self.game_data.icon_bubbles_green,
                "icon_scale": .15
            },
            "furnace": {
                "icon_img_impossible": self.game_data.icon_flame_dark_gray,
                "icon_img_possible": self.game_data.icon_flame_white,
                "icon_img_hovered": self.game_data.icon_flame_green,
                "icon_scale": .15
            },
            "spaceport": {
                "icon_img_impossible": self.game_data.icon_spaceship_dark_gray,
                "icon_img_possible": self.game_data.icon_spaceship_white,
                "icon_img_hovered": self.game_data.icon_spaceship_green,
                "icon_scale": .15
            },
            "greenhouse": {
                "icon_img_impossible": self.game_data.icon_tree_dark_gray,
                "icon_img_possible": self.game_data.icon_tree_white,
                "icon_img_hovered": self.game_data.icon_tree_green,
                "icon_scale": .15
            },
            "school": {
                "icon_img_impossible": self.game_data.icon_book_dark_gray,
                "icon_img_possible": self.game_data.icon_book_white,
                "icon_img_hovered": self.game_data.icon_book_green,
                "icon_scale": .15
            },
            "factory": {
                "icon_img_impossible": self.game_data.icon_factory_dark_gray,
                "icon_img_possible": self.game_data.icon_factory_white,
                "icon_img_hovered": self.game_data.icon_factory_green,
                "icon_scale": .15
            }
        }

    def on_draw(self):
        # if no building is selected, don't display anything
        current_colony = self.game_data.colonies[self.game_data.active_colony]
        # selected_building_tile_coords = current_colony.selected_building_tile_coords
        # if current_colony.selected_building_tile_coords is None:
        #     # clear the window
        #     self.content = {}
        # else:
        # clear the window
        self.content = {}
        if current_colony.selected_building_tile_coords is not None:
            # window sprite
            self.content["window_sprite"] = Sprite(
                img = self.game_data.side_window,
                x = self.game_data.window_width - self.game_data.side_window.width*2 - 15,
                y=self.game_data.window_height // 2,
                batch=self.batch,
                group=self.groups[1]
            )

            self.content["window_sprite"].opacity = 170
            self.content["window_sprite"].scale = 2
            self.content["window_sprite"].scale_y = 1.5
            # test window size
            # self.content["test_size_rect"] = shapes.Rectangle(
            #     x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 160,
            #     y = 25,
            #     width = 320,
            #     height = 618,
            #     color = (255, 255, 255, 255),
            #     batch=self.batch,
            #     group=self.groups[2]
            # )
            # window title
            selected_building = current_colony.selected_building
            if selected_building is None:
                # self.content["title_label"] = "CONSTRUIRE"
                self.content["title_label"] = Label("CONSTRUIRE", font_name=self.game_data.subtitle_font_name, font_size=15,
                    x=self.game_data.window_width - 25 - 315, y=self.game_data.window_height - 43, width=315,
                    align="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                # make a list of possible buildings to build
                # self.content["building_options_list"] = []
                building_options_dict = {}
                for building_index, building_name in enumerate(list(current_colony.building_types_dict.keys())[1:]):
                    # self.content["building_options_list"].append([])
                    # print(building_name)
                    building_option = {}
                    # area to click on
                    button_area = shapes.Rectangle(
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 160,
                        y = self.game_data.window_height - 135 - building_index * 62,
                        width = 320,
                        height = 55,
                        # color = (255, 0, 0, 127),
                        batch=self.batch,
                        group=self.groups[2]
                    )
                    if current_colony.can_add_building(building_name):
                        # show white resources values
                        # show green name if hovered
                        # building_sprite_img = self.building_icons[building_name]["icon_img_possible"]
                        if (self.game_data.mouse_x, self.game_data.mouse_y) in button_area:
                            button_area.color = (192, 192, 192, 63)
                            building_sprite_img = self.building_icons[building_name]["icon_img_hovered"]
                            self.game_data.mouse_clickable_area = True
                        else:
                            button_area.color = (0, 0, 0, 0)
                            building_sprite_img = self.building_icons[building_name]["icon_img_possible"]
                    else:
                        # show gray resources values
                        button_area.color = (0, 0, 0, 0)
                        building_sprite_img = self.building_icons[building_name]["icon_img_impossible"]
                    building_option["button_area"] = button_area
                    # building sprite
                    building_icon = Sprite(
                        img = building_sprite_img,
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 130,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8),
                        batch=self.batch,
                        group=self.groups[3]
                    )
                    # print(self.content["window_sprite"].width)
                    building_icon.scale = self.building_icons[building_name]["icon_scale"]
                    # building_options_list.append(building_sprite)
                    # building_options_list[building_name] = building_sprite
                    building_option["building_icon"] = building_icon
                    # power icon
                    power_icon = Sprite(
                        img = self.game_data.icon_bolt_light_gray,
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 60,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) + 13,
                        batch=self.batch,
                        group=self.groups[3]
                    )
                    power_icon.scale = .05
                    building_option["power_icon"] = power_icon
                    building_parameters_per_level = current_colony.building_types_dict[building_name].parameters_per_level
                    # power label
                    power_label_string = "{:+}".format(building_parameters_per_level[1]["power"]["produced"] -
                                                       building_parameters_per_level[1]["power"]["consumed"])
                    power_label = Label(power_label_string, font_name=self.game_data.default_font_name, font_size=14,
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 60,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) - 20,
                        anchor_x="center", batch=self.batch, group=self.groups[3])
                    building_option["power_label"] = power_label
                    # iron icon
                    iron_icon = Label("Fe", font_name=self.game_data.subtitle_font_name, font_size=15,
                        color = (192, 192, 192, 255),
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 15,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) + 15,
                        anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[3])
                    building_option["iron_icon"] = iron_icon
                    # iron label
                    iron_label_string = str(building_parameters_per_level[0]["construction_costs"]["iron"])
                    iron_label = Label(iron_label_string, font_name=self.game_data.default_font_name, font_size=14,
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 15,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) - 20,
                        anchor_x="center", batch=self.batch, group=self.groups[3])
                    building_option["iron_label"] = iron_label
                    # aluminium icon
                    aluminium_icon = Label("Al", font_name=self.game_data.subtitle_font_name, font_size=15,
                        color = (192, 192, 192, 255),
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 30,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) + 15,
                        anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[3])
                    building_option["aluminium_icon"] = aluminium_icon
                    # aluminium label
                    aluminium_label_string = str(building_parameters_per_level[0]["construction_costs"]["aluminium"])
                    aluminium_label = Label(aluminium_label_string, font_name=self.game_data.default_font_name, font_size=14,
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 30,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) - 20,
                        anchor_x="center", batch=self.batch, group=self.groups[3])
                    building_option["aluminium_label"] = aluminium_label
                    # copper icon
                    copper_icon = Label("Cu", font_name=self.game_data.subtitle_font_name, font_size=15,
                        color = (192, 192, 192, 255),
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 75,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) + 15,
                        anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[3])
                    building_option["copper_icon"] = copper_icon
                    # copper label
                    copper_label_string = str(building_parameters_per_level[0]["construction_costs"]["copper"])
                    copper_label = Label(copper_label_string, font_name=self.game_data.default_font_name, font_size=14,
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 75,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) - 20,
                        anchor_x="center", batch=self.batch, group=self.groups[3])
                    building_option["copper_label"] = copper_label
                    # "titanium": 0
                    # titanium icon
                    titanium_icon = Label("Ti", font_name=self.game_data.subtitle_font_name, font_size=15,
                        color = (192, 192, 192, 255),
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 120,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) + 15,
                        anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[3])
                    building_option["titanium_icon"] = titanium_icon
                    # copper label
                    titanium_label_string = str(building_parameters_per_level[0]["construction_costs"]["titanium"])
                    titanium_label = Label(titanium_label_string, font_name=self.game_data.default_font_name, font_size=14,
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 120,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) - 20,
                        anchor_x="center", batch=self.batch, group=self.groups[3])
                    building_option["titanium_label"] = titanium_label
                    building_options_dict[building_name] = building_option
                self.content["building_options_dict"] = building_options_dict
            else:
                # self.content["title_label"] = self.name_translation_en2fr[selected_building.name]
                self.content["title_label"] = Label(self.name_translation_en2fr[selected_building.name], font_name=self.game_data.subtitle_font_name, font_size=15,
                    x=self.game_data.window_width - 25 - 315, y=self.game_data.window_height - 43, width=315,
                    align="center", anchor_y="center", batch=self.batch, group=self.groups[2])

    def on_mouse_press(self, x, y):
        current_colony = self.game_data.colonies[self.game_data.active_colony]
        ...

    # def on_mouse_motion(self):
    #     pass


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
                x = (self.game_data.window_width // 2) - (3.5 * self.building_tile_size),
                y = (self.game_data.window_height // 2) - (3.5 * self.building_tile_size) + (horizontal_line_index * self.building_tile_size),
                x2 = (self.game_data.window_width // 2) + (3.5 * self.building_tile_size),
                y2 = (self.game_data.window_height // 2) - (3.5 * self.building_tile_size) + (horizontal_line_index * self.building_tile_size),
                width=5,
                color=self.bulding_grid_lines_color,
                batch=self.batch,
                group=self.groups[1]
            ))
        # 8 vertical lines
        for vertical_line_index in range(8):
            self.building_grid_lines.append(shapes.Line(
                x = (self.game_data.window_width // 2) - (3.5 * self.building_tile_size) + (vertical_line_index * self.building_tile_size),
                y = (self.game_data.window_height // 2) - (3.5 * self.building_tile_size) - 2,
                x2 = (self.game_data.window_width // 2) - (3.5 * self.building_tile_size) + (vertical_line_index * self.building_tile_size),
                y2 = (self.game_data.window_height // 2) + (3.5 * self.building_tile_size) + 3,
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
        self.left_window.opacity = 170
        self.left_window.scale = 2
        self.left_window.scale_y = 1.5

        # building tiles widgets
        self.building_tiles_widgets: list[list[BuildingWidget]] = [[BuildingWidget(
            self.game_data,
            line_index,
            column_index,
            batch=self.batch,
            groups=self.groups
        ) for column_index in range(7)] for line_index in range(7)]

        # right window widget
        self.right_window_widget = RightWindowWidget(self.game_data, self.batch, self.groups)

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
        self.left_window_content["module_cargo_icon"].scale = .12
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

        # reset the state of the mouse
        self.game_data.mouse_clickable_area = False

        # update the building widgets
        for line_index in range(len(self.building_tiles_widgets)):
            for column_index in range(len(self.building_tiles_widgets[line_index])):
                self.building_tiles_widgets[line_index][column_index].on_draw()

        # update the right window widget
        self.right_window_widget.on_draw()

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
        if button & mouse.LEFT:
            # send the left click to every building widget to select a building
            for line_index in range(len(self.building_tiles_widgets)):
                for column_index in range(len(self.building_tiles_widgets[line_index])):
                    self.building_tiles_widgets[line_index][column_index].on_mouse_press(x, y)
            # send the left click to the right widget
            self.right_window_widget.on_mouse_press(x, y)
        # unselect building on right click
        if button & mouse.RIGHT:
            self.game_data.colonies[self.game_data.active_colony].selected_building_tile_coords = None
        return "colony"


    def on_mouse_motion(self, x, y):
        self.game_data.mouse_x, self.game_data.mouse_y = x, y
        # self.game_data.mouse_clickable_area = False
        # send the mouse motion to the building widgets
        # for line_index in range(len(self.building_tiles_widgets)):
        #     for column_index in range(len(self.building_tiles_widgets[line_index])):
        #         self.building_tiles_widgets[line_index][column_index].on_mouse_motion()
        # send the mouse motion to the right window widget
        # self.right_window_widget.on_mouse_motion()


    def on_key_press(self, symbol, modifiers) -> str:
        return "colony"
