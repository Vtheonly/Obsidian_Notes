---
tags: [concept, auth, rbac, authorization]
type: concept
status: complete
related:
  - [[16 - Authentication and Authorization/01 - ABAC (Attribute-Based Access Control)]]
---

# RBAC (Role-Based Access Control)

## What it is

**RBAC** assigns permissions to roles, and roles to users. A user's permissions are the union of their roles' permissions.

```
User → Role → Permission
Alice → Admin → {create_user, delete_user, view_audit_log}
Bob → Chief → {accept_intern, reject_intern, view_interns}
Carol → Secretary → {create_intern, search_interns}
```

## Why

- **Simpler than per-user permissions** — assign a role, get all its permissions.
- **Auditable** — "what can an Admin do?" is one query.
- **Scalable** — adding a new permission means updating the role, not every user.

## The project's RBAC

The project has a degenerate RBAC:
- Roles: 1 (User), 4 (Admin), 5 (Chief). (No 2 or 3 in the sample data, despite `setAccessLevel` handling them.)
- Permissions: hardcoded checks like `if (roleId == 4)` for admin, `if (roleId == 5)` for chief.
- No `Permission` table — the mapping is in Java code.

## Problems

1. **Magic numbers** — `4` and `5` are scattered. Renumbering roles requires editing Java code.
2. **No permission table** — adding a new permission requires code changes.
3. **Coarse-grained** — all chiefs have all chief permissions; can't grant "accept interns" without "reject interns."
4. **No re-validation** — role checked once at login; never re-checked.

## The fix

### Option 1: Enum-based (simple)
```java
public enum Role {
    USER, SECRETARY, ADMIN, CHIEF;
}

public enum Permission {
    CREATE_INTERN, ACCEPT_INTERN, REJECT_INTERN, DELETE_USER, VIEW_AUDIT_LOG;
}

public class Authz {
    private static final Map<Role, Set<Permission>> ROLE_PERMISSIONS = Map.of(
        Role.USER, Set.of(),
        Role.SECRETARY, Set.of(Permission.CREATE_INTERN),
        Role.ADMIN, EnumSet.allOf(Permission.class),
        Role.CHIEF, Set.of(Permission.ACCEPT_INTERN, Permission.REJECT_INTERN)
    );

    public static void require(Session session, Permission permission) {
        Set<Permission> perms = ROLE_PERMISSIONS.get(session.getUser().getRole());
        if (!perms.contains(permission)) {
            throw new AuthorizationException("Missing permission: " + permission);
        }
    }
}
```

### Option 2: Database-driven (flexible)
```sql
CREATE TABLE roles (role_id NUMBER PRIMARY KEY, role_name VARCHAR2(50));
CREATE TABLE permissions (permission_id NUMBER PRIMARY KEY, permission_name VARCHAR2(50));
CREATE TABLE role_permissions (role_id NUMBER, permission_id NUMBER, PRIMARY KEY (role_id, permission_id));
```

Permissions can be added/removed via SQL, no code changes.

## Further reading

- NIST RBAC standard (INCITS 359-2004).
- *Role-Based Access Control* (Ferraiolo et al.).
