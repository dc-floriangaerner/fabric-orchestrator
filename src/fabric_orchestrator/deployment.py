# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Deployment orchestration for Fabric workspaces."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from azure.core.credentials import TokenCredential
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from fabric_cicd import deploy_with_config
from microsoft_fabric_api import FabricClient

from .config import get_workspace_name_from_config, load_workspace_config
from .deployment_config import CONFIG_FILE, SEPARATOR_LONG, SEPARATOR_SHORT
from .fabric_workspace_manager import ensure_workspace_exists
from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class DeploymentResult:
    """Result of a single workspace deployment.

    Attributes:
        workspace_folder: Name of the workspace folder
        workspace_name: Name of the workspace in Fabric
        success: Whether the deployment was successful
        error_message: Error message if deployment failed (empty string if successful)
    """

    workspace_folder: str
    workspace_name: str
    success: bool
    error_message: str = ""


@dataclass
class DeploymentSummary:
    """Summary of all workspace deployments.

    Attributes:
        environment: Target environment (dev/test/prod)
        duration: Total deployment duration in seconds
        results: List of deployment results for all workspaces
    """

    environment: str
    duration: float
    results: list[DeploymentResult]

    @property
    def total_workspaces(self) -> int:
        """Get total number of workspaces deployed."""
        return len(self.results)

    @property
    def successful_count(self) -> int:
        """Get number of successful deployments."""
        return sum(1 for r in self.results if r.success)

    @property
    def failed_count(self) -> int:
        """Get number of failed deployments."""
        return sum(1 for r in self.results if not r.success)


def create_fabric_client(
    token_credential: TokenCredential | ClientSecretCredential | DefaultAzureCredential,
) -> FabricClient:
    """Create and return Microsoft Fabric API client.

    Args:
        token_credential: Azure credential for authentication

    Returns:
        Initialized FabricClient instance for interacting with Fabric APIs

    Examples:
        >>> from azure.identity import DefaultAzureCredential
        >>> credential = DefaultAzureCredential()
        >>> client = create_fabric_client(credential)
    """
    return FabricClient(token_credential=token_credential)


def deploy_workspace(
    workspace_folder: str,
    workspaces_dir: str,
    environment: str,
    token_credential: TokenCredential | ClientSecretCredential | DefaultAzureCredential,
    capacity_id: str | None = None,
    service_principal_object_id: str | None = None,
    entra_admin_group_id: str | None = None,
    config_filename: str = CONFIG_FILE,
) -> DeploymentResult:
    """Deploy a single workspace using configuration file.

    This function orchestrates the deployment of a single Fabric workspace by:
    1. Loading the workspace configuration
    2. Ensuring the workspace exists (creating it if necessary)
    3. Deploying all items defined in the configuration

    Args:
        workspace_folder: Name of the workspace folder
        workspaces_dir: Root directory containing workspace folders
        environment: Target environment (dev/test/prod)
        token_credential: Azure credential for authentication
        capacity_id: Fabric capacity ID used when creating the workspace.
            Required if the workspace does not already exist and must be auto-created;
            optional if the target workspace already exists.
        service_principal_object_id: Azure AD Object ID of the service principal used for
            role assignment when a new workspace is created. Required for auto-creation
            scenarios where the service principal should be granted access; optional if
            the workspace already exists and no new role assignment is needed.
        entra_admin_group_id: Optional Azure AD Object ID of Entra ID group to grant
            admin permissions. If provided, the group will be assigned as a workspace admin.
        config_filename: Name of the configuration file. Defaults to CONFIG_FILE.

    Returns:
        DeploymentResult object with success status and error message if applicable.

    Examples:
        >>> from azure.identity import DefaultAzureCredential
        >>> credential = DefaultAzureCredential()
        >>> result = deploy_workspace(
        ...     workspace_folder="my-workspace",
        ...     workspaces_dir="workspaces",
        ...     environment="dev",
        ...     token_credential=credential,
        ...     capacity_id="12345678-1234-1234-1234-123456789012"
        ... )
        >>> if result.success:
        ...     print(f"Deployed {result.workspace_name} successfully!")
    """
    workspace_name = ""  # Initialize for error handling
    try:
        logger.info(f"\n{SEPARATOR_SHORT}")
        logger.info(f"Deploying workspace: {workspace_folder}")
        logger.info(f"{SEPARATOR_SHORT}\n")

        # Load workspace config
        config = load_workspace_config(workspace_folder, workspaces_dir, config_filename)
        workspace_name = get_workspace_name_from_config(config, environment)
        config_file_path = str(Path(workspaces_dir) / workspace_folder / config_filename)

        logger.info(f"-> Target workspace: {workspace_name}")
        logger.info(f"-> Config file: {config_file_path}")
        logger.info(f"-> Environment: {environment}")

        # Create Fabric API client
        fabric_client = create_fabric_client(token_credential)

        # Ensure workspace exists (create if necessary)
        workspace_id = ensure_workspace_exists(
            workspace_name=workspace_name,
            capacity_id=capacity_id,
            service_principal_object_id=service_principal_object_id,
            entra_admin_group_id=entra_admin_group_id,
            fabric_client=fabric_client,
        )
        logger.info(f"-> Workspace ensured with ID: {workspace_id}")

        # Deploy using config.yml
        logger.info("-> Deploying items using config-based deployment...")
        deploy_with_config(
            config_file_path=config_file_path, environment=environment, token_credential=token_credential
        )

        logger.info(f"\n[OK] Deployment to {workspace_name} completed successfully!\n")
        return DeploymentResult(workspace_folder=workspace_folder, workspace_name=workspace_name, success=True)

    except Exception as e:
        error_message = str(e)
        display_name = workspace_name if workspace_name else workspace_folder
        logger.error(f"\n[FAIL] ERROR: Deployment failed for workspace '{display_name}': {error_message}\n")
        return DeploymentResult(
            workspace_folder=workspace_folder,
            workspace_name=workspace_name if workspace_name else workspace_folder,
            success=False,
            error_message=error_message,
        )


def deploy_all_workspaces(
    workspace_folders: list[str],
    workspaces_directory: str,
    environment: str,
    token_credential: TokenCredential | ClientSecretCredential | DefaultAzureCredential,
    capacity_id: str | None = None,
    service_principal_object_id: str | None = None,
    entra_admin_group_id: str | None = None,
    config_filename: str = CONFIG_FILE,
) -> list[DeploymentResult]:
    """Deploy all specified workspaces and return results.

    This function orchestrates the deployment of multiple Fabric workspaces sequentially,
    continuing even if individual deployments fail (continue-on-failure behavior).

    Args:
        workspace_folders: List of workspace folder names to deploy
        workspaces_directory: Root directory containing workspace folders
        environment: Target environment (dev/test/prod)
        token_credential: Azure credential for authentication
        capacity_id: Optional Fabric workspace capacity ID for creation
        service_principal_object_id: Optional service principal object ID for role assignment
        entra_admin_group_id: Optional Entra ID group ID for admin permissions
        config_filename: Name of the configuration file. Defaults to CONFIG_FILE.

    Returns:
        List of DeploymentResult objects, one per workspace

    Examples:
        >>> from azure.identity import DefaultAzureCredential
        >>> credential = DefaultAzureCredential()
        >>> folders = ["workspace1", "workspace2", "workspace3"]
        >>> results = deploy_all_workspaces(
        ...     workspace_folders=folders,
        ...     workspaces_directory="workspaces",
        ...     environment="dev",
        ...     token_credential=credential
        ... )
        >>> successful = sum(1 for r in results if r.success)
        >>> print(f"Deployed {successful}/{len(results)} workspaces successfully")
    """
    results: list[DeploymentResult] = []

    logger.info(f"Starting deployment of {len(workspace_folders)} workspace(s)...\n")
    for i, workspace_folder in enumerate(workspace_folders, 1):
        logger.info(f"[{i}/{len(workspace_folders)}] Processing workspace: {workspace_folder}")

        result = deploy_workspace(
            workspace_folder=workspace_folder,
            workspaces_dir=workspaces_directory,
            environment=environment,
            token_credential=token_credential,
            capacity_id=capacity_id,
            service_principal_object_id=service_principal_object_id,
            entra_admin_group_id=entra_admin_group_id,
            config_filename=config_filename,
        )

        results.append(result)

    return results


def print_deployment_summary(summary: DeploymentSummary) -> None:
    """Print comprehensive deployment summary to console.

    Outputs a formatted summary including:
    - Environment and duration
    - Total, successful, and failed workspace counts
    - Lists of successful and failed deployments with error messages

    Args:
        summary: Deployment summary containing all results and metrics

    Examples:
        >>> from deployment import DeploymentSummary, DeploymentResult
        >>> results = [
        ...     DeploymentResult("ws1", "Workspace 1", True),
        ...     DeploymentResult("ws2", "Workspace 2", False, "Network error")
        ... ]
        >>> summary = DeploymentSummary("dev", 45.2, results)
        >>> print_deployment_summary(summary)
    """
    logger.info(f"\n{SEPARATOR_LONG}")
    logger.info("DEPLOYMENT SUMMARY")
    logger.info(SEPARATOR_LONG)
    logger.info(f"Environment: {summary.environment.upper()}")
    logger.info(f"Duration: {summary.duration:.2f} seconds")
    logger.info(f"Total workspaces: {summary.total_workspaces}")
    logger.info(f"Successful: {summary.successful_count}")
    logger.info(f"Failed: {summary.failed_count}")
    logger.info(SEPARATOR_LONG)

    # Report successful and failed deployments by iterating through results once
    successful = []
    failed = []
    for result in summary.results:
        if result.success:
            successful.append(result.workspace_name)
        else:
            failed.append((result.workspace_name, result.error_message))

    if successful:
        logger.info("\n[OK] SUCCESSFUL DEPLOYMENTS:")
        for full_name in successful:
            logger.info(f"  [OK] {full_name}")

    if failed:
        logger.error("\n[FAIL] FAILED DEPLOYMENTS:")
        for full_name, error in failed:
            logger.error(f"  [FAIL] {full_name}")
            logger.error(f"    Error: {error}")

    logger.info(f"\n{SEPARATOR_LONG}")


def build_deployment_results_json(summary: DeploymentSummary) -> dict[str, Any]:
    """Build the deployment results dictionary for JSON output.

    Creates a structured dictionary containing deployment metrics and individual
    workspace results, suitable for serialization to JSON for CI/CD reporting.

    Args:
        summary: Deployment summary object

    Returns:
        Dictionary containing deployment results for JSON serialization with structure:
        {
            "environment": str,
            "duration": float,
            "total_workspaces": int,
            "successful_count": int,
            "failed_count": int,
            "workspaces": [
                {
                    "name": str,
                    "full_name": str,
                    "status": "success" | "failure",
                    "error": str
                }
            ]
        }

    Examples:
        >>> from deployment import DeploymentSummary, DeploymentResult
        >>> results = [DeploymentResult("ws1", "Workspace 1", True)]
        >>> summary = DeploymentSummary("dev", 30.5, results)
        >>> json_output = build_deployment_results_json(summary)
        >>> print(json_output["environment"])
        'dev'
    """
    workspaces_list: list[dict[str, Any]] = []

    # Add all workspace results
    for result in summary.results:
        workspaces_list.append(
            {
                "name": result.workspace_folder,
                "full_name": result.workspace_name,
                "status": "success" if result.success else "failure",
                "error": result.error_message,
            }
        )

    # Sort workspaces by name for consistent output
    workspaces_list.sort(key=lambda x: x["name"])

    results_json = {
        "environment": summary.environment,
        "duration": summary.duration,
        "total_workspaces": summary.total_workspaces,
        "successful_count": summary.successful_count,
        "failed_count": summary.failed_count,
        "workspaces": workspaces_list,
    }

    return results_json


def save_deployment_results(summary: DeploymentSummary, results_filename: str) -> None:
    """Save deployment results to a JSON file.

    Args:
        summary: Deployment summary to save
        results_filename: Path to the output JSON file

    Examples:
        >>> from deployment import DeploymentSummary, DeploymentResult
        >>> results = [DeploymentResult("ws1", "Workspace 1", True)]
        >>> summary = DeploymentSummary("dev", 30.5, results)
        >>> save_deployment_results(summary, "results.json")
    """
    deployment_results_json = build_deployment_results_json(summary)
    with open(results_filename, "w", encoding="utf-8") as f:
        json.dump(deployment_results_json, f, indent=2)
    logger.info(f"\n-> Deployment results written to {results_filename}")
