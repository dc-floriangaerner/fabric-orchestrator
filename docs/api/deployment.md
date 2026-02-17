# Deployment API

Data models and types for deployment orchestration.

## Data Models

### DeploymentResult

Result of a single workspace deployment.

```python
@dataclass
class DeploymentResult:
    workspace_folder: str
    workspace_name: str
    success: bool
    error_message: str = ""
```

**Attributes:**
- `workspace_folder` (str): Name of the workspace folder
- `workspace_name` (str): Name of the deployed workspace
- `success` (bool): Whether deployment was successful
- `error_message` (str): Error message if deployment failed (default: "")

**Example:**
```python
result = DeploymentResult(
    workspace_folder="My Workspace",
    workspace_name="[D] My Workspace",
    success=True
)
```

---

### DeploymentSummary

Summary of all workspace deployments.

```python
@dataclass
class DeploymentSummary:
    environment: str
    duration: float
    results: list[DeploymentResult]
    
    @property
    def total_workspaces(self) -> int
    
    @property
    def successful_count(self) -> int
    
    @property
    def failed_count(self) -> int
```

**Attributes:**
- `environment` (str): Target environment (dev/test/prod)
- `duration` (float): Total deployment duration in seconds
- `results` (list[DeploymentResult]): List of individual workspace deployment results

**Properties:**
- `total_workspaces` (int): Total number of workspaces deployed
- `successful_count` (int): Number of successful deployments
- `failed_count` (int): Number of failed deployments

**Example:**
```python
summary = DeploymentSummary(
    environment="dev",
    duration=120.5,
    results=[result1, result2, result3]
)

print(f"Deployed {summary.successful_count}/{summary.total_workspaces} workspaces")
```

## CLI Usage

The CLI entry point provides command-line deployment functionality:

```bash
fabric-orchestrator --workspaces_directory ./workspaces --environment dev
```

**Arguments:**
- `--workspaces_directory` (str, required): Root directory containing workspace folders
- `--environment` (str, required): Target environment (dev/test/prod)

**Environment Variables:**
- `AZURE_CLIENT_ID`: Service Principal Client ID
- `AZURE_CLIENT_SECRET`: Service Principal Secret
- `AZURE_TENANT_ID`: Azure AD Tenant ID
- `FABRIC_CAPACITY_ID`: Capacity ID for workspace creation (optional)
- `DEPLOYMENT_SP_OBJECT_ID`: Service Principal Object ID (optional)
- `FABRIC_ADMIN_GROUP_ID`: Entra ID group ID (optional)
- `ACTIONS_RUNNER_DEBUG`: Enable debug logging (optional)

**Exit Codes:**
- `0` (EXIT_SUCCESS): All deployments successful
- `1` (EXIT_FAILURE): One or more deployments failed

**Output:**
Creates `deployment-results.json` with detailed deployment results.
