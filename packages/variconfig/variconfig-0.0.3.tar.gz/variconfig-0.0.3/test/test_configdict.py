import unittest
import os
import json
import yaml
import logging

from variconfig import ConfigDict



logger=logging.getLogger('variconfig')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

class TestConfigDict(unittest.TestCase):

    def setUp(self):
        # Example YAML content
        self.yaml_content = """
        root_dir: "."
        data_dir: "{{ root_dir }}/data"
        log_dir: "{{ root_dir }}/logs"
        db_name: "TestDB"
        logging_config:
          version: 1
          loggers:
            test_logger:
              level: "INFO"
        """

        # Example JSON content
        self.json_content = {
            "root_dir": ".",
            "data_dir": "{{ root_dir }}/data",
            "log_dir": "{{ root_dir }}/logs",
            "db_name": "TestDB",
            "logging_config": {
                "version": 1,
                "loggers": {
                    "test_logger": {
                        "level": "INFO"
                    }
                }
            }
        }
        
        # Example TOML content
        self.toml_content = """
        root_dir = "."
        data_dir = "{{ root_dir }}/data"
        log_dir = "{{ root_dir }}/logs"
        db_name = "TestDB"

        [logging_config]
        version = 1

        [logging_config.loggers.test_logger]
        level = "INFO"
        """

        # Example INI content
        self.ini_content = """
        [DEFAULT]
        root_dir = .
        data_dir = {{ root_dir }}/data
        log_dir = {{ root_dir }}/logs
        db_name = TestDB

        [logging_config]
        version = 1

        [logging_config.loggers.test_logger]
        level = INFO
        """

        # Write YAML file for testing
        with open('test_config.yml', 'w') as f:
            f.write(self.yaml_content)

        # Write JSON file for testing
        with open('test_config.json', 'w') as f:
            json.dump(self.json_content, f)
        
        # Write TOML file for testing
        with open('test_config.toml', 'w') as f:
            f.write(self.toml_content)

        # Write INI file for testing
        with open('test_config.ini', 'w') as f:
            f.write(self.ini_content)

    def tearDown(self):
        # Remove test files after each test
        for file in ['test_config.yml', 'test_config.json', 'test_config.toml', 'test_config.ini']:
            if os.path.exists(file):
                os.remove(file)

    def test_load_yaml(self):
        # Test loading from YAML
        config = ConfigDict.from_yaml('test_config.yml')
        self.assertEqual(config.db_name, "TestDB")
        self.assertEqual(config.data_dir, "./data")  # Template resolution

    def test_load_json(self):
        # Test loading from JSON
        config = ConfigDict.from_json('test_config.json')
        self.assertEqual(config.db_name, "TestDB")
        self.assertEqual(config.data_dir, "./data")  # Template resolution
        
    def test_load_toml(self):
        # Test loading from TOML
        config = ConfigDict.from_toml('test_config.toml')
        self.assertEqual(config.db_name, "TestDB")
        self.assertEqual(config.data_dir, "./data")  # Template resolution
        self.assertEqual(config.logging_config.loggers.test_logger.level, "INFO")

    def test_load_ini(self):
        # Test loading from INI
        config = ConfigDict.from_ini('test_config.ini')
        self.assertEqual(config.db_name, "TestDB")
        self.assertEqual(config.data_dir, "./data")  # Template resolution
        self.assertEqual(config.logging_config.loggers.test_logger.level, "INFO")

    def test_nested_access(self):
        # Test nested dictionary access
        config = ConfigDict.from_yaml('test_config.yml')
        self.assertEqual(config.logging_config.loggers.test_logger.level, "INFO")

    def test_update_configuration_by_setattr(self):
        # Test updating configuration values
        config = ConfigDict.from_yaml('test_config.yml')
        config.logging_config.loggers.test_logger.level = "DEBUG"
        self.assertEqual(config.logging_config.loggers.test_logger.level, "DEBUG")
        
    def test_update_configuration_by_dict(self):
        # Test by dictionary setting
        config = ConfigDict.from_yaml('test_config.yml')
        config['logging_config']['loggers']['test_logger']['level'] = "DEBUG"
        self.assertEqual(config.logging_config.loggers.test_logger.level, "DEBUG")
        
    def test_update_configuration_by_update(self):
        # Test by dictionary setting
        config = ConfigDict.from_yaml('test_config.yml')
        config.update({'logging_config': {'loggers': {'test_logger': {'level': "DEBUG"}}}})
        self.assertEqual(config.logging_config.loggers.test_logger.level, "DEBUG")
        
    def test_adding_new_configuration(self):
        # Test by dictionary setting
        config = ConfigDict.from_yaml('test_config.yml')
        config['new_config'] = {'key': {'nested_key': 5}}
        self.assertEqual(config['new_config']['key']['nested_key'], 5)
        self.assertEqual(config.new_config.key.nested_key, 5)
        
        config.new_config.key.nested_key = 6
        self.assertEqual(config['new_config']['key']['nested_key'], 6)
        self.assertEqual(config.new_config.key.nested_key, 6)
        
        config.new_config.key.nested_key = {'nested_key': 7}
        self.assertEqual(config['new_config']['key']['nested_key']['nested_key'], 7)
        self.assertEqual(config.new_config.key.nested_key.nested_key, 7)
        

    def test_to_dict(self):
        # Test conversion to dictionary
        config = ConfigDict.from_yaml('test_config.yml')
        config_dict = config.to_dict()
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict['db_name'], "TestDB")

    def test_template_resolution(self):
        # Test template resolution with nested templates
        config = ConfigDict.from_yaml('test_config.yml')
        self.assertEqual(config.data_dir, "./data")
        self.assertEqual(config.log_dir, "./logs")

if __name__ == '__main__':
    unittest.main()
