# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Fabric Orchestrator - Python library for orchestrating Microsoft Fabric workspace deployments

This library provides configuration-based CI/CD deployment capabilities for Microsoft Fabric,
enabling automated workspace management and deployment workflows.

Key Features:
- Configuration-based workspace deployment
- Automatic workspace creation and management
- Environment-specific deployments (dev/test/prod)
- Multi-workspace support with continue-on-failure
- Integration with Azure authentication

Main Components:
- deploy_all_workspaces: Deploy multiple workspaces from a directory
- deploy_workspace: Deploy a single workspace
- ensure_workspace_exists: Create workspace if needed
- create_azure_credential: Configure Azure authentication
- create_fabric_client: Initialize Fabric API client
"""

__version__ = "0.1.0"

# Import key functions for public API
from .deploy_to_fabric import (
    DeploymentResult,
    DeploymentSummary,
    create_azure_credential,
    create_fabric_client,
    deploy_all_workspaces,
    deploy_workspace,
    discover_workspace_folders,
    validate_environment,
)
from .fabric_workspace_manager import (
    add_entra_id_group_admin,
    add_workspace_admin,
    assign_workspace_role,
    check_workspace_exists,
    create_workspace,
    ensure_workspace_exists,
)
from .logger import get_logger, setup_logger

__all__ = [
    # Version
    "__version__",
    # Deployment functions
    "deploy_all_workspaces",
    "deploy_workspace",
    "discover_workspace_folders",
    "validate_environment",
    # Workspace management
    "ensure_workspace_exists",
    "create_workspace",
    "check_workspace_exists",
    "add_workspace_admin",
    "add_entra_id_group_admin",
    "assign_workspace_role",
    # Authentication
    "create_azure_credential",
    "create_fabric_client",
    # Logging
    "get_logger",
    "setup_logger",
    # Data classes
    "DeploymentResult",
    "DeploymentSummary",
]

