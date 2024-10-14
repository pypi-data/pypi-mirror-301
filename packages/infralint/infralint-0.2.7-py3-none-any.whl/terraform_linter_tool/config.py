import importlib.resources as pkg_resources
import logging
import shutil
from pathlib import Path
from typing import Optional  # Import Optional

import yaml

from terraform_linter_tool import \
    resources  # Assuming `resources` is inside your package

# Set up logging
logger = logging.getLogger(__name__)

# Define the default configuration location and the default values
CONFIG_DIR = Path.home() / ".infralint"
CONFIG_FILE = CONFIG_DIR / "config.yaml"


def ensure_config_exists():
    """
    Ensure that the configuration file exists in ~/.infralint. If not, copy the one from resources.
    """
    if not CONFIG_FILE.exists():
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            # Copy the config file from resources
            with pkg_resources.path(resources, 'config.yaml') as resource_config:
                shutil.copy(resource_config, CONFIG_FILE)
            logger.info(f"Default configuration copied to {CONFIG_FILE}")
        except Exception as e:
            logger.error(f"Failed to create default config: {e}")
            raise
    else:
        logger.debug(f"Configuration already exists at {CONFIG_FILE}")
    return CONFIG_FILE


def load_config(config_path: Optional[str] = None):  # Fix by using Optional[str]
    """
    Load the configuration from the provided path or the default ~/.infralint/config.yaml.
    """
    config_file = Path(config_path) if config_path else CONFIG_FILE

    if not config_file.exists():
        logger.error(f"Config file not found at: {config_file}")
        raise FileNotFoundError(f"Config file not found at: {config_file}")

    try:
        with config_file.open('r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Loaded configuration from: {config_file}")
            return config
    except Exception as e:
        logger.error(f"Failed to load configuration from {config_file}: {e}")
        raise