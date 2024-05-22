# Table of Contents

- [route](#route)
  - [Route](#route.Route)
    - [add_node](#route.Route.add_node)
    - [add_edge](#route.Route.add_edge)
    - [get_formatted_route](#route.Route.get_formatted_route)

<a id="route"></a>

# route

Route data type

<a id="route.Route"></a>

## Route Objects

```python
@dataclass
class Route()
```

Class for defining a route

<a id="route.Route.add_node"></a>

#### add_node

```python
def add_node(node: Node) -> None
```

Adds a node to the route

Uses [Node](node.md) class.

<a id="route.Route.add_edge"></a>

#### add_edge

```python
def add_edge(edge: Edge) -> None
```

Adds an edge to the route

Uses [Edge](edge.md) class.

<a id="route.Route.get_formatted_route"></a>

#### get_formatted_route

```python
def get_formatted_route() -> dict
```

Returns a route in the correct format for Capra Hircus
