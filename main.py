from utils.getter import get_instance

from controller.controller import GameController

import argparse
import pygame

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str)
    
    args = parser.parse_args()

    config_path = args.config

    # Game Entry
    pygame.init() 
    pygame.display.set_caption('Hide and Seek')
        
    game = GameController(config_path) 
    
    game.start()