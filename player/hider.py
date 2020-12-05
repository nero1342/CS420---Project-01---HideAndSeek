from player import Player
import random 
import time
from queue import Queue

class Hider(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.announce_cell = None

    def move(self, view):
        return self.heuristic(view)
    
    def heuristic(self, view):
        curr_map = view.map
        q = Queue()
        hider_pos = self.position
        seeker_pos = self.get_seeker_in_view_range(view.map)
        if seeker_pos[0] == -1: # there are no seeker in hider view, so use announce cell to get best move
            if self.announce_cell:
                q.put(self.announce_cell)
            else:
                return random.randint(0, 8)
        else:
            q.put(seeker_pos)
        d = [[0 for i in range(len(curr_map[0]))] for j in range(len(curr_map))]
        dir = view.Direction()
        while not q.empty():
            cur_pos = q.get()
            for i in range(len(dir)):
                v = (cur_pos[0] + dir[i][0], cur_pos[1] + dir[i][1])
                if (view.valid(v) and d[v[0]][v[1]] == 0):
                    d[v[0]][v[1]] = d[cur_pos[0]][cur_pos[1]] + 1
                    q.put(v)

        best_val = -1
        best_target = -1
        for j in range(len(dir)):
            tmp = (hider_pos[0] + dir[j][0], hider_pos[1] + dir[j][1])
            if view.valid(tmp) and d[tmp[0]][tmp[1]] >= best_val:
                if d[tmp[0]][tmp[1]] == best_val and random.randint(0, 1):
                    continue
                best_val = d[tmp[0]][tmp[1]]
                best_target = j
        return best_target
    def get_seeker_in_view_range(self, map):
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 3:
                    return (i, j)
        
        return (-1, -1)

    def update_announce_cell(self, pos):
        self.announce_cell = pos