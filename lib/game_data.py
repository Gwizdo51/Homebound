from pyglet import resource, font
import sys
from pathlib import Path

ROOT_DIR_PATH = str(Path(__file__).resolve().parents[1])
if ROOT_DIR_PATH not in sys.path:
    sys.path.insert(0, ROOT_DIR_PATH)

from lib.game_entities.colony import Colony


def center_image(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2


class GameData:
    "contains the current state of the game"

    def __init__(self, window_width, window_height):

        # window
        self.window_width, self.window_height = window_width, window_height

        # load resources
        self.load_resources()

        # mouse
        self.mouse_x, self.mouse_y = 0, 0
        self.mouse_clickable_area = False

        # flags
        self.sound_on = True
        self.saved_game_available = False
        self.exit_game = False
        self.game_paused = True

        # game data

        # colonies dictionary
        self.colonies: dict[str, Colony] = {
            # starting colony
            "moon": Colony(starting_colony=True),
            "mercury": Colony(),
            "venus": Colony(),
            "mars": Colony(),
            # Jupiter
            "ganymede": Colony(),
            "callisto": Colony(),
            # Saturn
            "titan": Colony(),
            "enceladus": Colony()
        }
        self.active_colony = "moon"

        # spaceships in transit
        self.flying_spaceships = []

        # research (currently researching + acquired)

        # earth goal (resources sent + required)


    def launch_ship(self):
        pass


    def update(self, dt):
        # update every colony
        # update every flying spaceships
        pass


    def load_resources(self):

        # tell pyglet where the resources are
        resource.path = ["assets"]
        resource.reindex()

        # fonts
        # blaster
        # https://fr.fonts2u.com/blaster-italic.police
        resource.add_font("blasteri.ttf")
        self.title_font_name = "Blaster"
        font.load(self.title_font_name, italic=True)
        # orbitron
        # https://fr.fonts2u.com/orbitron-black.police
        resource.add_font("orbitron-black.ttf")
        self.subtitle_font_name = "Orbitron"
        font.load(self.subtitle_font_name)
        # default
        self.default_font_name = "Arial"

        # main menu background image
        # https://getwallpapers.com/image/eyJpdiI6IjdQXC8rZkRRbUNRSml4QlllXC8xb253dz09IiwidmFsdWUiOiJ3UDZRS3RqeUxVVGhZQnBQYWhcL1IzZz09IiwibWFjIjoiNjAxYTI2NGI0MDAwZDA2NGIyZDk5MTdmNGE3OWVhMGNkODc1YjIwYTgxMDY5MDVmNTE2MGZjYmU4ZjhiZmMyZCJ9
        self.main_menu_background_img = resource.image("milky_way_cropped.jpg")
        self.main_menu_background_img_region = self.main_menu_background_img.get_region(
            x = self.main_menu_background_img.width - self.window_width,
            y = int((self.main_menu_background_img.height - self.window_height) / 2),
            width = self.window_width,
            height = self.window_height
        )

        # mute/unmute image
        # https://www.svgrepo.com/svg/486849/sound-loud
        self.sound_on_img = resource.image("sound_on.png")
        # https://www.svgrepo.com/svg/486852/sound-mute
        self.sound_off_img = resource.image("sound_off.png")

        # window with title bar
        self.side_window = resource.image("Example_Window.png")
        self.side_window.anchor_y = self.side_window.height // 2

        # moon background
        # https://www.space.com/734-moon-smart-1-returns-close-ups.html
        self.moon_background_img = resource.image("moon_surface_pixelated.png")
        # self.moon_background_img = resource.image("moon_surface.jpg")

        # game icon
        # https://www.pngegg.com/en/png-nocyw
        self.game_logo = resource.image("game-logo-32.png")

        # icons

        # workers
        # https://www.svgrepo.com/svg/334853/plane-alt
        self.icon_plane_light_gray = resource.image("icon-plane-c0c0c0.png")
        center_image(self.icon_plane_light_gray)
        # https://www.svgrepo.com/svg/385283/wrench-tool-options
        self.icon_wrench_light_gray = resource.image("icon-wrench-c0c0c0.png")
        center_image(self.icon_wrench_light_gray)
        # https://www.svgrepo.com/svg/152182/chemistry-lab-instrument
        self.icon_vial_light_gray = resource.image("icon-vial-c0c0c0.png")
        center_image(self.icon_vial_light_gray)

        # resources
        # https://www.svgrepo.com/svg/390846/lightning-bolt-weather-storm-energy-electricity
        self.icon_bolt_light_gray = resource.image("icon-lightning-bolt-c0c0c0.png")
        center_image(self.icon_bolt_light_gray)
        # https://www.svgrepo.com/svg/499449/water-drop
        self.icon_water_light_gray = resource.image("icon-water-c0c0c0.png")
        center_image(self.icon_water_light_gray)
        # https://www.svgrepo.com/svg/244783/apple
        self.icon_apple_light_gray = resource.image("icon-apple-c0c0c0.png")
        center_image(self.icon_apple_light_gray)
        # https://thenounproject.com/icon/iron-ingot-52023/
        self.icon_ingot_light_gray = resource.image("icon-ingot-c0c0c0.png")
        center_image(self.icon_ingot_light_gray)
        # https://www.svgrepo.com/svg/321290/rock
        self.icon_ore_light_gray = resource.image("icon-ore-c0c0c0.png")
        center_image(self.icon_ore_light_gray)

        # items
        # https://www.svgrepo.com/svg/161941/spaceship
        self.icon_spaceship_light_gray = resource.image("icon-spaceship-c0c0c0.png")
        center_image(self.icon_spaceship_light_gray)
        # https://www.svgrepo.com/svg/445050/container-optimize-solid
        self.icon_crate_light_gray = resource.image("icon-crate-c0c0c0.png")
        center_image(self.icon_crate_light_gray)
        # https://www.svgrepo.com/svg/244184/barrel
        self.icon_barrel_light_gray = resource.image("icon-barrel-c0c0c0.png")
        center_image(self.icon_barrel_light_gray)
        # https://www.svgrepo.com/svg/122440/car-seat
        self.icon_seat_light_gray = resource.image("icon-seat-c0c0c0.png")
        center_image(self.icon_seat_light_gray)
        # https://www.svgrepo.com/svg/436792/house-fill
        self.icon_house_light_gray = resource.image("icon-house-c0c0c0.png")
        center_image(self.icon_house_light_gray)

        # misc
        # https://www.svgrepo.com/svg/521755/minus
        self.icon_minus_white = resource.image("icon-minus-FFFFFF.png")
        center_image(self.icon_minus_white)
        # https://bdragon1727.itch.io/basic-pixel-health-bar-and-scroll-bar
        self.icon_selector = resource.image("icon-selector.png")
        center_image(self.icon_selector)

        # buildings
        self.icon_house_black = resource.image("icon-house-000000.png")
        center_image(self.icon_house_black)
        # https://www.svgrepo.com/svg/158880/solar-panels
        self.icon_solar_panels_black = resource.image("icon-solar-panels-000000.png")
        center_image(self.icon_solar_panels_black)
        self.icon_solar_panels_white = resource.image("icon-solar-panels-ffffff.png")
        center_image(self.icon_solar_panels_white)
        self.icon_solar_panels_green = resource.image("icon-solar-panels-68B842.png")
        center_image(self.icon_solar_panels_green)
        self.icon_solar_panels_dark_gray = resource.image("icon-solar-panels-808080.png")
        center_image(self.icon_solar_panels_dark_gray)
        # https://www.svgrepo.com/svg/412370/drill
        self.icon_drill_black = resource.image("icon-drill-000000.png")
        center_image(self.icon_drill_black)
        self.icon_drill_white = resource.image("icon-drill-ffffff.png")
        center_image(self.icon_drill_white)
        self.icon_drill_green = resource.image("icon-drill-68B842.png")
        center_image(self.icon_drill_green)
        self.icon_drill_dark_gray = resource.image("icon-drill-808080.png")
        center_image(self.icon_drill_dark_gray)
        self.icon_crate_black = resource.image("icon-crate-000000.png")
        center_image(self.icon_crate_black)
        self.icon_crate_white = resource.image("icon-crate-ffffff.png")
        center_image(self.icon_crate_white)
        self.icon_crate_green = resource.image("icon-crate-68B842.png")
        center_image(self.icon_crate_green)
        self.icon_crate_dark_gray = resource.image("icon-crate-808080.png")
        center_image(self.icon_crate_dark_gray)
        self.icon_barrel_black = resource.image("icon-barrel-000000.png")
        center_image(self.icon_barrel_black)
        self.icon_barrel_white = resource.image("icon-barrel-ffffff.png")
        center_image(self.icon_barrel_white)
        self.icon_barrel_green = resource.image("icon-barrel-68B842.png")
        center_image(self.icon_barrel_green)
        self.icon_barrel_dark_gray = resource.image("icon-barrel-808080.png")
        center_image(self.icon_barrel_dark_gray)
        # https://www.svgrepo.com/svg/385034/bubble-bubbles-washing-cleaning-soap
        self.icon_bubbles_black = resource.image("icon-bubbles-000000.png")
        center_image(self.icon_bubbles_black)
        self.icon_bubbles_white = resource.image("icon-bubbles-ffffff.png")
        center_image(self.icon_bubbles_white)
        self.icon_bubbles_green = resource.image("icon-bubbles-68B842.png")
        center_image(self.icon_bubbles_green)
        self.icon_bubbles_dark_gray = resource.image("icon-bubbles-808080.png")
        center_image(self.icon_bubbles_dark_gray)
        # https://www.svgrepo.com/svg/112303/flame
        self.icon_flame_black = resource.image("icon-flame-000000.png")
        center_image(self.icon_flame_black)
        self.icon_flame_white = resource.image("icon-flame-ffffff.png")
        center_image(self.icon_flame_white)
        self.icon_flame_green = resource.image("icon-flame-68B842.png")
        center_image(self.icon_flame_green)
        self.icon_flame_dark_gray = resource.image("icon-flame-808080.png")
        center_image(self.icon_flame_dark_gray)
        self.icon_spaceship_black = resource.image("icon-spaceship-000000.png")
        center_image(self.icon_spaceship_black)
        self.icon_spaceship_white = resource.image("icon-spaceship-ffffff.png")
        center_image(self.icon_spaceship_white)
        self.icon_spaceship_green = resource.image("icon-spaceship-68B842.png")
        center_image(self.icon_spaceship_green)
        self.icon_spaceship_dark_gray = resource.image("icon-spaceship-808080.png")
        center_image(self.icon_spaceship_dark_gray)
        # https://www.svgrepo.com/svg/513255/tree-decidious
        self.icon_tree_black = resource.image("icon-tree-000000.png")
        center_image(self.icon_tree_black)
        self.icon_tree_white = resource.image("icon-tree-ffffff.png")
        center_image(self.icon_tree_white)
        self.icon_tree_green = resource.image("icon-tree-68B842.png")
        center_image(self.icon_tree_green)
        self.icon_tree_dark_gray = resource.image("icon-tree-808080.png")
        center_image(self.icon_tree_dark_gray)
        # https://www.svgrepo.com/svg/485635/book
        self.icon_book_black = resource.image("icon-book-000000.png")
        center_image(self.icon_book_black)
        self.icon_book_white = resource.image("icon-book-ffffff.png")
        center_image(self.icon_book_white)
        self.icon_book_green = resource.image("icon-book-68B842.png")
        center_image(self.icon_book_green)
        self.icon_book_dark_gray = resource.image("icon-book-808080.png")
        center_image(self.icon_book_dark_gray)
        # https://www.svgrepo.com/svg/220523/factory
        self.icon_factory_black = resource.image("icon-factory-000000.png")
        center_image(self.icon_factory_black)
        self.icon_factory_white = resource.image("icon-factory-ffffff.png")
        center_image(self.icon_factory_white)
        self.icon_factory_green = resource.image("icon-factory-68B842.png")
        center_image(self.icon_factory_green)
        self.icon_factory_dark_gray = resource.image("icon-factory-808080.png")
        center_image(self.icon_factory_dark_gray)
