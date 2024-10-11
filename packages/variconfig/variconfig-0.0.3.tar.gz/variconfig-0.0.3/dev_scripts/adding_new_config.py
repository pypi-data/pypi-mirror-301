import os
from variconfig import ConfigDict

dirpath = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dirpath, 'config.yml')
print("Directory path:", dirpath)
print("Config path:", config_path)

config = ConfigDict.from_yaml(config_path)
print('-'*200)
print("Loaded config:", config)
print('-'*200)

config['new_config'] = {'key': {'nested_key': 5}}

print(f"New key added: {config['new_config']} {config.new_config}")

print(f"New nested key added: {config['new_config']['key']['nested_key']}  {config.new_config.key.nested_key}")
# print(config.__dict__)


config.new_config.key.nested_key = 6
print(f"New nested key added: {config['new_config']['key']['nested_key']}  {config.new_config.key.nested_key}")


config['new_config']['key']['nested_key']=7

print(f"New nested key added: {config['new_config']['key']['nested_key']}  {config.new_config.key.nested_key}")

print('Before update')
# config.new_config.key['nested_key']={'nested_key': 7}
config.new_config.key.nested_key = {'nested_key': 7}
print("After update")
print(config.new_config.key.nested_key)

print(f"New nested key added: {config['new_config']['key']['nested_key']['nested_key']}  {config.new_config.key.nested_key.nested_key}")