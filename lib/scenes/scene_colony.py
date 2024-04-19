from pyglet.text import Label, decode_attributed
from pyglet.text.layout import TextLayout
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


class RigthWindowWidgetContent:

    building_name_translation_en2fr = {
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

    def __init__(self, game_data: GameData, building_icons_dict: dict[str, dict[str]], batch, groups):
        # only called when the content of the right window has to be redrawn
        # contains the sprites and labels of the right window, according to the game state
        self.game_data = game_data
        self.building_icons_dict = building_icons_dict
        self.batch = batch
        self.groups = groups
        self.current_colony = self.game_data.colonies[self.game_data.active_colony]
        # the content of the right window
        self.content = {}
        if self.current_colony.selected_building_tile_coords is not None:
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
            self.selected_building = self.current_colony.selected_building
            if self.selected_building is None:
                # window title
                self.content["title_label"] = Label("CONSTRUIRE", font_name=self.game_data.subtitle_font_name, font_size=15,
                    x=self.game_data.window_width - 25 - 315, y=self.game_data.window_height - 43, width=315,
                    align="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                # make a list of possible buildings to build (without the headquarters)
                building_options_dict = {}
                for building_index, building_name in enumerate(list(self.current_colony.building_types_dict.keys())[1:]):
                    building_option = {}
                    building_option["button_area"] = shapes.Rectangle(
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 160,
                        y = self.game_data.window_height - 135 - building_index * 62,
                        width = 320,
                        height = 55,
                        batch=self.batch,
                        group=self.groups[2]
                    )
                    # building_option["button_area"] = button_area
                    # building icons
                    building_icon_impossible = Sprite(
                        img = self.building_icons_dict[building_name]["icon_img_impossible"],
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 130,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8),
                        batch=self.batch,
                        group=self.groups[3]
                    )
                    # building_icon_impossible.scale = self.building_icons_dict[building_name]["icon_scale"]
                    building_icon_impossible.scale = .15
                    building_option["building_icon_impossible"] = building_icon_impossible
                    building_icon_possible = Sprite(
                        img = self.building_icons_dict[building_name]["icon_img_possible"],
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 130,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8),
                        batch=self.batch,
                        group=self.groups[3]
                    )
                    building_icon_possible.scale = .15
                    building_option["building_icon_possible"] = building_icon_possible
                    building_icon_hovered = Sprite(
                        img = self.building_icons_dict[building_name]["icon_img_hovered"],
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 130,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8),
                        batch=self.batch,
                        group=self.groups[3]
                    )
                    building_icon_hovered.scale = .15
                    building_option["building_icon_hovered"] = building_icon_hovered
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
                    building_parameters_per_level = self.current_colony.building_types_dict[building_name].parameters_per_level
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
                    # titanium icon
                    titanium_icon = Label("Ti", font_name=self.game_data.subtitle_font_name, font_size=15,
                        color = (192, 192, 192, 255),
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 120,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) + 15,
                        anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[3])
                    building_option["titanium_icon"] = titanium_icon
                    # titanium label
                    titanium_label_string = str(building_parameters_per_level[0]["construction_costs"]["titanium"])
                    titanium_label = Label(titanium_label_string, font_name=self.game_data.default_font_name, font_size=14,
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 120,
                        y = self.game_data.window_height - 110 - int(building_index * 61.8) - 20,
                        anchor_x="center", batch=self.batch, group=self.groups[3])
                    building_option["titanium_label"] = titanium_label
                    building_options_dict[building_name] = building_option
                self.content["building_options_dict"] = building_options_dict
            else:
                # window title
                self.content["title_label"] = Label(self.building_name_translation_en2fr[self.selected_building.name], font_name=self.game_data.subtitle_font_name, font_size=15,
                    x=self.game_data.window_width - 25 - 315, y=self.game_data.window_height - 43, width=315,
                    align="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                # display for each building:
                # - building level
                # - workers:
                #     - production jobs: engineers + scientists
                #     - if constructing: engineers jobs
                #     - for each (grayed if not possible):
                #         - + button
                #         - - button
                #         - fill button
                #         - empty button
                # - upgrade button (grayed if impossible), that becomes a "cancel upgrade" button when constructing
                # - construction percentage when constructing
                # - destroy button (grayed when impossible, that transforms into a "sure?" button when pressed once
                # building level
                self.content["building_level_label"] = Label("NIVEAU", font_name=self.game_data.subtitle_font_name, font_size=15,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 100,
                    y = self.game_data.window_height - 110,
                    anchor_x="center", batch=self.batch, group=self.groups[2])
                self.content["building_level_value"] = Label("X", font_name=self.game_data.subtitle_font_name, font_size=22,
                    color = (255, 255, 255, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 30,
                    y = self.game_data.window_height - 110,
                    anchor_x="center", batch=self.batch, group=self.groups[2])
                # building power
                self.content["building_power_icon"] = Sprite(
                    img = self.game_data.icon_bolt_light_gray,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 60,
                    y = self.game_data.window_height - 105,
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["building_power_icon"].scale = .08
                self.content["building_power_value"] = Label("-XX", font_name=self.game_data.subtitle_font_name, font_size=15,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 110,
                    y = self.game_data.window_height - 110,
                    anchor_x="center", batch=self.batch, group=self.groups[2])
                # production jobs
                self.content["production_jobs_title"] = Label("PRODUCTION", font_name=self.game_data.subtitle_font_name, font_size=15,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15,
                    y = self.game_data.window_height - 140,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                # engineers
                self.content["production_jobs_engineers_icon"] = Sprite(
                    img = self.game_data.icon_wrench_light_gray,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 120,
                    y = self.game_data.window_height - 180,
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["production_jobs_engineers_icon"].scale = .18
                self.content["production_jobs_engineers_value"] = Label("XX/XX", font_name=self.game_data.default_font_name, font_size=14,
                    color = (255, 255, 255, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 60,
                    y = self.game_data.window_height - 180,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                # +1 button
                self.content["production_jobs_engineers_add_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 10,
                    y = self.game_data.window_height - 180,
                    width = 22,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["production_jobs_engineers_add_button_label"] = Label("+1", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15,
                    y = self.game_data.window_height - 175,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # -1 button
                self.content["production_jobs_engineers_remove_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 10,
                    y = self.game_data.window_height - 205,
                    width = 22,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["production_jobs_engineers_remove_button_label"] = Label("-1", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15,
                    y = self.game_data.window_height - 200,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # fill button
                self.content["production_jobs_engineers_fill_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 25,
                    y = self.game_data.window_height - 180,
                    width = 100,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["production_jobs_engineers_fill_button_label"] = Label("REMPLIR", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 75,
                    y = self.game_data.window_height - 175,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # empty button
                self.content["production_jobs_engineers_empty_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 25,
                    y = self.game_data.window_height - 205,
                    width = 100,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["production_jobs_engineers_empty_button_label"] = Label("VIDER", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 75,
                    y = self.game_data.window_height - 200,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # scientists
                self.content["production_jobs_scientists_icon"] = Sprite(
                    img = self.game_data.icon_vial_light_gray,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 120,
                    y = self.game_data.window_height - 230,
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["production_jobs_scientists_icon"].scale = .15
                self.content["production_jobs_scientists_value"] = Label("XX/XX", font_name=self.game_data.default_font_name, font_size=14,
                    color = (255, 255, 255, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 60,
                    y = self.game_data.window_height - 230,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                # +1 button
                self.content["production_jobs_scientists_add_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 10,
                    y = self.game_data.window_height - 230,
                    width = 22,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["production_jobs_scientists_add_button_label"] = Label("+1", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15,
                    y = self.game_data.window_height - 225,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # -1 button
                self.content["production_jobs_scientists_remove_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 10,
                    y = self.game_data.window_height - 255,
                    width = 22,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["production_jobs_scientists_remove_button_label"] = Label("-1", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15,
                    y = self.game_data.window_height - 250,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # fill button
                self.content["production_jobs_scientists_fill_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 25,
                    y = self.game_data.window_height - 230,
                    width = 100,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["production_jobs_scientists_fill_button_label"] = Label("REMPLIR", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 75,
                    y = self.game_data.window_height - 225,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # empty button
                self.content["production_jobs_scientists_empty_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 25,
                    y = self.game_data.window_height - 255,
                    width = 100,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["production_jobs_scientists_empty_button_label"] = Label("VIDER", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 75,
                    y = self.game_data.window_height - 250,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # construction jobs
                self.content["construction_jobs_title"] = Label("CONSTRUCTION", font_name=self.game_data.subtitle_font_name, font_size=15,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15,
                    y = self.game_data.window_height - 275,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                # engineers
                self.content["construction_jobs_engineers_icon"] = Sprite(
                    img = self.game_data.icon_wrench_light_gray,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 120,
                    y = self.game_data.window_height - 315,
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["construction_jobs_engineers_icon"].scale = .18
                self.content["construction_jobs_value"] = Label("XX/XX", font_name=self.game_data.default_font_name, font_size=14,
                    color = (255, 255, 255, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 60,
                    y = self.game_data.window_height - 315,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                # +1 button
                self.content["construction_jobs_add_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 10,
                    y = self.game_data.window_height - 315,
                    width = 22,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["construction_jobs_add_button_label"] = Label("+1", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15,
                    y = self.game_data.window_height - 310,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # -1 button
                self.content["construction_jobs_remove_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 10,
                    y = self.game_data.window_height - 340,
                    width = 22,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["construction_jobs_remove_button_label"] = Label("-1", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15,
                    y = self.game_data.window_height - 335,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # fill button
                self.content["construction_jobs_fill_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 25,
                    y = self.game_data.window_height - 315,
                    width = 100,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["construction_jobs_fill_button_label"] = Label("REMPLIR", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 75,
                    y = self.game_data.window_height - 310,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # empty button
                self.content["construction_jobs_empty_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 25,
                    y = self.game_data.window_height - 340,
                    width = 100,
                    height = 20,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["construction_jobs_empty_button_label"] = Label("VIDER", font_name=self.game_data.subtitle_font_name, font_size=13,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 75,
                    y = self.game_data.window_height - 335,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # upgrade button
                self.content["upgrade_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 150,
                    y = 35,
                    width = 142,
                    height = 23,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["upgrade_button_label"] = Label("AMELIORER", font_name=self.game_data.subtitle_font_name, font_size=15,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 80,
                    y = 40,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # upgrade percent
                self.content["upgrade_percent_label"] = Label("XX%", font_name=self.game_data.subtitle_font_name, font_size=12,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 80,
                    y = 70,
                    anchor_x="center", batch=self.batch, group=self.groups[2])
                # upgrade cost
                self.content["upgrade_power_icon"] = Sprite(
                    img = self.game_data.icon_bolt_light_gray,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 140,
                    y = 85,
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["upgrade_power_icon"].scale = .03
                self.content["upgrade_power_label"] = Label("+XXX", font_name=self.game_data.default_font_name, font_size=9,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 140,
                    y = 70,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                self.content["upgrade_iron_icon"] = Label("Fe", font_name=self.game_data.subtitle_font_name, font_size=12,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 110,
                    y = 80,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                self.content["upgrade_iron_label"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=9,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 110,
                    y = 65,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                self.content["upgrade_aluminium_icon"] = Label("Al", font_name=self.game_data.subtitle_font_name, font_size=12,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 80,
                    y = 85,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                self.content["upgrade_aluminium_label"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=9,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 80,
                    y = 70,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                self.content["upgrade_copper_icon"] = Label("Cu", font_name=self.game_data.subtitle_font_name, font_size=12,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 50,
                    y = 80,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                self.content["upgrade_copper_label"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=9,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 50,
                    y = 65,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                self.content["upgrade_titanium_icon"] = Label("Ti", font_name=self.game_data.subtitle_font_name, font_size=12,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 20,
                    y = 85,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                self.content["upgrade_titanium_label"] = Label("XXX", font_name=self.game_data.default_font_name, font_size=9,
                    color = (192, 192, 192, 255),
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 20,
                    y = 70,
                    anchor_x="center", anchor_y="center", batch=self.batch, group=self.groups[2])
                # destroy button
                self.content["destroy_button_area"] = shapes.Rectangle(
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 20,
                    y = 35,
                    width = 120,
                    height = 23,
                    color = (192, 192, 192, 0),
                    batch=self.batch,
                    group=self.groups[2]
                )
                self.content["destroy_button_label"] = Label("DETRUIRE", font_name=self.game_data.subtitle_font_name, font_size=15,
                    x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 + 80,
                    y = 40,
                    anchor_x="center", batch=self.batch, group=self.groups[3])
                # building specific stuff
                self.style_description = "{font_name '" + self.game_data.default_font_name + "'}{font_size 13}{color (255, 255, 255, 255)}"
                if self.selected_building.name == "headquarters":
                    # self.content["building_description_string"] = "{font_name '" + self.game_data.default_font_name + "'}{font_size 13}{color (255, 255, 255, 255)}"
                    self.content["building_description_string"] = self.style_description
                    self.content["building_description_string"] += "Le quartier général de la colonie. Offre un espace de stockage basique :\n\n\n"
                    self.content["building_description_string"] += "Nourriture : {bold True}" + str(self.selected_building.parameters["storage"]["food"]) + "{bold False}\n\n"
                    self.content["building_description_string"] += "Solides (minerai et métaux) : {bold True}" + str(self.selected_building.parameters["storage"]["iron"]) + "{bold False}\n\n"
                    self.content["building_description_string"] += "Liquides (eau, O2 et H2) : {bold True}" + str(self.selected_building.parameters["storage"]["water"])
                    # self.content["building_description_string"] = "TEST"
                    # self.content["building_description_document"] = decode_attributed(self.content["building_description_string"])
                    # print(self.content["building_description_document"].text)
                    # the text layout object needs to be manually deleted
                    self.content["building_description_layout"] = TextLayout(
                        # document=self.content["building_description_document"],
                        # document=decode_attributed(""),
                        document = decode_attributed(self.content["building_description_string"]),
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 150,
                        y = self.game_data.window_height - 370,
                        width = 300,
                        # height=0,
                        anchor_y="baseline",
                        multiline=True,
                        batch=self.batch,
                        group=self.groups[2]
                    )
                    # self.content["building_description_layout"].document = decode_attributed("{color (255, 0, 0, 255)}lol")
                    # print(type(self.content["building_description_layout"].document))
                elif self.selected_building.name in ["warehouse", "liquid_tank", "solar_panels", "electrolysis_station", "greenhouse", "spaceport"]:
                    # print("warehouse")
                    # self.content["building_description_string"] = self.style_description
                    # self.content["building_description_string"] += "Les entrepôts permettent de stocker des matières solides : nourriture, minéraux et métaux.\n\n\n"
                    # self.content["building_description_string"] += ""
                    self.content["building_description_layout"] = TextLayout(
                        # document=self.content["building_description_document"],
                        # document=decode_attributed(""),
                        document = decode_attributed(""),
                        x = self.game_data.window_width - self.content["window_sprite"].width // 2 - 15 - 150,
                        y = self.game_data.window_height - 370,
                        width = 300,
                        # height=0,
                        anchor_y="baseline",
                        multiline=True,
                        batch=self.batch,
                        group=self.groups[2]
                    )
                elif self.selected_building.name == "drilling_station":
                    print("drilling_station")
                elif self.selected_building.name == "furnace":
                    print("furnace")
                elif self.selected_building.name == "school":
                    print("school")
                elif self.selected_building.name == "factory":
                    print("factory")

    def on_draw(self):
        # redraw the colors and opacity of items in the window according to the game state
        if self.current_colony.selected_building_tile_coords is not None:
            # selected_building = self.current_colony.selected_building
            if self.selected_building is None:
                for building_name in self.content["building_options_dict"].keys():
                    building_option = self.content["building_options_dict"][building_name]
                    # set all building icons to transparent
                    building_option["building_icon_impossible"].opacity = 0
                    building_option["building_icon_possible"].opacity = 0
                    building_option["building_icon_hovered"].opacity = 0
                    if self.current_colony.can_add_building(building_name):
                        if (self.game_data.mouse_x, self.game_data.mouse_y) in building_option["button_area"]:
                            building_option["button_area"].color = (192, 192, 192, 63)
                            building_option["building_icon_hovered"].opacity = 255
                            self.game_data.mouse_clickable_area = True
                        else:
                            building_option["button_area"].color = (0, 0, 0, 0)
                            building_option["building_icon_possible"].opacity = 255
                    else:
                        # show gray resources values
                        building_option["button_area"].color = (0, 0, 0, 0)
                        building_option["building_icon_impossible"].opacity = 255
            else:
                self.content["building_level_value"].text = str(self.selected_building.level)
                self.content["building_power_value"].text = "{:+}".format(self.selected_building.parameters["power"]["produced"] -
                                                                          self.selected_building.parameters["power"]["consumed"])
                self.content["production_jobs_engineers_value"].text = f"{self.selected_building.assigned_workers["production"]["engineers"]}/{self.selected_building.parameters["jobs"]["production"]["engineers"]}"
                self.content["production_jobs_scientists_value"].text = f"{self.selected_building.assigned_workers["production"]["scientists"]}/{self.selected_building.parameters["jobs"]["production"]["scientists"]}"
                if self.selected_building.is_constructing:
                    self.content["construction_jobs_value"].text = f"{self.selected_building.assigned_workers["construction"]["engineers"]}/{self.selected_building.parameters["jobs"]["construction"]["engineers"]}"
                else:
                    self.content["construction_jobs_value"].text = f"{self.selected_building.assigned_workers["construction"]["engineers"]}/0"
                # production job engineers buttons
                if self.selected_building.can_assign_worker(True, "production", "engineers"):
                    self.content["production_jobs_engineers_add_button_label"].color = (255, 255, 255, 255)
                    self.content["production_jobs_engineers_fill_button_label"].color = (255, 255, 255, 255)
                    if (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["production_jobs_engineers_add_button_area"]:
                        self.content["production_jobs_engineers_add_button_label"].color = (0, 255, 0, 255)
                        self.game_data.mouse_clickable_area = True
                    elif (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["production_jobs_engineers_fill_button_area"]:
                        self.content["production_jobs_engineers_fill_button_label"].color = (0, 255, 0, 255)
                        self.game_data.mouse_clickable_area = True
                else:
                    self.content["production_jobs_engineers_add_button_label"].color = (255, 255, 255, 100)
                    self.content["production_jobs_engineers_fill_button_label"].color = (255, 255, 255, 100)
                if self.selected_building.can_assign_worker(False, "production", "engineers"):
                    self.content["production_jobs_engineers_remove_button_label"].color = (255, 255, 255, 255)
                    self.content["production_jobs_engineers_empty_button_label"].color = (255, 255, 255, 255)
                    if (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["production_jobs_engineers_remove_button_area"]:
                        self.content["production_jobs_engineers_remove_button_label"].color = (255, 0, 0, 255)
                        self.game_data.mouse_clickable_area = True
                    elif (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["production_jobs_engineers_empty_button_area"]:
                        self.content["production_jobs_engineers_empty_button_label"].color = (255, 0, 0, 255)
                        self.game_data.mouse_clickable_area = True
                else:
                    self.content["production_jobs_engineers_remove_button_label"].color = (255, 255, 255, 100)
                    self.content["production_jobs_engineers_empty_button_label"].color = (255, 255, 255, 100)
                # production job scientists buttons
                if self.selected_building.can_assign_worker(True, "production", "scientists"):
                    self.content["production_jobs_scientists_add_button_label"].color = (255, 255, 255, 255)
                    self.content["production_jobs_scientists_fill_button_label"].color = (255, 255, 255, 255)
                    if (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["production_jobs_scientists_add_button_area"]:
                        self.content["production_jobs_scientists_add_button_label"].color = (0, 255, 0, 255)
                        self.game_data.mouse_clickable_area = True
                    elif (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["production_jobs_scientists_fill_button_area"]:
                        self.content["production_jobs_scientists_fill_button_label"].color = (0, 255, 0, 255)
                        self.game_data.mouse_clickable_area = True
                else:
                    self.content["production_jobs_scientists_add_button_label"].color = (255, 255, 255, 100)
                    self.content["production_jobs_scientists_fill_button_label"].color = (255, 255, 255, 100)
                if self.selected_building.can_assign_worker(False, "production", "scientists"):
                    self.content["production_jobs_scientists_remove_button_label"].color = (255, 255, 255, 255)
                    self.content["production_jobs_scientists_empty_button_label"].color = (255, 255, 255, 255)
                    if (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["production_jobs_scientists_remove_button_area"]:
                        self.content["production_jobs_scientists_remove_button_label"].color = (255, 0, 0, 255)
                        self.game_data.mouse_clickable_area = True
                    elif (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["production_jobs_scientists_empty_button_area"]:
                        self.content["production_jobs_scientists_empty_button_label"].color = (255, 0, 0, 255)
                        self.game_data.mouse_clickable_area = True
                else:
                    self.content["production_jobs_scientists_remove_button_label"].color = (255, 255, 255, 100)
                    self.content["production_jobs_scientists_empty_button_label"].color = (255, 255, 255, 100)
                # construction job buttons
                if self.selected_building.can_assign_worker(True, "construction", "engineers"):
                    self.content["construction_jobs_add_button_label"].color = (255, 255, 255, 255)
                    self.content["construction_jobs_fill_button_label"].color = (255, 255, 255, 255)
                    if (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["construction_jobs_add_button_area"]:
                        self.content["construction_jobs_add_button_label"].color = (0, 255, 0, 255)
                        self.game_data.mouse_clickable_area = True
                    elif (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["construction_jobs_fill_button_area"]:
                        self.content["construction_jobs_fill_button_label"].color = (0, 255, 0, 255)
                        self.game_data.mouse_clickable_area = True
                else:
                    self.content["construction_jobs_add_button_label"].color = (255, 255, 255, 100)
                    self.content["construction_jobs_fill_button_label"].color = (255, 255, 255, 100)
                if self.selected_building.can_assign_worker(False, "construction", "engineers"):
                    self.content["construction_jobs_remove_button_label"].color = (255, 255, 255, 255)
                    self.content["construction_jobs_empty_button_label"].color = (255, 255, 255, 255)
                    if (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["construction_jobs_remove_button_area"]:
                        self.content["construction_jobs_remove_button_label"].color = (255, 0, 0, 255)
                        self.game_data.mouse_clickable_area = True
                    elif (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["construction_jobs_empty_button_area"]:
                        self.content["construction_jobs_empty_button_label"].color = (255, 0, 0, 255)
                        self.game_data.mouse_clickable_area = True
                else:
                    self.content["construction_jobs_remove_button_label"].color = (255, 255, 255, 100)
                    self.content["construction_jobs_empty_button_label"].color = (255, 255, 255, 100)
                # upgrade button
                if self.selected_building.is_constructing:
                    self.content["upgrade_button_label"].text = "ANNULER"
                    # upgrade cost
                    self.content["upgrade_power_icon"].opacity = 0
                    self.content["upgrade_power_label"].color = (192, 192, 192, 0)
                    self.content["upgrade_iron_icon"].color = (192, 192, 192, 0)
                    self.content["upgrade_iron_label"].color = (192, 192, 192, 0)
                    self.content["upgrade_aluminium_icon"].color = (192, 192, 192, 0)
                    self.content["upgrade_aluminium_label"].color = (192, 192, 192, 0)
                    self.content["upgrade_copper_icon"].color = (192, 192, 192, 0)
                    self.content["upgrade_copper_label"].color = (192, 192, 192, 0)
                    self.content["upgrade_titanium_icon"].color = (192, 192, 192, 0)
                    self.content["upgrade_titanium_label"].color = (192, 192, 192, 0)
                    # upgrade percent
                    self.content["upgrade_percent_label"].color = (192, 192, 192, 255)
                    self.content["upgrade_percent_label"].text = f"{round(self.selected_building.construction_workload_completed * 100 / self.selected_building.parameters["construction_workload"])} %"
                    if (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["upgrade_button_area"]:
                        self.content["upgrade_button_label"].color = (255, 127, 0, 255)
                        self.game_data.mouse_clickable_area = True
                    else:
                        self.content["upgrade_button_label"].color = (255, 255, 255, 255)
                else:
                    self.content["upgrade_button_label"].text = "AMELIORER"
                    # upgrade cost
                    # show next level upgrade cost if building is not at max level
                    if self.selected_building.level == self.selected_building.level_max:
                        self.content["upgrade_power_icon"].opacity = 0
                        self.content["upgrade_power_label"].color = (192, 192, 192, 0)
                        self.content["upgrade_iron_icon"].color = (192, 192, 192, 0)
                        self.content["upgrade_iron_label"].color = (192, 192, 192, 0)
                        self.content["upgrade_aluminium_icon"].color = (192, 192, 192, 0)
                        self.content["upgrade_aluminium_label"].color = (192, 192, 192, 0)
                        self.content["upgrade_copper_icon"].color = (192, 192, 192, 0)
                        self.content["upgrade_copper_label"].color = (192, 192, 192, 0)
                        self.content["upgrade_titanium_icon"].color = (192, 192, 192, 0)
                        self.content["upgrade_titanium_label"].color = (192, 192, 192, 0)
                    else:
                        self.content["upgrade_power_icon"].opacity = 255
                        self.content["upgrade_power_label"].color = (192, 192, 192, 255)
                        # self.content["upgrade_power_label"].text = "{:+}".format(
                        self.content["upgrade_power_label"].text = "-{}".format(
                            # self.selected_building.parameters_per_level[self.selected_building.level + 1]["power"]["produced"] -
                            # self.selected_building.parameters_per_level[self.selected_building.level + 1]["power"]["consumed"]
                            - self.selected_building.parameters_per_level[self.selected_building.level + 1]["power"]["consumed"]
                        )
                        self.content["upgrade_iron_icon"].color = (192, 192, 192, 255)
                        self.content["upgrade_iron_label"].color = (192, 192, 192, 255)
                        self.content["upgrade_iron_label"].text = str(self.selected_building.parameters["construction_costs"]["iron"])
                        self.content["upgrade_aluminium_icon"].color = (192, 192, 192, 255)
                        self.content["upgrade_aluminium_label"].color = (192, 192, 192, 255)
                        self.content["upgrade_aluminium_label"].text = str(self.selected_building.parameters["construction_costs"]["aluminium"])
                        self.content["upgrade_copper_icon"].color = (192, 192, 192, 255)
                        self.content["upgrade_copper_label"].color = (192, 192, 192, 255)
                        self.content["upgrade_copper_label"].text = str(self.selected_building.parameters["construction_costs"]["copper"])
                        self.content["upgrade_titanium_icon"].color = (192, 192, 192, 255)
                        self.content["upgrade_titanium_label"].color = (192, 192, 192, 255)
                        self.content["upgrade_titanium_label"].text = str(self.selected_building.parameters["construction_costs"]["titanium"])
                    # upgrade percent
                    self.content["upgrade_percent_label"].color = (192, 192, 192, 0)
                    if self.current_colony.can_upgrade_building():
                        if (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["upgrade_button_area"]:
                            self.content["upgrade_button_label"].color = (0, 255, 0, 255)
                            self.game_data.mouse_clickable_area = True
                        else:
                            self.content["upgrade_button_label"].color = (255, 255, 255, 255)
                    else:
                        self.content["upgrade_button_label"].color = (255, 255, 255, 100)
                # destroy button
                if self.current_colony.can_destroy_building():
                    if (self.game_data.mouse_x, self.game_data.mouse_y) in self.content["destroy_button_area"]:
                        self.content["destroy_button_label"].color = (255, 0, 0, 255)
                        self.game_data.mouse_clickable_area = True
                    else:
                        self.content["destroy_button_label"].color = (255, 255, 255, 255)
                else:
                    self.content["destroy_button_label"].color = (255, 255, 255, 100)
                # building specific stuff
                if self.selected_building.name == "warehouse":
                    self.content["building_description_string"] = self.style_description
                    self.content["building_description_string"] += "Les entrepôts permettent de stocker des matières solides : nourriture, minéraux et métaux raffinés.\n\n\n"
                    self.content["building_description_string"] += "Espace de stockage :\n\n"
                    if self.selected_building.level == self.selected_building.level_max:
                        self.content["building_description_string"] += "- Nourriture : {bold True}" + str(self.selected_building.parameters["storage"]["food"]) + "{bold False}\n\n"
                        self.content["building_description_string"] += "- Minerai et métaux : {bold True}" + str(self.selected_building.parameters["storage"]["iron"])
                    else:
                        # self.content["building_description_string"] += "{italic True}Niveau actuel :{italic False}\n\n"
                        self.content["building_description_string"] += "- Nourriture : {bold True}" + str(self.selected_building.parameters["storage"]["food"]) + "{bold False}\n\n"
                        self.content["building_description_string"] += "- Minerai et métaux : {bold True}" + str(self.selected_building.parameters["storage"]["iron"]) + "{bold False}\n\n"
                        self.content["building_description_string"] += "{italic True}Prochain niveau :{italic False}\n\n"
                        self.content["building_description_string"] += "- Nourriture : {bold True}" + str(self.selected_building.parameters_per_level[self.selected_building.level + 1]["storage"]["food"]) + "{bold False}\n\n"
                        self.content["building_description_string"] += "- Minerai et métaux : {bold True}" + str(self.selected_building.parameters_per_level[self.selected_building.level + 1]["storage"]["iron"])
                    self.content["building_description_layout"].document = decode_attributed(self.content["building_description_string"])
                elif self.selected_building.name == "liquid_tank":
                    self.content["building_description_string"] = self.style_description
                    self.content["building_description_string"] += "Les réservoirs permettent de stocker des substances liquides : eau, oxygène et hydrogène.\n\n\n"
                    self.content["building_description_string"] += "Espace de stockage :\n\n"
                    # if self.selected_building.level == self.selected_building.level_max:
                    self.content["building_description_string"] += "{bold True}" + str(self.selected_building.parameters["storage"]["water"]) + "{bold False}\n\n"
                    if self.selected_building.level != self.selected_building.level_max:
                        # self.content["building_description_string"] += "{italic True}Niveau actuel :{italic False} {bold True}" + str(self.selected_building.parameters["storage"]["water"]) + "{bold False}\n\n"
                        # self.content["building_description_string"] += "{bold True}" + str(self.selected_building.parameters["storage"]["water"]) + "{bold False}\n\n"
                        self.content["building_description_string"] += "{italic True}Prochain niveau :{italic False} {bold True}"+ str(self.selected_building.parameters_per_level[self.selected_building.level + 1]["storage"]["water"])
                    self.content["building_description_layout"].document = decode_attributed(self.content["building_description_string"])
                elif self.selected_building.name == "solar_panels":
                    self.content["building_description_string"] = self.style_description
                    self.content["building_description_string"] += "Les panneaux solaires permettent de produire de l'énergie électrique.\n\n\n"
                    self.content["building_description_string"] += "Energie produite :\n\n"
                    self.content["building_description_string"] += "{bold True}" + str(self.selected_building.parameters["power"]["produced"]) + "{bold False}\n\n"
                    if self.selected_building.level != self.selected_building.level_max:
                        self.content["building_description_string"] += "{italic True}Prochain niveau :{italic False} {bold True}"+ str(self.selected_building.parameters_per_level[self.selected_building.level + 1]["power"]["produced"])
                    self.content["building_description_layout"].document = decode_attributed(self.content["building_description_string"])
                elif self.selected_building.name == "electrolysis_station":
                    self.content["building_description_string"] = self.style_description
                    self.content["building_description_string"] += "Les stations d'électrolyses transforment l'eau en oxygène et hydrogène liquide.\n\n\n"
                    self.content["building_description_string"] += "Ratio de transformation:\n\n{bold True}1 H2O -> 1/2 O2 + 1 H2{bold False}\n\n\n"
                    self.content["building_description_string"] += "Vitesse de production :\n\n"
                    self.content["building_description_string"] += "{bold True}" + str(self.selected_building.parameters["production_speed"]) + "x{bold False}\n\n"
                    if self.selected_building.level != self.selected_building.level_max:
                        self.content["building_description_string"] += "{italic True}Prochain niveau :{italic False} {bold True}" + \
                            str(self.selected_building.parameters_per_level[self.selected_building.level + 1]["production_speed"]) + "x{bold False}\n\n"
                    self.content["building_description_layout"].document = decode_attributed(self.content["building_description_string"])
                elif self.selected_building.name == "greenhouse":
                    self.content["building_description_string"] = self.style_description
                    self.content["building_description_string"] += "Les Serres utilisent de l'eau pour produire de la nourriture et de l'oxygène.\n\n\n"
                    self.content["building_description_string"] += "Ratio de transformation:\n\n{bold True}1 H2O -> 5 nourriture + 1 02{bold False}\n\n\n"
                    self.content["building_description_string"] += "Vitesse de production :\n\n"
                    self.content["building_description_string"] += "{bold True}" + str(self.selected_building.parameters["production_speed"]) + "x{bold False}\n\n"
                    if self.selected_building.level != self.selected_building.level_max:
                        self.content["building_description_string"] += "{italic True}Prochain niveau :{italic False} {bold True}" + \
                            str(self.selected_building.parameters_per_level[self.selected_building.level + 1]["production_speed"]) + "x{bold False}\n\n"
                    self.content["building_description_layout"].document = decode_attributed(self.content["building_description_string"])
                elif self.selected_building.name == "spaceport":
                    self.content["building_description_string"] = self.style_description
                    self.content["building_description_string"] += "Les ports spaciaux permettent de lancer des missions de transport."
                    self.content["building_description_layout"].document = decode_attributed(self.content["building_description_string"])
                elif self.selected_building.name == "drilling_station":
                    ...
                elif self.selected_building.name == "furnace":
                    ...
                elif self.selected_building.name == "school":
                    ...
                elif self.selected_building.name == "factory":
                    ...


    def on_mouse_press(self, x, y):
        # check if a building tile is selected
        if self.current_colony.selected_building_tile_coords is not None:
            # check which building is on the tile
            if self.current_colony.selected_building is None:
                # check which option has been clicked on
                for building_name in self.content["building_options_dict"].keys():
                    if (x, y) in self.content["building_options_dict"][building_name]["button_area"]:
                        # print(building_name)
                        # add the building to the colony if possible
                        self.current_colony.add_building(building_name)
            else:
                if (x, y) in self.content["production_jobs_engineers_add_button_area"]:
                    # print("+1 engineer production")
                    self.selected_building.assign_worker(True, "production", "engineers")
                elif (x, y) in self.content["production_jobs_engineers_fill_button_area"]:
                    # print("fill engineer production")
                    self.selected_building.assign_worker(True, "production", "engineers", True)
                elif (x, y) in self.content["production_jobs_engineers_remove_button_area"]:
                    # print("-1 engineer production")
                    self.selected_building.assign_worker(False, "production", "engineers")
                elif (x, y) in self.content["production_jobs_engineers_empty_button_area"]:
                    # print("empty engineer production")
                    self.selected_building.assign_worker(False, "production", "engineers", True)
                elif (x, y) in self.content["production_jobs_scientists_add_button_area"]:
                    # print("+1 scientist production")
                    self.selected_building.assign_worker(True, "production", "scientists")
                elif (x, y) in self.content["production_jobs_scientists_fill_button_area"]:
                    # print("fill scientist production")
                    self.selected_building.assign_worker(True, "production", "scientists", True)
                elif (x, y) in self.content["production_jobs_scientists_remove_button_area"]:
                    # print("-1 scientist production")
                    self.selected_building.assign_worker(False, "production", "scientists")
                elif (x, y) in self.content["production_jobs_scientists_empty_button_area"]:
                    # print("empty scientist production")
                    self.selected_building.assign_worker(False, "production", "scientists", True)
                elif (x, y) in self.content["construction_jobs_add_button_area"]:
                    # print("+1 construction")
                    self.selected_building.assign_worker(True, "construction", "engineers")
                elif (x, y) in self.content["construction_jobs_fill_button_area"]:
                    # print("fill construction")
                    self.selected_building.assign_worker(True, "construction", "engineers", True)
                elif (x, y) in self.content["construction_jobs_remove_button_area"]:
                    # print("-1 construction")
                    self.selected_building.assign_worker(False, "construction", "engineers")
                elif (x, y) in self.content["construction_jobs_empty_button_area"]:
                    # print("empty construction")
                    self.selected_building.assign_worker(False, "construction", "engineers", True)
                elif (x, y) in self.content["upgrade_button_area"]:
                    if self.selected_building.is_constructing:
                        self.current_colony.cancel_building_construction()
                    else:
                        if self.current_colony.can_upgrade_building():
                            self.selected_building.upgrade()
                elif (x, y) in self.content["destroy_button_area"]:
                    self.current_colony.destroy_building()
                else:
                    # building specific stuff
                    ...

    def on_delete(self):
        # manually delete text layout objects
        if "building_description_layout" in self.content.keys():
            self.content["building_description_layout"].delete()


class RightWindowWidget:

    def __init__(self, game_data: GameData, batch, groups):
        self.game_data = game_data
        self.batch = batch
        self.groups = groups
        # right window state = (current_colony, current_building_coords, current_building)
        self.displayed_state = (self.game_data.active_colony, None, None)
        # building icons
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
        self.widget_content = RigthWindowWidgetContent(self.game_data, self.building_icons, self.batch, self.groups)

    @property
    def current_state(self):
        active_colony = self.game_data.active_colony
        current_colony = self.game_data.colonies[active_colony]
        if (current_colony.selected_building_tile_coords is not None) and (current_colony.selected_building is not None):
            current_building = current_colony.selected_building.name
        else:
            current_building = None
        return self.game_data.active_colony, current_colony.selected_building_tile_coords, current_building

    def on_draw(self):
        # if any value in the state has changed:
        # - redraw the entire window (create a new RightWindowWidgetContent object)
        # - update the window state (self.current_state)
        current_state = self.current_state
        if current_state != self.displayed_state:
            # print("right window state changed")
            self.widget_content.on_delete()
            self.widget_content = RigthWindowWidgetContent(self.game_data, self.building_icons, self.batch, self.groups)
            self.displayed_state = current_state
        # update the RightWindowWidgetContent object
        self.widget_content.on_draw()

    def on_mouse_press(self, x, y):
        # only send the mouse press if the current state is the one displayed
        if self.current_state == self.displayed_state:
            self.widget_content.on_mouse_press(x, y)


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
        self.left_window_content["water_available"].text = str(round(colony_resources["water"], 1))
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
