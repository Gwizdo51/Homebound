from pyglet import resource, font
import sys
from pathlib import Path

ROOT_DIR_PATH = str(Path(__file__).resolve().parents[1])
if ROOT_DIR_PATH not in sys.path:
    sys.path.insert(0, ROOT_DIR_PATH)

from lib.game_entities.colony import Colony


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
        self.colonies = {
            # starting colony
            "moon": ...,
            "mercury": ...,
            "venus": ...,
            "mars": ...,
            # Jupiter
            "ganymede": ...,
            "callisto": ...,
            # Saturn
            "titan": ...,
            "enceladus": ...
        }
        self.active_colony = "moon"

        # spaceships in transit
        # self.flying_spaceships = ...

        # research (currently researching + acquired)

        # earth goal (resources sent + required)


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


    def update(self, dt):
        # update every colony
        # update every flying spaceships
        pass
