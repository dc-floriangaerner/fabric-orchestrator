# Getting Started

## Installation

### From GitHub Packages

```bash
pip install fabric-orchestrator
```

### From Source

```bash
git clone https://github.com/dc-floriangaerner/fabric-orchestrator.git
cd fabric-orchestrator
pip install -e .
```

## Prerequisites

- Python 3.11 or higher
- Azure Service Principal with Fabric permissions
- Microsoft Fabric capacity

## Basic Usage

### Using the CLI

Deploy all workspaces to an environment:

```bash
fabric-orchestrator --workspaces_directory ./workspaces --environment dev
```

### Using the Python API

#### Check if Workspace Exists

```python
from fabric_orchestrator import check_workspace_exists
from microsoft_fabric_api import FabricClient
from azure.identity import ClientSecretCredential

credential = ClientSecretCredential(
    tenant_id="your-tenant-id",
    client_id="your-client-id",
    client_secret="your-client-secret"
)

fabric_client = FabricClient(credential)
workspace_id = check_workspace_exists("My Workspace", fabric_client)
```

#### Create a Workspace

```python
from fabric_orchestrator import create_workspace

workspace_id = create_workspace(
    workspace_name="My Workspace",
    capacity_id="your-capacity-id",
    fabric_client=fabric_client
)
```

#### Ensure Workspace Exists (Create if Missing)

```python
from fabric_orchestrator import ensure_workspace_exists

workspace_id = ensure_workspace_exists(
    workspace_name="My Workspace",
    capacity_id="your-capacity-id",
    service_principal_object_id="your-sp-object-id",
    entra_admin_group_id="your-group-id",
    fabric_client=fabric_client
)
```

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

## Next Steps

- [API Reference](api/overview.md) - Detailed API documentation
- [dc-fabric-cicd Wiki](https://github.com/dc-floriangaerner/dc-fabric-cicd/wiki) - Reference implementation examples
