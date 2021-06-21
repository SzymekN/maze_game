class Cell():

    def __init__(self, i, j, settings):
        self.visited = False
        self.walls = [True, True, True, True]
        self.x = i
        self.y = j
        self.size = settings.cell_width
        self.bg_colour = [201, 124, 119,255] 