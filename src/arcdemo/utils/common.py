from pathlib import Path

import yaml
from box import ConfigBox
from box.exceptions import BoxValueError

from arcdemo import logger


def read_config(config_file: Path) -> ConfigBox:
    try:
        with open(config_file, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"Config file loaded: {config_file}")
            return ConfigBox(content)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_file}")
    except BoxValueError as e:
        raise BoxValueError(f"Error in config file: {e}")
