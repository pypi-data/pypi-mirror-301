import os
from variconfig import ConfigDict, LoggingConfig


import logging


logger_variconfig=logging.getLogger('variconfig')
logger_variconfig.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger_variconfig.addHandler(ch)



logger=logging.getLogger('variconfig_dev')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

dirpath = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dirpath, 'config.yml')




config=ConfigDict.from_yaml(config_path)

f=os.path.dirname('./logs/variconfig.log')
os.makedirs(f, exist_ok=True)
logging_config=LoggingConfig(config.to_dict())

print(logging_config.__dict__.keys())
print(logging_config.config)
logger.debug(f"Debug")
logger.info(f"Info")
logger.error("Error")
logger.warning("Warning")
logger.critical("Critical")


# # print(logging_config)
# # # This will automatically update the logging configuration
print('-'*200)
# print(logging_config.logging_config.loggers.variconfig_dev)
# logging_config.logging_config.loggers.variconfig_dev.level = "DEBUG"
# print(logging_config.logging_config.loggers.variconfig_dev)


print(logging_config.logging_config.loggers.variconfig_dev)
logging_config.logging_config.loggers.variconfig_dev.level = "DEBUG"
logging_config.update_logger()
print(logging_config.logging_config.loggers.variconfig_dev)


# print(logging_config.config)

# print(type(logging_config.logging_config.loggers.variconfig_dev))
# print(logging_config.logging_config.loggers.variconfig_dev)

logger.debug(f"Debug")
logger.info(f"Info")
logger.error("Error")
logger.warning("Warning")
logger.critical("Critical")
print('-'*200)

