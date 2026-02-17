# Fabric Orchestrator

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Python library for orchestrating Microsoft Fabric workspace deployments across multiple environments.

## Overview

Fabric Orchestrator is a Python library extracted from the [dc-fabric-cicd](https://github.com/dc-floriangaerner/dc-fabric-cicd) reference architecture. It provides a reusable, pip-installable package for:

- **Multi-workspace deployment orchestration** - Deploy multiple Fabric workspaces from a single codebase
- **Workspace lifecycle management** - Auto-create workspaces and manage permissions
- **Environment-specific ID transformation** - Automatically replace workspace/lakehouse IDs for different environments
- **CI/CD integration** - Designed for GitHub Actions and Azure DevOps pipelines

## Installation

Install from GitHub Packages:

```bash
pip install fabric-orchestrator
```

Install from source:

```bash
git clone https://github.com/dc-floriangaerner/fabric-orchestrator.git
cd fabric-orchestrator
pip install -e .
```

## Quick Start

### Using the CLI

```bash
# Deploy all workspaces to dev environment
fabric-orchestrator --workspaces_directory ./workspaces --environment dev

# Deploy to production
fabric-orchestrator --workspaces_directory ./workspaces --environment prod
```

### Using the Python API

```python
from fabric_orchestrator import (
    check_workspace_exists,
    create_workspace,
    ensure_workspace_exists,
    DeploymentResult,
)
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

### Workspace Management

- **Auto-create workspaces** - Automatically create workspaces if they don't exist
- **Permission management** - Assign Service Principal and Entra ID group permissions
- **Workspace discovery** - Auto-discover workspace folders from directory structure

### Deployment Orchestration

- **Multi-workspace support** - Deploy multiple workspaces in a single run
- **Continue-on-failure** - Deploy all workspaces even if one fails
- **Deployment summary** - Detailed JSON output for CI/CD integration
- **Environment-specific configuration** - Use different settings for dev/test/prod

### ID Transformation

- **Automatic ID replacement** - Replace dev IDs with target environment IDs
- **Lakehouse references** - Transform lakehouse IDs in notebooks and pipelines
- **Workspace references** - Transform workspace IDs across environments
- **Connection strings** - Update SQL endpoints and connection strings

## Requirements

- Python 3.11+
- Azure Service Principal with Fabric permissions
- Microsoft Fabric capacity

### Dependencies

- `fabric-cicd>=0.1.0` - Core Fabric deployment library
- `azure-identity>=1.19.1` - Azure authentication
- `pyyaml>=6.0` - YAML configuration parsing
- `microsoft-fabric-api>=0.1.0b2` - Fabric REST API client

## Configuration

### Environment Variables

Required for authentication:
- `AZURE_CLIENT_ID` - Service Principal Client ID
- `AZURE_CLIENT_SECRET` - Service Principal Secret
- `AZURE_TENANT_ID` - Azure AD Tenant ID

Optional for workspace creation:
- `FABRIC_CAPACITY_ID` - Capacity ID for auto-creating workspaces
- `DEPLOYMENT_SP_OBJECT_ID` - Service Principal Object ID for admin role
- `FABRIC_ADMIN_GROUP_ID` - Entra ID group for centralized access

### Workspace Structure

Each workspace folder should contain:
- `config.yml` - Workspace names per environment
- `parameter.yml` - Environment-specific ID transformations
- Fabric items (Lakehouses, Notebooks, Pipelines, etc.)

Example structure:
```
workspaces/
└── My Workspace/
    ├── config.yml
    ├── parameter.yml
    ├── Lakehouse.Lakehouse/
    ├── Notebook.Notebook/
    └── DataPipeline.DataPipeline/
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/dc-floriangaerner/fabric-orchestrator.git
cd fabric-orchestrator

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_workspace_manager.py

# Run with coverage report
pytest --cov=fabric_orchestrator --cov-report=html
```

### Code Quality

```bash
# Format code with ruff
ruff format .

# Lint code
ruff check .

# Type checking
mypy src/fabric_orchestrator
```

## Documentation

- [API Reference](#) - Coming soon
- [dc-fabric-cicd Wiki](https://github.com/dc-floriangaerner/dc-fabric-cicd/wiki) - Reference implementation

## Contributing

Contributions are welcome! Please see the source repository for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [dc-fabric-cicd](https://github.com/dc-floriangaerner/dc-fabric-cicd) - Reference architecture using this library
- [fabric-cicd](https://github.com/microsoft/fabric-cicd) - Microsoft's official Fabric CI/CD library

## Acknowledgments

This library was extracted from the dc-fabric-cicd reference architecture to provide a reusable deployment orchestration solution for Microsoft Fabric.

## Support

For issues and questions:
- [GitHub Issues](https://github.com/dc-floriangaerner/fabric-orchestrator/issues)
- [dc-fabric-cicd Discussions](https://github.com/dc-floriangaerner/dc-fabric-cicd/discussions)
