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
        self.cell_w = self.settings.cell_width

        # player options
        self.x = self.cell_w / 2
        self.y = self.cell_w / 2
        self.size = self.cell_w / 4
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

        # Route
        self.last_pos = (0,0)
        self.route = [(self.last_pos)]


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

        self._update_route()

    def _update_route(self):
        current_pos = (self.x_index, self.y_index)
        # if player didn't move, skip
        if current_pos == self.last_pos:
            return

        # if player already been here remove node
        if current_pos in self.route:
            self.route.remove(self.last_pos)
            self.last_pos = current_pos
        # else add node
        else:
            self.last_pos = current_pos
            self.route.append(self.last_pos)

    def draw_route(self):
        # correct value to fit center of the square
        center = self.cell_w / 2
        last = None
        for segment in self.route:
            x = segment[0]
            y = segment[1]

            # draw node
            self.route_rect = Rect(x*self.cell_w + center, y*self.cell_w+center, self.size, self.size)
            self.route_rect.center = self.route_rect.topleft
            py_dr.ellipse(self.screen, self.colour, self.route_rect, 0)

            # draw connection between two nodes
            if len(self.route)>1 and last:
                 py_dr.line(
                        self.screen, self.colour, (last[0] * self.cell_w+center, last[1] * self.cell_w+center), (x * self.cell_w+center, y * self.cell_w+center), 2)

            # save current segment
            last = segment

            
    def draw_player(self):
        """Draw player"""
        self.player_rect = Rect(self.x, self.y, self.size, self.size)
        self.player_rect.center = self.player_rect.topleft
        py_dr.ellipse(self.screen, self.colour, self.player_rect, 0)
