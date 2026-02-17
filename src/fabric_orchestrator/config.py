# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Configuration management for Fabric workspace deployments."""

from pathlib import Path
from typing import Any

import yaml

from .deployment_config import CONFIG_FILE
from .logger import get_logger

logger = get_logger(__name__)


def load_workspace_config(
    workspace_folder: str, workspaces_dir: str, config_filename: str = CONFIG_FILE
) -> dict[str, Any]:
    """Load configuration file for a workspace.

    Args:
        workspace_folder: Name of the workspace folder
        workspaces_dir: Root directory containing workspace folders
        config_filename: Name of the configuration file to load. Defaults to CONFIG_FILE.

    Returns:
        Parsed configuration dictionary containing workspace settings.

    Raises:
        FileNotFoundError: If configuration file doesn't exist in the workspace folder
        yaml.YAMLError: If configuration file contains invalid YAML syntax

    Examples:
        >>> config = load_workspace_config("my-workspace", "workspaces")
        >>> workspace_name = config["core"]["workspace"]["dev"]
    """
    config_path = Path(workspaces_dir) / workspace_folder / config_filename
    if not config_path.exists():
        raise FileNotFoundError(f"{config_filename} not found in {workspace_folder}")

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config


def get_workspace_name_from_config(config: dict[str, Any], environment: str) -> str:
    """Extract workspace name for a specific environment from configuration.

    The function looks up the workspace name in the config dictionary
    using the path: core.workspace.<environment>

    Args:
        config: Parsed configuration dictionary from config.yml
        environment: Target environment (dev/test/prod)

    Returns:
        Workspace name for the specified environment

    Raises:
        KeyError: If environment is not defined in the configuration file

    Examples:
        >>> config = {"core": {"workspace": {"dev": "ws-dev", "prod": "ws-prod"}}}
        >>> get_workspace_name_from_config(config, "dev")
        'ws-dev'
    """
    try:
        workspace_name = config["core"]["workspace"][environment]
        return workspace_name
    except KeyError:
        raise KeyError(
            f"Workspace name for environment '{environment}' not found in config.yml. "
            f"Expected: core.workspace.{environment}"
        ) from None
