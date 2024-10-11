import yaml
import json
import re
import logging
import toml

from variconfig.utils.file_utils import ini_to_dict

logger = logging.getLogger(__name__)

class ConfigDict(dict):
    """
    A dictionary subclass for managing configurations with support for attribute access and template resolution.

    This class allows access to dictionary items as object attributes and resolves template variables
    in the form of `{{ var }}` by default. Users can specify their own template patterns for custom template handling.

    Parameters
    ----------
    dictionary : dict
        The initial dictionary to populate the ConfigDict object.
    template_pattern : str, optional
        Regular expression pattern to match the template variables, by default `r'\{\{\s*(\w+)\s*\}\}'`.

    Examples
    --------
    >>> config_data = {
    ...     "root_dir": ".",
    ...     "data_dir": "{{ root_dir }}/data"
    ... }
    >>> config = ConfigDict(config_data)
    >>> print(config.data_dir)
    './data'

    >>> config['new_config'] = {'key': 'value'}
    >>> print(config.new_config.key)
    'value'
    """
    
    def __init__(self, dictionary: dict, template_pattern=r'\{\{\s*(\w+)\s*\}\}'):
        """
    A dictionary subclass for managing configurations with support for attribute access and template resolution.

    This class allows access to dictionary items as object attributes and resolves template variables
    in the form of `{{ var }}` by default. Users can specify their own template patterns for custom template handling.

    Parameters
    ----------
    dictionary : dict
        The initial dictionary to populate the ConfigDict object.
    template_pattern : str, optional
        Regular expression pattern to match the template variables, by default `r'\{\{\s*(\w+)\s*\}\}'`.
    """
        dictionary = resolve_templates(dictionary, template_pattern)
        for key, value in dictionary.items():
            self._update_attribute(key, value)

    def __getitem__(self, key):
        """
        Get an item using attribute-style access.

        Parameters
        ----------
        key : str
            The key of the item to get.

        Returns
        -------
        object
            The value of the key, accessed as an attribute.
        """
        return getattr(self, key)

    def __setitem__(self, key, value):
        """
        Set an item using dictionary-style or attribute-style access.

        Parameters
        ----------
        key : str
            The key of the item to set.
        value : object
            The value to assign to the key.

        Returns
        -------
        None
        """
        self._update_attribute(key, value)

    def __getattr__(self, name: str):
        return self.__dict__.get(name)
    
    def __setattr__(self, key, value) -> None:
        """
        Set an item as an attribute. Handles both ConfigDict and standard dict assignments.

        Parameters
        ----------
        key : str
            The key to set.
        value : object
            The value to assign to the key.

        Returns
        -------
        None
        """
        if isinstance(value, dict) or isinstance(value, ConfigDict):
            self._update_attribute(key, value)
        else:
            super().__setattr__(key, value)

    def __repr__(self):
        """
        String representation of the ConfigDict object.

        Returns
        -------
        str
            String representation of the object showing its current attributes.
        """
        return __class__.__name__ + '(' + repr(self.__dict__) + ')'

    def _update_attribute(self, key, value):
        """
        Internal method to update the attribute dictionary.

        Parameters
        ----------
        key : str
            The key to update.
        value : object
            The value to assign to the key. If the value is a dict, it is converted to a ConfigDict.

        Returns
        -------
        None
        """
        if isinstance(value, dict):
            self.__dict__.update({key: ConfigDict(value)})
        else:
            self.__dict__.update({key: value})

    def update(self, dictionary):
        """
        Update the ConfigDict with values from another dictionary.

        Parameters
        ----------
        dictionary : dict
            The dictionary to update the ConfigDict with.

        Returns
        -------
        None
        """
        for key, value in dictionary.items():
            self._update_attribute(key, value)

    def to_dict(self):
        """
        Convert the ConfigDict to a standard Python dictionary.

        Returns
        -------
        dict
            A standard Python dictionary representation of the ConfigDict.
        """
        dictionary = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ConfigDict):
                dictionary.update({key: value.to_dict()})
            else:
                dictionary.update({key: value})
        return dictionary

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


def resolve_templates(d, template_pattern=r'\{\{\s*(\w+)\s*\}\}'):
    """
    Resolve template strings in the dictionary `d` using a user-specified template pattern.

    Args:
        d (dict): The dictionary with templates to be resolved.
        template_pattern (str): Regular expression pattern to match the template variables.
                                Default is '{{ var }}'.

    Returns:
        dict: Dictionary with resolved templates.
    """

    def substitute_value(value, mapping):
        # Perform substitution if the value is a string and contains templates
        if isinstance(value, str):
            while True:
                # Find all template variables based on the user-defined template pattern
                matches = re.findall(template_pattern, value)
                if not matches:
                    break  # Exit if no templates found

                # Replace each template with its value from the mapping
                for match in matches:
                    if match in mapping:
                        # Ensure proper substitution with the detected template format
                        value = re.sub(template_pattern.replace(r'\w+', match), mapping[match], value, count=1)
            return value
        return value

    # Recursive function to resolve all template variables in the dictionary
    def resolve_dict(d, mapping):
        resolved_dict = {}
        for key, value in d.items():
            if isinstance(value, dict):
                # Recursively resolve for nested dictionaries
                resolved_dict[key] = resolve_dict(value, mapping)
            else:
                # Substitute the value using the current mapping
                resolved_dict[key] = substitute_value(value, mapping)
            
            # Update the mapping with the resolved value (ensure it resolves for other keys)
            mapping[key] = resolved_dict[key]

        return resolved_dict

    # Initial resolution of templates
    return resolve_dict(d, d.copy())  # Pass a copy of the original dictionary for initial mapping
