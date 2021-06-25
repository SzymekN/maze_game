class Cell():

    def __init__(self, i, j, settings):
        self.visited = False
        self.walls = [True, True, True, True]
        self.x = i
        self.y = j
        self.size = settings.cell_width
        self.bg_colour = [201, 124, 119,255] 

        # A* parameters
        self.f = 0
        self.h = 0
        self.g = 0
        self.neighbours = []
        self.previous = None
