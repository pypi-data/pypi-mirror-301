# VariConfig

**VariConfig** is a flexible and powerful Python package for managing configuration files. It supports both YAML and JSON formats and allows for the use of variables within the configuration files, using template placeholders like `{{ var }}`.

## Features

- **Read Configurations**: Load configurations from YAML or JSON files.
- **Template Resolution**: Supports variables inside configuration files using template placeholders (e.g., `{{ var }}`).
- **Nested Configs**: Handles nested dictionaries as attribute-based objects for easy access.
- **Dynamic Updates**: Update configurations dynamically in the code.
- **Conversion**: Convert configurations back to standard Python dictionaries.

## Installation

To install VariConfig, use pip:

```bash
pip install variconfig
```

## Usage

### 1. Loading a Configuration

You can load configuration files in YAML or JSON format:

```python
from variconfig import ConfigDict

# Load a YAML file
config = ConfigDict.from_yaml('config.yml')

# Load a JSON file
config = ConfigDict.from_json('config.json')
```

### 2. Accessing Configuration Values

Once the configuration is loaded, values can be accessed as object attributes:

```python
# Access configuration values
print(config.data_dir)  # Output: path from config.yml
print(config.logging_config.loggers.matgraphdb.level)  # Output: INFO
```

### 3. Template Resolution

Variables can be defined using `{{ var }}` placeholders in the configuration file. These will be resolved when the configuration is loaded:

```yaml
root_dir: "."
data_dir: "{{ root_dir }}/data"
log_dir: "{{ root_dir }}/logs"
```

In the example above, `data_dir` will be resolved to `./data`, and `log_dir` will be resolved to `./logs`.

### 4. Updating Configurations

You can modify configuration values at runtime:

```python
# Update a configuration value
config.logging_config.loggers.matgraphdb.level = 'DEBUG'

# Print updated value
print(config.logging_config.loggers.matgraphdb.level)  # Output: DEBUG
```

### 5. Converting to Dictionary

If you need to convert the configuration back to a standard Python dictionary:

```python
config_dict = config.to_dict()
print(config_dict)
```

## Example Configuration (YAML)

```yaml
root_dir: "."
data_dir: "{{ root_dir }}/data"
log_dir: "{{ root_dir }}/logs"
db_name: 'VariConfig'

logging_config:
  version: 1
  disable_existing_loggers: False
  formatters:
    simple:
      format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
      datefmt: '%Y-%m-%d %H:%M:%S'
  handlers:
    console:
      class: logging.StreamHandler
      formatter: simple
      stream: ext://sys.stdout
    file:
      class: logging.FileHandler
      formatter: simple
      filename: "{{ log_dir }}/variconfig.log"
      mode: a
  loggers:
    variconfig:
      level: INFO
      handlers: [console]
      propagate: no
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
