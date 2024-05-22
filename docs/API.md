# Table of Contents

- [main](#main)
  - [Instruction](#main.Instruction)
  - [create_instruction](#main.create_instruction)
  - [stop_robot](#main.stop_robot)
  - [connect_to_robot](#main.connect_to_robot)
  - [get_instruction](#main.get_instruction)
  - [upload_json](#main.upload_json)

<a id="main"></a>

# main

API Module for controlling a Capra Hircus

<a id="main.Instruction"></a>

## Instruction Table

```python
class Instruction(Base)
```

Creates Instruction table in the database

<a id="main.create_instruction"></a>

## API Endpoints

#### create_instruction

```python
@app.post("/drive/", response_model=InstructionResponse)
async def create_instruction(instruction: InstructionCreate)
```

Creates a driving instruction and sends it to the robot  
Uses [InstructionCreate](create_instruction.md) model

<a id="main.stop_robot"></a>

#### stop_robot

```python
@app.post("/stop/")
def stop_robot()
```

Send instruction to the robot to stop driving

<a id="main.connect_to_robot"></a>

#### connect_to_robot

```python
@app.get("/connect_to_robot")
def connect_to_robot()
```

Establishes a connection to the Capra Hircus

<a id="main.get_instruction"></a>

#### get_instruction

```python
@app.get("/instructions/{instruction_id}", response_model=InstructionResponse)
def get_instruction(instruction_id: int)
```

Retrieves an instruction from the Database

<a id="main.upload_json"></a>

#### upload_json

```python
@app.post("/upload-json")
async def upload_json(file: UploadFile = File(...))
```

Endpoint to upload a JSON file
