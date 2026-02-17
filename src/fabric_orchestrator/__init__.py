"""Fabric Orchestrator - Python library for orchestrating Microsoft Fabric workspace deployments.

This library provides tools for:
- Deploying Fabric workspace items across multiple environments
- Managing workspace lifecycle (creation, permissions)
- Orchestrating multi-workspace deployments
- ID transformation for environment-specific configurations

Example:
    >>> from fabric_orchestrator import deploy_workspace, DeploymentConfig
    >>> config = DeploymentConfig(
    ...     workspace_name="My Workspace",
    ...     environment="dev",
    ...     workspace_folder="./workspaces/MyWorkspace"
    ... )
    >>> result = deploy_workspace(config)
"""

__version__ = "1.0.0"

# Core data models
from .deployer import DeploymentResult, DeploymentSummary

# Workspace management functions
from .workspace_manager import (
    assign_workspace_role,
    check_role_assignment_exists,
    check_workspace_exists,
    create_workspace,
    ensure_workspace_exists,
    grant_workspace_role,
)

# Configuration
from .config import (
    CONFIG_FILE,
    EXIT_FAILURE,
    EXIT_SUCCESS,
    RESULTS_FILENAME,
    SEPARATOR_LONG,
    SEPARATOR_SHORT,
    VALID_ENVIRONMENTS,
)

# Logging utilities
from .logger import get_logger, setup_logger

__all__ = [
    # Version
    "__version__",
    # Data models
    "DeploymentResult",
    "DeploymentSummary",
    # Workspace management
    "assign_workspace_role",
    "check_workspace_exists",
    "create_workspace",
    "ensure_workspace_exists",
    "check_role_assignment_exists",
    "grant_workspace_role",
    # Configuration
    "CONFIG_FILE",
    "VALID_ENVIRONMENTS",
    "SEPARATOR_LONG",
    "SEPARATOR_SHORT",
    "RESULTS_FILENAME",
    "EXIT_SUCCESS",
    "EXIT_FAILURE",
    # Logging
    "get_logger",
    "setup_logger",
]
