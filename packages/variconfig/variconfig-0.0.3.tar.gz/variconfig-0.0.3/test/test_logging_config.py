
import unittest
import logging
import os
import shutil
import json
from unittest.mock import patch
from logging.config import dictConfig

from variconfig import LoggingConfig
from variconfig.utils.file_utils import ini_to_dict


class TestLoggingConfig(unittest.TestCase):
    def setUp(self):
        # Set up a basic logging configuration dictionary
        self.logging_config_dict = {
            'version': 1,
            'formatters': {
                'simple': {
                    'format': '%(levelname)s %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                    'level': 'DEBUG',
                    'stream': 'ext://sys.stdout'
                }
            },
            'root': {
                'level': 'DEBUG',
                'handlers': ['console']
            }
        }
        # Create an instance of LoggingConfig
        self.logging_config = LoggingConfig(self.logging_config_dict)
    
    def test_apply_method(self):
        """Test that the apply method correctly applies the logging configuration."""
        with patch('logging.config.dictConfig') as mock_dictConfig:
            self.logging_config.apply()
            mock_dictConfig.assert_called_once_with(self.logging_config_dict)
    
    def test_update_logger_method(self):
        """Test that the update_logger method updates the logger configuration."""
        with patch('logging.config.dictConfig') as mock_dictConfig:
            self.logging_config.update_logger()
            mock_dictConfig.assert_called_once_with(self.logging_config_dict)
    
    def test_update_method(self):
        """Test that the update method updates the internal configuration and re-applies the logger."""
        new_config = {
            'version': 1,
            'formatters': {
                'detailed': {
                    'format': '%(asctime)s %(levelname)s %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'detailed',
                    'level': 'INFO',
                    'stream': 'ext://sys.stdout'
                }
            },
            'root': {
                'level': 'INFO',
                'handlers': ['console']
            }
        }
        with patch('logging.config.dictConfig') as mock_dictConfig:
            self.logging_config.update(new_config)
            mock_dictConfig.assert_called_with(new_config)
            self.assertEqual(
                self.logging_config['formatters']['detailed']['format'],
                '%(asctime)s %(levelname)s %(message)s'
            )
    
    def test_create_log_dir(self):
        """Test that _create_log_dir creates directories when needed."""
        log_file_path = 'logs/test.log'
        config_with_file = {
            'version': 1,
            'handlers': {
                'file': {
                    'class': 'logging.FileHandler',
                    'formatter': 'simple',
                    'filename': log_file_path,
                }
            },
            'root': {
                'handlers': ['file']
            }
        }
        # Remove the logs directory if it exists
        if os.path.exists('logs'):
            shutil.rmtree('logs')
        
        self.logging_config._create_log_dir(config_with_file)
        self.assertTrue(os.path.exists('logs'))
        # Clean up
        shutil.rmtree('logs')
    
    def test_from_json(self):
        """Test loading configuration from a JSON file."""
        test_json = 'test_logging_config.json'
        with open(test_json, 'w') as f:
            json.dump(self.logging_config_dict, f)
        try:
            logging_config = LoggingConfig.from_json(test_json)
            self.assertEqual(logging_config.to_dict(), self.logging_config_dict)
        finally:
            os.remove(test_json)
    
    def test_search_for_logging_config(self):
        """Test that _search_for_logging_config finds the logging configuration."""
        nested_config = {
            'some_key': {
                'another_key': {
                    'log_config': self.logging_config_dict
                }
            }
        }
        self.logging_config.update(nested_config)
        result = self.logging_config._search_for_logging_config(nested_config)
        self.assertEqual(result, self.logging_config_dict)
    
    def test_logging_config_key_not_found(self):
        """Test that a warning is logged when logging_config_key is not found."""
        with patch('logging.Logger.warning') as mock_warning:
            self.logging_config._update_logger(logging_config_key='nonexistent_key')
            mock_warning.assert_called()

    def test_from_yaml(self):
        """Test loading configuration from a YAML file."""
        try:
            import yaml
            test_yaml = 'test_logging_config.yaml'
            with open(test_yaml, 'w') as f:
                yaml.dump(self.logging_config_dict, f)
            logging_config = LoggingConfig.from_yaml(test_yaml)
            self.assertEqual(logging_config.to_dict(), self.logging_config_dict)
        except ImportError:
            self.skipTest("PyYAML is not installed.")
        finally:
            if os.path.exists('test_logging_config.yaml'):
                os.remove('test_logging_config.yaml')

    def test_from_toml(self):
        """Test loading configuration from a TOML file."""
        try:
            import toml
            test_toml = 'test_logging_config.toml'
            with open(test_toml, 'w') as f:
                toml.dump(self.logging_config_dict, f)
            logging_config = LoggingConfig.from_toml(test_toml)
            self.assertEqual(logging_config.to_dict(), self.logging_config_dict)
        except ImportError:
            self.skipTest("toml module is not installed.")
        finally:
            if os.path.exists('test_logging_config.toml'):
                os.remove('test_logging_config.toml')

    # def test_from_ini(self):
    #     """Test loading configuration from an INI file."""
    #     test_ini = 'test_logging_config.ini'
    #     with open(test_ini, 'w') as f:
    #         f.write("[root]\n")
    #         f.write("level=DEBUG\n")
    #     # Assuming ini_to_dict is implemented correctly
    #     with patch('ini_to_dict', return_value=self.logging_config_dict):
    #         logging_config = LoggingConfig.from_ini(test_ini)
    #         self.assertEqual(logging_config.to_dict(), self.logging_config_dict)
    #     if os.path.exists(test_ini):
    #         os.remove(test_ini)

if __name__ == '__main__':
    unittest.main()