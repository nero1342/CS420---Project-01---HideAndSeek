import pygame as pg 
from pygame.locals import *
import numpy as np 

class GraphicPygame:
    def __init__(self):
        super().__init__()
        pg.init() 
        self.screen = pg.display.set_mode((1000, 600))
        pg.display.set_caption('Hide and Seek')
        self.clock = pg.time.Clock()

    def draw(self, game_map):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
        temp = np.asarray(game_map).astype(int)
        surf = pg.surfarray.make_surface(temp)
        surf = pg.transform.scale(surf, (600, 600))  # Scaled a bit.  
        self.screen.blit(surf, (0, 0))
        pg.display.flip()
        self.clock.tick(1)
        print("Render")

        