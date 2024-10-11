import os
from variconfig import ConfigDict


dirpath = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dirpath, 'config.ini')
config_dict = ConfigDict.from_ini(config_path)

# print(config_dict)