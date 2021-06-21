from math import floor


class Settings():
    def __init__(self):
        """Game settings"""

        # general options
        self.screen_size = (500, 500)
        self.bg_color = (100,100,100)
        self.FPS = 60

        # cell options
        self.cell_width = 50
        self.draw_distance = 3

        # player speed
        self.player_speed = 5

        self._adjust_screen()

    def _adjust_screen(self):
        if self.screen_size[0] % self.cell_width != 0 or self.screen_size[1] % self.cell_width != 0:
            new_size = floor(self.screen_size[0]/self.cell_width)
            self.screen_size = (new_size * self.cell_width, new_size*self.cell_width)