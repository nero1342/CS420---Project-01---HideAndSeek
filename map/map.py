class Map:
    def __init__(self, size):
        super().__init__()
        self.size = size 
        # self.map = [[0 for _ in range(size[1])] for _ in range(size[0])]

    def load_map(self, path):
        with open(path, "r") as f:
            r, c = list(map(int, f.readline().split()))
            self.size = (r, c)  
            self.map = [[int(x) for x in line.split()] for line in f.readlines()]
        print(self.map)
        return

    def inside(self, player):
        x, y = player.position 
        row, col = self.size 
        return 0 <= x and x < row and 0 <= y and y < col 

    def getView(self, player):
        x, y = player.position
        r = player.view_range  
        view = self.map 

    
mp = Map(5) 
mp.load_map("input.txt")