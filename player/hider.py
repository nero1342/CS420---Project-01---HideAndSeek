from player import Player
import random 
class Hider(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def move(self, view):
        
        return random.randint(0, 8)