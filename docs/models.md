<a id="route_capra"></a>

# route\_capra

Route Class in Capra Hircus format

<a id="route_capra.CapraRoute"></a>

## CapraRoute Objects

```python
class CapraRoute(RouteAbstractClass)
```

Class for defining a route in Capra Hircus format

<a id="route_capra.CapraRoute.add_node"></a>

#### add\_node

```python
def add_node(node: Node) -> None
```

Adds a node to the route

<a id="route_capra.CapraRoute.add_edge"></a>

#### add\_edge

```python
def add_edge(edge: Edge) -> None
```

Adds an edge to the route

<a id="route_capra.CapraRoute.get_formatted_route"></a>

#### get\_formatted\_route

```python
def get_formatted_route() -> dict
```

Returns a route in the correct format for Capra Hircus

<a id="driving_instruction"></a>

# driving\_instruction

Module used for defining a DrivingInstruction

<a id="driving_instruction.DrivingInstruction"></a>

## DrivingInstruction Objects

```python
class DrivingInstruction(InstructionAbstractClass)
```

Class for defining a DrivingInstruction

<a id="driving_instruction.DrivingInstruction.get_formatted_instruction"></a>

#### get\_formatted\_instruction

```python
def get_formatted_instruction() -> dict
```

Returns a driving instruction in the correct format for Capra Hircus

<a id="edge"></a>

# edge

Edge data type

<a id="edge.Edge"></a>

## Edge Objects

```python
@dataclass
class Edge()
```

Class for defining an edge

<a id="edge.Edge.get_formatted_edge"></a>

#### get\_formatted\_edge

```python
def get_formatted_edge() -> dict
```

Returns an edge in the correct format for Capra Hircus

<a id="route_geojson"></a>

# route\_geojson

Route Class in GeoSJON format

<a id="route_geojson.GeoJSONRoute"></a>

## GeoJSONRoute Objects

```python
class GeoJSONRoute(RouteAbstractClass)
```

Class for defining a route in GeoJSON format

<a id="route_geojson.GeoJSONRoute.add_feature"></a>

#### add\_feature

```python
def add_feature(feature) -> None
```

Add GeoJSON feature to Route

<a id="coordinate"></a>

# coordinate

Class for defining a coordinate

<a id="coordinate.Coordinate"></a>

## Coordinate Objects

```python
class Coordinate()
```

Class for defining a coordinate

<a id="coordinate.Coordinate.get_coordinate"></a>

#### get\_coordinate

```python
def get_coordinate() -> list
```

Returns a formatted coordinate

<a id="instruction_response"></a>

# instruction\_response

Instruction Response model

<a id="instruction_response.InstructionResponse"></a>

## InstructionResponse Objects

```python
class InstructionResponse(InstructionCreate)
```

Instruction Response code

<a id="instruction_create"></a>

# instruction\_create

Instruction Pydantic Model

<a id="instruction_create.InstructionCreate"></a>

## InstructionCreate Objects

```python
class InstructionCreate(BaseModel)
```

Instruction model

<a id="instruction_create.InstructionCreate.check_angle"></a>

#### check\_angle

```python
@field_validator('angle')
@classmethod
def check_angle(cls, v)
```

Validate angle field

<a id="instruction_create.InstructionCreate.check_speed"></a>

#### check\_speed

```python
@field_validator('speed')
@classmethod
def check_speed(cls, v)
```

Validate speed field

<a id="instruction_create.InstructionCreate.check_distance"></a>

#### check\_distance

```python
@field_validator('distance')
@classmethod
def check_distance(cls, v)
```

Validate distance field

<a id="node"></a>

# node

Node data type

<a id="node.Node"></a>

## Node Objects

```python
@dataclass
class Node()
```

Class for defining a node

<a id="node.Node.get_formatted_node"></a>

#### get\_formatted\_node

```python
def get_formatted_node() -> dict
```

Returns a node in the corect format for Capra Hircus

