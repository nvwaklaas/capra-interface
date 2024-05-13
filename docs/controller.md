# Table of Contents

- [capra_control](#capra_control)
  - [ControlCapra](#capra_control.ControlCapra)
    - [connect_to_robot](#capra_control.ControlCapra.connect_to_robot)
    - [mq_set_mode](#capra_control.ControlCapra.mq_set_mode)
    - [load_path_file](#capra_control.ControlCapra.load_path_file)
    - [send_path](#capra_control.ControlCapra.send_path)
    - [calculate_distance_angle](#capra_control.ControlCapra.calculate_distance_angle)
    - [calculate_distances_from_path](#capra_control.ControlCapra.calculate_distances_from_path)
    - [send_instruction](#capra_control.ControlCapra.send_instruction)
    - [remote_control](#capra_control.ControlCapra.remote_control)

<a id="capra_control"></a>

# capra_control

Module containing helper functions for controlling a Capra Hircus Robot

<a id="capra_control.ControlCapra"></a>

## ControlCapra Methods

```python
class ControlCapra()
```

Class for controlling a Capra Hircus using MQTT Protocol

<a id="capra_control.ControlCapra.connect_to_robot"></a>

## connect_to_robot

```python
def connect_to_robot() -> None
```

Establishes connection to Capra Hircus

<a id="capra_control.ControlCapra.mq_set_mode"></a>

## mq_set_mode

```python
def mq_set_mode(mode: int) -> None
```

Sets the mode of the Capra Hircus.
Available modes are:

STOPPED=1

RUNNING=2

ABORTING=3

ABORTED=4

PAUSED=5

Modes are used to send different types of instructions to the robot.

<a id="capra_control.ControlCapra.load_path_file"></a>

## load_path_file

```python
@staticmethod
def load_path_file(filename: str) -> dict
```

load_path_file() loads a Capra Hircus path file in json format.
A Capra Hircus path file can be created using the Capra Commander Mobile application.
This mobile application can be found on the official Capra Hircus documentation

<a id="capra_control.ControlCapra.send_path"></a>

## send_path

```python
def send_path(filename: str) -> None
```

Sends a path to drive structured in the format as specified on the Capra Hircus documentation

<a id="capra_control.ControlCapra.calculate_distance_angle"></a>

## calculate_distance_angle

```python
def calculate_distance_angle(coord_1, coord_2) -> dict
```

Calculates the distance and angle between two coordinates using the Haversine formula

<a id="capra_control.ControlCapra.calculate_distances_from_path"></a>

## calculate_distances_from_path

```python
def calculate_distances_from_path(filename: str) -> list
```

Opens a route file and calculates distance between each node.

Input file should be a json file in the format that is used by
a Capra Hircus robot

<a id="capra_control.ControlCapra.send_instruction"></a>

## send_instruction

```python
def send_instruction(speed, angle: float = 0.0) -> None
```

Used for remotely controlling Capra Hircus using odometry.

<a id="capra_control.ControlCapra.remote_control"></a>

## remote_control

```python
def remote_control(distance: float = 0.1, speed: int = 0, angle=0.0) -> None
```

Instructs a Capra Hircus robot to drive for a given distance, with a given angle and speed.
