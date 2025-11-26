
# Exercise 1: Designing Foreign Key Behaviors

## The Scenario
You are designing a database for a **Project Management System**.
Tables:
1.  `Employees` (ID, Name, Role)
2.  `Projects` (ID, Name, Manager_ID)
3.  `Tasks` (ID, Description, Project_ID, Assigned_Employee_ID)

**Question:** Determine the correct `ON DELETE` behavior for:
1.  `Projects.Manager_ID` (References Employees)
2.  `Tasks.Project_ID` (References Projects)
3.  `Tasks.Assigned_Employee_ID` (References Employees)

---

## Detailed Solution & Reasoning

### 1. `Projects.Manager_ID`
*   **Relationship:** A project is managed by an employee.
*   **Action:** If the Employee (Manager) is deleted...
*   **Correct Choice: `SET NULL`** (or `RESTRICT`).
*   **Reasoning:** You should NOT delete the entire multi-million dollar Project just because the manager quit (`CASCADE` would be disastrous here). You might want to prevent deletion (`RESTRICT`) until a new manager is assigned, OR you simply leave the project managerless temporarily (`SET NULL`).

### 2. `Tasks.Project_ID`
*   **Relationship:** A task belongs to a specific project.
*   **Action:** If the Project is deleted...
*   **Correct Choice: `CASCADE`.**
*   **Reasoning:** A task cannot exist without a project. If the project is cancelled and removed from the DB, the tasks are irrelevant junk data. They should be cleaned up automatically.

### 3. `Tasks.Assigned_Employee_ID`
*   **Relationship:** A task is done by an employee.
*   **Action:** If the Employee is deleted...
*   **Correct Choice: `SET NULL`.**
*   **Reasoning:** The task still needs to be done! If Bob leaves the company, his tasks should remain in the list, perhaps marked as "Unassigned" (`NULL`), so the manager can reassign them to Alice. Do NOT use `CASCADE` (you'd lose the work) or `RESTRICT` (you couldn't remove the employee).

## Summary Table
| FK Column | Target | Behavior | Why? |
| :--- | :--- | :--- | :--- |
| `Manager_ID` | Employee | **SET NULL** | Project survives the manager. |
| `Project_ID` | Project | **CASCADE** | Tasks die with the project. |
| `Employee_ID` | Employee | **SET NULL** | Tasks must be reassigned. |
