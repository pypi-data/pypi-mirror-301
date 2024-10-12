import os
import sys

import yaml
from pathlib import Path

ENV_DATA_STORAGE_NAME_ENV_VAR_KEY = "BTPY_ENV_DATA_STORAGE_NAME"
ENV_DATA_STORAGE_NAME_CONFIG_KEY = "EnvDataStorageName"


def get_config_path(app_name: str) -> Path:
    if os.name == "nt":  # Windows
        return (
                Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming")) / app_name
        )
    elif os.name == "posix":  # Unix-like systems (Linux, macOS, etc.)
        if sys.platform == "darwin":  # macOS
            return Path.home() / "Library" / "Application Support" / app_name
        else:  # Linux and other Unix-like systems
            return (
                    Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / app_name
            )
    else:
        raise NotImplementedError(f"Unsupported platform: {os.name}")


def get_env_data_storage_name():
    # Try env var
    env_value = os.getenv(ENV_DATA_STORAGE_NAME_ENV_VAR_KEY)

    if env_value:
        return env_value

    # Try user config file
    conf = get_config_path("btpy")
    # conf = get_config_path("btpy").mkdir(parents=True, exist_ok=True)
    config_file_path = os.path.expanduser(os.path.join(conf, "config.yaml"))

    if not os.path.exists(config_file_path):
        raise FileNotFoundError(
            f"Failed to read env data storage name from file: {config_file_path} \
        (can also be set through env var: {ENV_DATA_STORAGE_NAME_ENV_VAR_KEY})")

    with open(config_file_path, "r") as config_file:
        config_yaml = yaml.safe_load(config_file)
        config_value = config_yaml[ENV_DATA_STORAGE_NAME_CONFIG_KEY]

        if config_value:
            return config_value
