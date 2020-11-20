import random
from enum import Enum
import copy 
class Obstacle(Enum):
    WALL = 1
    OBSTACLE = 2

class GameMap:
    def __init__(self, path):
        super().__init__()
        self.load_map(path)
        
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

    def inside(self, player):
        x, y = player.position 
        row, col = self.size 
        return 0 <= x and x < row and 0 <= y and y < col 

    def alive(self, player):
        x, y = player.position 
        id = player.id 
        return self.map[x][y] == id + 3

    def get_view(self, player):
        x, y = player.position
        r = player.view_range  
        view = copy.deepcopy(self)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                # Setting view here
                if max(abs(x - i),abs(y - j)) > r:
                    if (view.map[i][j] > 2): 
                        view.map[i][j] = 0
        return view


    def get_free_cell(self):
        free = [(i, j) for i in range(self.size[0]) for j in range(self.size[1]) if self.map[i][j] == 0]
        indice = random.choice(free)
        return indice

    def set_player_position(self, pos, id):
        self.map[pos[0]][pos[1]] = id + 3 

    def move(self, player, direction):
        # print(player.__class__.__name__)
        pass 
