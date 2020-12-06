
from map import *
from player import *
from graphic import *
import os
import yaml 
import pprint
import glob 
def get_function(name):
    return globals()[name]

    players = {}
    for pcfg in config['player']:
        for it in range(pcfg['count']):
            players[pcfg['name'] + '_' + str(it)] = get_instance(pcfg)

def get_instance(config, **kwargs):
    assert 'name' in config
    config.setdefault('args', {})
    if config['args'] is None:
        config['args'] = {}
    return globals()[config['name']](**config['args'], **kwargs)

def get_level_list():
    config_file = [os.path.join('./configs', f) for f in os.listdir('./configs')]
    
    level_list = []
    for i, f in enumerate(config_file):
        name = os.path.basename(f)[:-5]
        name = name.replace('_', ' ')
        level_list.append((name, i, f))
    return level_list

def get_map_list():
    lst = glob.glob('data_maps/*.png')
    print(lst)

def get_config(config_path):
    config = yaml.load(open(config_path, 'r'), Loader=yaml.Loader)
    assert config is not None, "Wrong config file path!"
    pprint.PrettyPrinter(indent=2).pprint(config)
    return config