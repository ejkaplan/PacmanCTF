class Location(object):
    
    '''
    Convenience class that I made to keep track of distances and to do things like manhattan distances.
    You don't need it, and all positions are presented to you as tuples, but you are welcome to import
    this class and use Location objects if you so desire.
    '''

    def __init__(self, r, c):
        self.row = r
        self.col = c

    def get_loc_in_dir(self, d):
        if d == None:
            return self
        directions = {'n': (-1, 0), 's': (1, 0), 'w': (0, -1), 'e': (0, 1)}
        d = d.lower()
        if d not in directions:
            return self
        d = directions[d]
        return Location(self.row + d[0], self.col + d[1])

    def isLegal(self, grid):
        if self.row < 0 or self.col < 0 or self.row >= len(grid) or self.col >= len(grid[self.row]):
            return False
        return True
    
    def get_tuple(self):
        return (self.row, self.col)
    
    def get_mirror(self, size):
        return Location(size - self.row - 1, size - self.col - 1)

    def manhattan_distance(self, other):
        return abs(self.row - other.row) + abs(self.col - other.col)

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def __lt__(self, other):
        return self.get_tuple() < other.get_tuple()

    def __str__(self):
        return "loc({},{})".format(self.row, self.col)
    