# API Reference

## Overview

Fabric Orchestrator provides a comprehensive API for managing Microsoft Fabric workspaces and orchestrating deployments.

## Modules

- [Workspace Management](workspace-management.md) - Functions for creating and managing workspaces
- [Deployment](deployment.md) - Functions for orchestrating deployments
- [Configuration](configuration.md) - Configuration constants and utilities

## Main Components

### Workspace Management

Create, check, and manage Microsoft Fabric workspaces:

```python
from fabric_orchestrator import (
    check_workspace_exists,
    create_workspace,
    ensure_workspace_exists,
    assign_workspace_role,
    add_workspace_admin,
    add_entra_id_group_admin,
)
```

### Deployment

Orchestrate multi-workspace deployments:

```python
from fabric_orchestrator import (
    DeploymentResult,
    DeploymentSummary,
)
```

### Configuration

Access configuration constants:

```python
from fabric_orchestrator import (
    CONFIG_FILE,
    VALID_ENVIRONMENTS,
    SEPARATOR_LONG,
    SEPARATOR_SHORT,
    RESULTS_FILENAME,
    EXIT_SUCCESS,
    EXIT_FAILURE,
)
```

### Logging

Setup and configure logging:

```python
from fabric_orchestrator import (
    get_logger,
    setup_logger,
)
```

## Type Hints

All public functions include comprehensive type hints for better IDE support and type checking.

## Error Handling

Functions raise exceptions for error conditions:
- `FileNotFoundError` - Configuration files not found
- `ValueError` - Invalid parameters
- `Exception` - API errors or unexpected conditions
