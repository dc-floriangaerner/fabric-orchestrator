# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Azure authentication credential management for Fabric deployments."""

import os

from azure.identity import ClientSecretCredential, DefaultAzureCredential

from .deployment_config import (
    ENV_AZURE_CLIENT_ID,
    ENV_AZURE_CLIENT_SECRET,
    ENV_AZURE_TENANT_ID,
)
from .logger import get_logger

logger = get_logger(__name__)


def create_credential_from_env() -> ClientSecretCredential | DefaultAzureCredential:
    """Create and return the appropriate Azure credential based on environment variables.

    This function checks for service principal credentials in environment variables.
    If all required variables (client ID, tenant ID, and client secret) are present,
    it creates a ClientSecretCredential. Otherwise, it falls back to DefaultAzureCredential
    which is suitable for local development and supports multiple authentication methods.

    Environment Variables:
        AZURE_CLIENT_ID: The client ID of the Azure service principal
        AZURE_TENANT_ID: The tenant ID of the Azure Active Directory
        AZURE_CLIENT_SECRET: The client secret of the Azure service principal

    Returns:
        ClientSecretCredential if service principal credentials are found in environment,
        DefaultAzureCredential otherwise for local development scenarios.

    Examples:
        >>> # In CI/CD pipelines with service principal
        >>> credential = create_credential_from_env()  # Returns ClientSecretCredential
        >>> # In local development
        >>> credential = create_credential_from_env()  # Returns DefaultAzureCredential
    """
    client_id = os.getenv(ENV_AZURE_CLIENT_ID)
    tenant_id = os.getenv(ENV_AZURE_TENANT_ID)
    client_secret = os.getenv(ENV_AZURE_CLIENT_SECRET)

    if client_id and tenant_id and client_secret:
        logger.info("-> Using ClientSecretCredential for authentication")
        return ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
    else:
        logger.info("-> Using DefaultAzureCredential for authentication (local development)")
        return DefaultAzureCredential()
