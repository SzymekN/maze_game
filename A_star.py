from typing import Counter


class A_Star():
    def __init__(self, m_game):

        # general game settings
        self.m_game = m_game
        self.settings = m_game.settings
        self.player = m_game.player
        self.maze_rows = m_game.rows
        self.maze_cols = m_game.cols
        self.screen = m_game.screen
        self.screen_rect = m_game.screen.get_rect()
        self.cell_w = self.settings.cell_width

        self.grid = m_game.maze.grid

        self.reset()

    def reset(self):

        self.player.reset()
        self.closed_set = []
        self.open_set = []
        self.start = self.grid[0][0]
        self.end = self.grid[self.maze_cols-1][self.maze_rows-1]
        self.open_set.append(self.start)
        self.path_found = False

        self.player = self.m_game.player
        self.route = self.player.route

        self.find_neighbours()
    def qucik_find(self):
        while len(self.open_set) > 0 and self.path_found == False and self.settings.q_solve:
            self.find_path()
        
        if self.settings.q_solve:
            self.player.route.insert(0,(self.end.x,self.end.y))

    def find_path(self):        
        self.route = []
        current = None
        if len(self.open_set) > 0 and self.path_found == False:
            lowest_cost = 0
            # select node closest to end of the maze
            for i in range(len(self.open_set)):
                if self.open_set[i].h < self.open_set[lowest_cost].h:
                    lowest_cost=i
            
            current = self.open_set[lowest_cost]

            if current == self.end:
                self.path_found = True
                return

            self.open_set.remove(current)
            self.closed_set.append(current)

            for neighbour in current.neighbours:
                if neighbour in self.closed_set:
                    continue

                temp_g = current.g + abs(current.x - neighbour.x) + abs(current.y - neighbour.y)
                new_path = False

                if neighbour in self.open_set:
                    if temp_g < neighbour.g:
                        neighbour.g = temp_g
                        new_path = True
                else:
                    neighbour.g = temp_g
                    new_path = True
                    self.open_set.append(neighbour)

                if new_path:
                    neighbour.h = abs(neighbour.x - self.end.x) + abs(neighbour.y - self.end.y)
                    neighbour.f = neighbour.h + neighbour.f
                    neighbour.previous = current

        if current:
            temp = current
        else:
            temp = self.end
        self.route.append((temp.x,temp.y))
        while temp.previous:
            self.route.append((temp.x,temp.y))
            temp = temp.previous
        self.route.append((0,0))
        self.player.route = self.route

    def find_neighbours(self):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                cell = self.grid[x][y]
            
                if y > 0 and not cell.walls[0]:
                    cell.neighbours.append(self.grid[x][y-1])
            
                if x < self.maze_cols and not cell.walls[1]:
                    cell.neighbours.append(self.grid[x+1][y])
            
                if y < self.maze_rows and not cell.walls[2]:
                    cell.neighbours.append(self.grid[x][y+1])
            
                if x > 0 and not cell.walls[3]:
                    cell.neighbours.append(self.grid[x-1][y])

