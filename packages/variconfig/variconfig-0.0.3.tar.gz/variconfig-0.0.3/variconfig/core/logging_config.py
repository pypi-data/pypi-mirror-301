import os
import json
import logging
import logging.config

import yaml
import toml

from variconfig.core.config import ConfigDict
from variconfig.utils.file_utils import ini_to_dict
from variconfig.utils.general_utils import find_key_in_nested_dict

logger = logging.getLogger(__name__)

class LoggingConfig(ConfigDict):
    """
    A configuration class for managing and applying logging configurations. This class extends `ConfigDict`
    and allows the user to apply and update logging configurations based on a provided dictionary.

    The class supports dynamic creation of log directories and the update of logging configurations using
    `logging.config.dictConfig`.

    Parameters
    ----------
    dictionary : dict
        A dictionary containing the logging configuration.
    template_pattern : str, optional
        A regex pattern for template variables within the configuration dictionary. Defaults to `r'\{\{\s*(\w+)\s*\}\}`.
        
    Methods
    -------
    apply(logging_config_key='logging_config')
        Applies the logging configuration using the specified key from the dictionary.
    
    update_logger(logging_config_key='logging_config')
        Updates the logger configuration using the specified key from the dictionary.

    update(dictionary, logging_config_key='logging_config')
        Updates the internal configuration dictionary and the logger configuration.
    
    _update_logger(logging_config_key='logging_config')
        Internal method that applies the logger configuration, checks for valid configurations, and sets up log directories.
    
    create_log_dir(dictionary)
        Creates the directory path for log files if the configuration contains a 'filename' field.

    Examples
    --------
    >>> logging_config = LoggingConfig(config.to_dict())
    >>> logging_config.apply()
    >>> logger.debug("This is a debug message")
    >>> logger.info("This is an info message")
    >>> logger.error("This is an error message")
    >>> logger.warning("This is a warning message")
    >>> logger.critical("This is a critical message")
    """

    def __init__(self, dictionary: dict, template_pattern=r'\{\{\s*(\w+)\s*\}\}'):
        """
        Initializes the LoggingConfig class and applies the logging configuration.
        
        Parameters
        ----------
        dictionary : dict
            A dictionary containing the logging configuration.
        template_pattern : str, optional
            A regex pattern for template variables within the configuration dictionary. Defaults to `r'\{\{\s*(\w+)\s*\}\}`.
        """
        super().__init__(dictionary, template_pattern)
        self._update_logger()
    
    def apply(self, logging_config_key='logging_config'):
        """
        Applies the logging configuration using the specified key from the internal configuration dictionary.
        
        Parameters
        ----------
        logging_config_key : str, optional
            The key in the configuration dictionary that holds the logging configuration. Defaults to 'logging_config'.
        """
        self._update_logger(logging_config_key=logging_config_key)
        
    def update_logger(self, logging_config_key='logging_config'):
        """
        Updates the logger configuration based on the specified key in the internal dictionary.
        
        Parameters
        ----------
        logging_config_key : str, optional
            The key in the configuration dictionary that holds the logging configuration. Defaults to 'logging_config'.
        """
        self._update_logger(logging_config_key=logging_config_key)
        
    def update(self, dictionary, logging_config_key='logging_config'):
        """
        Updates the internal configuration dictionary and re-applies the logger configuration.
        
        Parameters
        ----------
        dictionary : dict
            A dictionary containing new configuration values to update the internal state.
        logging_config_key : str, optional
            The key in the configuration dictionary that holds the logging configuration. Defaults to 'logging_config'.
        """
        super().update(dictionary)
        self._update_logger(logging_config_key=logging_config_key)
        
    def _update_logger(self, logging_config_key='logging_config'):
        """
        Internal method that applies the logging configuration and sets up log directories.
        Attempts to apply the logging configuration based on the given key. If the key is not found,
        it tries to use the entire configuration dictionary. 
        
        Parameters
        ----------
        logging_config_key : str, optional
            The key in the configuration dictionary that holds the logging configuration. Defaults to 'logging_config'.
        """
        if logging_config_key in self.__dict__.keys():
            logging_config = self[logging_config_key].to_dict()
            self._create_log_dir(logging_config)
            logging.config.dictConfig(logging_config)
            return logging_config
        else:
            logger.warning(f"Logging configuration key {logging_config_key} not found in the dictionary. "
                           "Trying 1 nested level up.")
        try:
            logging_config = self.to_dict()
            self._create_log_dir(logging_config)
            logging.config.dictConfig(logging_config)
            logger.info(f"Logger configuration updated: {logging_config}")
            return logging_config
        except Exception as e:
            logger.error(f"Failed to update logger configuration: {e}")
            
        logger.warning("Could not find logging configurations on the first two nest levels. Using Brute Force." 
                       "This will search the entire configuration dictionary for the arguments for logging.config.dictConfig.")
        
        try:
            logging_config = self._search_for_logging_config(self.to_dict())
            self._create_log_dir(logging_config)
            logging.config.dictConfig(logging_config)
            logger.info(f"Logger configuration updated: {logging_config}")
            return logging_config
        except Exception as e:
            logger.error(f"Failed to update logger configuration: {e}")
        
    
    def _create_log_dir(self, dictionary):
        """
        Creates the directory path for the log file if a 'filename' field is found in the logging configuration.
        
        Parameters
        ----------
        dictionary : dict
            The logging configuration dictionary to search for a 'filename' field.
        """
        filename = find_key_in_nested_dict(dictionary, 'filename')
        if filename:
            dir_path = os.path.dirname(filename)
            os.makedirs(dir_path, exist_ok=True)
        
    def _search_for_logging_config(self, dictionary):
        """
        This will search the entire configuration dictionary for the arguments for logging.config.dictConfig.
        
        Parameters
        ----------
        dictionary : dict
            The logging configuration dictionary to search for a 'filename' field.
        """
        logging_dict={}

        formatters = find_key_in_nested_dict(dictionary, 'formatters')
        handlers = find_key_in_nested_dict(dictionary, 'handlers')
        loggers= find_key_in_nested_dict(dictionary, 'loggers')
        version= find_key_in_nested_dict(dictionary, 'version')
        filters= find_key_in_nested_dict(dictionary, 'filters')
        root = find_key_in_nested_dict(dictionary, 'root')
        incremental = find_key_in_nested_dict(dictionary, 'incremental')
        disable_existing_loggers = find_key_in_nested_dict(dictionary, 'disable_existing_loggers')
        
        if formatters:
            logging_dict['formatters']=formatters
        if handlers:
            logging_dict['handlers']=handlers
        if loggers:
            logging_dict['loggers']=loggers
        if version:
            logging_dict['version']=version
        if filters:
            logging_dict['filters']=filters
        if root:
            logging_dict['root']=root
        if incremental:
            logging_dict['incremental']=incremental
        if disable_existing_loggers:
            logging_dict['disable_existing_loggers']=disable_existing_loggers
        return logging_dict
    
    @classmethod
    def from_yaml(cls, yaml_file):
        """
        Load a configuration from a YAML file.

        Parameters
        ----------
        yaml_file : str
            The path to the YAML file to load.

        Returns
        -------
        ConfigDict
            A ConfigDict object populated from the YAML file.

        Examples
        --------
        >>> config = ConfigDict.from_yaml('config.yml')
        >>> print(config.db_name)
        'my_database'
        """
        with open(yaml_file, 'r') as f:
            config = yaml.safe_load(f)
        return cls(config)
    
    @classmethod
    def from_json(cls, json_file):
        """
        Load a configuration from a JSON file.

        Parameters
        ----------
        json_file : str
            The path to the JSON file to load.

        Returns
        -------
        ConfigDict
            A ConfigDict object populated from the JSON file.

        Examples
        --------
        >>> config = ConfigDict.from_json('config.json')
        >>> print(config.logging_config.level)
        'DEBUG'
        """
        with open(json_file, 'r') as f:
            config = json.load(f)
        return cls(config)
    
    @classmethod
    def from_toml(cls, toml_file):
        """
        Load a configuration from a TOML file.

        Parameters
        ----------
        toml_file : str
            The path to the TOML file to load.

        Returns
        -------
        ConfigDict
            A ConfigDict object populated from the TOML file.

        Examples
        --------
        >>> config = ConfigDict.from_toml('config.toml')
        >>> print(config.db_name)
        'my_database'
        """
        with open(toml_file, 'r') as f:
            config = toml.load(f)
        return cls(config)

    @classmethod
    def from_ini(cls, ini_file):
        """
        Load a configuration from an INI file.

        Parameters
        ----------
        ini_file : str
            The path to the INI file to load.

        Returns
        -------
        ConfigDict
            A ConfigDict object populated from the INI file.

        Examples
        --------
        >>> config = ConfigDict.from_ini('config.ini')
        >>> print(config.db_name)
        'my_database'
        """
        config=ini_to_dict(ini_file)
        return cls(config)



