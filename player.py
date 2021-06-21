from math import floor
from pygame import draw as py_dr
from pygame import Rect

class Player():
    def __init__(self, m_game):
        """Initilize player"""

        # general game settings
        self.m_game = m_game
        self.settings = m_game.settings
        self.maze_rows = m_game.rows
        self.maze_cols = m_game.cols
        self.screen = m_game.screen
        self.screen_rect = m_game.screen.get_rect()

        # player options
        self.x = m_game.settings.cell_width / 2
        self.y = m_game.settings.cell_width / 2
        self.size = m_game.settings.cell_width / 4
        self.colour = (230, 242, 225)
        self.x_index = 0
        self.y_index = 0

        # player apperance
        self.player_rect = Rect(self.x, self.y, self.size, self.size)
        self.player_rect.center = self.player_rect.topleft

        # movement flags
        self.move_u = False
        self.move_r = False
        self.move_d = False
        self.move_l = False

    def update(self):
        """Update player position"""
        self.grid = self.m_game.maze.grid

        # find current cell
        self.x_index = floor(self.x / self.settings.cell_width)
        self.y_index = floor(self.y / self.settings.cell_width)
        cell = self.grid[self.x_index][self.y_index]

        # set boundaries
        top_wall = 0
        left_wall = 0
        right_wall = self.screen_rect.width
        bottom_wall = self.screen_rect.height

        cell_top = cell.y * cell.size
        cell_right = (cell.x + 1)* cell.size
        cell_bottom = (cell.y+1) * cell.size
        cell_left = cell.x * cell.size


        if cell.walls[0]:
            top_wall = cell_top
        
        if cell.walls[1]:
            right_wall = cell_right
        
        if cell.walls[2]:
            bottom_wall = cell_bottom
        
        if cell.walls[3]:
            left_wall = cell_left


        # if player won't pass through any wall move
        if self.move_u and self.player_rect.top - self.size/2> top_wall:
            self.y -= self.settings.player_speed

        if self.move_r and self.player_rect.right + self.size/2< right_wall:
            self.x += self.settings.player_speed
        
        if self.move_d and self.player_rect.bottom + self.size /2 < bottom_wall:
            self.y += self.settings.player_speed
            
        if self.move_l and self.player_rect.left - self.size/2> left_wall:
            self.x -= self.settings.player_speed


    def draw_player(self):
        """Draw player"""
        self.player_rect = Rect(self.x, self.y, self.size, self.size)
        self.player_rect.center = self.player_rect.topleft
        py_dr.ellipse(self.screen, self.colour, self.player_rect, 0)
