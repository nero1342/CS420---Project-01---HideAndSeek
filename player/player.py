
class Player:
    def __init__(self, movable, view_range):
        self.movable = movable
        self.view_range = view_range
        self.is_dead = False
        # self.position = position
        self.view_range
    def set_position(self, position):
        self.position = position

    def set_id(self, id):
        self.id = id 
        
    def dead(self):
        self.movable = False
        self.is_dead = True 
    def move(self, direction):
        return 
    
