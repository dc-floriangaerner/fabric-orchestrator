# Fabric Orchestrator

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A Python library for orchestrating Microsoft Fabric workspace deployments with configuration-based CI/CD.

## Overview

`fabric-orchestrator` provides a programmatic interface for deploying Microsoft Fabric workspace items (Lakehouses, Notebooks, Pipelines, Semantic Models, etc.) across multiple workspaces and environments. Built on top of the `fabric-cicd` library, it enables automated deployment workflows with workspace management capabilities.

### Key Features

- **Configuration-based deployment**: Define workspace deployments in YAML configuration files
- **Automatic workspace creation**: Create workspaces programmatically if they don't exist
- **Multi-workspace support**: Deploy multiple workspaces with continue-on-failure semantics
- **Environment management**: Support for dev/test/prod environment-specific deployments
- **ID transformation**: Automatically adjust workspace-specific references across environments
- **Azure authentication**: Seamless integration with Azure service principals and managed identities

## Installation

```bash
pip install fabric-orchestrator
```

For development installation:

```bash
git clone https://github.com/dc-floriangaerner/fabric-orchestrator.git
cd fabric-orchestrator
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
from fabric_orchestrator import (
    create_azure_credential,
    create_fabric_client,
    deploy_workspace,
    ensure_workspace_exists,
)

# Authenticate with Azure
credential = create_azure_credential()
fabric_client = create_fabric_client(credential)

# Ensure workspace exists
workspace_id = ensure_workspace_exists(
    workspace_name="[D] My Workspace",
    capacity_id="your-capacity-id",
    fabric_client=fabric_client,
)

# Deploy a single workspace
result = deploy_workspace(
    workspace_folder="Fabric Blueprint",
    workspaces_dir="./workspaces",
    environment="dev",
    token_credential=credential,
    capacity_id="your-capacity-id",
    service_principal_object_id="your-sp-object-id",
    entra_admin_group_id="your-admin-group-id",
)

print(f"Deployment {'succeeded' if result.success else 'failed'}: {result.workspace_name}")
```

### Deploy Multiple Workspaces

```python
from fabric_orchestrator import deploy_all_workspaces

# Deploy all workspaces in a directory
results = deploy_all_workspaces(
    workspace_folders=["Fabric Blueprint", "Another Workspace"],
    workspaces_directory="./workspaces",
    environment="dev",
    token_credential=credential,
    capacity_id="your-capacity-id",
    service_principal_object_id="your-sp-object-id",
    entra_admin_group_id="your-admin-group-id",
)

# Check results
for result in results:
    status = "✓" if result.success else "✗"
    print(f"{status} {result.workspace_name}")
```

## Configuration

### Workspace Structure

Each workspace requires a `config.yml` file:

```yaml
# workspaces/Fabric Blueprint/config.yml
workspace_names:
  dev: "[D] Fabric Blueprint"
  test: "[T] Fabric Blueprint"
  prod: "[P] Fabric Blueprint"
```

Optional `parameter.yml` for ID transformations:

```yaml
# workspaces/Fabric Blueprint/parameter.yml
find_replace:
  - find_value: "dev-lakehouse-id"
    replace_value:
      _ALL_: "$items.Lakehouse.lakehouse_bronze.id"
    item_type: "Notebook"
```

### Environment Variables

The library reads Azure credentials from environment variables:

- `AZURE_CLIENT_ID` - Service Principal Client ID
- `AZURE_CLIENT_SECRET` - Service Principal Secret
- `AZURE_TENANT_ID` - Azure AD Tenant ID

Optional variables for workspace creation:

- `FABRIC_CAPACITY_ID` - Fabric capacity ID
- `DEPLOYMENT_SP_OBJECT_ID` - Service Principal Object ID
- `FABRIC_ADMIN_GROUP_ID` - Entra ID admin group ID


## API Reference

### Deployment Functions

- `deploy_workspace()` - Deploy a single workspace
- `deploy_all_workspaces()` - Deploy multiple workspaces
- `discover_workspace_folders()` - Find all workspace folders in a directory

### Workspace Management

- `ensure_workspace_exists()` - Create workspace if it doesn't exist
- `create_workspace()` - Create a new workspace
- `check_workspace_exists()` - Check if workspace exists
- `add_workspace_admin()` - Add admin to workspace
- `assign_workspace_role()` - Assign role to user/group

### Authentication

- `create_azure_credential()` - Create Azure credential
- `create_fabric_client()` - Initialize Fabric API client

### Logging

- `get_logger()` - Get module logger
- `setup_logger()` - Configure logging

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/dc-floriangaerner/fabric-orchestrator.git
cd fabric-orchestrator

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=fabric_orchestrator --cov-report=html

# Run specific test
pytest tests/test_deploy_to_fabric.py -v
```

### Code Quality

```bash
# Lint code
ruff check src/

# Format code
ruff format src/

# Type checking
mypy src/
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Create an issue describing the change
2. Fork the repository
3. Create a feature branch (`feature/<issue-number>-description`)
4. Make changes and add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [Documentation](https://github.com/dc-floriangaerner/fabric-orchestrator/wiki)
- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [fabric-cicd Library](https://pypi.org/project/fabric-cicd/)
- [Issue Tracker](https://github.com/dc-floriangaerner/fabric-orchestrator/issues)

## Credits

Built with:
- [fabric-cicd](https://github.com/microsoft/fabric-cicd) - Microsoft Fabric deployment library
- [microsoft-fabric-api](https://pypi.org/project/microsoft-fabric-api/) - Fabric REST API client
- [azure-identity](https://pypi.org/project/azure-identity/) - Azure authentication

---

**Note**: This library is in early development. APIs may change between versions. Use semantic versioning to pin to specific  versions in production.
