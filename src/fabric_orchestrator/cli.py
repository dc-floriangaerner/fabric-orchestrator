"""Command-line interface for fabric-orchestrator."""

import argparse
import json
import os
import sys
import time

from fabric_cicd import append_feature_flag, change_log_level

from .config import (
    ENV_ACTIONS_RUNNER_DEBUG,
    ENV_DEPLOYMENT_SP_OBJECT_ID,
    ENV_FABRIC_ADMIN_GROUP_ID,
    ENV_FABRIC_CAPACITY_ID,
    EXIT_FAILURE,
    EXIT_SUCCESS,
    RESULTS_FILENAME,
    SEPARATOR_LONG,
    VALID_ENVIRONMENTS,
)
from .deployer import (
    DeploymentSummary,
    build_deployment_results_json,
    create_azure_credential,
    deploy_all_workspaces,
    discover_workspace_folders,
    print_deployment_summary,
    validate_environment,
)
from .logger import get_logger

logger = get_logger(__name__)


def main() -> None:
    """Main CLI entry point for fabric-orchestrator."""
    # Enable experimental features
    append_feature_flag("enable_experimental_features")
    append_feature_flag("enable_config_deploy")

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Fabric Orchestrator - Deploy Microsoft Fabric workspaces across environments"
    )
    parser.add_argument(
        "--workspaces_directory",
        type=str,
        required=True,
        help="Root directory containing workspace folders",
    )
    parser.add_argument(
        "--environment",
        type=str,
        required=True,
        choices=list(VALID_ENVIRONMENTS),
        help="Target environment (dev/test/prod)",
    )

    args = parser.parse_args()

    workspaces_directory = args.workspaces_directory
    environment = args.environment

    # Force unbuffered output for CI/CD logs
    sys.stdout.reconfigure(line_buffering=True, write_through=True)
    sys.stderr.reconfigure(line_buffering=True, write_through=True)

    # Enable debugging if ACTIONS_RUNNER_DEBUG is set
    if os.getenv(ENV_ACTIONS_RUNNER_DEBUG, "false").lower() == "true":
        change_log_level("DEBUG")

    logger.info(f"\n{SEPARATOR_LONG}")
    logger.info("FABRIC MULTI-WORKSPACE DEPLOYMENT")
    logger.info(SEPARATOR_LONG)
    logger.info(f"Environment: {environment.upper()}")
    logger.info(f"Workspaces directory: {workspaces_directory}")
    logger.info(f"{SEPARATOR_LONG}\n")

    try:
        # Validate environment
        validate_environment(environment)

        # Authenticate
        token_credential = create_azure_credential()

        # Get workspace creation configuration from environment
        capacity_id = os.getenv(ENV_FABRIC_CAPACITY_ID)
        service_principal_object_id = os.getenv(ENV_DEPLOYMENT_SP_OBJECT_ID)
        entra_admin_group_id = os.getenv(ENV_FABRIC_ADMIN_GROUP_ID)

        # Auto-discover all workspace folders
        workspace_folders = discover_workspace_folders(workspaces_directory)

        # Track deployment duration
        deployment_start_time = time.time()

        # Deploy all workspaces
        results = deploy_all_workspaces(
            workspace_folders=workspace_folders,
            workspaces_directory=workspaces_directory,
            environment=environment,
            token_credential=token_credential,
            capacity_id=capacity_id,
            service_principal_object_id=service_principal_object_id,
            entra_admin_group_id=entra_admin_group_id,
        )

        # Calculate deployment duration
        deployment_duration = time.time() - deployment_start_time

        # Create deployment summary
        summary = DeploymentSummary(environment=environment, duration=deployment_duration, results=results)

        # Write deployment results to JSON file for CI/CD summary
        deployment_results_json = build_deployment_results_json(summary)
        with open(RESULTS_FILENAME, "w", encoding="utf-8") as f:
            json.dump(deployment_results_json, f, indent=2)
        logger.info(f"\n-> Deployment results written to {RESULTS_FILENAME}")

        # Print comprehensive deployment summary
        print_deployment_summary(summary)

        # Exit with appropriate code
        if summary.failed_count > 0:
            logger.warning(f"\nDeployment completed with {summary.failed_count} failure(s)\n")
            sys.exit(EXIT_FAILURE)
        else:
            logger.info(f"\nAll {summary.successful_count} workspace(s) deployed successfully!\n")
            sys.exit(EXIT_SUCCESS)

    except (ValueError, FileNotFoundError) as e:
        logger.error(f"\n[FAIL] VALIDATION ERROR: {e!s}\n")
        sys.exit(EXIT_FAILURE)
    except Exception as e:
        logger.error(f"\n[FAIL] CRITICAL ERROR: {e!s}\n")
        sys.exit(EXIT_FAILURE)


if __name__ == "__main__":
    main()
