from pygame.locals import *
import pygame
import os
 
n_row = 20 
n_col = 30
typeTile = "1"
def init_display():
    global screen, tile, tile2, display, WINDOW_SIZE
    WINDOW_SIZE = (n_col * 32 + 10, n_row * 32 + 10)
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
    display = pygame.Surface((WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    tile = pygame.image.load("../data_image/wall.png")
    tile2 = pygame.image.load("../data_image/obstacle.png")
 
 
def tiles(map1):
    global tile, tile2 
    for y, line in enumerate(map1):
        for x, c in enumerate(line):
            if c == "1":
                display.blit(tile, (x * 16, y * 16))
            if c == "2":
                display.blit(tile2, (x * 16, y * 16))
 
 
def map_to_list():
    start = "1"* n_col + '\n';
    map1 = "1" + "0" * (n_col - 2) + "1\n"
    map1 = start + map1 * (n_row - 2) + start
    map1 = map1.splitlines()
    map2 = []
    for n, line in enumerate(map1):
        map2.append(list(map1[n]))
    return map2
 
 
map1 = map_to_list()
 
pygame.init()
init_display()
loop = 1
last_pos = x, y = pygame.mouse.get_pos()
letter = "spazio"

while loop:
 
    display.fill((0, 0, 0))
    tiles(map1)
    for event in pygame.event.get():
        if event.type == QUIT:
            loop = 0
        if event.type == pygame.KEYDOWN:
            if event.key == K_s:
                num_file = len(os.listdir('../data_maps'))
                map_name = f"../data_maps/map_{num_file // 2}.png"
                map_file = f"../data_maps/map_{num_file // 2}.txt"

                pygame.image.save(screen, map_name)
                with open(map_file, "w") as f:
                    print(n_row, n_col, file = f)
                    for i in range(n_row):
                        for j in range(n_col):
                            print(map1[i][j], end = ' ', file = f )
                        print(file = f)
                print("Save {} successfully.".format(map_file))
                # os.startfile(map_name)
            if event.key == K_d:
                map1 = map_to_list()
            if event.key == K_1:
                typeTile = "1"
            if event.key == K_2:
                typeTile = "2"
                    
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            # You divide by 32 for its scaled (pygame.transform.scale)
            x, y = int(x / 32), int(y / 32)
            # x and y are col and row (the opposite)
            row, col = y, x
            map1[row][col] = typeTile
        elif pygame.mouse.get_pressed()[2]:
            x, y = pygame.mouse.get_pos()
            # You divide by 32 for its scaled (pygame.transform.scale)
            x, y = int(x / 32), int(y / 32)
            # x and y are col and row (the opposite)
            row, col = y, x
            map1[row][col] = "0"
 

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()


pygame.quit()