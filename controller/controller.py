import pygame as pg 
from pygame.locals import *
import numpy as np 

class GameController:
    def __init__(self, config, map, players, graphic):
        self.config = config
        self.time = config['controller']['time']
        self.graphic = graphic
        self.map = map 
        self.players = players 
        self.lst_player = list(self.players.keys())
        print(self.lst_player)


        
        pg.init() 
        self.screen = pg.display.set_mode((1000, 600))
        pg.display.set_caption('Hide and Seek')
        self.clock = pg.time.Clock()

        
        # while True:
            
        # Fill background

    def get_player(self, turn_id):
        return self.players[self.lst_player[turn_id]]

    def init_game(self):
        for i in range(len(self.lst_player)):
            pos = self.map.get_free_cell()
            player = self.get_player(i) 
            player.set_position(pos)
            player.set_id(i)
            self.map.set_player_position(player, i)
        self.map.print_map()
        
    def run_turn(self, turn_id):
        player = self.get_player(turn_id)
        if player.movable and self.map.alive(player):
            print("Time remain:{} - Turn: {}".format(self.time, turn_id))
            self.take_turn(player)
            return True 
        return False 
    def draw(self):
        temp = np.asarray(self.map.map).astype(int)
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
        surf = pg.surfarray.make_surface(temp)
        surf = pg.transform.scale(surf, (600, 600))  # Scaled a bit.  
        self.screen.blit(surf, (0, 0))
        pg.display.flip()
        self.clock.tick(1)
        print("Render")
    
    def run_game(self):
        self.init_game()
        turn_id = 0
        while self.time > 0:
            if self.run_turn(turn_id):
                self.graphic.draw(self.map.map)
            turn_id = (turn_id + 1) % (len(self.lst_player))
            # self.time -= 1
        pass

    def take_turn(self, player):
        player_view = self.map.get_view(player)
        # print("Seeker's map")
        # player_view.print_map()
        direction = player.move(player_view)
        lst_dead = self.map.move(player, direction)
        [self.get_player(id).dead() for id in lst_dead]
        # print("Org map")
        # self.map.print_map()