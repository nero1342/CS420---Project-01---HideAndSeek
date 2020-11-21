import pygame_menu
import pygame
from utils.getter import get_level_list

class Menu():
  def __init__(self):
    self.surface = pygame.display.set_mode((400, 300))
    self.menu = pygame_menu.Menu(300, 400, 'Hide&Seek', theme=pygame_menu.themes.THEME_SOLARIZED)
    
  def create_menu(self, cb_list):

      assert 'play_cb' in cb_list
      self.menu.add_button('Play', cb_list['play_cb'])

      assert 'select_level_cb' in cb_list
      level_list = get_level_list()
      assert len(level_list) > 0
      level_selector = self.menu.add_selector('', level_list, onchange=cb_list['select_level_cb'])
      # Set default level, maybe a litte hack here
      cb_list['select_level_cb'](*level_list[level_selector.get_value()[1]])

      self.menu.add_button('Quit', pygame_menu.events.EXIT)

  def add_level(self, level_list, cb):
    self.menu.add_selector('Level :' , level_list, on_change=cb)

  def display(self):
    self.menu.mainloop(self.surface)
