from pygame import draw as py_dr
from random import choice

def draw_maze(m_game):
    """Draw cells, and walls between them"""
    drawn = m_game.grid[0][0]
    # size
    s = m_game.settings.cell_width
    for y in range(len(m_game.grid)):
        for x in range(len(m_game.grid[y])):
            drawn = m_game.grid[y][x]
            py_dr.rect(m_game.screen, drawn.bg_colour, (drawn.x*s, drawn.y*s,s,s))

            if drawn.walls[0] == True:
                py_dr.line(
                    m_game.screen, (60,60,60), (drawn.x * s , drawn.y*s ), ((drawn.x + 1)*s, drawn.y*s), 2)

            if drawn.walls[1] == True:
                py_dr.line(m_game.screen, (60,60,60), ((
                    drawn.x + 1) * s-2, drawn.y*s), ((drawn.x + 1)*s-2, (drawn.y+1)*s), 2)

            if drawn.walls[2] == True:
                py_dr.line(
                    m_game.screen, (60,60,60), (drawn.x * s, (drawn.y+1)*s-2), ((drawn.x + 1)*s, (drawn.y+1)*s-2), 2)

            if drawn.walls[3] == True:
                py_dr.line(
                    m_game.screen, (60,60,60), (drawn.x * s, drawn.y*s), (drawn.x*s, (drawn.y+1)*s), 2)
            


def highlight_current(m_game, current):
    """Highlight current cell when drawing"""
    s = m_game.settings.cell_width 
    py_dr.rect(m_game.screen, (200,20,20), (current.x*s+2 , current.y*s+2,s-4,s-4))
            
def check_neighbours(m_game,current):
    """Check if neighbouring cells were visited or not"""
    neighbours = []
    x = current.x
    y = current.y
    top, right, bottom, left = None, None, None, None

    if y > 0:
        top = m_game.grid[x][y-1]
    if x < m_game.cols - 1: 
        right = m_game.grid[x+1][y]
    if y < m_game.rows - 1:
        bottom = m_game.grid[x][y+1]
    if x > 0:
        left = m_game.grid[x-1][y]

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

def remove_walls(current, next):
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

def generate_maze(m_game, current):
    highlight_current(m_game, current)

    next = check_neighbours(m_game, current)

    if next:
        # set next cell as visited
        next.visited = True 
        next.bg_colour=(20,20,20)

        # add current cell to stack
        m_game.route.append(current)

        # remove walls between cells
        remove_walls(current,next)

        # set new current cell
        m_game.current = next

    # if no neighbours found move one step back
    elif len(m_game.route) > 0:
        m_game.current = m_game.route.pop()


