from utils.getter import get_instance

from controller.controller import GameController

import argparse
import yaml 
import pprint 

def go(config):

    # Define map
    map = get_instance(config['map'])
    
    graphic = get_instance(config['graphic'])

    # Define Player
    players = {}
    for pcfg in config['player']:
        for it in range(pcfg['count']):
            players[pcfg['name'] + '_' + str(it)] = get_instance(pcfg)
    # print(players)
    
    # Define controller 
    game = GameController(  config= config,
                            graphic= graphic,
                            map= map,
                            players = players) 
    
    game.run_game()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--config')
    
    args = parser.parse_args()

    config_path = args.config
    config = yaml.load(open(config_path, 'r'), Loader=yaml.Loader)
    assert config is not None, "Do not have config file!"
    pprint.PrettyPrinter(indent=2).pprint(config)

    go(config)
