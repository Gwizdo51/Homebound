from pyglet import resource, font


class GameState:
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

        # game data
        # self.submenu_1_clicks = self.submenu_2_clicks = self.submenu_3_clicks = 0


    def load_resources(self):

        # tell pyglet where the resources are
        resource.path = ["assets"]
        resource.reindex()

        # fonts
        # blaster
        # https://fr.fonts2u.com/blaster-italic.police
        resource.add_font("blasteri.ttf")
        self.title_font_name = "Blaster"
        self.title_font = font.load(self.title_font_name, italic=True)
        # orbitron
        # https://fr.fonts2u.com/orbitron-black.police
        resource.add_font("orbitron-black.ttf")
        self.subtitle_font_name = "Orbitron"
        self.subtitle_font = font.load(self.subtitle_font_name)
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
        pass
