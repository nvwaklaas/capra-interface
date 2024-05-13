# Table of Contents

* [main](#main)
  * [Instruction](#main.Instruction)
  * [InstructionCreate](#main.InstructionCreate)
  * [InstructionResponse](#main.InstructionResponse)
  * [create\_instruction](#main.create_instruction)
  * [stop\_robot](#main.stop_robot)
  * [connect\_to\_robot](#main.connect_to_robot)
  * [get\_instruction](#main.get_instruction)
  * [upload\_json](#main.upload_json)

<a id="main"></a>

# main

API Module for controlling a Capra Hircus

<a id="main.Instruction"></a>

## Instruction Objects

```python
class Instruction(Base)
```

Creates Instruction table in the database

<a id="main.InstructionCreate"></a>

## InstructionCreate Objects

```python
class InstructionCreate(BaseModel)
```

Instruction model

<a id="main.InstructionResponse"></a>

## InstructionResponse Objects

```python
class InstructionResponse(InstructionCreate)
```

Instruction Response code

<a id="main.create_instruction"></a>

#### create\_instruction

```python
@app.post("/drive/", response_model=InstructionResponse)
async def create_instruction(instruction: InstructionCreate)
```

Creates a driving instruction and sends it to the robot

<a id="main.stop_robot"></a>

#### stop\_robot

```python
@app.post("/stop/")
def stop_robot()
```

Send instruction to the robot to stop driving

<a id="main.connect_to_robot"></a>

#### connect\_to\_robot

```python
@app.get("/connect_to_robot")
def connect_to_robot()
```

Establishes a connection to the Capra Hircus

<a id="main.get_instruction"></a>

#### get\_instruction

```python
@app.get("/instructions/{instruction_id}", response_model=InstructionResponse)
def get_instruction(instruction_id: int)
```

Retrieves an instruction from the Database

<a id="main.upload_json"></a>

#### upload\_json

```python
@app.post("/upload-json")
async def upload_json(file: UploadFile = File(...))
```

Endpoint to upload a JSON file

