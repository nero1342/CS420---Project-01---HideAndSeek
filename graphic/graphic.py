import pygame as pg 
from pygame.locals import *
import numpy as np 
import os 
from enum import Enum 
class Type(Enum):
    STREET = 0
    WALL = 1
    OBSTACLE = 2 
    SEEKER = 3
    HIDER = 4 

class GraphicPygame:
    def __init__(self, data_image_dir):
        super().__init__()
        self.data_image_dir = data_image_dir
        self.img = {}
        
        self.img[Type.WALL] = pg.image.load(os.path.join(data_image_dir, "wall.png"))
        self.img[Type.OBSTACLE] = pg.image.load(os.path.join(data_image_dir, "obstacle.png"))
        self.img[Type.SEEKER] = pg.image.load(os.path.join(data_image_dir, "monkey.png"))
        self.img[Type.HIDER] = pg.image.load(os.path.join(data_image_dir, "pig.png"))
        pg.init() 
        pg.display.set_caption('Hide and Seek')
        
    def draw(self, game_map):
        n_row = len(game_map)
        n_col = len(game_map[0])
        WINDOW_SIZE = (n_col * 32 + 10, n_row * 32 + 10)
        screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)
        display = pg.Surface((WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
        display.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        for i in range(n_row):
            for j in range(n_col):
                id = int(game_map[i][j])#self.getID(game_map[i][j])
                # print(n_row, n_col, id, self.img[Type(id)])
                if id:
                    display.blit(self.img[Type(id)], (j * 16, i * 16))
        
        pg.time.Clock().tick(10)
        screen.blit(pg.transform.scale(display, WINDOW_SIZE), (0, 0))
        pg.display.update()