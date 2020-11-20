from player import Player
class Hider(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def move(self, view):
        pass