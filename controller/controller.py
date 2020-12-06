import numpy as np 
import pygame_menu
from menu import Menu
from utils.getter import *
import time
import random

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
        # print(self.type_player_alive)
        # print(self.lst_player)

        for i in range(len(self.lst_player)):
            pos = self.map.get_free_cell()
            player = self.get_player(i) 
            player.set_position(pos)
            player.set_id(i)
            # print(i, self.lst_player[i])
            self.map.set_player_position(player, i)
        # self.map.print_map()
        
    def run_turn(self, turn_id):
        player = self.get_player(turn_id)
        if player.movable:
            # print("Time remain:{} - Turn: {}".format(self.time, turn_id))
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
        # return
        turn_id = 0
        announce_turn = random.randint(7, 11)
        while self.time > 0:
            # self.graphic.draw(self.map.get_system_view(self.get_player(turn_id)).map)
            # continue
            if announce_turn == 0:
                list_announce_cell = self.get_announce_list()
                self.map.update_announce_cell(list_announce_cell)
                self.graphic.draw(self.map.get_system_view(self.players.values()).map, time_tick = 5)
                self.map.clear_announce_cell()
                # time.sleep(1)
                announce_turn = random.randint(5, 10)
            if self.run_turn(turn_id):
                if turn_id == 0:
                    announce_turn -= 1
                    self.time -= 1
                    self.graphic.draw(self.map.get_system_view(self.players.values()).map, time_tick = 10)
                # self.graphic.draw(self.map.get_system_view(self.players.values()).map)
                # continue
                #self.graphic.draw(self.get_player(turn_id).visited_map.map)
                #self.graphic.draw(self.map.map)
                winner = self.check_stop_game()
                if winner is not None:
                    print("Winner is ", winner)
                    break
            turn_id = (turn_id + 1) % (len(self.lst_player))
            
                
        pass
        self.graphic.extract_video()
        self.graphic.reset_screen()

    def get_announce_list(self):
        list_announce_cell = []
        for i in range(len(self.lst_player)):
            player = self.players[self.lst_player[i]]
            if type(player).__name__ == 'Hider' and not player.is_dead:
                pos = player.position
                possible_cell = []
                for i in range(-3, 4):
                    for j in range(-3, 4):
                        if abs(i) + abs(j) > 3 or i + j == 0:
                            continue
                        cell = (pos[0] + i, pos[1] + j)
                        if self.map.valid((pos[0] + i, pos[1] + j)) and self.map.is_announce_cell(cell):
                            possible_cell.append(cell)
                if len(possible_cell) > 0:
                    announce_cell = random.choice(possible_cell)
                    list_announce_cell.append((announce_cell, -player.id - 3))
                    player.update_announce_cell(announce_cell)
        return list_announce_cell
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
        if not player.is_dead and not self.map.alive(player):
            self.map.print_map()
            exit(0)
        for id in lst_dead:
            self.type_player_alive[self.get_player(id).__class__.__name__] -= 1
       