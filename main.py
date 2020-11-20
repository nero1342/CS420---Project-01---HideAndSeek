import argparse
import yaml 
import pprint 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config')
    
    args = parser.parse_args()

    config_path = args.config
    config = yaml.load(open(config_path, 'r'), Loader=yaml.Loader)
    assert config is not None, "Do not have config file!"
    pprint.PrettyPrinter(indent=2).pprint(config)

    

