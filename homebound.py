import pyglet
from pyglet.window import key, mouse

from lib.game_manager import GameManager


class GameWindow(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        # init pyglet window
        super().__init__(*args, **kwargs)
        # create the game manager and give it the window handlers
        self.game_manager = GameManager(self.width, self.height)
        self.push_handlers(self.game_manager)
        # cursors types
        self.cursors = {
            "default": self.get_system_mouse_cursor(self.CURSOR_DEFAULT),
            "hand": self.get_system_mouse_cursor(self.CURSOR_HAND)
        }
        # window icon
        self.set_icon(self.game_manager.game_data.game_logo)
        # FPS
        self.fps_counter = pyglet.window.FPSDisplay(window=self, color=(255, 0, 0, 255))

        # self.counter = 0

    # mouse events
    def on_mouse_motion(self, x, y, dx, dy):
        # pass
        # print(f"mouse position: {x} {y}")
        # print("window on_mouse_motion call")
        # print(f"clickable area : {self.game_manager.game_state.mouse_clickable_area}")
        # update the cursor shape
        if self.game_manager.game_data.mouse_clickable_area:
            self.set_mouse_cursor(self.cursors["hand"])
        else:
            self.set_mouse_cursor(self.cursors["default"])

    def on_mouse_press(self, x, y, button, modifiers):
        # print("window mouse press")
        # print(f"mouse pressed at {x} {y}, button: {button}")
        # if button & mouse.LEFT:
        #     print("left button")
        # elif button & mouse.RIGHT:
        #     print("right button")
        # elif button & mouse.MIDDLE:
        #     print("middle button")
        # elif button & mouse.MOUSE4:
        #     print("MOUSE4 button")
        # elif button & mouse.MOUSE5:
        #     print("MOUSE5 button")
        # else:
        #     print("unknown button")
        if self.game_manager.game_data.exit_game:
            self.close()

    # def on_mouse_release(self, x, y, button, modifiers):
    #     pass

    # def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    #     pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

    def on_mouse_enter(self, x, y):
        # print("mouse entered the window")
        pass

    def on_mouse_leave(self, x, y):
        # print("mouse left the window")
        pass

    # keyboard events
    def on_key_press(self, symbol, modifiers):
        # print(symbol)
        if symbol == key.ESCAPE:
            # exit()
            self.close()
            # pass
            # self.has_exit = True

    # def on_key_release(self, symbol, modifiers):
    #     pass

    # window events
    def on_activate(self):
        # print("window is activated")
        pass

    def on_deactivate(self):
        # print("window is deactivated")
        pass

    # def on_hide(self):
    #     # print("window is hidden")
    #     pass

    # def on_show(self):
    #     # print("window is shown")
    #     pass

    def on_close(self):
        # print("window is closed")
        self.close()
        # super().on_close()

    # update window display
    def on_draw(self):
        # print(f"on_draw call #{self.counter}")
        # self.counter += 1
        self.clear()
        # self.game_manager.scenes[self.game_manager.current_scene].batch.draw()
        # self.game_manager.scenes[self.game_manager.current_scene].draw()
        self.game_manager.current_scene.draw()
        # update the cursor shape
        self.dispatch_event("on_mouse_motion", self.game_manager.game_data.mouse_x, self.game_manager.game_data.mouse_y, 0, 0)
        # FPS
        self.fps_counter.draw()

    # only useful for stuff that needs to know how much time passed between each frames
    def update(self, dt):
        # print(dt)
        self.game_manager.update(dt)


if __name__ == "__main__":
    # init the window
    window = GameWindow(1280, 720, "Homebound", resizable=False)
    # update the game 60 times per seconds
    update_rate = 30
    pyglet.clock.schedule_interval(window.update, 1/update_rate)
    # run the game
    pyglet.app.run()
