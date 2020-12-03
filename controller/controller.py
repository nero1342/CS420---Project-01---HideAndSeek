import numpy as np 
import pygame_menu
from menu import Menu
from utils.getter import *

class GameController:
    def __init__(self, config_path):
        self.config_path = config_path

    def get_player(self, turn_id):
        return self.players[self.lst_player[turn_id]]

    def init_game(self):
        config = get_config(self.config_path)
        self.time = config['controller']['time']
        self.graphic = get_instance(config['graphic'])
        self.map = get_instance(config['map']) 
        # [TODO]: Must refactor here
        self.players = {}
        for pcfg in config['player']:
            for it in range(pcfg['count']):
                self.players[pcfg['name'] + '_' + str(it)] = get_instance(pcfg)
        self.lst_player = list(self.players.keys())
        self.type_player_alive = {}
        for player in self.players.values():
            if (self.type_player_alive.get(player.__class__.__name__)):
                self.type_player_alive[player.__class__.__name__] += 1
            else:
                self.type_player_alive[player.__class__.__name__] = 1
        print(self.type_player_alive)
        print(self.lst_player)

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
    
    def set_level(self, level_name, level_id, config_path):
        self.config_path = config_path
        print(self.config_path)

    def start(self):
        if self.config_path is None:
            menu = Menu()
            cb_list = {
                'select_level_cb': self.set_level,
                'play_cb': self.run_game
            }
            menu.create_menu(cb_list)
            menu.display()
        else:
            self.run_game()

    def run_game(self):
        self.init_game()
        turn_id = 0
        while self.time > 0:
            # self.graphic.draw(self.map.get_system_view(self.get_player(turn_id)).map)
            # continue
            if self.run_turn(turn_id):
                self.graphic.draw(self.map.get_system_view(self.players.values()).map)
                # continue
                #self.graphic.draw(self.get_player(turn_id).visited_map.map)
                #self.graphic.draw(self.map.map)
                winner = self.check_stop_game()
                if winner is not None:
                    print("Winner is ", winner)
                    break
            turn_id = (turn_id + 1) % (len(self.lst_player))
            # self.time -= 1
        pass
        self.graphic.extract_video()
        self.graphic.reset_screen()

    def check_stop_game(self):
        alive = []
        for type, cnt in self.type_player_alive.items():
            if (cnt):
                alive.append(type)
        if (len(alive) == 1):
            return alive[0]
        return None
    def take_turn(self, player):
        player_view = self.map.get_view(player)
        direction = player.move(player_view)
        lst_dead = self.map.move(player, direction)
        [self.get_player(id).dead() for id in lst_dead]
        for id in lst_dead:
            self.type_player_alive[self.get_player(id).__class__.__name__] -= 1
       