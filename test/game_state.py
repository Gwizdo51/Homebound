class GameState:
    "contains the current state of the game"

    def __init__(self, window_width, window_height):

        # window
        self.window_width, self.window_height = window_width, window_height

        # font
        self.font = "Arial"

        # mouse
        self.mouse_x, self.mouse_y = 0, 0
        self.mouse_clickable_area = False

        # game data
        self.submenu_1_clicks = self.submenu_2_clicks = self.submenu_3_clicks = 0

    def update(self, dt):
        pass
