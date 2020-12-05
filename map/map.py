import random
from enum import Enum

import copy 

class Obstacle(Enum):
    WALL = 1
    OBSTACLE = 2


class GameMap:
    class Direction:
        def __init__(self):
            self.x = [0, 0, 0, 1, 1, 1, -1, -1, -1]
            self.y = [0, -1, 1, 0, -1, 1, 0, -1, 1]
            
            
        pass 

        def __getitem__(self, id):
            return(self.x[id], self.y[id]) 

        def __len__(self):
            return len(self.x)
            
    def __init__(self, path):
        super().__init__()
        self.load_map(path)
        self.lst_obs = {1, 2}
        self.id = {}

        self.nxt = {
                0: {1, 4, 5},
                1: {2},
                2: {3},
                3: {},
                4: {8},
                5: {6, 9, 10},
                6: {7, 11},
                7: {},
                8: {12},
                9: {13, 14},
                10: {15},
                11: {},
                12: {},
                13: {},
                14: {},
                15: {}
            }

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
        dirx = (1, 1, -1, -1)
        diry = (1, -1, 1, -1)
        x, y = player.position
        r = player.view_range
        if type(player).__name__ == 'Hider':
            view_value = -2
        else:
            view_value = -1
        print(player.id)
        view = copy.deepcopy(self)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                # Setting view here
                if (view.is_player_here((i, j))): 
                    view.map[i][j] = 0
        for p in range(4):
            lst = []
            for i in range(r + 1):
                for j in range(r + 1):
                    pos = (i * dirx[p] + x, j * diry[p] + y) 
                    lst.append(pos)
            in_view = [0] * len(lst)
            in_view[0] = 1
            for i in range(len(lst)):
                pos = lst[i]
                if in_view[i] == 0:
                    continue 
                if (self.inside(pos) and self.map[pos[0]][pos[1]] in self.lst_obs):
                    continue
                if (self.map[pos[0]][pos[1]] == 0):
                    view.map[pos[0]][pos[1]] = view_value
                else:
                    view.map[pos[0]][pos[1]] = self.map[pos[0]][pos[1]]
                for j in self.nxt[i]:
                    in_view[j] = 1
            print(in_view)
        return view
    
    def get_system_view(self, players):
        dirx = (1, 1, -1, -1)
        diry = (1, -1, 1, -1)
        view = copy.deepcopy(self)
        for player in players:
            x, y = player.position
            if player.is_dead:
                continue
            r = player.view_range 
            # Get view street value. if hider so view = -2, player  view = -1
            if type(player).__name__ == 'Hider':
                view_value = -2
            else:
                view_value = -1
            for p in range(4):
                lst = []
                for i in range(r + 1):
                    for j in range(r + 1):
                        pos = (i * dirx[p] + x, j * diry[p] + y) 
                        lst.append(pos)
                in_view = [0] * len(lst)
                in_view[0] = 1
                for i in range(len(lst)):
                    pos = lst[i]
                    if in_view[i] == 0:
                        continue 
                    if (self.inside(pos) and self.map[pos[0]][pos[1]] in self.lst_obs):
                        continue
                    if -4 < view.map[pos[0]][pos[1]] < 0 and view.map[pos[0]][pos[1]] != view_value:
                        view.map[pos[0]][pos[1]] = -3
                    elif self.map[pos[0]][pos[1]] == 0:
                        view.map[pos[0]][pos[1]] = view_value
                    else: 
                        view.map[pos[0]][pos[1]] = self.map[pos[0]][pos[1]]
                    for j in self.nxt[i]:
                        in_view[j] = 1
                # print(in_view)
        return view

    def update_announce_cell(self, list_announce_cell):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] < -3:
                    self.map[i][j] = 0
        for cell in list_announce_cell:
            self.map[cell[0][0]][cell[0][1]] = cell[1]
    
    def clear_announce_cell(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] < -3:
                    self.map[i][j] = 0
  
    def get_free_cell(self):
        free = [(i, j) for i in range(self.size[0]) for j in range(self.size[1]) if self.map[i][j] == 0]
        indice = random.choice(free)
        return indice
    def is_announce_cell(self, pos):
        return self.map[pos[0]][pos[1]] not in [1, 2] 
    def set_player_position(self, player, id):
        pos = player.position
        self.map[pos[0]][pos[1]] = id + 3 
        print(id+3)
        self.id[id + 3] = player.__class__.__name__ 

    def move(self, player, direction):
        # Return list of Players is dead after this move
        x, y = player.position
        newX = x + self.Direction()[direction][0] 
        newY = y + self.Direction()[direction][1]
        ret = []

        if (self.valid((newX, newY))):
            if (self.map[newX][newY] == self.map[x][y]):
                # The same property 
                return ret
            if (self.is_player_here((newX, newY))):
                if (player.__class__.__name__ == "Seeker" 
                    and self.id[self.map[newX][newY]] == "Hider"):
                    ret.append(self.map[newX][newY] - 3) 
                    print("Seeker -> Hider")
            print("Move from ({}, {}) to ({},{})".format(x, y, newX, newY))
            player.set_position((newX, newY))
            self.map[newX][newY] = self.map[x][y]
            self.map[x][y] = 0
        return ret
