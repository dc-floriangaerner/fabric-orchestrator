# Fabric Orchestrator

Python library for orchestrating Microsoft Fabric workspace deployments across multiple environments.

## Overview

Fabric Orchestrator is a Python library extracted from the [dc-fabric-cicd](https://github.com/dc-floriangaerner/dc-fabric-cicd) reference architecture. It provides a reusable, pip-installable package for:

- **Multi-workspace deployment orchestration** - Deploy multiple Fabric workspaces from a single codebase
- **Workspace lifecycle management** - Auto-create workspaces and manage permissions
- **Environment-specific ID transformation** - Automatically replace workspace/lakehouse IDs for different environments
- **CI/CD integration** - Designed for GitHub Actions and Azure DevOps pipelines

## Installation

```bash
pip install fabric-orchestrator
```

## Quick Example

```python
from fabric_orchestrator import check_workspace_exists, create_workspace
from microsoft_fabric_api import FabricClient
from azure.identity import ClientSecretCredential

# Setup authentication
credential = ClientSecretCredential(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-client-secret"
)

fabric_client = FabricClient(credential)

# Check if workspace exists
workspace_id = check_workspace_exists("My Workspace", fabric_client)

# Create workspace if it doesn't exist
if not workspace_id:
    workspace_id = create_workspace(
        workspace_name="My Workspace",
        capacity_id="your-capacity-id",
        fabric_client=fabric_client
    )
```

## Features

- **Workspace Management** - Auto-create workspaces and manage permissions
- **Deployment Orchestration** - Deploy multiple workspaces in a single run
- **ID Transformation** - Automatic environment-specific ID replacement
- **CI/CD Integration** - Built for automation pipelines

## Next Steps

- [Getting Started](getting-started.md) - Installation and basic usage
- [API Reference](api/overview.md) - Complete API documentation
- [Contributing](contributing.md) - Development guidelines
