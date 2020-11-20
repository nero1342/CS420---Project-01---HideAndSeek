import random
from enum import Enum

import copy 

class Direction:
    def __init__(self):
        self.x = [0, 0, 0, 1, 1, 1, -1, -1, -1]
        self.y = [0, -1, 1, 0, -1, 1, 0, -1, 1]

    def __getitem__(self, id):
        return(self.x[id], self.y[id]) 

class Obstacle(Enum):
    WALL = 1
    OBSTACLE = 2


class GameMap:
    def __init__(self, path):
        super().__init__()
        self.load_map(path)
        self.lst_obs = {Obstacle.WALL, Obstacle.OBSTACLE}
        self.id = {}
    def load_map(self, path):
        with open(path, "r") as f:
            r, c = list(map(int, f.readline().split()))
            self.size = (r, c)  
            self.map = [[int(x) for x in line.split()] for line in f.readlines()]
        print(self.map)
        return

    def print_map(self):
        mp = self.map
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                print(mp[i][j], end = ' ')
            print()

    def is_player_here(self, position):
        x, y = position
        return self.map[x][y] > 2

    def inside(self, position):
        x, y = position 
        row, col = self.size 
        return 0 <= x and x < row and 0 <= y and y < col 

    def valid(self, position):
        x, y = position 
        return self.inside(position) and (self.map[x][y] not in self.lst_obs)

    def alive(self, player):
        x, y = player.position 
        id = player.id 
        return self.map[x][y] == id + 3

    def in_view(self, player, target):
        x, y = player.position
        r = player.view_range  
        i, j = target
        return max(abs(x - i),abs(y - j)) <= r

    def get_view(self, player):
        view = copy.deepcopy(self)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                # Setting view here
                if not self.in_view(player, (i, j)):
                    if (view.is_player_here((i, j))): 
                        view.map[i][j] = 0
        return view


    def get_free_cell(self):
        free = [(i, j) for i in range(self.size[0]) for j in range(self.size[1]) if self.map[i][j] == 0]
        indice = random.choice(free)
        return indice

    def set_player_position(self, player, id):
        pos = player.position
        self.map[pos[0]][pos[1]] = id + 3 
        self.id[id + 3] = player.__class__.__name__ 

    def move(self, player, direction):
        # Return list of Players is dead after this move
        x, y = player.position
        newX = x + Direction()[direction][0] 
        newY = y + Direction()[direction][1]
        ret = []

        if (self.valid((newX, newY))):
            if (self.map[newX][newY] == self.map[x][y]):
                # The same property 
                return ret
            if (self.is_player_here((newX, newY))):
                if (player.__class__.__name__ == "Seeker" 
                    and self.id[self.map[newX][newY]] == "Hider"):
                    ret.append(self.map[newX][newY] - 3) 
            print("Move from ({}, {}) to ({},{})".format(x, y, newX, newY))
            player.set_position((newX, newY))
            self.map[newX][newY] = self.map[x][y]
            self.map[x][y] = 0
        return ret
