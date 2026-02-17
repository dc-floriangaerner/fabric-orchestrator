# Configuration API

Configuration constants and utilities.

## Constants

### File Names

```python
CONFIG_FILE = "config.yml"
RESULTS_FILENAME = "deployment-results.json"
```

### Environments

```python
VALID_ENVIRONMENTS = {"dev", "test", "prod"}
```

Valid deployment environment names.

### Console Output

```python
SEPARATOR_LONG = "=" * 70
SEPARATOR_SHORT = "=" * 60
```

Separators for console output formatting.

### Exit Codes

```python
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
```

Standard exit codes for CLI applications.

## Environment Variables

### Required for Authentication

- `AZURE_CLIENT_ID` - Service Principal Client ID
- `AZURE_TENANT_ID` - Azure AD Tenant ID
- `AZURE_CLIENT_SECRET` - Service Principal Secret

### Optional for Workspace Creation

- `FABRIC_CAPACITY_ID` - Fabric capacity ID for auto-creating workspaces
- `DEPLOYMENT_SP_OBJECT_ID` - Service Principal Object ID for admin role assignment
- `FABRIC_ADMIN_GROUP_ID` - Entra ID group Object ID for centralized admin access
- `ACTIONS_RUNNER_DEBUG` - Enable debug logging (set to "true")

## Usage Example

```python
from fabric_orchestrator import VALID_ENVIRONMENTS, CONFIG_FILE

def validate_environment(env: str) -> None:
    if env not in VALID_ENVIRONMENTS:
        raise ValueError(f"Invalid environment: {env}")
    
def load_config(workspace_folder: str) -> dict:
    config_path = Path(workspace_folder) / CONFIG_FILE
    with open(config_path) as f:
        return yaml.safe_load(f)
```
