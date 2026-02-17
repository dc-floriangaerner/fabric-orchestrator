# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Workspace discovery utilities for Fabric deployments."""

from pathlib import Path

from .deployment_config import CONFIG_FILE
from .logger import get_logger

logger = get_logger(__name__)


def get_workspace_folders(workspaces_dir: str, config_filename: str = CONFIG_FILE) -> list[str]:
    """Get all workspace folders from the workspaces directory.

    Scans the workspaces directory and returns all subdirectories that contain
    a valid configuration file.

    Args:
        workspaces_dir: Root directory containing workspace folders
        config_filename: Name of the configuration file to look for. Defaults to CONFIG_FILE.

    Returns:
        Sorted list of workspace folder names that contain the configuration file

    Raises:
        FileNotFoundError: If workspaces directory doesn't exist
        ValueError: If no workspace folders with configuration file are found

    Examples:
        >>> folders = get_workspace_folders("workspaces")
        >>> print(folders)
        ['workspace1', 'workspace2', 'workspace3']
    """
    workspaces_path = Path(workspaces_dir)
    if not workspaces_path.exists():
        raise FileNotFoundError(f"Workspaces directory not found: {workspaces_dir}")

    workspace_folders = [
        folder.name
        for folder in workspaces_path.iterdir()
        if folder.is_dir() and (folder / config_filename).exists()
    ]

    if not workspace_folders:
        raise ValueError(
            f"No workspace folders with '{config_filename}' found in {workspaces_dir}. "
            "Each workspace folder must contain a config.yml file."
        )

    return sorted(workspace_folders)


def discover_workspace_folders(workspaces_directory: str, config_filename: str = CONFIG_FILE) -> list[str]:
    """Discover and return all workspace folders to deploy.

    Automatically discovers all workspace folders in the workspaces directory
    that contain a valid configuration file.

    Args:
        workspaces_directory: Root directory containing workspace folders
        config_filename: Name of the configuration file to look for. Defaults to CONFIG_FILE.

    Returns:
        Sorted list of workspace folder names to deploy

    Raises:
        ValueError: If no workspace folders are found
        FileNotFoundError: If workspaces directory doesn't exist

    Examples:
        >>> folders = discover_workspace_folders("workspaces")
        -> Discovered 3 workspace(s): workspace1, workspace2, workspace3
        >>> print(folders)
        ['workspace1', 'workspace2', 'workspace3']
    """
    workspace_folders = get_workspace_folders(workspaces_directory, config_filename)
    logger.info(f"-> Discovered {len(workspace_folders)} workspace(s): {', '.join(workspace_folders)}\n")
    return workspace_folders
