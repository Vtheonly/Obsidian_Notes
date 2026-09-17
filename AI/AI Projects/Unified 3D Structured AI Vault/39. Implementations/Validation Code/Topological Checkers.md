---
tags: [implementation, validation, topological]
---

# Topological Checkers

Reference for topological validators.

```python
def build_connectivity_graph(model):
    # Build a graph: nodes = spaces, edges = doors between spaces
    import networkx as nx
    G = nx.Graph()
    for space in model.by_type("IfcSpace"):
        G.add_node(space.GlobalId)
    for door in model.by_type("IfcDoor"):
        # Find the two spaces the door connects
        # (simplified)
        spaces = find_spaces_connected_by_door(door)
        if len(spaces) == 2:
            G.add_edge(spaces[0].GlobalId, spaces[1].GlobalId)
    return G

def is_reachable(graph, source, target):
    import networkx as nx
    return nx.has_path(graph, source, target)

def all_reachable_from_entrance(graph, entrance):
    return all(is_reachable(graph, entrance, n) for n in graph.nodes)

def every_door_connects_two_spaces(model):
    issues = []
    for door in model.by_type("IfcDoor"):
        spaces = find_spaces_connected_by_door(door)
        if len(spaces) != 2:
            issues.append(f"Door {door.GlobalId} connects {len(spaces)} spaces")
    return issues
```

See [[Topological Validation]], [[Adjacency and Containment]].

## Related Concepts

- [[Topological Validation]]
- [[Adjacency and Containment]]
- [[BIM Rule Checkers]]
