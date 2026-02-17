# Workspace Management API

Functions for creating and managing Microsoft Fabric workspaces.

## Functions

### check_workspace_exists

Check if a workspace with the given name exists.

```python
def check_workspace_exists(
    workspace_name: str,
    fabric_client: FabricClient
) -> str | None
```

**Parameters:**
- `workspace_name` (str): Name of the workspace to check
- `fabric_client` (FabricClient): Microsoft Fabric API client

**Returns:**
- `str | None`: Workspace ID if exists, None if not found

**Raises:**
- `Exception`: If API call fails

**Example:**
```python
workspace_id = check_workspace_exists("[D] My Workspace", fabric_client)
if workspace_id:
    print(f"Workspace exists with ID: {workspace_id}")
```

---

### create_workspace

Create a new Fabric workspace with the specified capacity.

```python
def create_workspace(
    workspace_name: str,
    capacity_id: str | None,
    fabric_client: FabricClient
) -> str
```

**Parameters:**
- `workspace_name` (str): Display name for the new workspace
- `capacity_id` (str | None): Fabric capacity ID (GUID) - mandatory
- `fabric_client` (FabricClient): Microsoft Fabric API client

**Returns:**
- `str`: Workspace ID of the newly created workspace

**Raises:**
- `Exception`: If workspace creation fails or capacity_id is None

**Example:**
```python
workspace_id = create_workspace(
    workspace_name="[D] My Workspace",
    capacity_id="your-capacity-id",
    fabric_client=fabric_client
)
```

---

### ensure_workspace_exists

Ensure a workspace exists, creating it if necessary, and assign permissions.

```python
def ensure_workspace_exists(
    workspace_name: str,
    capacity_id: str | None,
    service_principal_object_id: str | None,
    entra_admin_group_id: str | None,
    fabric_client: FabricClient
) -> str
```

**Parameters:**
- `workspace_name` (str): Name of the workspace
- `capacity_id` (str | None): Capacity ID for workspace creation
- `service_principal_object_id` (str | None): Service Principal Object ID for admin role
- `entra_admin_group_id` (str | None): Entra ID group ID for admin access
- `fabric_client` (FabricClient): Microsoft Fabric API client

**Returns:**
- `str`: Workspace ID

**Raises:**
- `Exception`: If workspace operations fail

**Example:**
```python
workspace_id = ensure_workspace_exists(
    workspace_name="[D] My Workspace",
    capacity_id="your-capacity-id",
    service_principal_object_id="sp-object-id",
    entra_admin_group_id="group-id",
    fabric_client=fabric_client
)
```

---

### assign_workspace_role

Assign a role to a principal in a workspace.

```python
def assign_workspace_role(
    workspace_id: str,
    principal_id: str,
    role: Literal["Admin", "Contributor", "Member"],
    fabric_client: FabricClient
) -> None
```

**Parameters:**
- `workspace_id` (str): Workspace ID
- `principal_id` (str): Principal ID (Service Principal or User Object ID)
- `role` (str): Role to assign (Admin, Contributor, or Member)
- `fabric_client` (FabricClient): Microsoft Fabric API client

**Raises:**
- `Exception`: If role assignment fails

**Example:**
```python
assign_workspace_role(
    workspace_id="workspace-id",
    principal_id="sp-object-id",
    role="Admin",
    fabric_client=fabric_client
)
```

---

### add_workspace_admin

Add Service Principal as workspace admin.

```python
def add_workspace_admin(
    workspace_id: str,
    service_principal_object_id: str | None,
    fabric_client: FabricClient
) -> None
```

**Parameters:**
- `workspace_id` (str): Workspace ID
- `service_principal_object_id` (str | None): Service Principal Object ID
- `fabric_client` (FabricClient): Microsoft Fabric API client

**Example:**
```python
add_workspace_admin(
    workspace_id="workspace-id",
    service_principal_object_id="sp-object-id",
    fabric_client=fabric_client
)
```

---

### add_entra_id_group_admin

Add Entra ID group as workspace admin.

```python
def add_entra_id_group_admin(
    workspace_id: str,
    entra_group_id: str | None,
    fabric_client: FabricClient
) -> None
```

**Parameters:**
- `workspace_id` (str): Workspace ID
- `entra_group_id` (str | None): Entra ID group Object ID
- `fabric_client` (FabricClient): Microsoft Fabric API client

**Example:**
```python
add_entra_id_group_admin(
    workspace_id="workspace-id",
    entra_group_id="group-id",
    fabric_client=fabric_client
)
```

---

### check_role_assignment_exists

Check if a role assignment already exists for a principal.

```python
def check_role_assignment_exists(
    workspace_id: str,
    principal_id: str,
    role: str,
    fabric_client: FabricClient
) -> bool
```

**Parameters:**
- `workspace_id` (str): Workspace ID
- `principal_id` (str): Principal ID
- `role` (str): Role name
- `fabric_client` (FabricClient): Microsoft Fabric API client

**Returns:**
- `bool`: True if role assignment exists, False otherwise

**Example:**
```python
exists = check_role_assignment_exists(
    workspace_id="workspace-id",
    principal_id="sp-object-id",
    role="Admin",
    fabric_client=fabric_client
)
```
