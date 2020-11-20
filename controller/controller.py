

class GameController:
    def __init__(self, config, map, players):
        self.config = config
        self.time = config['controller']['time']
        self.map = map 
        self.players = players 
        self.lst_player = list(self.players.keys())
        print(self.lst_player)

    def get_player(self, turn_id):
        return self.players[self.lst_player[turn_id]]

    def init_game(self):
        for i in range(len(self.lst_player)):
            pos = self.map.get_free_cell()
            player = self.get_player(i) 
            player.set_position(pos)
            player.set_id(i)
            self.map.set_player_position(pos, i)
        self.map.print_map()
        
    def run_game(self):
        self.init_game()
        turn_id = 0
        while self.time > 0:
            #
            print("Time remain:{} - Turn: {}".format(self.time, turn_id))
            #  
            player = self.get_player(turn_id)
            #
            if self.map.alive(player):
                self.take_turn(player)
            self.time -= 1
            
            turn_id = (turn_id + 1) % (len(self.lst_player))
        pass

    def take_turn(self, player):
        player_view = self.map.get_view(player)
        player_view.print_map()
        direction = player.move(player_view)
        self.map.move(player, direction)