from pygame import draw as py_dr
from random import choice
from math import floor

import pygame
from pygame.display import set_allow_screensaver
from cell import Cell

class Maze():

    def __init__(self, m_game):
        """Initialize Maze"""

        # x,y indexes in grid
        self.x_index = m_game.player.x_index
        self.y_index = m_game.player.y_index
        # number of columns, rows
        self.rows = m_game.rows
        self.cols = m_game.cols
        # player fov
        self.fov = m_game.settings.draw_distance 
        # max distance beetwen first and last cell
        self.max_dist = m_game.rows + m_game.cols
        # fov paremeter 
        self.divisor = 255 / self.max_dist

        self.m_game = m_game
        self.settings = m_game.settings
        self.player = m_game.player
        self.screen = m_game.screen

        # set maze size
        self.grid = []

        # create list of cells in maze
        for j in range(self.rows):
            self.grid.append([])
            for i in range(self.cols):
                self.grid[j].append(Cell(j, i, self.settings))

        # set first cell as start
        self.current = self.grid[floor(self.cols/2)][floor(self.rows/2)]
        self.current.bg_colour = [60,60,60, 255]
        self.current.visited = True
        self.route = []

        self.generate_maze(self.current)
        while len(self.route) > 0:
            self.generate_maze(self.current)
            
        # set right bottom cell as exit    
        self.grid[0][0].bg_colour = [82, 181, 43, 255]
        self.grid[self.cols-1][self.rows-1].bg_colour = [82, 181, 43, 255]

    def draw_maze(self):
        if self.settings.FOV:
            self.draw_maze_fov()
        else:
            self.draw_maze_no_fov()

    def draw_maze_fov(self):
        """Draw cells, and walls between them"""
        drawn = self.grid[self.x_index][self.y_index] 
        self.y_index = self.player.y_index
        self.x_index = self.player.x_index
        # size
        s = self.settings.cell_width
        for y in range(len(self.grid[0])):
            for x in range(len(self.grid)):

                drawn = self.grid[x][y]
                colour = drawn.bg_colour
                alpha = self.calculate_alpha(x,y)
                colour[3] = alpha
                # draw cell on surface
                cell = pygame.Surface((s,s), pygame.SRCALPHA)
                cell.fill(colour)
                self.screen.blit(cell,((drawn.x*s, drawn.y*s)))


                if drawn.walls[0] == True:
                    wall = pygame.Surface((s,2))
                    wall.set_alpha(alpha)
                    wall.fill((20,20,20))
                    self.screen.blit(wall,((drawn.x * s , drawn.y*s )))

                if drawn.walls[1] == True:
                    wall = pygame.Surface((2,s))
                    wall.set_alpha(alpha)
                    wall.fill((20,20,20))
                    self.screen.blit(wall,((drawn.x + 1) * s-2, drawn.y*s))

                if drawn.walls[2] == True:
                    wall = pygame.Surface((s,2))
                    wall.set_alpha(alpha)
                    wall.fill((20,20,20))
                    self.screen.blit(wall,((drawn.x * s, (drawn.y+1)*s-2)))

                if drawn.walls[3] == True:
                    wall = pygame.Surface((2,s))
                    wall.set_alpha(alpha)
                    wall.fill((20,20,20))
                    self.screen.blit(wall,((drawn.x * s, drawn.y*s)))

    def draw_maze_no_fov(self):
        """Draw cells, and walls between them"""

        # size
        s = self.settings.cell_width
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):

                drawn = self.grid[x][y]
                # draw cell on surface
                py_dr.rect(self.screen, drawn.bg_colour, (drawn.x*s, drawn.y*s,s,s))

                if drawn.walls[0] == True:
                    py_dr.line(
                        self.screen, (20,20,20), (drawn.x * s , drawn.y*s ), ((drawn.x + 1)*s, drawn.y*s), 2)

                if drawn.walls[1] == True:
                    py_dr.line(self.screen, (20,20,20), ((
                        drawn.x + 1) * s-2, drawn.y*s), ((drawn.x + 1)*s-2, (drawn.y+1)*s), 2)

                if drawn.walls[2] == True:
                    py_dr.line(
                        self.screen, (20,20,20), (drawn.x * s, (drawn.y+1)*s-2), ((drawn.x + 1)*s, (drawn.y+1)*s-2), 2)

                if drawn.walls[3] == True:
                    py_dr.line(
                        self.screen, (20,20,20), (drawn.x * s, drawn.y*s), (drawn.x*s, (drawn.y+1)*s), 2)


    def calculate_alpha(self,x,y):
        # calculate alpha based on distance
        distance = ((abs(self.y_index - y)**2 + abs(self.x_index - x)**2)+0.1)**(1/2)
        alpha = 255 - distance * self.divisor * self.fov
        if alpha < 0:
            alpha = 0
        return alpha

    def highlight_current(self, current):
        """Highlight current cell when drawing"""
        s = self.settings.cell_width 
        py_dr.rect(self.screen, (200,20,20), (current.x*s+2 , current.y*s+2,s-4,s-4))
                
    def check_neighbours(self,current):
        """Check if neighbouring cells were visited or not"""
        neighbours = []
        x = current.x
        y = current.y
        top, right, bottom, left = None, None, None, None

        if y > 0:
            top = self.grid[x][y-1]
        if x < self.cols - 1: 
            right = self.grid[x+1][y]
        if y < self.rows - 1:
            bottom = self.grid[x][y+1]
        if x > 0:
            left = self.grid[x-1][y]

        if top and not top.visited:
            neighbours.append(top)

        if right and not right.visited:
            neighbours.append(right)

        if bottom and not bottom.visited:
            neighbours.append(bottom)

        if left and not left.visited:
            neighbours.append(left)

        if len(neighbours) > 0:
            return choice(neighbours)
        else:
            return None

    def remove_walls(self,current, next):
        """Remove walls between cells"""
        x =  next.x - current.x 
        y =  next.y - current.y 

        if x == 1:
            current.walls[1] = False
            next.walls[3] = False
        elif x == -1:
            current.walls[3] = False
            next.walls[1] = False

        if y == 1:
            current.walls[2] = False
            next.walls[0] = False
        elif y == -1:
            current.walls[0] = False
            next.walls[2] = False

    def generate_maze(self, current):
        self.highlight_current(current)

        next = self.check_neighbours(current)

        if next:
            # set next cell as visited
            next.visited = True 
            next.bg_colour=[60,60,60,255]

            # add current cell to stack
            self.route.append(current)

            # remove walls between cells
            self.remove_walls(current,next)

            # set new current cell
            self.current = next

        # if no neighbours found move one step back
        elif len(self.route) > 0:
            self.current = self.route.pop()


