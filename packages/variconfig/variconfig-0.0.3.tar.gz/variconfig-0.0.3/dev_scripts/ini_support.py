import os
from variconfig import ConfigDict
import toml

dirpath = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dirpath, 'config.toml')
config_dict = ConfigDict.from_toml(config_path)

print(config_dict)


with open(config_path, 'r') as f:
    config = toml.load(f)

print(config)