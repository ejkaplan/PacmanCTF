from random import randint, choice
from location import *

'''
Functions for generating new mazes. You will not need to use anything in this file.
'''

def maze_gen(rows, cols, n_spawns, min_dist, max_dist):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    spawns = []
    while len(spawns) < n_spawns:
        sp = None
        while not sp or sp in spawns:
            sp = (choice(range(2, rows - 2, 2)),
                  choice(range(2, cols - 2, 2)))
        spawns.append(sp)
    carvers = []
    for spawn in spawns:
        dirs = list("nsew")
        for _ in range(randint(2, 4)):
            d = choice(dirs)
            dirs.remove(d)
            carvers.append(
                Carver(grid, spawn[0], spawn[1], d, min_dist, max_dist))
    n = 0
    while len(carvers) > 0:
        n += 1
        dead = []
        for carver in carvers:
            grid[carver.pos.row][carver.pos.col] = 1
            grid[
                len(grid) - carver.pos.row - 1][len(grid[0]) - carver.pos.col - 1] = 1
        for carver in carvers:
            carver.update()
        for carver in carvers:
            if grid[carver.pos.row][carver.pos.col] == 1:
                dead.append(carver)
                continue
            for other in carvers:
                if other == carver:
                    continue
                if carver.pos == other.pos:
                    grid[carver.pos.row][carver.pos.col] = 1
                    grid[
                        len(grid) - carver.pos.row - 1][len(grid) - carver.pos.col - 1] = 1
                    dead.append(carver)
                    dead.append(other)
        for carver in dead:
            if carver in carvers:
                carvers.remove(carver)
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if not grid[r][c]: continue
            if r < len(grid) // 2:
                grid[r][c] = 1
            elif r > len(grid) // 2:
                grid[r][c] = 2
            elif c < len(grid[r]) // 2:
                grid[r][c] = 1
            else:
                grid[r][c] = 2
    return grid


class Carver(object):

    def __init__(self, grid, row, col, heading, min_dist, max_dist):
        self.pos = Location(row, col)
        self.grid = grid
        self.heading = heading
        self.min_dist = min_dist
        self.max_dist = max_dist
        self.dist = choice(range(min_dist, max_dist + 1, 2))

    def turn(self):
        if self.pos.row % 2 != 0 or self.pos.col % 2 != 0:
            return
        dirs = list("nesw")
        c = dirs.index(self.heading)
        turn = choice([-1, 1])
        new_dir = dirs[(c + turn) % 4]
        next_pos = self.pos.get_loc_in_dir(new_dir)
        if not next_pos.isLegal(self.grid):
            new_dir = dirs[(c - turn) % 4]
        self.heading = new_dir

    def update(self):
        nextPos = self.pos.get_loc_in_dir(self.heading)
        if not nextPos.isLegal(self.grid) or self.dist == 0:
            self.turn()
            nextPos = self.pos.get_loc_in_dir(self.heading)
            self.dist = choice(range(self.min_dist, self.max_dist + 1, 2))
        else:
            self.dist -= 1
        self.pos = nextPos