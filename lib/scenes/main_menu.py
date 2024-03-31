from pyglet.text import Label
import pyglet.shapes as shapes
from pyglet.sprite import Sprite
from pyglet.window import key, mouse
import sys
from pathlib import Path

ROOT_DIR_PATH = str(Path(__file__).resolve().parents[1])
if ROOT_DIR_PATH not in sys.path:
    sys.path.insert(0, ROOT_DIR_PATH)

from lib.scenes.scene_interface import Scene
from lib.game_state import GameState


class SceneMainMenu(Scene):

    def __init__(self, game_state: GameState):
        super().__init__(game_state)

        # background image
        self.background_sprite = Sprite(img=self.game_state.main_menu_background_img_region, batch=self.batch)

        # game title
        self.game_title = Label("HOMEBOUND", font_name=self.game_state.title_font_name, font_size=65, italic=True,
            x=self.game_state.window_width/2, y=self.game_state.window_height*13/16,
            anchor_x="center", anchor_y="center", batch=self.batch)

        # resume button
        self.resume_button = shapes.Rectangle(x=self.game_state.window_width/2 - 109, y=self.game_state.window_height / 2,
            width=219, height=23, color=(0, 0, 0, 0), batch=self.batch)
        self.resume_button_label = Label("CONTINUER", font_name=self.game_state.subtitle_font_name, font_size=25,
            x=self.game_state.window_width/2, y=self.game_state.window_height/2,
            anchor_x="center", batch=self.batch)

        # new game button
        self.new_game_button = shapes.Rectangle(x=self.game_state.window_width/2 - 183, y=self.game_state.window_height / 2 - 75,
            width=366, height=23, color=(0, 0, 0, 0), batch=self.batch)
        self.new_game_button_label = Label("NOUVELLE PARTIE", font_name=self.game_state.subtitle_font_name, font_size=25,
            color=(200, 200, 200, 255), x=self.game_state.window_width/2, y=self.game_state.window_height/2 - 75,
            anchor_x="center", batch=self.batch)

        # exit button
        self.exit_button = shapes.Rectangle(x=self.game_state.window_width/2 - 83, y=self.game_state.window_height / 2 - 150,
            width=167, height=23, color=(0, 0, 0, 0), batch=self.batch)
        self.exit_button_label = Label("QUITTER", font_name=self.game_state.subtitle_font_name, font_size=25,
            color=(200, 200, 200, 255), x=self.game_state.window_width/2, y=self.game_state.window_height/2 - 150,
            anchor_x="center", batch=self.batch)

        # mute toggle button
        self.sound_button = shapes.Rectangle(x=self.game_state.window_width*5/6, y=self.game_state.window_height/8 + 10,
            width=90, height=70, color=(0, 0, 0, 0), batch=self.batch)
        self.sound_button_sprite = None


    def draw(self):

        # update the batch

        # resume button label color
        if self.game_state.saved_game_available:
            self.resume_button_label.color = (200, 200, 200, 255)
        else:
            self.resume_button_label.color = (100, 100, 100, 255)

        # sound sprite
        if self.sound_button_sprite is not None:
            self.sound_button_sprite.delete()
        if self.game_state.sound_on:
            self.sound_button_sprite = Sprite(img=self.game_state.sound_on_img,
                x=self.game_state.window_width*5/6, y=self.game_state.window_height/8, batch=self.batch)
        else:
            self.sound_button_sprite = Sprite(img=self.game_state.sound_off_img,
                x=self.game_state.window_width*5/6, y=self.game_state.window_height/8, batch=self.batch)
        self.sound_button_sprite.scale = .35

        # draw the batch
        self.batch.draw()


    def on_mouse_press(self, x, y, button, modifiers) -> str:
        if button & mouse.LEFT:
            if (x, y) in self.sound_button:
                self.game_state.sound_on = not self.game_state.sound_on
            if (x, y) in self.exit_button:
                self.game_state.exit_game = True
        return "main menu"


    def on_mouse_motion(self, x, y):
        self.game_state.mouse_x, self.game_state.mouse_y = x, y
        # if (x, y) in self.resume_button:
        #     print("hovering self.resume_button")
        # elif (x, y) in self.new_game_button:
        #     print("hovering self.new_game_button")
        # elif (x, y) in
        # else:
        #     print("not hovering")
        self.game_state.mouse_clickable_area = ((x, y) in self.new_game_button) or ((x, y) in self.exit_button) or ((x, y) in self.sound_button)
        if self.game_state.saved_game_available:
            self.game_state.mouse_clickable_area = self.game_state.mouse_clickable_area or ((x, y) in self.resume_button)


    def on_key_press(self, symbol, modifiers) -> str:
        return "main menu"
