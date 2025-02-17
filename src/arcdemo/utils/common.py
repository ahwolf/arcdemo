from pathlib import Path

import yaml  # type: ignore
from box import ConfigBox

from arcdemo import logger


def read_config(config_file: Path) -> ConfigBox:
    """Reads the configuration file and returns a ConfigBox object."""
    try:
        with open(config_file, "r", encoding="utf-8") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info("Config file loaded: %s", config_file)
            return ConfigBox(content)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Config file not found: {config_file}") from exc
