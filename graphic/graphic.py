import pygame as pg 
from pygame._sdl2.video import Window

from pygame.locals import *
import numpy as np 
import os 
from enum import Enum 
class Type(Enum):
    STREET_IN_HIDER_VIEW = -2
    STREET_IN_SEEKER_VIEW = -1
    STREET = 0
    WALL = 1
    OBSTACLE = 2 
    SEEKER = 3
    HIDER = 4 
    HIDER2 = 5
class GraphicPygame:
    def __init__(self, data_image_dir):
        super().__init__()
        self.data_image_dir = data_image_dir
        self.img = {}
        self.img[Type.STREET_IN_HIDER_VIEW] = pg.image.load(os.path.join(data_image_dir, "pink.png"))
        self.img[Type.STREET_IN_SEEKER_VIEW] = pg.image.load(os.path.join(data_image_dir, "white.png"))
        self.img[Type.STREET] = pg.image.load(os.path.join(data_image_dir, "street.jpg"))
        self.img[Type.WALL] = pg.image.load(os.path.join(data_image_dir, "wall.png"))
        self.img[Type.OBSTACLE] = pg.image.load(os.path.join(data_image_dir, "obstacle.png"))
        self.img[Type.SEEKER] = pg.image.load(os.path.join(data_image_dir, "monkey.png"))
        self.img[Type.HIDER] = pg.image.load(os.path.join(data_image_dir, "pig.png"))
        self.img[Type.HIDER2] = pg.image.load(os.path.join(data_image_dir, "monkey2.png"))
        pg.init() 
        pg.display.set_caption('Hide and Seek')
        window = Window.from_display_module()
        window.position = (0, 0)
        self.whole_game = []
        self.cnt  = 0
    def draw(self, game_map):
        block = 17
        n_row = len(game_map)
        n_col = len(game_map[0])
        extend_for_text = 150
        WINDOW_SIZE = (n_col * block + 10 + extend_for_text, n_row * block + 10)
        SCREEN_SIZE = (WINDOW_SIZE[0] * 2, WINDOW_SIZE[1] * 2)
        
        self.WS = WINDOW_SIZE
        screen = pg.display.set_mode(SCREEN_SIZE, 0, 32)
        display = pg.Surface((WINDOW_SIZE))
        black = (0, 0, 0)
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        display.fill(black)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        for i in range(n_row):
            for j in range(n_col):
                id = max(-2, int(game_map[i][j]))#self.getID(game_map[i][j])
                id = min(4, id)#self.getID(game_map[i][j])
                # id = max(0, id)
                # print(n_row, n_col, id, self.img[Type(id)])
                if id != 0:
                    if Type(id) == Type.HIDER:
                        display.blit(self.img[Type.STREET_IN_HIDER_VIEW], (j * block, i * block))
                    
                    if Type(id) == Type.SEEKER:
                        display.blit(self.img[Type.STREET_IN_SEEKER_VIEW], (j * block, i * block))
                    display.blit(self.img[Type(id)], (j * block, i * block))
        
        self.cnt += 1
        font = pg.font.Font('freesansbold.ttf', 10)
        text = font.render('Time remain: {}'.format(self.cnt), True, green, black)
        textRect = text.get_rect()
        # set the center of the rectangular object.
        textRect.center =((WINDOW_SIZE[0] - extend_for_text // 2), WINDOW_SIZE[1] // 8)
        display.blit(text, textRect)
        
        pg.time.Clock().tick(10)
        screen.blit(pg.transform.scale(display, SCREEN_SIZE), (0, 0))
        pg.display.update()
        string_image = pg.image.tostring(screen, 'RGB')
        temp_surf = pg.image.fromstring(string_image,SCREEN_SIZE,'RGB' )
        tmp_arr = pg.surfarray.array3d(temp_surf)
        self.whole_game.append(tmp_arr)

    def extract_video(self):
        import cv2
        import numpy as np
        from cv2 import VideoWriter, VideoWriter_fourcc

        width = self.WS[0]
        height = self.WS[1]
        FPS = 10
        seconds = 10
        
        fourcc = VideoWriter_fourcc(*'MP42')
        num_file = len(os.listdir('./outputs'))
        level_name = 'test' + str(num_file).zfill(3) # must change to name of level
        path_to_save = os.path.join('./outputs', level_name + '.avi')
        video = VideoWriter(path_to_save, fourcc, float(FPS), (width, height))

        for i, frame in enumerate(self.whole_game):
            print("Extract frame {}".format(i))
            frame = frame.transpose(1, 0, 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            video.write(frame)

        video.release()
        print("Extracted successfully.")
    def reset_screen(self):
        pg.display.set_mode((400, 300), 0, 32)